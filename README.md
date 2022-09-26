# MO412 - Graph Algorithms

## Links

- [personal blog](https://p-mo412a-2022s2-lucasguesserts.blogspot.com/)
- [professor's blog](https://net-sci-questions.blogspot.com/)
- [website of the discipline](https://www.ic.unicamp.br/~meidanis/courses/mo412/2022s2/)
- [book network science by Albert-László Barabási](http://networksciencebook.com/)

## venv

```sh
python -m venv venv
. .venv/bin/activate
pip install -r requirements.txt
pip freeze > requirements.txt
deactivate
```

## Build reports with latex

### Requirements

```sh
# Fedora
sudo dnf install -y texlive-scheme-full
sudo dnf install -y latexmk
```

### Compile

In the directory where all files are located (usually the `report` dir), execute:

```sh
latexmk
```

## Author

Lucas Guesser Targino da Silva
