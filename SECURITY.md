# Security Policy

`entropyseed` is designed for offline use on Windows and Linux.

## Current security posture

- OS CSPRNG entropy from `secrets.token_bytes` is mandatory.
- Manual typing, dice rolls, and timer jitter are optional additive sources.
- Each source is SHA-512 hashed independently before HKDF-SHA512 mixing.
- The default behavior never writes mnemonic, entropy, seed, QR, audio, or video data to disk.
- Clipboard integration is intentionally disabled.
- Webcam, audio, and mouse collection are intentionally not part of the maintained implementation.

## Safe use

Run this project on a trusted offline machine. Verify the displayed mnemonic on paper or another durable offline medium. Do not photograph, paste, upload, print through networked services, or store the mnemonic in a password manager unless that is part of your own threat model.

## Reporting issues

Do not include generated mnemonics, entropy, or private wallet details in bug reports. Share only code paths, command lines, and non-secret diagnostics.
