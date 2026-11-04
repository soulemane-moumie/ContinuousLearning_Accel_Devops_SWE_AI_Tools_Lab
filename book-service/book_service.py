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
    """Create, retrieve, list, and delete books stored in memory."""

    @staticmethod
    def _validate_non_empty_string(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value.strip()

    def __init__(self) -> None:
        """Initialize an empty collection and start book IDs at one."""
        self._books: list[dict[str, str | int]] = []
        self._next_id: int = 1

    def create_book(self, title: str, author: str) -> dict[str, str | int]:
        """Validate, store, and return a book with a unique ID.

        Args:
            title: The book's non-empty title.
            author: The book's non-empty author.

        Returns:
            The created book, containing its ID, title, and author.

        Raises:
            ValueError: If either value is not a non-empty string.
        """
        book: dict[str, str | int] = {
            "id": self._next_id,
            "title": self._validate_non_empty_string(title, "title"),
            "author": self._validate_non_empty_string(author, "author"),
        }
        self._books.append(book)
        self._next_id += 1
        return book.copy()

    def get_book(self, book_id: int) -> dict[str, str | int]:
        """Return the book with the requested ID.

        Args:
            book_id: The ID of the book to retrieve.

        Returns:
            A copy of the matching book.

        Raises:
            ValueError: If ``book_id`` is not an integer.
            KeyError: If no book has the requested ID.
        """
        if type(book_id) is not int:
            raise ValueError("book_id must be an integer")

        for book in self._books:
            if book["id"] == book_id:
                return book.copy()
        raise KeyError(f"Book with id {book_id} was not found")

    def list_books(
        self,
        search: str | None = None,
        sort_by: str | None = None,
        ascending: bool = True,
    ) -> list[dict[str, str | int]]:
        """Return books, optionally filtering by text and sorting by a field.

        Args:
            search: Optional case-insensitive text to match in titles or authors.
            sort_by: Optional field to sort by: ``"id"``, ``"title"``, or
                ``"author"``.
            ascending: Whether to sort in ascending order when ``sort_by`` is
                provided.

        Returns:
            The matching books in insertion order or the requested sort order.

        Raises:
            ValueError: If ``search`` is not a string or ``sort_by`` is not a
                supported field.
        """
        books = self._books
        if search is not None:
            if not isinstance(search, str):
                raise ValueError("search must be a string")
            query = search.casefold()
            books = [
                book
                for book in books
                if query in str(book["title"]).casefold()
                or query in str(book["author"]).casefold()
            ]

        if sort_by is not None:
            if not isinstance(sort_by, str) or sort_by not in {"id", "title", "author"}:
                raise ValueError("sort_by must be 'id', 'title', or 'author'")
            books = sorted(books, key=lambda book: book[sort_by], reverse=not ascending)

        return [book.copy() for book in books]

    def delete_book(self, book_id: int) -> None:
        """Delete the book with the requested ID.

        Args:
            book_id: The ID of the book to delete.

        Raises:
            KeyError: If no book has the requested ID.
        """
        book = self.get_book(book_id)
        self._books.remove(book)


def demo() -> None:
    """Demonstrate creating, retrieving, listing, and deleting books."""
    service = BookService()
    first_book = service.create_book("The Hobbit", "J. R. R. Tolkien")
    second_book = service.create_book("Dune", "Frank Herbert")

    assert service.get_book(first_book["id"]) == first_book
    assert service.list_books() == [first_book, second_book]

    service.delete_book(second_book["id"])
    assert second_book["id"] not in [book["id"] for book in service.list_books()]
