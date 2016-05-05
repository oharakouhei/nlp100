
# coding: utf-8

# # 第5章: 係り受け解析
# 
# 夏目漱石の小説『吾輩は猫である』の文章（[neko.txt](http://www.cl.ecei.tohoku.ac.jp/nlp100/data/neko.txt)）をCaboChaを使って係り受け解析し，その結果をneko.txt.cabochaというファイルに保存せよ．このファイルを用いて，以下の問に対応するプログラムを実装せよ．

# ## 40. 係り受け解析結果の読み込み（形態素）
# 形態素を表すクラスMorphを実装せよ．このクラスは表層形（surface），基本形（base），品詞（pos），品詞細分類1（pos1）をメンバ変数に持つこととする．さらに，CaboChaの解析結果（neko.txt.cabocha）を読み込み，各文をMorphオブジェクトのリストとして表現し，3文目の形態素列を表示せよ．

# ### neko.txt.cabochaの作成
# 形態素も出すような形式にするためにオプション -f1 をつける
# ```
# $ cabocha -f1 neko.txt >> neko.txt.cabocha
# ```

# In[ ]:

class Morph(object):

    def __init__(self, surface=None, base=None, pos=None, pos1=None):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1

    def __str__(self):
        return '<surface: {0} base: {1}, pos: {2}, pos1: {3}>'.format(self.surface, self.base, self.pos, self.pos1)

    def __repr__(self):
        return self.__str__()


# In[ ]:

class Main(object):
    
    def __init__(self):
        pass

    def solve(self):
        with open('source/neko.txt.cabocha', 'r') as f:
            morphologies = []
            sentence = []
            for line in f.readlines():
                if line.strip() == 'EOS':
                    if len(sentence) > 0:
                        morphologies.append(sentence)
                        sentence = []
                elif not line.startswith('*'):
                    surface, result = line.split("\t")
                    results = result.split(',')
                    sentence.append(Morph(surface, results[6], results[0], results[1]))
            print(morphologies[2])
        
        return None

if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 41. 係り受け解析結果の読み込み（文節・係り受け）
# 40に加えて，文節を表すクラスChunkを実装せよ．このクラスは形態素（Morphオブジェクト）のリスト（morphs），係り先文節インデックス番号（dst），係り元文節インデックス番号のリスト（srcs）をメンバ変数に持つこととする．さらに，入力テキストのCaboChaの解析結果を読み込み，１文をChunkオブジェクトのリストとして表現し，8文目の文節の文字列と係り先を表示せよ．第5章の残りの問題では，ここで作ったプログラムを活用せよ．

# In[ ]:

class Chunk(object):
    def __init__(self, morphs=None, dst=None, srcs=None):
        if morphs is None: morphs = []
        if srcs is None: srcs = []
        self.morphs = morphs
        self.dst = dst
        self.srcs = srcs
        
    def get_text(self):
        return ''.join([m.surface for m in self.morphs if m.pos != '記号'])

    def append(self, morph):
        self.morphs.append(morph)
                
    def __str__(self):
        return '<text: {0}, srcs: {1}, dst: {2}>'.format(self.get_text(), str(self.srcs), self.dst)

    def __repr__(self):
        return self.__str__()


# In[ ]:

class ParseCabochaTextToChunks(object):
    
    def __init__(self):
        pass

    def parse(self, filename):
        with open(filename, 'r') as f:
            sentences = [] # sentenceの集合
            sentence = [] # 1文単位で各要素にchunkを保存するリスト
            chunk = None
            
            for line in f.readlines():
                if line.strip() == 'EOS':
                    self.set_srcs(sentence)
                    # self.reset_dst(sentence) # 不要だと考え一度コメントアウト
                    sentences.append(sentence)
                    sentence = []   
                else:
                    if line.startswith('*'):
                        chunk = self.parse_chunk_header(line)
                        sentence.append(chunk)
                    else:
                        morph = self.parse_morph(line)
                        chunk.append(morph)
                        
        return sentences

    # EOS時に実行する
    def set_srcs(self, sentence):
        for index, chunk in enumerate(sentence):
            # dstが存在していれば
            if chunk.dst != -1:
                sentence[chunk.dst].srcs.append(index)
     
#     # EOS時に実行する
#     # 1文の最後のchunkのdstを-1からNoneに設定する
#     def reset_dst(self, sentence):
#         if len(sentence) > 0:
#             sentence[-1].dst = None
    
    # 1文の最初に実行
    # * 2 4D 0/1 1.227694 等の行の、4Dから4を取り出しdstとして保存
    def parse_chunk_header(self, line):
        chunk = Chunk()
        chunk.dst = int(line.split()[2][:-1])
        return chunk

    # 形態素の行で実行
    # 形態素解析
    def parse_morph(self, line):
        surface, result = line.split("\t")
        results = result.split(',')
        morph = Morph(surface, results[6], results[0], results[1])
        return morph


# In[ ]:

import pickle

class Main(object):
    def __init__(self):
        pass
    
    def solve(self):
        pcttc = ParseCabochaTextToChunks()
        sentences = pcttc.parse('source/neko.txt.cabocha')
        with open('source/neko.txt.cabocha.pickle', 'wb') as w:
            pickle.dump(sentences, w) 
        print(text[7])

if __name__ == "__main__":
    m = Main()
    m.solve()


# ## 42. 係り元と係り先の文節の表示
# 係り元の文節と係り先の文節のテキストをタブ区切り形式ですべて抽出せよ．ただし，句読点などの記号は出力しないようにせよ．

# In[ ]:

import pickle

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)
        
        for sentence in sentences:
            for chunk in sentence:
                if -1 != chunk.dst:
                    print('{0}\t{1}'.format(chunk.get_text(), sentence[chunk.dst].get_text()))

if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 43. 名詞を含む文節が動詞を含む文節に係るものを抽出
# 名詞を含む文節が，動詞を含む文節に係るとき，これらをタブ区切り形式で抽出せよ．ただし，句読点などの記号は出力しないようにせよ．

# In[ ]:

import pickle

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)
        
        for sentence in sentences:
            for chunk in sentence:
                if -1 != chunk.dst:
                    if '名詞' in [m.pos for m in chunk.morphs] and '動詞' in [m.pos for m in sentence[chunk.dst].morphs]:
                        print('{0}\t{1}'.format(chunk.get_text(), sentence[chunk.dst].get_text()))

if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 44. 係り受け木の可視化
# 与えられた文の係り受け木を有向グラフとして可視化せよ．可視化には，係り受け木を[DOT言語](https://ja.wikipedia.org/wiki/DOT%E8%A8%80%E8%AA%9E)に変換し，[Graphviz](http://www.graphviz.org/)を用いるとよい．また，Pythonから有向グラフを直接的に可視化するには，[pydot](https://github.com/erocarrera/pydot)を使うとよい

# In[ ]:

import pickle
from pydot import pydot
# 以下画像表示用
from PIL import Image 
import matplotlib.pyplot as plt
import numpy as np
get_ipython().magic('matplotlib inline')

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)
        
        # 8行目だけ可視化
        sentence = sentences[7]
        edges = []
        for chunk in sentence:
            if -1 != chunk.dst:
                edges.append((chunk.get_text(), sentence[chunk.dst].get_text()))
       
        g = pydot.graph_from_edges(edges)
        g.write_jpeg('44.png', prog='dot')
        im = Image.open("44.png", "r")
        plt.imshow(np.array(im))
                
if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 45. 動詞の格パターンの抽出
# 今回用いている文章をコーパスと見なし，日本語の述語が取りうる格を調査したい． 動詞を述語，動詞に係っている文節の助詞を格と考え，述語と格をタブ区切り形式で出力せよ． ただし，出力は以下の仕様を満たすようにせよ．
# 
# * 動詞を含む文節において，最左の動詞の基本形を述語とする
# * 述語に係る助詞を格とする
# * 述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる
# 
# 「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える． この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
# 
# ```
# 始める  で
# 見る    は を
# ```
# 
# このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
# 
# コーパス中で頻出する述語と格パターンの組み合わせ
# 「する」「見る」「与える」という動詞の格パターン（コーパス中で出現頻度の高い順に並べよ）
# 

# In[ ]:

import pickle

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)
        
        verbs = dict()
        with open("45.txt", "w") as w:
            for sentence in sentences:
                for chunk in sentence:
                    has_verb = False
                    has_joshi = False
                    base = ""
                    # chunk内が述語があるか走査
                    for m in chunk.morphs:
                        if '動詞' == m.pos:
                            base = m.base
                            has_verb = True
                    # 述語があれば、述語に係る助詞（格）を取得
                    if has_verb:
                        joshis = []
                        for src in chunk.srcs:
                            for sm in sentence[src].morphs:
                                if '助詞' == sm.pos:
                                    joshis.append(sm.base)
                                    has_joshi = True # srcsのchunkのうち一つでも助詞を含んでいれば、Trueにして良い
                        if has_joshi:
                            w.write("{0}\t{1}\n".format(base, " ".join(joshis)))

    
if __name__ == '__main__':
    m = Main()
    m.solve()


# In[ ]:

# python内でcountもしてしまう場合
import pickle
from collections import defaultdict

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)
        
        verbs = dict()
        for sentence in sentences:
            for chunk in sentence:
                has_verb = False
                base = ""
                # chunk内が述語があるか走査
                for m in chunk.morphs:
                    if '動詞' == m.pos:
                        base = m.base
                        has_verb = True
                # 述語があれば、述語に係る助詞（格）を取得
                if has_verb:
                    for src in chunk.srcs:
                        for sm in sentence[src].morphs:
                            if '助詞' == sm.pos:
                                if base not in verbs:
                                    verbs[base] = defaultdict(int)
                                verbs[base][sm.base] += 1
                                

        for verb, joshi_dict in verbs.items():
            joshi_group = ""
            for joshi, count in joshi_dict.items():
                # countも出力
                joshi_group += joshi +"("+ str(count) + ") "
            print("{0}\t{1}".format(verb, joshi_group[0:-1]))
    
if __name__ == '__main__':
    m = Main()
    m.solve()


# 確認するUNIXコマンド
# ```
# $ sort 45.txt | grep "^する\|見る\|与える" | uniq -c | sort -r
# ```

# ## 46. 動詞の格フレーム情報の抽出
# 45のプログラムを改変し，述語と格パターンに続けて項（述語に係っている文節そのもの）をタブ区切り形式で出力せよ．45の仕様に加えて，以下の仕様を満たすようにせよ．
# 
# * 項は述語に係っている文節の単語列とする（末尾の助詞を取り除く必要はない）
# * 述語に係る文節が複数あるときは，助詞と同一の基準・順序でスペース区切りで並べる
# 
# 「吾輩はここで始めて人間というものを見た」という例文（neko.txt.cabochaの8文目）を考える． この文は「始める」と「見る」の２つの動詞を含み，「始める」に係る文節は「ここで」，「見る」に係る文節は「吾輩は」と「ものを」と解析された場合は，次のような出力になるはずである．
# 
# ```
# 始める  で      ここで
# 見る    は を   吾輩は ものを
# ```

# In[ ]:

import pickle

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)
        
        verbs = dict()
#         for sentence in sentences:
        sentence = sentences[7]
        for chunk in sentence:
            has_verb = False
            has_joshi = False
            base = ""
            # chunk内が述語があるか走査
            for m in chunk.morphs:
                if '動詞' == m.pos:
                    base = m.base
                    has_verb = True
            # 述語があれば、述語に係る助詞（格）を取得
            if has_verb:
                joshis = []
                joshi_chunks = []
                for src in chunk.srcs:
                    for sm in sentence[src].morphs:
                        if '助詞' == sm.pos:
                            joshis.append(sm.base)
                            joshi_chunks.append(sentence[src].get_text())
                            has_joshi = True # srcsのchunkのうち一つでも助詞を含んでいれば、Trueにして良い
                if has_joshi:
                    print("{0}\t{1}\t{2}".format(base, " ".join(joshis), " ".join(joshi_chunks)))

    
if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 47. 機能動詞構文のマイニング
# 動詞のヲ格にサ変接続名詞が入っている場合のみに着目したい．46のプログラムを以下の仕様を満たすように改変せよ．
# 
# * 「サ変接続名詞+を（助詞）」で構成される文節が動詞に係る場合のみを対象とする
# * 述語は「サ変接続名詞+を+動詞の基本形」とし，文節中に複数の動詞があるときは，最左の動詞を用いる
# * 述語に係る助詞（文節）が複数あるときは，すべての助詞をスペース区切りで辞書順に並べる
# * 述語に係る文節が複数ある場合は，すべての項をスペース区切りで並べる（助詞の並び順と揃えよ）
# 
# 例えば「別段くるにも及ばんさと、主人は手紙に返事をする。」という文から，以下の出力が得られるはずである．
# 
# ```
# 返事をする      と に は        及ばんさと 手紙に 主人は
# このプログラムの出力をファイルに保存し，以下の事項をUNIXコマンドを用いて確認せよ．
# ```
# 
# * コーパス中で頻出する述語（サ変接続名詞+を+動詞）
# * コーパス中で頻出する述語と助詞パターン

# In[ ]:

import pickle

class Main(object):
    
    def __init__(self):
        pass
    
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)
        
        verbs = dict()
#         for sentence in sentences:
        sentence = sentences[948]
        for chunk in sentence:
            has_verb = False
            has_joshi = False
            base = ""
            # chunk内に述語があるか走査
            for m in chunk.morphs:
                if '動詞' == m.pos:
                    base = m.base
                    has_verb = True
            # 述語があれば、述語に係る助詞（格）を取得
            if has_verb:
                joshis = []
                joshi_chunks = []
                for src in chunk.srcs:
                    if "サ変接続" in [m.pos1 for m in sentence[src].morphs] and "を" in [m.surface for m in sentence[src].morphs]:
                        base = sentence[src].get_text() + sentence[sentence[src].dst].get_text() # 述語の更新
                        continue
                    # 述語に係る助詞を抽出する
                    for sm in sentence[src].morphs:
                        if '助詞' == sm.pos:
                            joshis.append(sm.base)
                            joshi_chunks.append(sentence[src].get_text())
                            has_joshi = True # srcsのchunkのうち一つでも助詞を含んでいれば、Trueにして良い
                if has_joshi:
                    print("{0}\t{1}\t{2}".format(base, " ".join(joshis), " ".join(joshi_chunks)))
                    #=> 返事をする	さ と は に	及ばんさと 及ばんさと 主人は 手紙に
                    # 終助詞の「さ」も入っているのはおかしい（？） 「述語に係る助詞」は何助詞があるのか

    
if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 48. 名詞から根へのパスの抽出
# 文中のすべての名詞を含む文節に対し，その文節から構文木の根に至るパスを抽出せよ． ただし，構文木上のパスは以下の仕様を満たすものとする．
# 
# * 各文節は（表層形の）形態素列で表現する
# * パスの開始文節から終了文節に至るまで，各文節の表現を"->"で連結する
# 
# 「吾輩はここで始めて人間というものを見た」という文（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
# 
# ```
# 吾輩は -> 見た
# ここで -> 始めて -> 人間という -> ものを -> 見た
# 人間という -> ものを -> 見た
# ものを -> 見た
# ```

# In[ ]:

# 再帰関数を使うver
import pickle

SENTENCE_INDEX = 7

class Main(object):
    def __init__(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            self.sentences = pickle.load(f)
    
    # 再帰
    def get_paths(self, sentence_index, chunk_index, paths = None):
        if paths is None: paths = []
        chunk = self.sentences[sentence_index][chunk_index]
        paths.append(chunk.get_text())
        if -1 != chunk.dst:
            paths = self.get_paths(sentence_index, chunk.dst, paths)
        return paths
        
    def solve(self):        
        for chunk_index, chunk in enumerate(self.sentences[SENTENCE_INDEX]):
            for m in chunk.morphs:
                if '名詞' == m.pos:
                    paths = self.get_paths(SENTENCE_INDEX, chunk_index)
                    print(" -> ".join(paths))

if __name__ == '__main__':
    m = Main()
    m.solve()


# In[ ]:

# 再帰関数を使わないver
import pickle

class Main(object):
    def __init__(self):
        pass
        
    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)

        sentence = sentences[7]
        for index, chunk in enumerate(sentence):
            if '名詞' in [m.pos for m in chunk.morphs]:
                paths = []
                node = index
                while True:
                    paths.append(sentence[node].get_text())
                    node = sentence[node].dst
                    if -1 == node:
                        break
                print(" -> ".join(paths))

if __name__ == '__main__':
    m = Main()
    m.solve()


# ## 49. 名詞間の係り受けパスの抽出
# 文中のすべての名詞句のペアを結ぶ最短係り受けパスを抽出せよ．ただし，名詞句ペアの文節番号がiとj（i<j）のとき，係り受けパスは以下の仕様を満たすものとする．
# 
# * 問題48と同様に，パスは開始文節から終了文節に至るまでの各文節の表現（表層形の形態素列）を"->"で連結して表現する
# * 文節iとjに含まれる名詞句はそれぞれ，XとYに置換する
# 
# また，係り受けパスの形状は，以下の2通りが考えられる．
# 
# * 文節iから構文木の根に至る経路上に文節jが存在する場合: 文節iから文節jのパスを表示
# * 上記以外で，文節iと文節jから構文木の根に至る経路上で共通の文節kで交わる場合: 文節iから文節kに至る直前のパスと文節jから文節kに至る直前までのパス，文節kの内容を"|"で連結して表示．簡易に示すと，ik間のパス|jk間のパス|k
# 
# 例えば，「吾輩はここで始めて人間というものを見た。」という文（neko.txt.cabochaの8文目）から，次のような出力が得られるはずである．
# 
# ```
# Xは | Yで -> 始めて -> 人間という -> ものを | 見た            # 「吾輩は」と「ここで」のペア
# Xは | Yという -> ものを | 見た                                   # 「吾輩は」と「人間という」のペア
# Xは | Yを | 見た                                                  # 「吾輩は」と「ものを」のペア
# Xで -> 始めて -> Yを                                             # 「ここで」と「人間という」のペア
# Xで -> 始めて -> 人間という -> Yを                              # 「ここで」と「ものを」のペア
# Xという -> Yを                                                   # 「人間という」と「ものを」のペア
# ```
# この8文目には名詞句が4つ存在するので，それらの組み合わせは、4C2 = 6通りある．出力が6種になるのはこのためである．

# In[ ]:

import pickle

SENTENCE_INDEX = 7

class Main(object):
    
    def __init__(self):
        pass

    def solve(self):
        with open('source/neko.txt.cabocha.pickle', 'rb') as f:
            sentences = pickle.load(f)

        sentence = sentences[SENTENCE_INDEX]
        
        for i in range(len(sentence)-1):
            if '名詞' in [m.pos for m in sentence[i].morphs]:
                for j in range(i+1, len(sentence)):
                    if '名詞' in [m.pos for m in sentence[j].morphs]:
                        # Get indices of morphs to be replaced by 'X' or 'Y'
                        # XまたはYと置き換える形態素indexを取得
                        index_x = []
                        index_x_flag = False
                        for index, m in enumerate(sentence[i].morphs):
                            if m.pos == '名詞':
                                index_x_flag = True
                                index_x.append(index)
                            else:
                                if index_x_flag:
                                    break
                        index_y = []
                        index_y_flag = False
                        for index, m in enumerate(sentence[j].morphs):
                            if m.pos == '名詞':
                                index_y_flag = True
                                index_y.append(index)
                            else:
                                if index_y_flag:
                                    break

                        # Get paths of syntax tree
                        # それぞれの名詞から根へのパスを取得
                        path_i = []
                        path_j = []

                        node = i
                        while True:
                            path_i.append(node)
                            node = sentence[node].dst
                            if -1 == node:
                                break
                        node = j
                        while True:
                            path_j.append(node)
                            node = sentence[node].dst
                            if -1 == node:
                                break

                        # Display syntax tree
                        if set(path_i) >= set(path_j):
                            path_texts = self.get_replaced_texts(sentence, sorted(list(set(path_i) - set(path_j)) + [j]), i, j, index_x, index_y)
                            print(' -> '.join(path_texts))
                        else:
                            path_i_only_texts = self.get_replaced_texts(sentence, sorted(list(set(path_i) - set(path_j))), i, j, index_x, index_y)
                            path_j_only_texts = self.get_replaced_texts(sentence, sorted(list(set(path_j) - set(path_i))), i, j, index_x, index_y)
                            path_common_texts = self.get_replaced_texts(sentence, sorted(list(set(path_i) & set(path_j))), i, j, index_x, index_y)                            
                            print('{0} | {1} | {2}'.format(' -> '.join(path_i_only_texts), ' -> '.join(path_j_only_texts), ' -> '.join(path_common_texts)))

        return None

    def get_replaced_texts(self, sentence, path, i, j, replaced_morphs_i, replaced_morphs_j):
        texts = []
        for index in path:
            chunk_text = ''
            if index == i:
                for index_i, m in enumerate(sentence[index].morphs):
                    if index_i == replaced_morphs_i[0]:
                        chunk_text += 'X'
                    elif index_i in replaced_morphs_i:
                        # 名詞の連接の場合（例：「二三ページを」）は、「Xページを」などとせず、「Xを」とする
                        pass
                    else:
                        chunk_text += m.surface
            elif index == j:
                for index_j, m in enumerate(sentence[index].morphs):
                    if index_j == replaced_morphs_j[0]:
                        chunk_text += 'Y'
                    elif index_j in replaced_morphs_j:
                        pass
                    else:
                        chunk_text += m.surface
            else:
                chunk_text += sentence[index].get_text()
            texts.append(chunk_text)
        return texts
    
if __name__ == '__main__':
    m = Main()
    m.solve()

