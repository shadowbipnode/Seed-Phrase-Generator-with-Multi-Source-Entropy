# entropyseed

[![Tests](https://github.com/shadowbipnode/Seed-Phrase-Generator-with-Multi-Source-Entropy/actions/workflows/tests.yml/badge.svg)](https://github.com/shadowbipnode/Seed-Phrase-Generator-with-Multi-Source-Entropy/actions/workflows/tests.yml)

Offline BIP39 English mnemonic generation with mandatory operating-system CSPRNG entropy and optional local supplemental entropy.

Run this only on a trusted offline machine. Review the code, install dependencies before going offline, and keep generated mnemonics away from cameras, printers, cloud sync, clipboard tools, and networked services.

The original webcam/audio/mouse implementation is preserved unchanged under `legacy/`. The maintained generator does not use webcam, microphone, mouse tracking, network access, telemetry, clipboard, QR output, audio output, or video output.

## Release Status

Current project version: 2.2.0.

The maintained CLI is tested on Windows and Linux with Python 3.11, 3.12, and 3.13 through GitHub Actions.

## Installation From Source

Python 3.11 or newer is recommended.

Install the CLI from a local checkout:

```bash
python -m pip install -r requirements.txt
python -m pip install .
entropyseed --self-test
```

The installed command is:

```bash
entropyseed
```

## Running From The Repository

You can also run the repository entry point directly:

```bash
python -m pip install -r requirements.txt
python seedgen.py --self-test
python seedgen.py
```

The generator itself uses only the Python standard library. `pytest` is listed for the test suite.

## Examples

Show help:

```bash
python seedgen.py --help
```

Generate a 12-word mnemonic:

```bash
python seedgen.py
```

Generate a 24-word mnemonic:

```bash
python seedgen.py --strength 256
```

Add hidden manual typing entropy:

```bash
python seedgen.py --manual
```

Add dice-roll entropy:

```bash
python seedgen.py --dice
```

Add timer jitter:

```bash
python seedgen.py --timer-jitter
```

Generate 24 words with manual, dice, timer jitter, and confirmation:

```bash
python seedgen.py --strength 256 --manual --dice --timer-jitter --confirm
```

Run internal checks without generating or printing a mnemonic:

```bash
python seedgen.py --self-test
```

After installing from source, replace `python seedgen.py` with `entropyseed` in the examples above.

## Safe Usage

- Disconnect networking before generation.
- Use a trusted, clean operating system and terminal.
- Run `python seedgen.py --self-test` before generating a mnemonic.
- Write the mnemonic by hand on durable offline media.
- Verify the written words before funding any wallet.
- Store backups according to your own risk model.

When `--confirm` is used, the program selects 4 random word positions and asks you to re-enter those words.

## Entropy Sources

OS CSPRNG entropy from `secrets.token_bytes` is always included and cannot be disabled. Manual typing, dice rolls, and timer jitter are supplemental only.

Dice input accepts digits `1` through `6`; spaces are ignored. For 12-word generation, at least 50 dice rolls are required. For 24-word generation, at least 99 dice rolls are required.

Timer jitter displays a short collection message and progress dots. It is collected in memory and should complete quickly.

## Security Notes

By default and by design, this project never saves these to disk:

- QR codes
- audio
- video
- seed material
- entropy material
- mnemonic text

Clipboard support is disabled. Write the mnemonic down using your own offline backup process.

Passing tests and self-tests only check expected software behavior. They do not prove the operating system, terminal, firmware, hardware, or physical environment is safe.

Do not include generated seed material, mnemonics, entropy, QR codes, audio, video, screenshots, or wallet-private details in bug reports or public issues.

## Tests

```bash
python -m pytest -q
python seedgen.py --help
python seedgen.py --self-test
```

## Repository Layout

- `seedgen.py` - maintained CLI entry point.
- `entropyseed/` - maintained implementation.
- `tests/` - unit tests.
- `legacy/` - preserved original implementation and README.
