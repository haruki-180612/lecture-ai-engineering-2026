from types import SimpleNamespace
from unittest.mock import patch

from app.ask import ask


def test_ask_prints_input_and_output_token_counts(capsys):
    usage = SimpleNamespace(prompt_token_count=123, response_token_count=45)
    response = SimpleNamespace(text="回答です", usage_metadata=usage)

    with patch("app.ask.genai.Client") as client_cls:
        client = client_cls.return_value
        client.models.generate_content.return_value = response

        with patch("app.ask.get_api_key", return_value="fake-key"):
            result = ask("これはテストです")

    assert result == "回答です"
    captured = capsys.readouterr().out
    assert "[入力トークン数] 123" in captured
    assert "[出力トークン数] 45" in captured
