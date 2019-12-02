__author__ = 'luohua139'
import hashlib
import sys
import gensim
from gensim.models import Word2Vec,Doc2Vec,word2vec
from gensim import models
from gensim import corpora

texte = [["我","爱","北京","天安门","首都","北京"],["天安门","上","红旗","飘飘"],["大雪","在","飘飘"]]

def test():
    dic = corpora.Dictionary(texte)
    print(dic.token2id)
    cp = [dic.doc2bow(tx) for tx in texte]
    print(cp)
    tfidf = models.TfidfModel(cp)
    doc_bow = [(0,1),(1,1)]
    print(tfidf[doc_bow])
    word = Word2Vec(texte,min_count=1)

if __name__ == '__main__':
    test()

