# Python `venv`

```sh
python -m venv .venv
. ./.venv/bin/activate
pip install requirements.txt
deactivate
python -m pip freeze > requirements.txt
```