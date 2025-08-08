"""The frontend pipeline: raw text -> analysed :class:`Utterance`.

Tokenization is deliberately dependency-free: maximal runs of CJK, Latin and
punctuation are peeled off with one regex. Each CJK run is converted with
:func:`chinese_g2p` and sandhi is applied across the run before it is split into
one word per character, which gives the phraser real word boundaries to place
breaks on without pulling in a segmenter such as jieba.
"""

from __future__ import annotations

import re

from prosodia.frontend.g2p.chinese import chinese_g2p
from prosodia.frontend.g2p.english import english_word_to_syllable
from prosodia.frontend.g2p.sandhi import apply_sandhi
from prosodia.frontend.normalize.pipeline import Normalizer, detect_language
from prosodia.frontend.phrasing import PhraseBreaker, RuleBasedPhraser
from prosodia.frontend.symbols import break_for_punct
from prosodia.types import BreakLevel, Language, Utterance, Word

_CJK_RUN = re.compile(r"[一-鿿]+")
_TOKEN = re.compile(r"[一-鿿]+|[A-Za-z]+|\s+|[^\sA-Za-z一-鿿]")


class TextFrontend:
    """Turn text into an :class:`Utterance` ready for synthesis."""

    def __init__(
        self,
        language: Language = Language.AUTO,
        normalize: bool = True,
        phraser: PhraseBreaker | None = None,
    ) -> None:
        self.language = language
        self.normalize = normalize
        self.phraser: PhraseBreaker = phraser or RuleBasedPhraser()

    def process(self, text: str) -> Utterance:
        lang = self.language
        if lang == Language.AUTO:
            lang = detect_language(text)
        normalized = Normalizer(lang).normalize(text) if self.normalize else text
        words = self._tokenize(normalized)
        self.phraser.assign(words)
        return Utterance(text=text, normalized=normalized, language=lang, words=words)

    def _tokenize(self, text: str) -> list[Word]:
        words: list[Word] = []
        for tok in _TOKEN.findall(text):
            if tok.isspace():
                continue
            if _CJK_RUN.fullmatch(tok):
                syllables = chinese_g2p(tok)
                apply_sandhi(syllables)
                if len(syllables) == len(tok):
                    for ch, syl in zip(tok, syllables):
                        words.append(Word(text=ch, syllables=[syl]))
                else:  # pragma: no cover - mismatched g2p output
                    words.append(Word(text=tok, syllables=syllables))
            elif tok.isalpha():
                words.append(Word(text=tok, syllables=[english_word_to_syllable(tok)]))
            else:
                level = break_for_punct(tok)
                if words and level != BreakLevel.NONE:
                    prev = words[-1]
                    prev.break_after = BreakLevel(max(int(prev.break_after), int(level)))
        return words
