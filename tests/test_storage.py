from booklib import __version__
from booklib import storage


def test_version_format():
  assert isinstance(__version__, str) and __version__


def test_add_and_list(tmp_path, monkeypatch):
  # redirect storage to temp dir
  monkeypatch.setenv("HOME", str(tmp_path))
  b = storage.add_book("The Pragmatic Programmer", "Hunt & Thomas", ["programming", "classic"])
  assert b.id == 1
  books = storage.list_books()
  assert len(books) == 1
  assert books[0].title.startswith("The Pragmatic")

