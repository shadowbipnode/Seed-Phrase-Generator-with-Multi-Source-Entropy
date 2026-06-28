# entropyseed

Modern, offline BIP39 mnemonic generation with mandatory operating-system CSPRNG entropy and optional human-supplied entropy.

The original webcam/audio/mouse implementation has been preserved unchanged under `legacy/`.

## Features

- Generates valid BIP39 English mnemonics.
- Supports 128-bit entropy for 12 words and 256-bit entropy for 24 words.
- Always includes `secrets.token_bytes` OS CSPRNG entropy.
- Optionally adds manual typing, dice rolls, and timer jitter.
- Hashes every entropy source independently with SHA-512.
- Mixes source digests with HKDF-SHA512.
- Runs offline after dependencies are installed.
- Compatible with Windows and Linux.
- Does not use webcam, microphone, mouse tracking, clipboard, QR output, or media files.

## Install

Python 3.10 or newer is recommended.

```bash
python -m pip install -r requirements.txt
```

The generator itself uses only the Python standard library. `pytest` is listed for the test suite.

## Usage

Show help:

```bash
python seedgen.py --help
```

Generate a 12-word mnemonic with mandatory OS CSPRNG entropy:

```bash
python seedgen.py
```

Generate a 24-word mnemonic with manual typing, dice rolls, and confirmation:

```bash
python seedgen.py --strength 256 --manual --dice --confirm
```

Add timer jitter:

```bash
python seedgen.py --timer-jitter
```

When `--confirm` is used, the program selects 4 random word positions and asks you to re-enter those words.

## Security Behavior

By default and by design, this project never saves these to disk:

- QR codes
- audio
- video
- seed material
- entropy material
- mnemonic text

Clipboard support is disabled. Write the mnemonic down using your own offline backup process.

## Tests

```bash
python -m pytest -q
```

## Repository Layout

- `seedgen.py` - maintained CLI entry point.
- `entropyseed/` - maintained implementation.
- `tests/` - unit tests.
- `legacy/` - preserved original implementation and README.

## Notes

Dice entropy accepts digits `1` through `6`; spaces are ignored. Manual typing input is hidden when the terminal supports it. Optional sources supplement the mandatory OS CSPRNG; they are not required for secure generation on a healthy operating system.
