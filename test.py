import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


def test_add_new_book_valid_and_invalid(collector):
    # Добавляем корректную книгу
    collector.add_new_book("Книга 1")
    assert "Книга 1" in collector.books_genre
    assert collector.books_genre["Книга 1"] == ''

    # Добавляем пустое название — не добавится
    collector.add_new_book("")
    assert "" not in collector.books_genre

    # Добавляем книгу с названием длиннее 40 символов — не добавится
    long_name = "X" * 41
    collector.add_new_book(long_name)
    assert long_name not in collector.books_genre

    # Добавляем книгу, которая уже есть — словарь не поменяется
    before = dict(collector.books_genre)
    collector.add_new_book("Книга 1")
    assert collector.books_genre == before


@pytest.mark.parametrize("genre", ['Фантастика', 'Ужасы', 'Комедии'])
def test_set_book_genre_valid_and_invalid(collector, genre):
    collector.add_new_book("Книга 2")
    collector.set_book_genre("Книга 2", genre)
    assert collector.get_book_genre("Книга 2") == genre

    # Попытка задать жанр несуществующей книге — без изменений
    collector.set_book_genre("Неизвестная книга", genre)
    assert collector.get_book_genre("Неизвестная книга") is None

    # Попытка задать неизвестный жанр — игнорируется
    collector.set_book_genre("Книга 2", "Не жанр")
    assert collector.get_book_genre("Книга 2") == genre


def test_get_book_genre_and_default(collector):
    collector.add_new_book("Книга 3")
    assert collector.get_book_genre("Книга 3") == ''

    collector.set_book_genre("Книга 3", "Фантастика")
    assert collector.get_book_genre("Книга 3") == "Фантастика"

    assert collector.get_book_genre("Нет книги") is None


def test_get_books_with_specific_genre(collector):
    collector.add_new_book("Книга 4")
    collector.add_new_book("Книга 5")
    collector.set_book_genre("Книга 4", "Фантастика")
    collector.set_book_genre("Книга 5", "Фантастика")
    collector.add_new_book("Книга 6")
    collector.set_book_genre("Книга 6", "Комедии")

    assert set(collector.get_books_with_specific_genre("Фантастика")) == {"Книга 4", "Книга 5"}
    assert collector.get_books_with_specific_genre("Комедии") == ["Книга 6"]
    assert collector.get_books_with_specific_genre("Не жанр") == []


def test_get_books_genre_returns_entire_dict(collector):
    collector.add_new_book("Книга 7")
    collector.add_new_book("Книга 8")
    expected = collector.books_genre.copy()
    assert collector.get_books_genre() == expected


def test_get_books_for_children(collector):
    collector.add_new_book("Детская книга")
    collector.set_book_genre("Детская книга", "Мультфильмы")

    collector.add_new_book("Страшилка")
    collector.set_book_genre("Страшилка", "Ужасы")

    collector.add_new_book("Детектив для взрослых")
    collector.set_book_genre("Детектив для взрослых", "Детективы")

    collector.add_new_book("Фантастика для всех")
    collector.set_book_genre("Фантастика для всех", "Фантастика")

    children_books = collector.get_books_for_children()
    assert set(children_books) == {"Детская книга", "Фантастика для всех"}


def test_add_and_delete_book_in_favorites(collector):
    collector.add_new_book("Избранная книга")
    collector.set_book_genre("Избранная книга", "Комедии")

    collector.add_book_in_favorites("Избранная книга")
    assert "Избранная книга" in collector.favorites

    before = list(collector.favorites)
    collector.add_book_in_favorites("Избранная книга")
    assert collector.favorites == before

    collector.add_book_in_favorites("Неизвестная книга")
    assert "Неизвестная книга" not in collector.favorites

    collector.delete_book_from_favorites("Избранная книга")
    assert "Избранная книга" not in collector.favorites

    collector.delete_book_from_favorites("Неизвестная книга")  # без ошибок


def test_get_list_of_favorites_books_returns_correct_list(collector):
    collector.add_new_book("Книга А")
    collector.add_new_book("Книга Б")
    collector.add_book_in_favorites("Книга А")
    collector.add_book_in_favorites("Книга Б")

    favorites = collector.get_list_of_favorites_books()
    assert set(favorites) == {"Книга А", "Книга Б"}


@pytest.mark.parametrize('book_name', ['Книга X', 'Another book', 'Book 123'])
def test_add_new_book_parametrized(collector, book_name):
    collector.add_new_book(book_name)
    assert book_name in collector.books_genre
    assert collector.books_genre[book_name] == ''