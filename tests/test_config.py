from emojify_cli.config import init_config, merge_config
from emojify_cli.defaults import DEFAULT_CONFIG
import json
import os

def test_merge_config_override():
    base = {"a": 1, "b": {"x": 1}}
    override = {"b": {"x": 2}}
    result = merge_config(base, override)
    assert result["b"]["x"] == 2

def test_init_config_creates_file(tmp_path, monkeypatch):
    # força o HOME para o diretório temporário
    monkeypatch.setenv("HOME", str(tmp_path))

    rc, msg = init_config(DEFAULT_CONFIG)

    assert rc == 0
    assert "created" in msg.lower()

    cfg_path = tmp_path / ".emojify.json"
    assert cfg_path.exists()

    data = json.loads(cfg_path.read_text())
    assert data == DEFAULT_CONFIG

def test_init_config_fails_if_file_exists(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))

    cfg_path = tmp_path / ".emojify.json"
    cfg_path.write_text("{}")

    rc, msg = init_config(DEFAULT_CONFIG)

    assert rc != 0
    assert "already exists" in msg.lower()

def test_cli_config_init(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))

    import subprocess
    result = subprocess.run(
        ["emojify", "config", "--init"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert (tmp_path / ".emojify.json").exists()

