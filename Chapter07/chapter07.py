
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
import types

def generate_database():
    with gzip.open('source/artist.json.gz', 'rb') as f:
        line = f.readline()
        i = 0
        r = redis.StrictRedis()
        while line:
            i += 1
            data = json.loads(line.decode('utf-8'))
            line = f.readline()
            if 'area' in data:
                r.set(data['name'], data['area'])
            else:
                r.set(data['name'], 'No Information')
            if 10 == i:
                break

# import json


if __name__ == '__main__':
    generate_database()

    r = redis.StrictRedis()
    print(r.config_get('databases'))
    print(r.info('keyspace'))
    print(r.keys())
    print(r.flushall())

