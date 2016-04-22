
# coding: utf-8

# # 言語処理100本ノック

# ## 00. 文字列の逆順
# 文字列"stressed"の文字を逆に（末尾から先頭に向かって）並べた文字列を得よ．

# In[ ]:

str = "stressed"
print str[::-1]


# ## 01. 「パタトクカシーー」
# 「パタトクカシーー」という文字列の1,3,5,7文字目を取り出して連結した文字列を得よ．

# In[ ]:

str = u"パタトクカシーー"
print str[::2]


# ## 02. 「パトカー」＋「タクシー」＝「パタトクカシーー」
# 「パトカー」＋「タクシー」の文字を先頭から交互に連結して文字列「パタトクカシーー」を得よ．

# In[ ]:

str1 = u"パトカー"
str2 = u"タクシー"
result = "".join([a + b for a, b in zip(str1, str2)])
print result


# ## 03. 円周率
# "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."という文を単語に分解し，各単語の（アルファベットの）文字数を先頭から出現順に並べたリストを作成せよ．

# In[ ]:

str = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
str = str.translate(None, ".,") # .と,の削除

list = [len(word) for word in str.split()]

print list


# ## 04. 元素記号
# "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."という文を単語に分解し，1, 5, 6, 7, 8, 9, 15, 16, 19番目の単語は先頭の1文字，それ以外の単語は先頭に2文字を取り出し，取り出した文字列から単語の位置（先頭から何番目の単語か）への連想配列（辞書型もしくはマップ型）を作成せよ．

# In[ ]:

str = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
str= str.translate(None, ".,") # .と,の削除
words_list = str.split()

achar_list = [1, 5, 6, 7, 8, 9, 15, 16, 19] # 何番目の単語を先頭一文字だけ取得するかのリスト

dict = {}

for i, word in enumerate(words_list):
    index = i + 1 # 何番目の単語か
    clen = 1 if index in achar_list else 2 # 先頭から何文字切り出すか
    dict[index] = word[:clen]
    
print dict


# ## 05. n-gram
# 与えられたシーケンス（文字列やリストなど）からn-gramを作る関数を作成せよ．この関数を用い，"I am an NLPer"という文から単語bi-gram，文字bi-gramを得よ．

# In[ ]:

# 単語n-gramなのか文字n-gramなのか用
(
    TYPE_WORD,
    TYPE_CHAR
) = range(0, 2)

#
# ngramを切り出す関数
# @param input 入力文(ピリオドやコンマを含まない)
# @param n n-gram
# @param type 単語n-gramなのか文字n-gramなのか
# @return ngram_list n-gramのリスト
#
def ngram(input, n, type=TYPE_CHAR):
    if TYPE_WORD == type:
         input = input.split()
            
    last = len(input) - n + 1
    ngram_list = [input[i] + "-" + input[i+1] for i in range(0, last)] # ハイフンでつなげる
    return ngram_list
    
str = "I am an NLPer"
print ngram(str, 2, TYPE_WORD)
print ngram(str, 2, TYPE_CHAR)


# ## 06. 集合
# "paraparaparadise"と"paragraph"に含まれる文字bi-gramの集合を，それぞれ, XとYとして求め，XとYの和集合，積集合，差集合を求めよ．さらに，'se'というbi-gramがXおよびYに含まれるかどうかを調べよ．

# In[ ]:

str_x = "paraparaparadise"
str_y = "paragraph"
X = set(ngram(str_x, 2)) # ngramのlistをsetに
Y = set(ngram(str_y, 2))

print X.union(Y)                 # 和集合
print X.intersection(Y)     # 積集合
print X.difference(Y)        # 差集合

print "se" in X     # in: X に "se" が含まれていれば True, いなければ False
print "se" in Y     # ほとんど同上（X -> Y）


# ## 07. テンプレートによる文生成
# 引数x, y, zを受け取り「x時のyはz」という文字列を返す関数を実装せよ．さらに，x=12, y="気温", z=22.4として，実行結果を確認せよ．

# In[ ]:

x = 12
y = u'気温'
z = 22.4

def function(x, y, z):
    return unicode(x) + u'時の' + unicode(y) + u'は' + unicode(z)

print function(x, y, z)


# ## 08. 暗号文
# 与えられた文字列の各文字を，以下の仕様で変換する関数cipherを実装せよ．
# 
# * 英小文字ならば(219 - 文字コード)の文字に置換
# * その他の文字はそのまま出力
# 
# この関数を用い，英語のメッセージを暗号化・復号化せよ．

# In[ ]:

## いわゆるatbash暗号
# 出典: Wikipedia 英語版 "Atbash" より
str = "Atbash is a simple substitution cipher for the Hebrew alphabet."

# 同一関数で暗号化と復号化をできる
# chr() はASCIIコードから具体的な文字に変換してくれる関数（chr(97) -> 'a'）．
# ord() はその逆だけど，Unicode であれば Unicode コードポイントを返してくれる．
# chr() の Unicode 版が unichr()
def cipher(input):
    ret = ""
    for char in input:
        ret += chr(219-ord(char)) if char.islower() else char
    return ret

str = cipher(str)
print str
str = cipher(str)
print str


# ## 09. Typoglycemia
# スペースで区切られた単語列に対して，各単語の先頭と末尾の文字は残し，それ以外の文字の順序をランダムに並び替えるプログラムを作成せよ．ただし，長さが４以下の単語は並び替えないこととする．適当な英語の文（例えば"I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."）を与え，その実行結果を確認せよ．

# In[ ]:

import random

str = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
words = str.split()
shuffled_list = []

for word in words:
    if len(word) <= 4:
        pass
    else:
        char_list = list(word)    # 文字列をリストにできる！
        mid_list = char_list[1:-1]
        random.shuffle(mid_list)
        word = word[0] + "".join(mid_list) + word[-1]
    shuffled_list.append(word)

shuffled_str = " ".join(shuffled_list)
print shuffled_str

