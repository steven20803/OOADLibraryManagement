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

> Default API Document: http://127.0.0.1:8000/docs
