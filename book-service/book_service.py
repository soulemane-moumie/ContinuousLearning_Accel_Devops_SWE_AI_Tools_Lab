"""In-memory book management with create, retrieve, list, and delete operations.

``create_book`` validates and stores a book with a unique ID; ``get_book``
retrieves one by ID; ``list_books`` optionally filters and sorts the collection;
and ``delete_book`` removes a book by ID. Lookup and deletion raise ``KeyError``
when the ID is unknown.

Example:
    >>> service = BookService()
    >>> book = service.create_book("Dune", "Frank Herbert")
    >>> service.get_book(book["id"])["title"]
    'Dune'
    >>> service.list_books(search="dune")
    [{'id': 1, 'title': 'Dune', 'author': 'Frank Herbert'}]
    >>> service.delete_book(book["id"])
"""


class BookService:
    """Manage books in memory."""

    def __init__(self) -> None:
        self.books: list[dict[str, str | int]] = []
        self._next_id = 1

    def create_book(self, title: str, author: str) -> dict[str, str | int]:
        """Create and return a book with a unique ID."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("author must be a non-empty string")

        book: dict[str, str | int] = {
            "id": self._next_id,
            "title": title.strip(),
            "author": author.strip(),
        }
        self.books.append(book)
        self._next_id += 1
        return book

    def get_book(self, book_id: int) -> dict[str, str | int]:
        """Return the book matching the ID, or raise an error if not found."""
        for book in self.books:
            if book["id"] == book_id:
                return book
        raise KeyError(f"Book with id {book_id} was not found")

    def list_books(
        self,
        search: str | None = None,
        sort_by: str | None = None,
        ascending: bool = True,
    ) -> list[dict[str, str | int]]:
        """Return books, optionally filtered by search and sorted."""
        books = self.books
        if search is not None:
            query = search.casefold()
            books = [
                book
                for book in books
                if query in str(book["title"]).casefold()
                or query in str(book["author"]).casefold()
            ]

        if sort_by is not None:
            if sort_by not in {"id", "title", "author"}:
                raise ValueError("sort_by must be 'id', 'title', or 'author'")
            books = sorted(books, key=lambda book: book[sort_by], reverse=not ascending)

        return list(books)

    def delete_book(self, book_id: int) -> None:
        """Delete the book matching the ID, or raise an error if not found."""
        book = self.get_book(book_id)
        self.books.remove(book)


def demo() -> None:
    """Demonstrate creating, retrieving, listing, and deleting books."""
    service = BookService()
    first_book = service.create_book("The Hobbit", "J. R. R. Tolkien")
    second_book = service.create_book("Dune", "Frank Herbert")

    assert service.get_book(first_book["id"]) == first_book
    assert service.list_books() == [first_book, second_book]

    service.delete_book(second_book["id"])
    assert second_book["id"] not in [book["id"] for book in service.list_books()]
