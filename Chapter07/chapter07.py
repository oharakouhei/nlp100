
# coding: utf-8

# # 第7章: データベース
# 
# artist.json.gzは，オープンな音楽データベースMusicBrainzの中で，アーティストに関するものをJSON形式に変換し，gzip形式で圧縮したファイルである．このファイルには，1アーティストに関する情報が1行にJSON形式で格納されている．jsonの形式は[100本ノックのページを参照](http://www.cl.ecei.tohoku.ac.jp/nlp100/#ch7)．
# 
# artist.json.gzのデータをKey-Value-Store (KVS) およびドキュメント志向型データベースに格納・検索することを考える．KVSとしては，LevelDB，Redis，KyotoCabinet等を用いよ．ドキュメント志向型データベースとして，MongoDBを採用したが，CouchDBやRethinkDB等を用いてもよい．

# ## 60. KVSの構築
# Key-Value-Store (KVS) を用い，アーティスト名（name）から活動場所（area）を検索するためのデータベースを構築せよ．

# In[ ]:

import redis
import gzip
import json
import codecs

def generate_database():
    with gzip.open('source/artist.json.gz', 'rb') as f:
        line = f.readline()
        r = redis.StrictRedis()
        while line:
            data = json.loads(line.decode('utf-8'))
            line = f.readline()
            if 'area' in data:
                r.set(data['name'], data['area'])
            else:
                r.set(data['name'], 'No Information')

# import json


if __name__ == '__main__':
    generate_database()


# ## 61. KVSの検索
# 60で構築したデータベースを用い，特定の（指定された）アーティストの活動場所を取得せよ．

# In[ ]:

# pythonで書く場合
import redis

if __name__ == '__main__':
    r = redis.StrictRedis()
    print(r.get("Einkaufen Einkaufen"))


# コマンドラインで叩く場合
# ```
# $ redis-cli
# 127.0.0.1:6379> keys *                                # redisに登録されているkeyの一覧
#      1) "Einkaufen Einkaufen"
#      2) "Micah Templeton-Wolfe"
#      3) "Richard Calkin"
#      4) "Z\xc3\xa9 Neguinho do C\xc3\xb4co"
#      5) "\xed\x8c\x90\xeb\x8b\xa4\xed\x92\x80"
#      6) "Hermanastra"
#      7) "Nocturnal Sea"
#      8) "Juiceppe"
#      9) "Ms. Corona"
#     10) "The SALOVERS"
# ...
#     864784) "Archyp"
#     864785) "Rivo Drei"
#     864786) "No Talent"
#     864787) "Teka Tema"
#     864788) "Mike Marlin"
#     864789) "\xe4\xba\x95\xe4\xb8\x8a\xe4\xbf\x8a\xe5\xbd\xa6"
# 
# 127.0.0.1:6379> get "Einkaufen Einkaufen"
# "No Information"
# 127.0.0.1:6379> get "Hermanastra"
# "Spain"
# ```

# ## 62. KVS内の反復処理
# 60で構築したデータベースを用い，活動場所が「Japan」となっているアーティスト数を求めよ．

# In[ ]:

import redis

if __name__ == '__main__':
    r = redis.StrictRedis()
    nof_ja = 0
    for key in r.scan_iter():
        if 'Japan' == r.get(key).decode('utf-8'):
            nof_ja += 1
    print(nof_ja)


# ## 63. オブジェクトを値に格納したKVS
# KVSを用い，アーティスト名（name）からタグと被タグ数（タグ付けされた回数）のリストを検索するためのデータベースを構築せよ．さらに，ここで構築したデータベースを用い，アーティスト名からタグと被タグ数を検索せよ．

# In[ ]:

import redis
import gzip
import json

def generate_database():
    with gzip.open('source/artist.json.gz', 'rb') as f:
        line = f.readline()
        i = 0
        r = redis.StrictRedis()
        while line:
            i += 1
            data = json.loads(line.decode('utf-8'))
            line = f.readline()
            if 'tags' in data:
                for hash_tags in data['tags']:
                    r.hset(data['name'], hash_tags['value'], hash_tags['count'])
                
if __name__ == '__main__':
    generate_database()


# In[ ]:

import redis

# artist全体に関する操作を行うクラス
class Artists(object):
    def __init__(self):
        r = redis.StrictRedis()
    
    # 
    # 一覧表示するメソッド
    # @param start 何件目から取得するか
    # @param n 何件取得するか
    #
    def list(self, start, n):
        if start < 0:
            print('0以上の整数で入力してください')
            return
        if n < 0:
            print('0以上の整数で入力してください')
            return
        i = 0
        for key in r.scan_iter():
            i += 1
            if i < start:
                continue
            else:
                print(key.decode('utf-8'))
                if start <= (i - n + 1):
                    break

    
    def find_by_name(self, name):
        if r.exists(name):
            self.tags = dict()
            for field in r.hkeys(name):
                self.tags[field] = int(r.hget(name, field))
            print('データが見つかりました')
            return self.tags
        else:
            print('データがありません')
            return
        
    # タグ付けされた総回数を返すメソッド
    def total_taged_count(self):
        total = 0
        for field in self.tags:
            total += self.tags[field]
        return total

if __name__ == '__main__':
    artists = Artists()
    artists.list(100, 10)
    artists.find_by_name('黒住憲五')
    print(artists.total_taged_count())


# ## 64. MongoDBの構築
# アーティスト情報（artist.json.gz）をデータベースに登録せよ．さらに，次のフィールドでインデックスを作成せよ: name, aliases.name, tags.value, rating.value

# In[ ]:

import gzip
import pymongo

if __name__ == '__main__':
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.nlp100_chapter07
    artists = db.artists
    with gzip.open('source/artist.json.gz', 'rb') as f:
        line = f.readline()
        while line:
            data = json.loads(line.decode('utf-8'))
            artists.insert_one(data)
            line = f.readline()


# ### インデックス
# ```
# > db.artists.createIndex({name: 1})
# {
# 	"createdCollectionAutomatically" : false,
# 	"numIndexesBefore" : 3,
# 	"numIndexesAfter" : 3,
# 	"note" : "all indexes already exist",
# 	"ok" : 1
# }
# > db.artists.createIndex({'aliases.name': 1})
# {
# 	"createdCollectionAutomatically" : false,
# 	"numIndexesBefore" : 2,
# 	"numIndexesAfter" : 3,
# 	"ok" : 1
# }
# > db.artists.createIndex({'tags.value': 1})
# {
# 	"createdCollectionAutomatically" : false,
# 	"numIndexesBefore" : 3,
# 	"numIndexesAfter" : 4,
# 	"ok" : 1
# }
# > db.artists.createIndex({'rating.value': 1})
# {
# 	"createdCollectionAutomatically" : false,
# 	"numIndexesBefore" : 4,
# 	"numIndexesAfter" : 5,
# 	"ok" : 1
# }
# ```
# インデックスは、以下で確認できる
# ```
# > db.artists.getIndexes()
# ```

# ## 65. MongoDBの検索
# MongoDBのインタラクティブシェルを用いて，"Queen"というアーティストに関する情報を取得せよ．さらに，これと同様の処理を行うプログラムを実装せよ．

# ### mongodb
# ```
# > db.artists.findOne({name: 'Queen'})
# ```

# In[ ]:

import pymongo

# pythonでは
if __name__ == '__main__':
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.nlp100_chapter07
    artists = db.artists
    print(artists.find_one({'name': 'Queen'}))


# ## 66. 検索件数の取得
# MongoDBのインタラクティブシェルを用いて，活動場所が「Japan」となっているアーティスト数を求めよ．

# ```
# > db.artists.find({area: 'Japan'}).count()
# 22821
# ```

# ## 67. 複数のドキュメントの取得
# 特定の（指定した）別名を持つアーティストを検索せよ．

# ```
# > db.artists.findOne({'aliases.name': 'Queen'})
# ```

# ## 68. ソート
# "dance"というタグを付与されたアーティストの中でレーティングの投票数が多いアーティスト・トップ10を求めよ．

# * find({}, {}): 第一引数：検索条件, 第二引数：表示するfieldの設定（デフォルト1。表示させたくないフィールドを0にする）
# * sort({}): sortするfield。1昇順。-1降順
# * limit()： 取得してくる件数
# ```
# > db.artists.find({'tags.value': 'dance'}, {'_id': 0, 'id': 0, 'sort_name': 0, 'gid': 0, 'tags': 0, 'begin': 0, 'ended': 0, 'aliases': 0}).sort({'rating.value': -1}).limit(100)
# ```

# ## 69. Webアプリケーションの作成
# ユーザから入力された検索条件に合致するアーティストの情報を表示するWebアプリケーションを作成せよ．アーティスト名，アーティストの別名，タグ等で検索条件を指定し，アーティスト情報のリストをレーティングの高い順などで整列して表示せよ．

# railsなどで作成すれば良い。
