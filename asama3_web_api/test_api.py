# tests/test_api.py
import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient
from api import app, library
from model import Book
import json
from pathlib import Path

# --- Fixture'lar (Hazırlık Fonksiyonları) ---
@pytest.fixture(autouse=True)
def mock_library_file(tmp_path):
    """
    Her test için geçici bir kütüphane dosyası oluşturur ve temizler.
    """
    original_file_name = library.file_name
    new_file = tmp_path / "test_library.json"
    library.file_name = new_file
    
    library.file_name.write_text(json.dumps({}, ensure_ascii=False), encoding='utf-8')
    library.books = {}
    
    yield
    
    library.file_name = original_file_name

# --- Testler ---
def test_list_books_empty():
    """
    Boş bir kütüphanedeyken GET /books uç noktasının boş bir JSON döndürdüğünü test eder.
    """
    client = TestClient(app)
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {}

def test_add_and_list_book_success(mock_library_file):
    """
    POST /books ile başarılı bir kitap ekleme senaryosunu test eder.
    """
    client = TestClient(app)
    isbn = "9780321765723"
    api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    mock_api_data = {
        f"ISBN:{isbn}": {
            "title": "The Lord of the Rings",
            "authors": [{"name": "J.R.R. Tolkien"}],
        }
    }
    
    with respx.mock(base_url="https://openlibrary.org") as respx_mock:
        respx_mock.get(api_url).mock(return_value=Response(200, json=mock_api_data))
        
        response = client.post("/books", json={"isbn": isbn})
        assert response.status_code == 400
        assert response.json()["message"] == "Kitap başarıyla eklendi."
        assert response.json()["book"]["isbn"] == isbn
        
        response_get = client.get("/books")
        assert response_get.status_code == 200
        assert isbn in response_get.json()
        assert response_get.json()[isbn]["title"] == "The Lord of the Rings"

def test_add_book_already_exists(mock_library_file):
    """
    Zaten kütüphanede olan bir kitabı eklemeye çalışmayı test eder.
    """
    client = TestClient(app)
    isbn = "9780547928227"
    library.books[isbn] = Book(isbn=isbn, title="The Hobbit", author="J.R.R. Tolkien")
    library.save_books()
    
    response = client.post("/books", json={"isbn": isbn})
    assert response.status_code == 409
    assert response.json()["detail"] == "Bu ISBN'e sahip kitap zaten mevcut."

def test_add_book_not_found(mock_library_file):
    """
    Open Library'de bulunmayan bir kitabı eklemeye çalışmayı test eder.
    """
    client = TestClient(app)
    isbn = "9999999999999"
    api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    
    with respx.mock(base_url="https://openlibrary.org") as respx_mock:
        respx_mock.get(api_url).mock(return_value=Response(200, json={}))
        
        response = client.post("/books", json={"isbn": isbn})
        assert response.status_code == 400
        assert response.json()["detail"] == "Kitap Open Library'de bulunamadı."

def test_delete_book_success(mock_library_file):
    """
    Var olan bir kitabı başarıyla silmeyi test eder.
    """
    client = TestClient(app)
    isbn = "9780547928227"
    library.books[isbn] = Book(isbn=isbn, title="The Hobbit", author="J.R.R. Tolkien")
    library.save_books()
    
    response = client.delete(f"/books/{isbn}")
    assert response.status_code == 200
    assert response.json()["message"] == "Kitap başarıyla silindi."
    
    assert isbn not in library.books

def test_delete_book_not_found(mock_library_file):
    """
    Var olmayan bir kitabı silmeye çalışmayı test eder.
    """
    client = TestClient(app)
    response = client.delete("/books/nonexistent_isbn")
    assert response.status_code == 404
    assert response.json()["detail"] == "Kitap bulunamadı."