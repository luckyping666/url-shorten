from app.utils.short_id import generate_short_id, DEFAULT_LENGTH


def test_generate_short_id_length():
    short_id = generate_short_id()
    assert len(short_id) == DEFAULT_LENGTH


def test_generate_short_id_unique():
    ids = {generate_short_id() for _ in range(1000)}
    assert len(ids) == 1000
