import hello


def test_ambiente_padrao(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    assert hello.get_environment() == "development"


def test_ambiente_definido(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    assert hello.get_environment() == "production"


def test_versao(monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    assert hello.get_version() == "dev"
    monkeypatch.setenv("APP_VERSION", "main-abc1234")
    assert hello.get_version() == "main-abc1234"


def test_mensagem_diferente_por_ambiente():
    dev = hello.build_message("development", "v1")
    prod = hello.build_message("production", "v1")
    assert dev != prod
    assert "Running in: development" in dev
    assert "Running in: production" in prod


def test_main_imprime_versao(monkeypatch, capsys):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("APP_VERSION", "main-abc1234")
    hello.main()
    out = capsys.readouterr().out
    assert "Running in: production" in out
    assert "Version: main-abc1234" in out
