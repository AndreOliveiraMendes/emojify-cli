from emojify_cli.config import merge_config

def test_merge_config_override():
    base = {"a": 1, "b": {"x": 1}}
    override = {"b": {"x": 2}}
    result = merge_config(base, override)
    assert result["b"]["x"] == 2

