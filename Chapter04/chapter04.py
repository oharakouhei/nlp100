
# coding: utf-8

# # 第4章: 形態素解析
# 
# 夏目漱石の小説『吾輩は猫である』の文章（[neko.txt](http://www.cl.ecei.tohoku.ac.jp/nlp100/data/neko.txt)）をMeCabを使って形態素解析し，その結果をneko.txt.mecabというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．
# 
# 
# なお，問題37, 38, 39はmatplotlibもしくはGnuplotを用いるとよい．

# ### mecabファイルの作成
# ```
# $ mecab source/neko.txt >> source/neko.txt.mecab
# ```
# により、neko.txt.mecabを作成した。

# ## 30. 形態素解析結果の読み込み
# 形態素解析結果（neko.txt.mecab）を読み込むプログラムを実装せよ．ただし，各形態素は表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をキーとするマッピング型に格納し，1文を形態素（マッピング型）のリストとして表現せよ．第4章の残りの問題では，ここで作ったプログラムを活用せよ．

# In[ ]:

import pickle

class Main(object):
    
    def __init__(self):
        pass

    def solve(self):
        with open('source/neko.txt.mecab', 'r') as f:
            morphologies = [] # 形態素
            sentence = []
            for line in f.readlines():
                if line == 'EOS\n':
                    if len(sentence) > 0: # 文の中身が入っていれば
                        morphologies.append(sentence)
                        sentence = []
                else:
                    surface, result = line.split("\t") # surface（表層系）（実際に文中に現れた単語）とresult（その形態素解析結果）に分割
                    results = result.split(',')
                    sentence.append({'surface': surface, 'base': results[6], 'pos': results[0], 'pos1': results[1]})
         
        with open('source/neko.txt.mecab.pickle', 'wb') as w:
                    pickle.dump(morphologies, w) 
        return None

if __name__ == '__main__':
    m = Main()
    m.solve()


# ### pickleファイル
# 以下では、30. によって作成したpickleファイルを使用する

# ## 31. 動詞
# 動詞の表層形をすべて抽出せよ．

# In[ ]:

import pickle

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

for sentence in morphologies:
    for morphology in sentence:
        if '動詞' == morphology['pos']:
            print(morphology['surface'])


# ## 32. 動詞の原形
# 動詞の原形をすべて抽出せよ．

# In[ ]:

import pickle

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

for sentence in morphologies:
    for morphology in sentence:
        if '動詞' == morphology['pos']:
            print(morphology['base'])


# ## 33. サ変名詞
# サ変接続の名詞をすべて抽出せよ．

# In[ ]:

import pickle

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

for sentence in morphologies:
    for morphology in sentence:
        if '名詞' == morphology['pos'] and 'サ変接続' == morphology['pos1']:
            print(morphology)


# ## 34. 「AのB」
# 2つの名詞が「の」で連結されている名詞句を抽出せよ．

# In[ ]:

import pickle

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

for sentence in morphologies:
    temp_noun_phrases = ""
    for i, morphology in enumerate(sentence):
        if i < 2:
            continue
        if '名詞' == sentence[i-2]['pos']:
            if 'の' == sentence[i-1]['surface']:
                if '名詞' == morphology['pos']:
                    temp_noun_phrase = sentence[i-2]['surface'] + sentence[i-1]['surface'] + morphology['surface']
                    print(temp_noun_phrase)


# ## 35. 名詞の連接
# 名詞の連接（連続して出現する名詞）を最長一致で抽出せよ．

# In[ ]:

import pickle

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

for sentence in morphologies:
    nouns = []
    for i, morphology in enumerate(sentence):
        if '名詞' == morphology['pos']:
            nouns.append(morphology['surface'])
            continue
        else:
            if 2 <= len(nouns):
                print("".join(nouns))
            nouns = []


# ## 36. 単語の出現頻度
# 文章中に出現する単語とその出現頻度を求め，出現頻度の高い順に並べよ．

# In[ ]:

import pickle
from collections import defaultdict 

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

# term frequency
tf = defaultdict(int)
for sentence in morphologies:
    for morphology in sentence:
        tf[morphology["base"]] += 1

for k in sorted(tf, key=lambda x: tf[x], reverse=True):
    print(k, ",", tf[k])


# ## 37. 頻度上位10語
# 出現頻度が高い10語とその出現頻度をグラフ（例えば棒グラフなど）で表示せよ．

# In[ ]:

import pickle
from collections import Counter, defaultdict 
import numpy as np
import matplotlib.pyplot as plt
# jupyterで表示するのに必要
get_ipython().magic('matplotlib inline')

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

# term frequency
tf = [m['base'] for sentence in morphologies for m in sentence]
count = Counter(tf)
top10 = count.most_common(10)
ind = np.arange(10)
width = 0.35

plt.bar(ind, [f for w, f in top10], width) # plt.bar(横軸, 縦軸, 横幅)
plt.title('Top 10 of Term Frequency in Bocchan')
plt.xlabel('Terms')
plt.ylabel('Frequency')
plt.xticks(ind + width / 2, [w for w, f in top10]) # 軸ラベル
plt.show()


# ## 38. ヒストグラム
# 単語の出現頻度のヒストグラム（横軸に出現頻度，縦軸に出現頻度をとる単語の種類数を棒グラフで表したもの）を描け．

# In[ ]:

import pickle
from collections import Counter, defaultdict 
import numpy as np
import matplotlib.pyplot as plt
# jupyterで表示するのに必要
get_ipython().magic('matplotlib inline')

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

# term frequency
tf = [m['base'] for sentence in morphologies for m in sentence]
count = Counter(tf)

plt.hist([f for w, f in count.items()], bins=100, range=(0, 10000))
plt.title('Histogram of Term Frequency in Bocchan')
plt.xlabel('Term Frequency')
plt.ylabel('Freqency')
plt.show()


# ## 39. Zipfの法則
# 単語の出現頻度順位を横軸，その出現頻度を縦軸として，両対数グラフをプロットせよ．

# In[ ]:

import pickle
from collections import Counter, defaultdict 
import numpy as np
import matplotlib.pyplot as plt
# jupyterで表示するのに必要
get_ipython().magic('matplotlib inline')

with open('source/neko.txt.mecab.pickle', 'rb') as f:
    morphologies = pickle.load(f)

# term frequency
tf = [m['base'] for sentence in morphologies for m in sentence]
count = Counter(tf)

top = count.most_common()
rank = np.arange(len(top)) + 1
freq = [f for w, f in top]
plt.scatter(rank, freq, s=10)
plt.title('Relationship between Rank and Value of Term Frequency')
plt.xlabel('Rank (Logarithmic)')
plt.ylabel('Term Frequency (Logarithmic)')
plt.xscale('log')
plt.yscale('log')
plt.show()

