# OOAD

### Getting Started

#### MacOS
```shell
git clone https://github.com/steven20803/OOADLibraryManagement
cd OOADLibraryManagement
python3 -m venv env
source env/bin/activate
pip3 install poetry
poetry install --no-root
touch demo.sqlite
python3 main.py
```

#### Windows
```shell
git clone https://github.com/steven20803/OOADLibraryManagement
cd OOADLibraryManagement
python -m venv env
.\env\Scripts\activate
pip install poetry
poetry install --no-root
New-Item demo.sqlite -type file
python main.py
```

**$Execute$ sql.sql to init database and insert dummy data**

### Useful plugins for VsCode
- [SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite)
- [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)  

### Linting & Formatting
Using `pylint`, `black` and `isort` to lint and format the code.

```shell
# generate pylintrc to customize pylint
pylint --generate-rcfile > pylintrc
```
```shell
# enable execute permission
chmod +x ./lint_and_format.sh

# run linting and formatting
./lint_and_format.sh
```
---

> Default API Document: http://127.0.0.1:8000/docs

