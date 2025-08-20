import pytest
import json
from pathlib import Path
from library import Library
from model import Book

@pytest.fixture(autouse=True)
def teardown(tmp_path):
    """
    Her testten sonra geçici dosyaları temizler.
    """
    yield
    # Test bittikten sonra dosya temizlenir.
    file_path = tmp_path / "test_library.json"
    if file_path.exists():
        file_path.unlink()

@pytest.fixture
def library(tmp_path):
    """
    Testler için geçici bir kütüphane nesnesi oluşturur.
    """
    file_path = tmp_path / "test_library.json"
    return Library(file_path)

def test_library_init_with_new_file(tmp_path):
    """
    Dosya yokken Library nesnesi oluşturulduğunda yeni dosya yaratıldığını test eder.
    """
    file_path = tmp_path / "new_library.json"
    assert not file_path.exists()
    
    lib = Library(file_path)
    assert lib.file_name == file_path
    assert lib.file_name.exists()
    assert lib.books == {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        assert content == {}

def test_library_init_with_existing_file(tmp_path):
    """
    Dosya varken Library nesnesi oluşturulduğunda var olan dosyanın yüklendiğini test eder.
    """
    file_path = tmp_path / "existing_library.json"
    initial_data = {
        "9780547928227": {"title": "The Hobbit", "author": "J.R.R. Tolkien"}
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f)
        
    lib = Library(file_path)
    assert "9780547928227" in lib.books
    assert lib.books["9780547928227"].title == "The Hobbit"

def test_add_book_new(library, capsys):
    """
    Kütüphaneye yeni bir kitap eklemeyi test eder.
    """
    book = Book('1234567890', 'Python Crash Course', 'Eric Matthes')
    library.add_book(book)
    
    assert book.isbn in library.books
    assert len(library.books) == 1
    
    with open(library.file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data['1234567890']['title'] == 'Python Crash Course'

def test_add_book_existing(library, capsys):
    """
    Zaten var olan bir kitabı eklemeye çalışıldığında hata mesajı verip vermediğini test eder.
    """
    existing_book = Book('1234567890', 'Python Crash Course', 'Eric Matthes')
    library.add_book(existing_book)
    
    # Aynı ISBN'e sahip farklı bir kitap eklemeyi dene
    new_book_with_same_isbn = Book('1234567890', 'Fluent Python', 'Luciano Ramalho')
    library.add_book(new_book_with_same_isbn)
    
    # Hata mesajının çıktıda olup olmadığını kontrol et
    captured = capsys.readouterr()
    assert "Bu ISBN koduna sahip bir kitap zaten veri tabanında mevcut" in captured.out
    
    # Kitap sayısının değişmediğini kontrol et
    assert len(library.books) == 1
    # Var olan kitabın değişmediğini kontrol et
    assert library.books['1234567890'].title == 'Python Crash Course'

def test_remove_book_existing(library):
    """
    Var olan bir kitabın başarıyla silindiğini test eder.
    """
    book = Book('1234567890', 'Python Crash Course', 'Eric Matthes')
    library.add_book(book)
    
    assert book.isbn in library.books
    
    library.remove_book(book.isbn)
    assert book.isbn not in library.books
    
    with open(library.file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert book.isbn not in data

def test_remove_book_not_found(library, capsys):
    """
    Olmayan bir kitabı silmeye çalışıldığında hata mesajı verip vermediğini test eder.
    """
    library.remove_book("nonexistent_isbn")
    
    captured = capsys.readouterr()
    assert "Kitap bulunamadı." in captured.out
    
    assert len(library.books) == 0

def test_find_book_existing(library, capsys):
    """
    Var olan bir kitabın doğru şekilde bulunup döndürüldüğünü test eder.
    """
    book = Book('1234567890', 'Python Crash Course', 'Eric Matthes')
    library.add_book(book)
    
    found_book = library.find_book(book.isbn)
    assert found_book is not None
    assert found_book.isbn == book.isbn
    
    captured = capsys.readouterr()
    assert str(book) in captured.out

def test_find_book_not_found(library, capsys):
    """
    Olmayan bir kitabın aranmasında None döndürüldüğünü test eder.
    """
    found_book = library.find_book("nonexistent_isbn")
    assert found_book is None
    
    captured = capsys.readouterr()
    assert "Kitap bulunamadı." in captured.out