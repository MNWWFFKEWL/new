import sys
import pathlib

# Ensure repository root is importable
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from plugins import model


def test_connect_uses_env_var(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "env-key")
    assert model.connect() == "env-key"


def test_connect_env_indirection(monkeypatch):
    monkeypatch.setenv("CUSTOM_KEY", "other-key")
    assert model.connect("env:CUSTOM_KEY") == "other-key"
