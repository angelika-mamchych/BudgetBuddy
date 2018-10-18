# BudgetBuddy
Program that allows you to calculate taxes and fees

## Prerequisites
- Python 3
- [SQLite](https://www.sqlite.org/download.html)
- pip3​

## 3 steps to launch the BudgetBuddy
### Dowloads
### SQLite
after created a folder sqlite and extract in it download file, in terminal: 
```shell
sudo apt install sqlite3
```
next steps
```shell
git clone https://github.com/angelika-mamchych/BudgetBuddy
cd BudgetBuddy
```

### Build
pip install for Ubuntu 18.04
```shell
sudo apt update
sudo apt install python3-pip
```
next steps
```shell
python3 -m pip install --user -r requirements.txt
python3 init_db.py
```

### Run
```shell
python3 app.py
```
