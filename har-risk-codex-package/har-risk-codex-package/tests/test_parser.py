from pathlib import Path

from har_engine.parser import parse_har


def test_parse_har_basic(tmp_path: Path) -> None:
    har = {
        "log": {
            "entries": [
                {
                    "startedDateTime": "2026-04-01T10:00:00Z",
                    "request": {
                        "method": "POST",
                        "url": "https://api.mixpanel.com/track?query=oncology",
                        "headers": [{"name": "Content-Type", "value": "application/json"}],
                        "cookies": [{"name": "sid", "value": "abc123"}],
                        "postData": {"text": '{"email":"person@example.com"}'},
                    }
                }
            ]
        }
    }
    path = tmp_path / "sample.har"
    path.write_text(__import__("json").dumps(har), encoding="utf-8")

    entries = parse_har(path)
    assert len(entries) == 1
    assert entries[0].host == "api.mixpanel.com"
    assert entries[0].query_params["query"] == "oncology"
    assert entries[0].body_json == {"email": "person@example.com"}
