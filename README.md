# emojify-cli

Convert text into Discord emoji codes.

## Installation (local)

```bash
pip install -e .
```

## Usage

```
emojify "hello world"
emojify -c "hi!"
```

Output

```
:regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_l: :regional_indicator_o:   :regional_indicator_w: :regional_indicator_o: :regional_indicator_r: :regional_indicator_l: :regional_indicator_d:
:regional_indicator_h::regional_indicator_i::exclamation:
```

(note: spaces in the input are preserved)

## Features

- Letter → regional indicator emojis
- Number and symbol support
- User-defined macros via config file
  - code `000` is reserved for the `#` character itself

For a full list of options and a brief explanation, use the command below:

```bash
emojify --help
```

### Note for Termux users

On Termux, prefer using `virtualenv` instead of `python -m venv`
for proper isolation:

```bash
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
```

