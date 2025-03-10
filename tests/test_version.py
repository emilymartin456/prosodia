import prosodia


def test_version_is_a_nonempty_string():
    assert isinstance(prosodia.__version__, str)
    assert prosodia.__version__


def test_version_has_three_parts():
    core = prosodia.__version__.split(".dev")[0]
    assert len(core.split(".")) == 3
