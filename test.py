import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


# Тесты метода add_new_book
def test_add_new_book_valid_name(collector):
    collector.add_new_book("Книга 1")
    assert "Книга 1" in collector.books_genre
    assert collector.books_genre["Книга 1"] == ''


def test_add_new_book_empty_string(collector):
    collector.add_new_book("")
    assert "" not in collector.books_genre


def test_add_new_book_name_too_long(collector):
    long_name = "X" * 41
    collector.add_new_book(long_name)
    assert long_name not in collector.books_genre


def test_add_new_book_duplicate(collector):
    collector.add_new_book("Книга 1")
    before = dict(collector.books_genre)
    collector.add_new_book("Книга 1")
    assert collector.books_genre == before


# Тесты метода set_book_genre
def test_set_book_genre_for_existing_book(collector):
    collector.add_new_book("Книга 2")
    collector.set_book_genre("Книга 2", "Фантастика")
    assert collector.books_genre["Книга 2"] == "Фантастика"


def test_set_book_genre_with_invalid_genre_does_not_change(collector):
    collector.add_new_book("Книга 2")
    collector.set_book_genre("Книга 2", "Фантастика")
    collector.set_book_genre("Книга 2", "Не жанр")
    assert collector.books_genre["Книга 2"] == "Фантастика"


def test_set_book_genre_for_nonexistent_book_does_nothing(collector):
    collector.set_book_genre("Неизвестная", "Фантастика")
    assert "Неизвестная" not in collector.books_genre


# Тесты метода get_book_genre
def test_get_book_genre_existing_book(collector):
    collector.add_new_book("Книга 3")
    collector.set_book_genre("Книга 3", "Ужасы")
    assert collector.get_book_genre("Книга 3") == "Ужасы"


def test_get_book_genre_book_without_genre_returns_empty(collector):
    collector.add_new_book("Книга 4")
    assert collector.get_book_genre("Книга 4") == ''


def test_get_book_genre_nonexistent_book_returns_empty_string(collector):
    assert collector.get_book_genre("Нет книги") == ''


# Тесты метода get_books_with_specific_genre
def test_get_books_with_specific_genre_existing_genre(collector):
    collector.add_new_book("Книга 5")
    collector.add_new_book("Книга 6")
    collector.set_book_genre("Книга 5", "Фантастика")
    collector.set_book_genre("Книга 6", "Фантастика")
    books = collector.get_books_with_specific_genre("Фантастика")
    assert set(books) == {"Книга 5", "Книга 6"}


def test_get_books_with_specific_genre_no_books(collector):
    books = collector.get_books_with_specific_genre("Не жанр")
    assert books == []


# Тесты метода get_books_genre
def test_get_books_genre_returns_entire_dict(collector):
    collector.add_new_book("Книга 7")
    expected = collector.books_genre.copy()
    assert collector.get_books_genre() == expected


# Тесты метода get_books_for_children
def test_get_books_for_children_returns_correct_books(collector):
    collector.add_new_book("Детская книга")
    collector.set_book_genre("Детская книга", "Мультфильмы")

    collector.add_new_book("Страшилка")
    collector.set_book_genre("Страшилка", "Ужасы")

    collector.add_new_book("Фантастика для детей")
    collector.set_book_genre("Фантастика для детей", "Фантастика")

    children_books = collector.get_books_for_children()
    assert set(children_books) == {"Детская книга", "Фантастика для детей"}


# Тесты метода add_book_in_favorites
def test_add_book_in_favorites_existing_book(collector):
    collector.add_new_book("Избранная книга")
    collector.add_book_in_favorites("Избранная книга")
    assert "Избранная книга" in collector.favorites


def test_add_book_in_favorites_duplicate_does_not_add_twice(collector):
    collector.add_new_book("Избранная книга")
    collector.add_book_in_favorites("Избранная книга")
    before = list(collector.favorites)
    collector.add_book_in_favorites("Избранная книга")
    assert list(collector.favorites) == before


def test_add_book_in_favorites_nonexistent_book_does_not_add(collector):
    collector.add_book_in_favorites("Неизвестная")
    assert "Неизвестная" not in collector.favorites


# Тесты метода delete_book_from_favorites
def test_delete_book_from_favorites_existing(collector):
    collector.add_new_book("Книга для удаления")
    collector.add_book_in_favorites("Книга для удаления")
    collector.delete_book_from_favorites("Книга для удаления")
    assert "Книга для удаления" not in collector.favorites


def test_delete_book_from_favorites_nonexistent_book_does_not_error(collector):
    # Проверим, что удаления несуществующей книги не вызывает исключений
    try:
        collector.delete_book_from_favorites("Нет книги")
    except Exception:
        pytest.fail("Удаление несуществующей книги вызвало ошибку")


# Тесты метода get_list_of_favorites_books
def test_get_list_of_favorites_books_returns_all(collector):
    collector.add_new_book("Фаворит 1")
    collector.add_new_book("Фаворит 2")
    collector.add_book_in_favorites("Фаворит 1")
    collector.add_book_in_favorites("Фаворит 2")
    favorites = collector.get_list_of_favorites_books()
    assert set(favorites) == {"Фаворит 1", "Фаворит 2"}