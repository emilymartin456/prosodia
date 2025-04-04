import pytest

from prosodia.config import Config
from prosodia.errors import ConfigError
from prosodia.types import Language


def test_defaults_validate():
    cfg = Config().validate()
    assert cfg.audio.sample_rate == 22050
    assert cfg.frontend.language is Language.AUTO


def test_from_dict_partial_override():
    cfg = Config.from_dict({"audio": {"sample_rate": 16000}, "frontend": {"language": "zh"}})
    assert cfg.audio.sample_rate == 16000
    assert cfg.frontend.language is Language.ZH
    # untouched sections keep defaults
    assert cfg.synthesis.backend == "reference"


def test_from_dict_rejects_unknown_key():
    with pytest.raises(ConfigError):
        Config.from_dict({"audio": {"sampl_rate": 16000}})


def test_validate_rejects_bad_sample_rate():
    with pytest.raises(ConfigError):
        Config.from_dict({"audio": {"sample_rate": 0}})


def test_roundtrip_dict():
    cfg = Config.from_dict({"expressive": {"emotion": "happy"}})
    again = Config.from_dict(cfg.to_dict())
    assert again.expressive.emotion == "happy"
