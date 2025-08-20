# api.py
import json
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List, Optional

# SlowAPI için gerekli importlar
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from model import Book
from library import Library
from utils import fetch_book_from_api, validate_isbn

# Pydantic Veri Modelleri
class BookModel(BaseModel):
    isbn: str
    title: str
    author: str
    
    @classmethod
    def from_book_class(cls, book: Book):
        return cls(isbn=book.isbn, title=book.title, author=book.author)

class ISBNModel(BaseModel):
    isbn: str

# --- SlowAPI Entegrasyonu ---
# Limiter nesnesini oluştur
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter  # Limiter'ı uygulamanın state'ine ekle
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Uygulama başladığında kütüphane nesnesini oluştur ve yükle
library = Library()

@app.get("/books", response_model=Dict[str, BookModel])
@limiter.limit("10/minute")  # Dakikada 10 istek limiti
async def list_books(request: Request):
    """
    Kütüphanedeki tüm kitapları listeler.
    """
    if not library.books:
        return {}
    
    return {isbn: BookModel.from_book_class(book) for isbn, book in library.books.items()}

@app.post("/books", status_code=201)
@limiter.limit("5/minute")  # Dakikada 5 istek limiti
async def add_book(request: Request, isbn_data: ISBNModel):
    """
    Belirtilen ISBN'e sahip kitabı Open Library'den alıp kütüphaneye ekler.
    """
    isbn = isbn_data.isbn.replace("-", "").replace(" ", "")
    
    if not validate_isbn(isbn):
        raise HTTPException(status_code=400, detail="Geçersiz ISBN formatı.")

    if library.find_book(isbn):
        raise HTTPException(status_code=409, detail="Bu ISBN'e sahip kitap zaten mevcut.")

    book = await fetch_book_from_api(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap Open Library'de bulunamadı.")
    
    library.add_book(book)
    return {"message": "Kitap başarıyla eklendi.", "book": BookModel.from_book_class(book)}

@app.delete("/books/{isbn}", status_code=200)
@limiter.limit("3/minute")  # Dakikada 3 istek limiti
async def remove_book(request: Request, isbn: str):
    """
    Belirtilen ISBN'e sahip kitabı kütüphaneden siler.
    """
    if not library.find_book(isbn):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")

    library.remove_book(isbn)
    return {"message": "Kitap başarıyla silindi."}