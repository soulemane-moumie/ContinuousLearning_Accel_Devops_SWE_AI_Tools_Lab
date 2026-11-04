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
        ...

    def list_books(
        self,
        search: str | None = None,
        sort_by: str | None = None,
        ascending: bool = True,
    ) -> list[dict[str, str | int]]:
        """Return books, optionally filtered by search and sorted."""
        ...

    def delete_book(self, book_id: int) -> None:
        """Delete the book matching the ID, or raise an error if not found."""
        ...
