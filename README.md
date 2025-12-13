# emojify-cli

Convert text into Discord emoji codes.

## Install (local)

```bash
pip install -e .
```

## Usage

```
mojify "hello world"
emojify -c "hi!"
```

### Note for Termux users

On Termux, prefer using `virtualenv` instead of `python -m venv`
for proper isolation:

```bash
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
```

