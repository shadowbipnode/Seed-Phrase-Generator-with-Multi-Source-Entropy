# Changelog

## 2.2.0

- Added GitHub Actions tests for Windows and Ubuntu across Python 3.11, 3.12, and 3.13.
- Added Python packaging metadata and the `entropyseed` console script.
- Added release checklist documentation.
- Updated README installation, usage, self-test, security, and release status sections.

## 2.1.0

- Added BIP39 English test vectors and mnemonic checksum validation.
- Added tests for 128-bit and 256-bit generated mnemonic validation.
- Tightened HKDF-SHA512 and entropy-source input validation.
- Added additional HKDF-SHA512 vectors and deterministic-output tests.
- Required dice input to contain only digits `1` through `6`.
- Required at least 50 dice rolls for 12-word generation and 99 for 24-word generation.
- Clarified that dice, manual typing, and timer jitter supplement mandatory OS CSPRNG entropy.
- Made timer-jitter collection announce itself and show short progress.
- Added `python seedgen.py --self-test` for internal checks without mnemonic generation.
- Updated README and SECURITY with quick start, safe usage, examples, self-test usage, and a realistic threat model.

## 1.0.0

- Preserved the original webcam/audio/mouse implementation under `legacy/`.
- Added `entropyseed`, a simple offline BIP39 generator.
- Added mandatory OS CSPRNG entropy plus optional manual typing, dice rolls, and timer jitter.
- Added independent SHA-512 hashing per entropy source and HKDF-SHA512 mixing.
- Added 12-word and 24-word BIP39 mnemonic generation.
- Disabled QR, audio, video, seed, entropy, and clipboard output.
- Added confirmation by 4 random word positions.
- Added tests and project security documentation.
