class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def to_dict(self):
        return {"title": self.title, "author": self.author}
    
    @classmethod
    def from_dict(cls, isbn, data):
        return cls(isbn=isbn, title=data['title'], author=data['author'])