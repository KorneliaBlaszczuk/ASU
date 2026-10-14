
from content_generator import ContentGenerator

def test_duplicate_returns_same_content():
    generator = ContentGenerator()

    assert generator.duplicate() == generator.duplicate()


def test_random_returns_ten_lowercase_letters():
    generator = ContentGenerator()

    content = generator.random()

    assert len(content) == 10
    assert content.islower()
    assert content.isalpha()


def test_empty_returns_empty_string():
    generator = ContentGenerator()

    assert generator.empty() == ""


def test_unique_returns_different_content():
    generator = ContentGenerator()

    first = generator.unique()
    second = generator.unique()

    assert first != second


def test_unique_content_has_counter_prefix():
    generator = ContentGenerator()

    first = generator.unique()
    second = generator.unique()

    assert first.startswith("UQ1")
    assert second.startswith("UQ2")
