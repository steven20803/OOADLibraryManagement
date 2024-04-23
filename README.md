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

### Local Dev
如果還沒有建立 .sqlite 資料庫，請執行以下操作  
1. 在 root 建立 demo.sqlite檔案
2. 對demo.sqlite執行sql.sql檔案中的指令，可以透過vscode sqlite插件指令執行
3. launch the server: 執行 python main.py 或是 python3 main.py
4. swagger 文件在 http://127.0.0.1:8000/docs, 可以透過try it out 來試著呼叫API查看功能
