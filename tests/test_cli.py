import prosodia.cli as cli


def test_version(capsys):
    try:
        cli.main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    out = capsys.readouterr().out
    assert "prosodia" in out


def test_no_command_prints_help(capsys):
    rc = cli.main([])
    assert rc == 1
    assert "usage" in capsys.readouterr().out.lower()


def test_normalize(capsys):
    rc = cli.main(["normalize", "2026年", "--lang", "zh"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "二零二六年"


def test_phonemize(capsys):
    rc = cli.main(["phonemize", "你好"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == "ni3 hao3"


def test_prosody(capsys):
    rc = cli.main(["prosody", "你好，世界。"])
    assert rc == 0
    assert "规范化" in capsys.readouterr().out


def test_emotions(capsys):
    rc = cli.main(["emotions"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "happy" in out and "neutral" in out


def test_say_writes_wav(tmp_path, capsys):
    out = tmp_path / "a.wav"
    rc = cli.main(["say", "你好", "-o", str(out), "-e", "happy"])
    assert rc == 0
    assert out.exists()


def test_stream_writes_wav(tmp_path, capsys):
    out = tmp_path / "b.wav"
    rc = cli.main(["stream", "你好。世界。", "-o", str(out)])
    assert rc == 0
    assert out.exists()
    assert "RTF" in capsys.readouterr().out


def test_bench(capsys):
    rc = cli.main(["bench", "你好世界", "--repeat", "2"])
    assert rc == 0
    assert "RTF" in capsys.readouterr().out
