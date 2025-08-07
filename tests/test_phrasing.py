from prosodia.frontend.phrasing import NoopPhraser, RuleBasedPhraser
from prosodia.types import BreakLevel, Syllable, Word


def make_words(n):
    return [Word(text=str(i), syllables=[Syllable(str(i))]) for i in range(n)]


def test_noop_only_closes_sentence():
    words = make_words(3)
    NoopPhraser().assign(words)
    assert words[-1].break_after is BreakLevel.SENTENCE
    assert words[0].break_after is BreakLevel.NONE


def test_rule_based_inserts_phrase_breaks():
    words = make_words(30)
    RuleBasedPhraser(max_syllables=10).assign(words)
    broken = [i for i, w in enumerate(words[:-1]) if w.break_after == BreakLevel.PHRASE]
    # roughly every 10 words a phrase break is inserted
    assert broken == [9, 19]
    assert words[-1].break_after is BreakLevel.SENTENCE


def test_rule_based_respects_existing_break():
    words = make_words(6)
    words[2].break_after = BreakLevel.PHRASE
    RuleBasedPhraser(max_syllables=4).assign(words)
    # counter resets at the manual break, so no extra break right after it
    assert words[3].break_after is BreakLevel.NONE


def test_rejects_bad_budget():
    try:
        RuleBasedPhraser(max_syllables=0)
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("expected ValueError")
