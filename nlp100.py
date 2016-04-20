
# coding: utf-8

# # 言語処理100本ノック

# ## 00. 文字列の逆順

# In[ ]:

str = "stressed"
print str[::-1]


# ## 01. 「パタトクカシーー」

# In[ ]:

str = u"パタトクカシーー"
print str[::2]


# ## 02. 「パトカー」＋「タクシー」＝「パタトクカシーー」

# In[ ]:

str1 = u"パトカー"
str2 = u"タクシー"
result = "".join([a + b for a, b in zip(str1, str2)])
print result


# ## 03. 円周率

# In[ ]:

str = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
str = str.translate(None, ".,") # .と,の削除

list = [len(word) for word in str.split()]

print list


# ## 04. 元素記号

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
def ngram(input, n, type):
    if TYPE_WORD == type:
         input = input.split()
            
    last = len(input) - n + 1
    ngram_list = [input[i] + "-" + input[i+1] for i in range(0, last)] # ハイフンでつなげる
    return ngram_list
    
str = "I am an NLPer"
print ngram(str, 2, TYPE_WORD)
print ngram(str, 2, TYPE_CHAR)



# In[ ]:



