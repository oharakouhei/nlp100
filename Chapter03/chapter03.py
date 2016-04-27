
# coding: utf-8

# # 第3章: 正規表現
# Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzがある．
# * 1行に1記事の情報がJSON形式で格納される
# * 各行には記事名が"title"キーに，記事本文が"text"キーの辞書オブジェクトに格納され，そのオブジェクトがJSON形式で書き出される
# * ファイル全体はgzipで圧縮される
# 以下の処理を行うプログラムを作成せよ．

# ## 20. JSONデータの読み込み
# Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．問題21-29では，ここで抽出した記事本文に対して実行せよ．

# In[ ]:

import gzip
import json

filepath = "source/jawiki-country.json.gz"

def get_article(title):
    with gzip.open(filepath, "r") as f:
        article_json = f.readline()
        while article_json:
            article_dict = json.loads(article_json.decode('utf-8'))
            if article_dict["title"] == title:
                return article_dict["text"]
            article_json = f.readline()
    return ""
            
            
print(get_article("イギリス"))


# ## 21. カテゴリ名を含む行を抽出
# 記事中でカテゴリ名を宣言している行を抽出せよ．

# In[ ]:

lines = get_article("イギリス").split("\n")

for line in lines:
    if "Category" in line:
        print(line)


# ## 22. カテゴリ名の抽出
# 記事のカテゴリ名を（行単位ではなく名前で）抽出せよ．

# In[ ]:

import re

lines = get_article("イギリス").split("\n")

for line in lines:
    category_line = re.search("^\[\[Category:(.*)(|\|.*)\]\]$", line)
    if category_line is not None:
        print(category_line.group(1))


# ## 23. セクション構造
# 記事中に含まれるセクション名とそのレベル（例えば"== セクション名 =="なら1）を表示せよ．

# In[ ]:

import re

lines = get_article("イギリス").split("\n")

for line in lines:
    # (.*?)でなく(.*)とすると、"セクション="が抽出されてしまう
    section_title_line = re.search("^(=+)(.*?)(=+)$", line)
    if section_title_line is not None:
        print(section_title_line.group(2), ": ", len(section_title_line.group(1)))


# ## 24. ファイル参照の抽出
# 記事から参照されているメディアファイルをすべて抜き出せ．

# In[ ]:

import re

lines = get_article("イギリス").split("\n")

for line in lines:
    file_line = re.search("(File|ファイル):(.*?)\|", line)
    if file_line is not None:
        print(file_line.group(2))


# ## 25. テンプレートの抽出
# 記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ．

# In[ ]:

import re

lines = re.split(r"\n[\|}]", get_article("イギリス"))
temp_dict = {}

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = temp_line.group(2)

# valueで並べ替えでprint
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)


# ## 26. 強調マークアップの除去
# 25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）を除去してテキストに変換せよ（参考: マークアップ早見表）

# In[ ]:

import re

temp_dict = {}
lines = re.split(r"\n[\|}]", get_article("イギリス"))

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        # 'が2~5個存在しているものを空文字に変換
        temp_dict[temp_line.group(1)] = re.sub(r"'{2,5}", r"", temp_line.group(2))

# Python3 参照
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)


# ## 27. 内部リンクの除去
# 26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，テキストに変換せよ（参考: [マークアップ早見表](https://ja.wikipedia.org/wiki/Help:%E6%97%A9%E8%A6%8B%E8%A1%A8)）．

# In[ ]:

import re

def remove_markup(str):
    str = re.sub(r"'{2,5}", r"", str)
    # 文字クラス[]の中では、^は補集合を表す。[^|\]]は、|と]を除く文字の集合を意味
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str)
    return str

temp_dict = {}
lines = re.split(r"\n[\|}]", get_article("イギリス"))

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        # 'が2~5個存在しているものを空文字に変換
        temp_dict[temp_line.group(1)] = remove_markup(temp_line.group(2))

# Python3 参照
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)


# ## 28. MediaWikiマークアップの除去
# 27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，国の基本情報を整形せよ．

# In[ ]:

import re

def remove_markup(str):
    str = re.sub(r"'{2,5}", r"", str) # 強調除去
    # 文字クラス[]の中では、^は補集合を表す。[^|\]]は、|と]を除く文字の集合を意味
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str) # 内部リンク除去
    str = re.sub(r"\{{2}.+?\|.+?\|(.+?)\}{2}", r"\1 ", str) # 国名
    str = re.sub(r"<.*?>", r"", str) # htmlタグ
    str = re.sub(r"\[.*?\]", r"", str) # 外部リンク
    return str

temp_dict = {}
lines = re.split(r"\n[\|}]", get_article("イギリス"))

for line in lines:
    temp_line = re.search("^(.*?)\s=\s(.*)", line, re.S)
    if temp_line is not None:
        # 'が2~5個存在しているものを空文字に変換
        temp_dict[temp_line.group(1)] = remove_markup(temp_line.group(2))

# Python3 参照
for k, v in sorted(temp_dict.items(), key=lambda x: x[1]):
    print(k, v)


# ## 29. 国旗画像のURLを取得する
# テンプレートの内容を利用し，国旗画像のURLを取得せよ．（ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）

# In[ ]:

import re
import requests

# 複雑な入れ子構造になっているjsonを、1層の（入れ子構造になっていない）dict型に変換
def json_search(json_data):
    ret_dict = {}
    for k, v in json_data.items():
        if isinstance(v, list):
            for e in v:
                ret_dict.update(json_search(e))
        elif isinstance(v, dict):
            ret_dict.update(json_search(v))
        else:
            ret_dict[k] = v
    return ret_dict


def remove_markup(str):
    str = re.sub(r"'{2,5}", r"", str)
    str = re.sub(r"\[{2}([^|\]]+?\|)*(.+?)\]{2}", r"\2", str)
    str = re.sub(r"\{{2}.+?\|.+?\|(.+?)\}{2}", r"\1 ", str)
    str = re.sub(r"<.*?>", r"", str)
    str = re.sub(r"\[.*?\]", r"", str)
    return str

temp_dict = {}
lines = get_article("イギリス").split("\n")

for line in lines:
    temp_line = re.search("^\|(.*?)\s=\s(.*)", line)
    if temp_line is not None:
        temp_dict[temp_line.group(1)] = remove_markup(temp_line.group(2))

url = "https://en.wikipedia.org/w/api.php"
payload = {"action": "query",
           "titles": "File:{}".format(temp_dict[u"国旗画像"]),
           "prop": "imageinfo",
           "format": "json",
           "iiprop": "url"}

json_data = requests.get(url, params=payload).json()
print(json_search(json_data)["url"])

