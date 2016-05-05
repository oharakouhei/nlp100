
# coding: utf-8

# # 第6章: 英語テキストの処理
# 英語のテキスト（[nlp.txt](http://www.cl.ecei.tohoku.ac.jp/nlp100/data/nlp.txt)）に対して，以下の処理を実行せよ．

# ## 50. 文区切り
# (. or ; or : or ? or !) → 空白文字 → 英大文字というパターンを文の区切りと見なし，入力された文書を1行1文の形式で出力せよ．

# In[ ]:

import re
import pickle

class Main(object):
    def __init__(self):
        pass
    
    # [.;:?!]\s+で区切れば済む話だが、題意に忠実に
    def generate_sentences(self):
        with open("source/nlp.txt", "r") as f:
            text = f.read()

        # re.split('[.;:?!]\s+([A-Z])', text)では、大文字まで区切ってしまうので、
        # 後から大文字はmergeする
        sentences = []
        uppercase_letter = ''
        for sentence in re.split('[.;:?!]\s+([A-Z])', text):
            if re.match('^[A-Z]$', sentence):
                uppercase_letter = sentence
            else:
                sentences.append(uppercase_letter + sentence)
                uppercase_letter = ''
                
        return sentences
    
    def solve(self):
        sentences = []
        sentences = self.generate_sentences()
        with open("source/nlp.txt.pickle", "wb") as w:
            pickle.dump(sentences, w)
            
        for sentence in sentences:
            print(sentence)
            
if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 51. 単語の切り出し
# 空白を単語の区切りとみなし，50の出力を入力として受け取り，1行1単語の形式で出力せよ．ただし，文の終端では空行を出力せよ．

# In[ ]:

import pickle

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open("source/nlp.txt.pickle", "rb") as f:
            sentences = pickle.load(f)
        
        for sentence in sentences:
            words = sentence.split()
            for word in words:
                print(word)
            print("\n")
        
if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 52. ステミング
# 51の出力を入力として受け取り，Porterのステミングアルゴリズムを適用し，単語と語幹をタブ区切り形式で出力せよ． Pythonでは，Porterのステミングアルゴリズムの実装として[stemming](https://pypi.python.org/pypi/stemming)モジュールを利用するとよい．

# In[ ]:

import pickle
from stemming.porter2 import stem

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open("source/nlp.txt.pickle", "rb") as f:
            sentences = pickle.load(f)
        
        for sentence in sentences:
            words = sentence.split()
            for word in words:
                print(stem(word))
            print("\n")
        
if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 53. Tokenization
# [Stanford Core NLP](http://stanfordnlp.github.io/CoreNLP/)を用い，入力テキストの解析結果をXML形式で得よ．また，このXMLファイルを読み込み，入力テキストを1行1単語の形式で出力せよ．

# ## 54. 品詞タグ付け
# Stanford Core NLPの解析結果XMLを読み込み，単語，レンマ，品詞をタブ区切り形式で出力せよ．

# ## 55. 固有表現抽出
# 入力文中の人名をすべて抜き出せ．

# ## 56. 共参照解析
# Stanford Core NLPの共参照解析の結果に基づき，文中の参照表現（mention）を代表参照表現（representative mention）に置換せよ．ただし，置換するときは，「代表参照表現（参照表現）」のように，元の参照表現が分かるように配慮せよ．

# ## 57. 係り受け解析
# Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）を有向グラフとして可視化せよ．可視化には，係り受け木をDOT言語に変換し，Graphvizを用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，pydotを使うとよい．

# ## 58. タプルの抽出
# Stanford Core NLPの係り受け解析の結果（collapsed-dependencies）に基づき，「主語 述語 目的語」の組をタブ区切り形式で出力せよ．ただし，主語，述語，目的語の定義は以下を参考にせよ．
# 
# * 述語: nsubj関係とdobj関係の子（dependant）を持つ単語
# * 主語: 述語からnsubj関係にある子（dependent）
# * 目的語: 述語からdobj関係にある子（dependent）

# ## 59. S式の解析
# Stanford Core NLPの句構造解析の結果（S式）を読み込み，文中のすべての名詞句（NP）を表示せよ．入れ子になっている名詞句もすべて表示すること．
