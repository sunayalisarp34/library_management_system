import pytest
from model import Book

@pytest.fixture
def sample_book():
    """
    Testler için örnek bir Book nesnesi oluşturur.
    """
    return Book(isbn='978-0321765723', title='The Lord of the Rings', author='J.R.R. Tolkien')

def test_book_attributes(sample_book):
    """
    Kitap nesnesinin doğru niteliklere sahip olup olmadığını kontrol eder.
    """
    assert sample_book.isbn == '978-0321765723'
    assert sample_book.title == 'The Lord of the Rings'
    assert sample_book.author == 'J.R.R. Tolkien'

def test_book_str_representation(sample_book):
    """
    __str__ metodunun beklenen formatta çıktı verip vermediğini kontrol eder.
    """
    expected_str = "The Lord of the Rings by J.R.R. Tolkien (ISBN: 978-0321765723)"
    assert str(sample_book) == expected_str

def test_book_to_dict_method(sample_book):
    """
    to_dict metodunun doğru sözlüğü döndürüp döndürmediğini test eder.
    """
    expected_dict = {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"}
    assert sample_book.to_dict() == expected_dict

def test_book_from_dict_method():
    """
    from_dict sınıf metodunun doğru Book nesnesini oluşturup oluşturmadığını test eder.
    """
    data = {"title": "The Hobbit", "author": "J.R.R. Tolkien"}
    isbn = "9780547928227"
    book = Book.from_dict(isbn, data)
    assert isinstance(book, Book)
    assert book.isbn == isbn
    assert book.title == "The Hobbit"
    assert book.author == "J.R.R. Tolkien"