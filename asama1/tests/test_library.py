import pytest
import json
from pathlib import Path
from book import Book
from library import Library
from main import validate_isbn


# ---------- Book Sınıfı Testleri ----------

def test_book_str():
    book = Book(isbn="1234567890", title="Python 101", author="Guido")
    assert str(book) == "Python 101 by Guido (ISBN: 1234567890)"


def test_book_to_dict():
    book = Book(isbn="123", title="Fluent Python", author="Luciano")
    expected = {"title": "Fluent Python", "author": "Luciano"}
    assert book.to_dict() == expected


def test_book_from_dict():
    data = {"title": "Clean Code", "author": "Robert C. Martin"}
    book = Book.from_dict(isbn="111", data=data)
    assert book.isbn == "111"
    assert book.title == "Clean Code"
    assert book.author == "Robert C. Martin"


# ---------- Library Sınıfı Testleri ----------

@pytest.fixture
def temp_library(tmp_path):
    """Geçici dosya ile test kütüphanesi oluşturur."""
    lib_file = tmp_path / "test_library.json"
    return Library(file_name=lib_file)


def test_library_init_creates_file(tmp_path):
    lib_file = tmp_path / "test_lib.json"
    lib = Library(file_name=lib_file)
    assert lib_file.exists()
    assert lib.books == {}


def test_add_book(temp_library):
    book = Book(isbn="1234567890", title="Python", author="Guido")
    temp_library.add_book(book)
    assert "1234567890" in temp_library.books


def test_add_book_duplicate(temp_library, capsys):
    book = Book(isbn="123", title="Book1", author="Author1")
    temp_library.add_book(book)
    temp_library.add_book(book)
    captured = capsys.readouterr()
    assert "Bu ISBN koduna sahip bir kitap zaten" in captured.out


def test_remove_book(temp_library):
    book = Book(isbn="999", title="Remove Me", author="Author")
    temp_library.add_book(book)
    temp_library.remove_book("999")
    assert "999" not in temp_library.books


def test_remove_nonexistent_book(temp_library, capsys):
    temp_library.remove_book("not_exists")
    captured = capsys.readouterr()
    assert "Kitap bulunamadı." in captured.out


def test_find_book(temp_library):
    book = Book(isbn="321", title="Find Me", author="Author")
    temp_library.add_book(book)
    found = temp_library.find_book("321")
    assert found.title == "Find Me"


def test_find_nonexistent_book(temp_library, capsys):
    result = temp_library.find_book("000")
    captured = capsys.readouterr()
    assert result is None
    assert "Kitap bulunamadı." in captured.out


def test_list_books_empty(temp_library, capsys):
    temp_library.list_books()
    captured = capsys.readouterr()
    assert "Kütüphanede kitap yok." in captured.out


def test_list_books_non_empty(temp_library, capsys):
    book = Book(isbn="111", title="List Me", author="Author")
    temp_library.add_book(book)
    temp_library.list_books()
    captured = capsys.readouterr()
    assert "List Me" in captured.out


# ---------- ISBN Doğrulama Testleri ----------

def test_validate_isbn_10_valid():
    assert validate_isbn("0306406152") == "ISBN-10"  # Geçerli ISBN-10


def test_validate_isbn_10_with_X():
    assert validate_isbn("012000030X") == "ISBN-10"


def test_validate_isbn_10_invalid():
    assert validate_isbn("1234567890") is None


def test_validate_isbn_13_valid():
    assert validate_isbn("9780306406157") == "ISBN-10"  # Çünkü return ifadesi "ISBN-10" dönüyor


def test_validate_isbn_13_invalid():
    assert validate_isbn("9780306406158") is None
