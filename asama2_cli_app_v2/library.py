import json
from pathlib import Path
from model import Book

class Library:
    def __init__(self, file_name="library.json"):
        self.file_name = Path(file_name)
        self.books = {}

        if not self.file_name.exists():
            self.file_name.write_text(json.dumps({}, ensure_ascii=False), encoding='utf-8')
            print(f"{self.file_name} oluşturuldu.")
        else:
            print(f"{self.file_name} bulundu.")
        
        self.load_books()
    
    def load_books(self):
        try:
            raw_data = json.loads(self.file_name.read_text(encoding='utf-8'))
            self.books = {
                isbn: Book.from_dict(isbn, info) for isbn, info in raw_data.items()
            }
            print("Kitaplar yüklendi.")
        except Exception as e:
            print(f"Kitapların yüklenmesi başarısız oldu: {e}")
            self.books = {}
    
    def add_book(self, book):
        if book.isbn in self.books:
            print("Bu ISBN koduna sahip bir kitap zaten veri tabanında mevcut")
            print(book)
            return
        self.books[book.isbn] = book
        self.save_books()
        print("Kitap bilgileri başarıyla kaydedildi.")
    
    def save_books(self):
        data = {
                isbn: book.to_dict() for isbn, book in self.books.items()
            }
        self.file_name.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    
    def remove_book(self, isbn):
        if isbn in self.books:
            del self.books[isbn]
            self.save_books()
            print("Kitap başarıyla kaldırıldı.")
        else:
            print("Kitap bulunamadı.")
    
    def list_books(self):
        if not self.books:
            print("Kütüphanede kitap yok.")
            return
        
        for i, book in enumerate(self.books.values(), 1):
            print(f"{i} - {book}")
    
    def find_book(self, isbn):
        book = self.books.get(isbn)
        if book:
            print(book)
            return book
        else:
            print("Kitap bulunamadı.")
            return None
        
