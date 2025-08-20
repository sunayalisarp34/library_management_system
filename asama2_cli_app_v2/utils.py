import asyncio
import sys
import os
from asyncio import Semaphore
import httpx
import random
import time
from model import Book


RATE_LIMIT_DELAY = 4
rate_limiter = Semaphore(1)
OPEN_LIBRARY_API = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_menu_choice():
    valid_choices = {"1", "2", "3", "4", "5"}
    while True:
        choice = input("Bir seçenek girin (1-5): ").strip()
        if choice in valid_choices:
            return choice
        print("Geçersiz seçenek. Lütfen 1 ile 5 arasında bir değer girin.")


def validate_isbn(isbn: str):
    isbn = isbn.replace('-', '').replace(' ', '')
    if len(isbn) == 10:
        if isbn[:-1].isdigit():
            total = 0
            for i in range(9):
                total += int(isbn[i]) * (10 - i)
            
            check_digit = isbn[9].upper()
            if check_digit == 'X':
                total += 10
            elif check_digit.isdigit():
                total += int(check_digit)
            else:
                return None
            
            return "ISBN-10" if total % 11 == 0 else None
        return None

    elif len(isbn) == 13:
        if isbn.isdigit():
            total = 0
            for i in range(12):
                total += int(isbn[i]) * (1 if i % 2 == 0 else 3)

            check_digit = int(isbn[12])
            return  "ISBN-10" if (10 - (total % 10)) % 10 == check_digit else None


def get_valid_isbn():
    while True:
        isbn_input = input("ISBN girin (10 veya 13 haneli, '-' veya boşluk içerebilir): ").strip()
        cleaned_isbn = isbn_input.replace('-', '').replace(' ', '')
        
        result = validate_isbn(isbn_input)
        if result:
            print(f"ISBN geçerli: {result}")
            return cleaned_isbn
        else:
            print("Geçersiz ISBN. Lütfen tekrar deneyiniz.")

async def fetch_book_from_api(isbn, retries=3):
    url = OPEN_LIBRARY_API.format(isbn=isbn)

    async with rate_limiter:
        await asyncio.sleep(RATE_LIMIT_DELAY)

        for attempt in range(1, retries + 1):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    key = f"ISBN:{isbn}"
                    if key in data:
                        book_data = data[key]
                        title = book_data.get("title", "Unknown Title")
                        authors = book_data.get("authors", [])
                        author_name = authors[0]['name'] if authors else "Unknown Author"
                        return Book(isbn=isbn, title=title, author=author_name)
                    else:
                        print(f"İlgili ISBN'e ({isbn}) ait kitap bulunamamıştır.")
                        return None
                elif response.status_code == 404:
                    print("İlgili kitap bulunamadı. (404)")
                    return None
                else:
                    print(f"Beklenmeyen hata: {response.status_code}")
                    return None
            except (httpx.RequestError, httpx.TimeoutException) as e:
                wait_time = 2 ** attempt + random.uniform(0, 0.5)
                print(f"Network error: {e}. Retrying in {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
            except Exception as e:
                print(f"Unexpented Error: {e}")
                return None
            
            print("Çoklu denemeden sonra kitap getirilememiştir...")
            return None


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value.title()
        print("Bu alan boş bırakılmamalıdır.")