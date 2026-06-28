"""Compatibility wrapper for the offline entropy generator.

The original hardware-recording implementation is preserved in ``legacy/``.
Use ``python seedgen.py`` for the maintained CLI.
"""

from entropyseed.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
