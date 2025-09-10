import pytest
from main import BooksCollector  # предполагаем, что класс в файле main.py


@pytest.fixture
def collector():
    return BooksCollector()


def test_add_new_book_valid_and_invalid(collector):
    # Добавляем корректную книгу
    collector.add_new_book("Книга 1")
    assert "Книга 1" in collector.books_genre
    assert collector.books_genre["Книга 1"] == ''

    # Добавляем книгу с длиной 0 (пустое название) - не добавится
    collector.add_new_book("")
    assert "" not in collector.books_genre

    # Добавляем книгу с длиной > 40 - не добавится
    long_name = "X" * 41
    collector.add_new_book(long_name)
    assert long_name not in collector.books_genre

    # Добавляем книгу, которая уже есть - не изменит словарь
    before = dict(collector.books_genre)
    collector.add_new_book("Книга 1")
    assert collector.books_genre == before


@pytest.mark.parametrize("genre", ['Фантастика', 'Ужасы', 'Комедии'])
def test_set_book_genre_valid_and_invalid(collector, genre):
    collector.add_new_book("Книга 2")
    collector.set_book_genre("Книга 2", genre)
    assert collector.get_book_genre("Книга 2") == genre

    # Попытка задать жанр несуществующей книге - жанр не изменится
    collector.set_book_genre("Неизвестная книга", genre)
    assert collector.get_book_genre("Неизвестная книга") is None

    # Попытка задать жанр, который не в списке genre - игнорируется
    collector.set_book_genre("Книга 2", "Не жанр")
    assert collector.get_book_genre("Книга 2") == genre


def test_get_book_genre_and_default(collector):
    collector.add_new_book("Книга 3")
    assert collector.get_book_genre("Книга 3") == ''  # по умолчанию пустая строка

    collector.set_book_genre("Книга 3", "Фантастика")
    assert collector.get_book_genre("Книга 3") == "Фантастика"

    # Для книги, которой нет
    assert collector.get_book_genre("Нет книги") is None


def test_get_books_with_specific_genre(collector):
    collector.add_new_book("Книга 4")
    collector.add_new_book("Книга 5")
    collector.set_book_genre("Книга 4", "Фантастика")
    collector.set_book_genre("Книга 5", "Фантастика")
    collector.add_new_book("Книга 6")
    collector.set_book_genre("Книга 6", "Комедии")

    books_fantasy = collector.get_books_with_specific_genre("Фантастика")
    assert set(books_fantasy) == {"Книга 4", "Книга 5"}

    books_comedy = collector.get_books_with_specific_genre("Комедии")
    assert books_comedy == ["Книга 6"]

    # Жанр отсутствует в списке genre — возвращается пустой список
    assert collector.get_books_with_specific_genre("Не жанр") == []


def test_get_books_genre_returns_entire_dict(collector):
    collector.add_new_book("Книга 7")
    collector.add_new_book("Книга 8")
    expected_dict = collector.books_genre.copy()
    assert collector.get_books_genre() == expected_dict


def test_get_books_for_children(collector):
    collector.add_new_book("Детская книга")
    collector.set_book_genre("Детская книга", "Мультфильмы")  # подходит детям

    collector.add_new_book("Страшилка")
    collector.set_book_genre("Страшилка", "Ужасы")  # возрастной жанр

    collector.add_new_book("Детектив для взрослых")
    collector.set_book_genre("Детектив для взрослых", "Детективы")  # возрастной жанр

    collector.add_new_book("Фантастика для всех")
    collector.set_book_genre("Фантастика для всех", "Фантастика")  # подходит детям

    children_books = collector.get_books_for_children()
    # В списке должны быть книги без возрастного рейтинга
    assert set(children_books) == {"Детская книга", "Фантастика для всех"}


def test_add_and_delete_book_in_favorites(collector):
    collector.add_new_book("Избранная книга")
    collector.set_book_genre("Избранная книга", "Комедии")

    # Добавляем в избранное
    collector.add_book_in_favorites("Избранная книга")
    assert "Избранная книга" in collector.favorites

    # Пытаемся добавить заново — список не должен измениться
    before = list(collector.favorites)
    collector.add_book_in_favorites("Избранная книга")
    assert collector.favorites == before

    # Пытаемся добавить книгу, которой нет в словаре — не добавится
    collector.add_book_in_favorites("Неизвестная книга")
    assert "Неизвестная книга" not in collector.favorites

    # Удаляем из избранного
    collector.delete_book_from_favorites("Избранная книга")
    assert "Избранная книга" not in collector.favorites

    # Удаляем несуществующую книгу из избранного — без ошибок
    collector.delete_book_from_favorites("Неизвестная книга")


def test_get_list_of_favorites_books_returns_correct_list(collector):
    collector.add_new_book("Книга А")
    collector.add_new_book("Книга Б")
    collector.add_book_in_favorites("Книга А")
    collector.add_book_in_favorites("Книга Б")
    favorites_list = collector.get_list_of_favorites_books()

    assert set(favorites_list) == {"Книга А", "Книга Б"}


@pytest.mark.parametrize('book_name', ['Книга X', 'Another book', 'Book 123'])
def test_add_new_book_parametrized(collector, book_name):
    collector.add_new_book(book_name)
    assert book_name in collector.books_genre
    assert collector.books_genre[book_name] == ''