from model import Book
from library import Library
import sys
from utils import clear_screen, get_non_empty_input, get_valid_isbn, get_valid_menu_choice


def main():
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
            b_title = get_non_empty_input("Kitap Adı: ")
            b_author = get_non_empty_input("Yazar Adı: ")
            b_isbn = get_valid_isbn()
            book = Book(isbn=b_isbn, title=b_title, author=b_author)
            lib.add_book(book)
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
    main()