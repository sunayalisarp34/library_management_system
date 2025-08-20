import httpx
import pytest
import respx
from httpx import Response
from model import Book
from utils import fetch_book_from_api

@pytest.mark.asyncio
async def test_fetch_book_from_api_success():
    """
    API'den başarılı bir şekilde kitap verisi çekmeyi test eder.
    """
    isbn = "9780321765723"
    api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    
    mock_response_data = {
        f"ISBN:{isbn}": {
            "title": "The Lord of the Rings",
            "authors": [{"name": "J.R.R. Tolkien"}],
        }
    }
    
    with respx.mock(base_url="https://openlibrary.org") as respx_mock:
        respx_mock.get(api_url).mock(return_value=Response(200, json=mock_response_data))
        
        book = await fetch_book_from_api(isbn)
        
        assert isinstance(book, Book)
        assert book.isbn == isbn
        assert book.title == "The Lord of the Rings"
        assert book.author == "J.R.R. Tolkien"

@pytest.mark.asyncio
async def test_fetch_book_from_api_not_found():
    """
    API'de bulunamayan bir kitap için None döndürmeyi test eder.
    """
    isbn = "9999999999999"
    api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    
    # API'den boş bir cevap döneceğini taklit et
    mock_response_data = {}
    
    with respx.mock(base_url="https://openlibrary.org") as respx_mock:
        respx_mock.get(api_url).mock(return_value=Response(200, json=mock_response_data))
        
        book = await fetch_book_from_api(isbn)
        
        assert book is None

@pytest.mark.asyncio
async def test_fetch_book_from_api_connection_error():
    """
    Ağ hatası durumunda fonksiyonun None döndürmesini test eder.
    """
    isbn = "9780321765723"
    api_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    
    with respx.mock(base_url="https://openlibrary.org") as respx_mock:
        respx_mock.get(api_url).mock(side_effect=httpx.ConnectError("Connection failed"))
        
        book = await fetch_book_from_api(isbn, retries=1) # Deneme sayısını 1'e düşür
        
        assert book is None