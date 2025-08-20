import os

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


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value.title()
        print("Bu alan boş bırakılmamalıdır.")