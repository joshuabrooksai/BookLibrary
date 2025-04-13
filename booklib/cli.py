from __future__ import annotations

import argparse
from typing import List

from . import __version__
from .storage import list_books, add_book, get_book, update_book, delete_book


def _print_book(b) -> None:
  print(f"#{b.id} | {b.title} — {b.author} | tags={','.join(b.tags)} | rating={b.rating} | {b.status}")


def main(argv: List[str] | None = None) -> None:
  parser = argparse.ArgumentParser(prog="booklib", description="Personal book library CLI")
  parser.add_argument("--version", action="version", version=f"booklib {__version__}")

  sub = parser.add_subparsers(dest="cmd")

  sub.add_parser("list", help="List all books")

  sub.add_parser("stats", help="Show simple stats")

  p_add = sub.add_parser("add", help="Add a new book")
  p_add.add_argument("title")
  p_add.add_argument("author")
  p_add.add_argument("--tags", default="")

  p_upd = sub.add_parser("update", help="Update a book")
  p_upd.add_argument("id", type=int)
  p_upd.add_argument("--title")
  p_upd.add_argument("--author")
  p_upd.add_argument("--tags")
  p_upd.add_argument("--rating", type=float)
  p_upd.add_argument("--status")

  p_del = sub.add_parser("delete", help="Delete a book")
  p_del.add_argument("id", type=int)

  args = parser.parse_args(argv)

  if args.cmd == "list":
    for b in list_books():
      _print_book(b)
    return

  if args.cmd == "add":
    tags = [t for t in args.tags.split(",") if t]
    b = add_book(args.title, args.author, tags)
    _print_book(b)
    return

  if args.cmd == "update":
    fields = {}
    if args.title is not None:
      fields["title"] = args.title
    if args.author is not None:
      fields["author"] = args.author
    if args.tags is not None:
      fields["tags"] = [t for t in args.tags.split(",") if t]
    if args.rating is not None:
      fields["rating"] = args.rating
    if args.status is not None:
      fields["status"] = args.status
    b = update_book(args.id, **fields)
    if b:
      _print_book(b)
    else:
      print("not found")
    return

  if args.cmd == "delete":
    ok = delete_book(args.id)
    print("ok" if ok else "not found")
    return

  if args.cmd == "stats":
    books = list_books()
    total = len(books)
    done = sum(1 for b in books if b.status == "done")
    reading = sum(1 for b in books if b.status == "reading")
    unread = sum(1 for b in books if b.status == "unread")
    avg = (
      sum(b.rating for b in books if isinstance(b.rating, (int, float))) / max(1, sum(1 for b in books if b.rating is not None))
    )
    print(f"total={total} done={done} reading={reading} unread={unread} avg_rating={avg:.2f}")
    return

  parser.print_help()


if __name__ == "__main__":
  main()
