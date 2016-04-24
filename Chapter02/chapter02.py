
# coding: utf-8

# # 第2章: UNIXコマンドの基礎
# hightemp.txtは，日本の最高気温の記録を「都道府県」「地点」「℃」「日」のタブ区切り形式で格納したファイルである．以下の処理を行うプログラムを作成し，hightemp.txtを入力ファイルとして実行せよ．さらに，同様の処理をUNIXコマンドでも実行し，プログラムの実行結果を確認せよ．

# ## 10. 行数のカウント
# 行数をカウントせよ．確認にはwcコマンドを用いよ．

# In[ ]:

import sys

filepath = "source/hightemp.txt"

# ターミナルから $ python filename と実行する場合は　　f = open(argv[1])
f = open(filepath)
lines = f.readlines()
print(len(lines))

f.close()


# ## 11. タブをスペースに置換
# タブ1文字につきスペース1文字に置換せよ．確認にはsedコマンド，trコマンド，もしくはexpandコマンドを用いよ．

# In[ ]:

import sys
filepath = "source/hightemp.txt"

with open(filepath) as f:
    str = f.read()

print str.replace("\t", " "),


# ## 12. 1列目をcol1.txtに，2列目をcol2.txtに保存
# 各行の1列目だけを抜き出したものをcol1.txtに，2列目だけを抜き出したものをcol2.txtとしてファイルに保存せよ．確認にはcutコマンドを用いよ．

# In[ ]:

import sys
filepath = "source/hightemp.txt"

def write_col(source_lines, colunm_number, filename):
    col = []
    for line in source_lines:
        col.append(line.split()[colunm_number] + "\n")
    with open(filename, "w") as writer:
        writer.writelines(col)


with open(filepath) as f:
    lines = f.readlines()

# 実際に保存されると面倒なのでコメントアウト
#write_col(lines, 0, "col1.txt")
#write_col(lines, 1, "col2.txt")


# ## 13. col1.txtとcol2.txtをマージ
# 12で作ったcol1.txtとcol2.txtを結合し，元のファイルの1列目と2列目をタブ区切りで並べたテキストファイルを作成せよ．確認にはpasteコマンドを用いよ．

# In[ ]:

# こういう書き方ができるのは強い
with open("col1.txt") as f1, open("col2.txt") as f2:
    lines1, lines2 = f1.readlines(), f2.readlines()

with open("merge.txt", "w") as writer:
    for col1, col2 in zip(lines1, lines2):
        # writer.write("\t".join([col1.rstrip(), col2])) # 見た目を良くするため、col1だけ末尾の改行を除去


# ## 14. 先頭からN行を出力
# 自然数Nをコマンドライン引数などの手段で受け取り，入力のうち先頭のN行だけを表示せよ．確認にはheadコマンドを用いよ．

# In[ ]:

import sys
filepath = "source/hightemp.txt"
#N = int(sys.argv[2])
N = 3

with open(filepath) as f:
    lines = f.readlines()

for line in lines[:N]:
    print line,


# ## 15. 末尾のN行を出力
# 自然数Nをコマンドライン引数などの手段で受け取り，入力のうち末尾のN行だけを表示せよ．確認にはtailコマンドを用いよ．

# In[ ]:

import sys
filepath = "source/hightemp.txt"
#N = int(sys.argv[2])
N = 3

with open(filepath) as f:
    lines = f.readlines()

line_len = len(lines)
for line in lines[line_len-N:]:
    print line,


# ## 16. ファイルをN分割する
# 自然数Nをコマンドライン引数などの手段で受け取り，入力のファイルを行単位でN分割せよ．同様の処理をsplitコマンドで実現せよ．

# In[ ]:

import sys
filepath = "source/hightemp.txt"
N = 4 # 分割する数

def split_file(filepath, n):
    with open(filepath) as f:
        lines = f.readlines() # 大規模なファイルでないと仮定
        

    # 行数がn分割できなければエラーを出す
    if 0 != len(lines) % n:
        raise Exception("Undevided by n = %d", n)
    else:
        nof_lines = len(lines) / n

    for i in range(n):
        print "%d: " % i
        print "".join(lines[i*nof_lines:(i+1)*nof_lines])
        # with open(targetfile.txt, " w") as w:
        #    w.writelines(lines[i*nof_lines:(i+1)*nof_lines])
        
#  プログラムを直接呼び出した時、__name__は'__main__'となる
if  __name__ == '__main__':
    try:
        split_file(filepath, N)
    except Exception as err:
        print("Error:", err)


# ## 17. １列目の文字列の異なり
# 1列目の文字列の種類（異なる文字列の集合）を求めよ．確認にはsort, uniqコマンドを用いよ．

# In[ ]:

import sys
filepath = "source/hightemp.txt"
prefectures = set()

with open(filepath) as f:
    line = f.readline()
    while line:
        prefectures.add(line.split()[0])
        line = f.readline()

for pref in prefectures:
    print(pref)


# ## 18. 各行を3コラム目の数値の降順にソート
# 各行を3コラム目の数値の逆順で整列せよ（注意: 各行の内容は変更せずに並び替えよ）．確認にはsortコマンドを用いよ（この問題はコマンドで実行した時の結果と合わなくてもよい）．

# In[ ]:

import sys
filepath = "source/hightemp.txt"

with open(filepath) as f:
    lines = f.readlines()

# sorted, keyオプションでソートする基準
for line in sorted(lines, key=lambda x: x.split()[2], reverse=True):
    print line,


# ## 19. 各行の1コラム目の文字列の出現頻度を求め，出現頻度の高い順に並べる
# 各行の1列目の文字列の出現頻度を求め，その高い順に並べて表示せよ．確認にはcut, uniq, sortコマンドを用いよ．

# In[ ]:

import sys
from collections import defaultdict
filepath = "source/hightemp.txt"
# dict の初期値を defaultdict で設定できる。dict[key] += 1 などが書ける
prefectures = defaultdict(int)

with open(filepath) as f:
    line = f.readline()
    while line:
        prefectures[line.split()[0]] += 1
        line = f.readline()

for k, v in sorted(prefectures.items(), key=lambda x: x[1], reverse=True):
    print "%s: %d回" % (k, v)

