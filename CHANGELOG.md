# Changelog

## 1.0.0

- Preserved the original webcam/audio/mouse implementation under `legacy/`.
- Added `entropyseed`, a simple offline BIP39 generator.
- Added mandatory OS CSPRNG entropy plus optional manual typing, dice rolls, and timer jitter.
- Added independent SHA-512 hashing per entropy source and HKDF-SHA512 mixing.
- Added 12-word and 24-word BIP39 mnemonic generation.
- Disabled QR, audio, video, seed, entropy, and clipboard output.
- Added confirmation by 4 random word positions.
- Added tests and project security documentation.
