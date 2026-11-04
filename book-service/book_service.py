class BookService:
    """Manage books in memory."""

    def create_book(self, title: str, author: str) -> dict[str, str | int]:
        """Create and return a book with a unique ID."""
        ...

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
