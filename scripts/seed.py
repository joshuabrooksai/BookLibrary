from __future__ import annotations

import json
from pathlib import Path

from booklib.storage import _save


def main():
  here = Path(__file__).parent
  data = json.loads((here / "sample-data.json").read_text())
  _save(data)
  print("seeded", len(data.get("items", [])), "books")


if __name__ == "__main__":
  main()

