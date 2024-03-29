import classes as cl

##### cl_head_pull: Finding the head of the current clause.
# When can we say that the current node is not the root of 
# the interrogative clause?
# In particular: when is the WH word is in situ?


### Root: Relations to potentially pull along

chp_0_0 = cl.Snippet("chp_0_0")
chp_0_0.request = '''pattern { a: CAND -> CUR ; CUR[IntClause="Yes"] ;
\tw: CUR -[cue:wh]-> WH }
without { CAND -[cue:wh]-> WH } % no loop
without { CUR[Quoted="Yes"] }'''
chp_0_0.command = '''del_feat CUR.IntClause ; CAND.IntClause = "Yes" ;
\tdel_edge w ; add_edge CAND -[cue:wh]-> WH ;'''
# It handles the case where CAND already has an edge -[cue:wh]-> CUR

cl_head_pull = cl.DisjRule("cl_head_pull", root = chp_0_0)

### Clause relations: csubj, ccomp, xcomp, advcl, acl
chp_1_0 = cl.Snippet("chp_1_0") 
chp_1_0.request = '''pattern { CAND -[csubj|ccomp|xcomp|advcl|acl]-> CUR }'''

# CUR is participial or infinitival + preposition (except passé composé)
chp_2_0 = cl.Snippet("chp_2_0")
chp_2_0.request = '''pattern { CUR[VerbForm="Part"|"Inf"] ;
\tCUR -> P ; P[upos="ADP",!ExtPos] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }
without { a.label = acl ; P[lemma="à"|"de"|"sur"] } % (*)'''
# e.g. Il a réussi en faisant quoi ? advcl(réussi,faisant)
# (*) interrogatives subordinated to an NP
#   e.g. "nos questions sur comment s'installer"

# CUR is participial or infinitival + prepositional locution (except passé composé)
chp_2_1 = cl.Snippet("chp_2_1")
chp_2_1.request = '''pattern { CUR[VerbForm="Part"|"Inf"] ;
\tCUR -> P ; P[ExtPos="ADP"] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''
# e.g. Il a réussi en faisant quoi ? advcl(réussi,faisant)

# CUR's copula or auxiliary is participial or infinitival
# + preposition (except passé composé)
chp_2_2 = cl.Snippet("chp_2_2")
chp_2_2.request = '''pattern { CUR -[1=aux|cop]-> V ;
\tV[VerbForm="Part"|"Inf"] ; CUR -> P ; P[upos="ADP",!ExtPos] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''

# CUR's copula or auxiliary is participial or infinitival
# + prepositional locution (except passé composé)
chp_2_3 = cl.Snippet("chp_2_3")
chp_2_3.request = '''pattern { CUR -[1=aux|cop]-> V ;
\tV[VerbForm="Part"|"Inf"] ; CUR -> P ; P[ExtPos="ADP"] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''

# Additionnal marker
chp_2_4 = cl.Snippet("chp_2_4")
chp_2_4.request = '''pattern { CUR -[mark]-> Q ;
\tQ[upos="SCONJ",!ExtPos] ; CAND << Q ; Q << CUR }'''
# e.g. Il sait que/si tu fais quoi ? ccomp(sait,fait)

# Additionnal marker locution
chp_2_5 = cl.Snippet("chp_2_5")
chp_2_5.request = '''pattern { CUR -[mark]-> Q ;
\tQ[ExtPos="SCONJ"] ; CAND << Q ; Q << CUR }'''
# e.g. Il sait que/si tu fais quoi ? ccomp(sait,fait)

# Additionnal marker locution
chp_2_6 = cl.Snippet("chp_2_6")
chp_2_6.request = '''pattern { CUR -[mark]-> Q ;
\tQ[ExtPos="SCONJ"] ; CAND << Q ; Q << CUR }'''
# e.g. Il sait que/si tu fais quoi ? ccomp(sait,fait)

# In situ or fronted WH word with xcomp infinitive complement
chp_2_7 = cl.Snippet("chp_2_7")
chp_2_7.request = '''pattern { CAND << CUR ; a.label = xcomp ;
\tCUR[VerbForm="Inf"] }
without { CUR -[cue:wh]-> WH2 }
without { CAND << WH ; WH << CUR }'''
# e.g. Il sait faire quoi ? xcomp(sait,faire)
# e.g. Elle est prête à les rejoindre où ? xcomp(prête, rejoindre)
# e.g. Il sait qui fait quoi. : no pull

# In situ or fronted WH word with xcomp complement and infinitival copula
chp_2_8 = cl.Snippet("chp_2_8")
chp_2_8.request = '''pattern { CAND << CUR ; a.label = xcomp ;
\tCUR -[1=aux|cop]-> V ; V[VerbForm="Inf"] }
without { CUR -[cue:wh]-> WH2 }
without { CAND << WH ; WH << CUR }'''


### Nominal relations: nsubj, obj, (iobj,) obl, nmod, (det), advmod
chp_1_1 = cl.Snippet("chp_1_1_5") 
chp_1_1.request = '''pattern { CAND -[nsubj|obj|obl|nmod|det|advmod]-> CUR }
without { CAND[lemma="savoir"] ; CAND -[obj|obl]-> CUR }'''
# Exceptionnaly taken vocabulary into account
# cf ph_edge_b_2_3

# Globally, these relations are rare, and only occur with in-situ WH words,
# especially when the WH phrase cannot be extracted
# e.g. T'as acheté un jeans avec combien de trous ? obj(acheté,jean)

##### Adding edges

cl_head_pull.add_snippets([chp_1_0, chp_1_1], chp_0_0)

layer = [chp_2_0, chp_2_1, chp_2_2, chp_2_3, chp_2_4,
         chp_2_5, chp_2_6, chp_2_7, chp_2_8]
cl_head_pull.add_snippets(layer, chp_1_0)

