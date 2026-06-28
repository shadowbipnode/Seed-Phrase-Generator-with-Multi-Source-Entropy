# Release Checklist

Use this checklist for the v2.2.0 release.

## Pre-release checks

- Confirm `entropyseed.__version__` and `pyproject.toml` use the same version.
- Review `README.md`, `SECURITY.md`, and `CHANGELOG.md` for current behavior.
- Confirm no generated mnemonic, seed, entropy, QR, audio, video, or other sensitive material is committed.
- Run the Windows and Linux test commands below from a clean checkout.
- Confirm GitHub Actions passes on Windows and Ubuntu for supported Python versions.

## Windows test commands

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python seedgen.py --self-test
python seedgen.py --help
python -m pip install .
entropyseed --self-test
```

## Linux test commands

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 seedgen.py --self-test
python3 seedgen.py --help
python3 -m pip install .
entropyseed --self-test
```

## Tag creation

```bash
git status
git tag -a v2.2.0 -m "Release v2.2.0"
git push origin v2.2.0
```

## GitHub release notes template

```markdown
## entropyseed v2.2.0

### Changes

- Added GitHub Actions tests for Windows and Ubuntu.
- Added Python packaging metadata and the `entropyseed` console script.
- Added release checklist documentation.
- Updated README installation, usage, test, and release notes.

### Verification

- `python -m pytest -q`
- `python seedgen.py --self-test`
- `python seedgen.py --help`

### Notes

Run on a trusted offline machine. Passing tests do not prove a computer is safe.
Do not include generated seed material, mnemonics, entropy, QR codes, audio, video, screenshots, or wallet-private details in issues or screenshots.
```
