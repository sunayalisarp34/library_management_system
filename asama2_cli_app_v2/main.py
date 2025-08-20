import asyncio
from model import Book
from library import Library
import sys
from utils import (clear_screen,  
                   get_valid_isbn, 
                   get_valid_menu_choice,
                   fetch_book_from_api)


async def main():
    lib = Library()
    while True:
        clear_screen()
        print("\n--- Kütüphane Yönetimi ---")
        print("1 - Kitap Ekle")
        print("2 - Kitapları Listele")
        print("3 - Kitap Ara")
        print("4 - Kitap Sil")
        print("5 - Çıkış")

        choice = get_valid_menu_choice()

        if choice == "1":
            b_isbn = get_valid_isbn()
            if lib.find_book(isbn=b_isbn):
                print(f"Aranılan kitap zaten kütüphanede mevcut:\n{lib.find_book(isbn=isbn)}")
            else:
                book = await fetch_book_from_api(isbn=b_isbn)
                if book:
                    lib.add_book(book)
                else:
                    print("Aranılan kitap getirilemedi.")
            input("\nDevam etmek için Enter'a basın...")
        
        elif choice == "2":
            lib.list_books()
            input("\nDevam etmek için Enter'a basın...")
        
        elif choice == "3":
            isbn = get_valid_isbn()
            lib.find_book(isbn)
            input("\nDevam etmek için Enter'a basın...")
        
        elif choice == "4":
            lib.list_books()
            isbn = get_valid_isbn()
            lib.remove_book(isbn)
            input("\nDevam etmek için Enter'a basın...")
        
        elif choice == "5":
            print("Programdan Çıkılıyor.")
            sys.exit()

if __name__ == '__main__':
    asyncio.run(main())