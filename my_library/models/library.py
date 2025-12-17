class Library:
    def __init__(self):
        self.books = {}
        self.users = {}

    def add_book(self, book):
        self.books[book.book_id] = book

    def search_by_title(self, title):
        return [b for b in self.books.values() if title.lower() in b.title.lower()]

    def search_by_author(self, author):
        return [b for b in self.books.values() if author.lower() in b.author.lower()]

    def borrow_book(self, book_id, user):
        book = self.books.get(book_id)
        if book and book.borrow() and user.borrow_book(book_id):
            return True
        return False

    def return_book(self, book_id, user):
        book = self.books.get(book_id)
        if book and user.return_book(book_id):
            book.return_book()
            return True
        return False
