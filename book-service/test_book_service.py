import pytest

from book_service import BookService


@pytest.mark.parametrize(
    ("title", "author"),
    [
        ("", "Author"),
        ("   ", "Author"),
        ("Title", ""),
        ("Title", "   "),
        (None, "Author"),
        ("Title", 1),
    ],
)
def test_create_book_rejects_invalid_fields(title, author):
    service = BookService()

    with pytest.raises(ValueError):
        service.create_book(title, author)

    assert service.list_books() == []


def test_create_book_trims_fields_and_assigns_unique_ids():
    service = BookService()

    first = service.create_book("  Dune  ", " Frank Herbert ")
    second = service.create_book("Dune", "Frank Herbert")

    assert first == {"id": 1, "title": "Dune", "author": "Frank Herbert"}
    assert second["id"] == 2
    assert service.list_books() == [first, second]


def test_returned_books_cannot_mutate_stored_records():
    service = BookService()
    created = service.create_book("Dune", "Frank Herbert")
    created["title"] = "Changed"

    retrieved = service.get_book(1)
    retrieved["author"] = "Changed"
    listed = service.list_books()
    listed[0]["title"] = "Changed again"

    assert service.get_book(1) == {
        "id": 1,
        "title": "Dune",
        "author": "Frank Herbert",
    }


def test_get_book_raises_for_missing_ids():
    service = BookService()

    for book_id in (0, -1, 1):
        with pytest.raises(KeyError):
            service.get_book(book_id)


@pytest.mark.parametrize("book_id", [True, False, "1", 1.0, None])
def test_get_book_rejects_non_integer_ids(book_id):
    with pytest.raises(ValueError, match="book_id must be an integer"):
        BookService().get_book(book_id)


def test_search_matches_title_or_author_without_case_sensitivity():
    service = BookService()
    dune = service.create_book("Dune", "Frank Herbert")
    hobbit = service.create_book("The Hobbit", "J. R. R. Tolkien")

    assert service.list_books(search="DUNE") == [dune]
    assert service.list_books(search="tolkien") == [hobbit]
    assert service.list_books(search="missing") == []


@pytest.mark.parametrize("search", [1, [], True])
def test_search_rejects_non_string_values(search):
    with pytest.raises(ValueError, match="search must be a string"):
        BookService().list_books(search=search)


@pytest.mark.parametrize(
    ("sort_by", "ascending", "expected_ids"),
    [
        ("id", True, [1, 2, 3]),
        ("id", False, [3, 2, 1]),
        ("title", True, [2, 3, 1]),
        ("title", False, [1, 2, 3]),
        ("author", True, [2, 3, 1]),
        ("author", False, [1, 3, 2]),
    ],
)
def test_list_books_sorts_by_field(sort_by, ascending, expected_ids):
    service = BookService()
    service.create_book("Zulu", "C. Author")
    service.create_book("Alpha", "A. Author")
    service.create_book("Alpha", "B. Author")

    books = service.list_books(sort_by=sort_by, ascending=ascending)

    assert [book["id"] for book in books] == expected_ids


def test_sorting_is_stable_for_equal_values():
    service = BookService()
    first = service.create_book("Same", "Author")
    second = service.create_book("Same", "Author")

    assert service.list_books(sort_by="title") == [first, second]


def test_list_books_rejects_invalid_sort_field():
    for sort_by in ("publisher", []):
        with pytest.raises(ValueError):
            BookService().list_books(sort_by=sort_by)


def test_delete_book_removes_only_matching_book_and_raises_if_missing():
    service = BookService()
    first = service.create_book("First", "Author")
    second = service.create_book("Second", "Author")

    service.delete_book(first["id"])

    assert service.list_books() == [second]
    with pytest.raises(KeyError):
        service.delete_book(first["id"])


def test_large_list_can_be_searched_sorted_and_deleted():
    service = BookService()
    books = [
        service.create_book(f"Book {index}", f"Author {index}")
        for index in range(1_000)
    ]

    assert len(service.list_books()) == 1_000
    assert service.get_book(books[-1]["id"]) == books[-1]
    assert service.list_books(search="Book 999") == [books[-1]]
    assert service.list_books(sort_by="id", ascending=False)[0] == books[-1]

    service.delete_book(books[-1]["id"])
    assert len(service.list_books()) == 999
