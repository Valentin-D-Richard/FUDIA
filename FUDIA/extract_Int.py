import sys, os, json
from grewpy import Request, Corpus, Graph, set_config
set_config("sud")
corpora_path= "/Users/perrier/recherche/Autogramm/methode-Guy/corpora/"
corpus_name= sys.argv[1]
corpus_path = corpora_path + corpus_name
corpus= Corpus(corpus_path)
selected_sent=corpus.search(Request("G[upos=NOUN]; D[upos=CCONJ]; G -[DESC]-> L1 ; G >> L1;  D -[RIGHT]-> D; D < L1").without("G -[cc]-> D"))
selected_corpus= open('results.conll', mode='w', encoding='utf-8')
list_id_sent =[]
for s in selected_sent:
    id=s['sent_id']
    g= corpus.get(id)
    #print(g)
    c= g.to_conll()
    selected_corpus.write(c+'\n')
#print(list_id_sent)
selected_corpus.close()
print(len(selected_sent))

