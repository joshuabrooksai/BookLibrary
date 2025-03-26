from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional


DATA_DIR = Path.home() / ".booklibrary"
DB_FILE = DATA_DIR / "books.json"


@dataclass
class Book:
  id: int
  title: str
  author: str
  tags: List[str]
  rating: Optional[float] = None
  status: str = "unread"  # unread | reading | done


def _ensure_store() -> None:
  DATA_DIR.mkdir(parents=True, exist_ok=True)
  if not DB_FILE.exists():
    DB_FILE.write_text(json.dumps({"seq": 0, "items": []}, ensure_ascii=False, indent=2))


def _load() -> dict:
  _ensure_store()
  return json.loads(DB_FILE.read_text())


def _save(payload: dict) -> None:
  DB_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def list_books() -> List[Book]:
  data = _load()
  return [Book(**b) for b in data.get("items", [])]


def add_book(title: str, author: str, tags: List[str] | None = None) -> Book:
  data = _load()
  seq = int(data.get("seq", 0)) + 1
  book = Book(id=seq, title=title, author=author, tags=tags or [])
  data["seq"] = seq
  data.setdefault("items", []).append(asdict(book))
  _save(data)
  return book


def get_book(book_id: int) -> Optional[Book]:
  data = _load()
  for b in data.get("items", []):
    if b["id"] == book_id:
      return Book(**b)
  return None


def update_book(book_id: int, **fields) -> Optional[Book]:
  data = _load()
  items = data.get("items", [])
  for i, b in enumerate(items):
    if b["id"] == book_id:
      b.update({k: v for k, v in fields.items() if v is not None})
      items[i] = b
      _save(data)
      return Book(**b)
  return None


def delete_book(book_id: int) -> bool:
  data = _load()
  items = data.get("items", [])
  new_items = [b for b in items if b["id"] != book_id]
  if len(new_items) != len(items):
    data["items"] = new_items
    _save(data)
    return True
  return False

