import pytest
from main import get_valid_menu_choice, get_non_empty_input, get_valid_isbn, validate_isbn


# -------- get_valid_menu_choice Testleri --------

def test_get_valid_menu_choice_valid(monkeypatch):
    # İlk denemede direkt geçerli bir giriş
    monkeypatch.setattr("builtins.input", lambda _: "3")
    assert get_valid_menu_choice() == "3"


def test_get_valid_menu_choice_invalid_then_valid(monkeypatch, capsys):
    # Önce hatalı, sonra doğru giriş
    inputs = iter(["9", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_valid_menu_choice()
    captured = capsys.readouterr()

    assert "Geçersiz seçenek" in captured.out
    assert result == "2"


# -------- get_non_empty_input Testleri --------

def test_get_non_empty_input(monkeypatch, capsys):
    # Önce boş string, sonra geçerli string
    inputs = iter(["   ", "python "])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_non_empty_input("Kitap Adı: ")
    captured = capsys.readouterr()

    assert "boş bırakılmamalıdır" in captured.out
    assert result == "Python"  # .title() uygulanmış olmalı


# -------- get_valid_isbn Testleri --------

def test_get_valid_isbn_valid(monkeypatch, capsys):
    # Geçerli ISBN (9780306406157)
    monkeypatch.setattr("builtins.input", lambda _: "9780306406157")

    result = get_valid_isbn()
    captured = capsys.readouterr()

    assert "ISBN geçerli" in captured.out
    assert result == "9780306406157"  # temizlenmiş ISBN


def test_get_valid_isbn_invalid_then_valid(monkeypatch, capsys):
    # Önce geçersiz ISBN, sonra geçerli
    inputs = iter(["1234567890", "0306406152"])  # ilk yanlış, ikinci doğru
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_valid_isbn()
    captured = capsys.readouterr()

    assert "Geçersiz ISBN" in captured.out
    assert result == "0306406152"


# -------- validate_isbn Doğrudan Test (tekrar güvence için) --------

@pytest.mark.parametrize("isbn,expected", [
    ("0306406152", "ISBN-10"),    # Geçerli ISBN-10
    ("012000030X", "ISBN-10"),    # ISBN-10, X ile biten
    ("9780306406157", "ISBN-10"), # Geçerli ISBN-13 ama dönüş "ISBN-10"
    ("1234567890", None),         # Geçersiz ISBN-10
    ("9780306406158", None),      # Geçersiz ISBN-13
])
def test_validate_isbn(isbn, expected):
    assert validate_isbn(isbn) == expected
