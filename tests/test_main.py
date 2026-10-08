import main


def test_open_google(monkeypatch):
    opened_urls = []

    monkeypatch.setattr(
        main.webbrowser,
        "open",
        lambda url: opened_urls.append(url)
    )

    main.processCommand("open google")

    assert opened_urls == ["https://google.com"]


def test_open_youtube(monkeypatch):
    opened_urls = []

    monkeypatch.setattr(
        main.webbrowser,
        "open",
        lambda url: opened_urls.append(url)
    )

    main.processCommand("open youtube")

    assert opened_urls == ["https://youtube.com"]


def test_play_known_song(monkeypatch):
    opened_urls = []

    monkeypatch.setattr(
        main.musicLibrary,
        "music",
        {"believer": "https://example.com/believer"}
    )

    monkeypatch.setattr(
        main.webbrowser,
        "open",
        lambda url: opened_urls.append(url)
    )

    main.processCommand("play believer")

    assert opened_urls == ["https://example.com/believer"]


def test_play_unknown_song(monkeypatch):
    spoken_messages = []

    monkeypatch.setattr(
        main.musicLibrary,
        "music",
        {}
    )

    monkeypatch.setattr(
        main,
        "speak",
        lambda text: spoken_messages.append(text)
    )

    main.processCommand("play unknown song")

    assert spoken_messages == [
        "Sorry, I don't have that song in my library."
    ]


def test_news_command(monkeypatch):
    spoken_messages = []

    class FakeResponse:
        status_code = 200

        def json(self):
            return {
                "articles": [
                    {"title": "Test News One"},
                    {"title": "Test News Two"}
                ]
            }

    monkeypatch.setattr(
        main.requests,
        "get",
        lambda url: FakeResponse()
    )

    monkeypatch.setattr(
        main,
        "speak",
        lambda text: spoken_messages.append(text)
    )

    main.processCommand("give me news")

    assert spoken_messages == [
        "Test News One",
        "Test News Two"
    ]


def test_ai_fallback(monkeypatch):
    spoken_messages = []

    monkeypatch.setattr(
        main,
        "aiProcess",
        lambda command: "AI response"
    )

    monkeypatch.setattr(
        main,
        "speak",
        lambda text: spoken_messages.append(text)
    )

    main.processCommand("tell me something interesting")

    assert spoken_messages == ["AI response"]


def test_command_is_case_insensitive(monkeypatch):
    opened_urls = []

    monkeypatch.setattr(
        main.webbrowser,
        "open",
        lambda url: opened_urls.append(url)
    )

    main.processCommand("OPEN FACEBOOK")

    assert opened_urls == ["https://facebook.com"]