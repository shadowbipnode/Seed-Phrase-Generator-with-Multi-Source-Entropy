# Security Policy

`entropyseed` is designed for offline use on Windows and Linux.

## Threat Model

This project is intended to reduce mistakes while generating a BIP39 English mnemonic on a trusted offline machine. It does not make an untrusted computer safe.

In scope:

- Correct BIP39 checksum handling for generated and test-vector mnemonics.
- Mandatory operating-system CSPRNG entropy.
- Optional local supplemental entropy from manual typing, dice rolls, and timer jitter.
- In-memory entropy mixing with SHA-512 source hashing and HKDF-SHA512.
- Avoiding project-created files containing mnemonics, entropy, seed material, QR codes, audio, or video.
- Avoiding clipboard use, telemetry, and network functionality.

Out of scope:

- Malware, keyloggers, terminal capture, screen capture, compromised firmware, or a hostile operating system.
- Weak backups, photographed mnemonics, cloud sync, printers, password managers, or other user-chosen storage.
- Supply-chain compromise before the code reaches the offline machine.
- Physical observation, coercion, theft, or device tampering.
- Wallet software bugs or incorrect wallet derivation paths after the mnemonic is generated.

## Current Security Posture

- OS CSPRNG entropy from `secrets.token_bytes` is mandatory.
- Manual typing, dice rolls, and timer jitter are optional additive sources.
- Each source is SHA-512 hashed independently before HKDF-SHA512 mixing.
- The default behavior never writes mnemonic, entropy, seed, QR, audio, or video data to disk.
- Clipboard integration is intentionally disabled.
- Webcam, audio, and mouse collection are intentionally not part of the maintained implementation.

## Safe Use

Run this project on a trusted offline machine. Verify the displayed mnemonic on paper or another durable offline medium. Do not photograph, paste, upload, print through networked services, or store the mnemonic in a password manager unless that is part of your own threat model.

Before generating a mnemonic, run:

```bash
python seedgen.py --self-test
```

The self-test checks the wordlist shape, known BIP39 vectors, HKDF vectors, and basic entropy mixing. Passing self-tests do not prove the machine is safe.

## Reporting issues

Do not include generated mnemonics, entropy, or private wallet details in bug reports. Share only code paths, command lines, and non-secret diagnostics.
