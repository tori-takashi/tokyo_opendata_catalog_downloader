# 東京都オープンデータカタログダウンローダ

CSVのURLの配列を渡したら、CSVをダウンロードします。
結合させるかをオプションで切り替えることができます。

# 使い方

## target.csvにダウンロードしたいCKANページをはる

https://catalog.data.metro.tokyo.lg.jp/dataset/t131113d0000000022

など。

## ダウンローダ実行

$ python downloader.py

downloaded_merged.csvが出てくる

説明は適当なので必要があればissueまで