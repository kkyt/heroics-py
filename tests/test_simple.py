#coding: utf8

import os
from heroics import create_heroics_client

def test_simple():
    api = create_heroics_client('kuankr_nlp')
    r = api.pinyin.text('我爱北京天安门', multi=1)
    assert r=={"pinyin":[["wo3"],["ai4"],["bei3","bei4"],["jing1"],["tian1"],["an1"],["men2"]]}

    r = api.pinyin.text('我爱北京天安门')
    assert r=={'pinyin':['wo3','ai4','bei3','jing1','tian1','an1','men2']}

    n = 0
    a = []
    for x in api.pinyin.list.stream():
        n += 1
        if n>3:
            break
        assert len(x)==2
        a.append(x)


if __name__ == '__main__':
    test_simple()
