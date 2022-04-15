# Line Bot Sample

Line developerを利用したLine内Botのソースコード

## 環境構築

python3動作環境で以下のコマンドを使用して、必要なパッケージを一括インストールします。

```
$ pip install -r requirements.txt
```

仮想環境を利用する場合（venv環境構築）

```sh
> python -m venv (environment_name)
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process # for windows
> .\(environment_name)\Scripts\Activate.ps1
(environment_name)> pip install --upgrade pip # need admin (skip)
(environment_name)> pip install -r requirements.txt
(environment_name)> python3 ***.py # run program
(environment_name)> deactivate
```
## ファイル詳細

receive.py : メインプログラム

 * Lineメッセージを受け取るプログラム
   常時起動させることでメッセージを受け取り、各処理を行う

data/ : データディレクトリ

 * conf.json
   TOKENやIDの設定を保存するファイル

 package/ : パッケージディレクトリ

 * 自作した関数などを機能ごとにファイル分けして使用

 * testcode.py
   テスト用のコード

## 参考

1. [PythonでGoogle Sheetsを編集する方法](https://www.twilio.com/blog/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python-jp)



   