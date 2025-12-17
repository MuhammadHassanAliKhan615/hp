class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book_id):
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
            return True
        return False

    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False
