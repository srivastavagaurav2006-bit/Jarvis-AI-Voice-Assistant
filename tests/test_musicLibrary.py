import musicLibrary


def test_music_library_is_dictionary():
    assert isinstance(musicLibrary.music, dict)


def test_music_library_is_not_empty():
    assert len(musicLibrary.music) > 0


def test_song_names_are_strings():
    for song in musicLibrary.music:
        assert isinstance(song, str)


def test_song_urls_are_strings():
    for url in musicLibrary.music.values():
        assert isinstance(url, str)


def test_song_urls_are_valid_http_urls():
    for url in musicLibrary.music.values():
        assert url.startswith(("http://", "https://"))