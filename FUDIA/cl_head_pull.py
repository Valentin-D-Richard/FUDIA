import classes as cl

##### cl_head_pull: Finding the head of the current clause.
# When can we say that the current node is not the root of 
# the interrogative clause?
# In particular: when is the WH word is in situ?


### Root: Relations to potentially pull along

chp_0_0 = cl.Snippet("chp_0_0")
chp_0_0.pattern = '''pattern { a: CAND -> CUR ; CUR[IntClause="Yes"] ;
\tw: CUR -[cue:wh]-> WH }
without { CAND -[cue:wh]-> WH } % no loop
without { CUR[Quoted="Yes"] }'''
chp_0_0.command = '''del_feat CUR.IntClause ; CAND.IntClause = "Yes" ;
\tdel_edge w ; add_edge CAND -[cue:wh]-> WH ;'''
# It handles the case where CAND already has an edge -[cue:wh]-> CUR

cl_head_pull = cl.DisjPat("cl_head_pull", root = chp_0_0)

### Clause relations: csubj, ccomp, xcomp, advcl, acl
chp_1_0 = cl.Snippet("chp_1_0") 
chp_1_0.pattern = '''pattern { CAND -[csubj|ccomp|xcomp|advcl|acl]-> CUR }'''

# CUR is participial or infinitival + preposition (except passé composé)
chp_2_0 = cl.Snippet("chp_2_0")
chp_2_0.pattern = '''pattern { CUR[VerbForm="Part"|"Inf"] ;
\tCUR -> P ; P[upos="ADP"] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''
# e.g. Il a réussi en faisant quoi ? advcl(réussi,faisant)

# CUR is participial or infinitival + prepositional locution (except passé composé)
chp_2_1 = cl.Snippet("chp_2_1")
chp_2_1.pattern = '''pattern { CUR[VerbForm="Part"|"Inf"] ;
\tCUR -> P ; P[ExtPos="ADP"] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''
# e.g. Il a réussi en faisant quoi ? advcl(réussi,faisant)

# CUR's copula or auxiliary is participial or infinitival
# + preposition (except passé composé)
chp_2_2 = cl.Snippet("chp_2_2")
chp_2_2.pattern = '''pattern { CUR -[1=aux|cop]-> V ;
\tV[VerbForm="Part"|"Inf"] ; CUR -> P ; P[upos="ADP"] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''

# CUR's copula or auxiliary is participial or infinitival
# + prepositional locution (except passé composé)
chp_2_3 = cl.Snippet("chp_2_3")
chp_2_3.pattern = '''pattern { CUR -[1=aux|cop]-> V ;
\tV[VerbForm="Part"|"Inf"] ; CUR -> P ; P[ExtPos="ADP"] }
without { CUR -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''

# Additionnal marker
chp_2_4 = cl.Snippet("chp_2_4")
chp_2_4.pattern = '''pattern { CUR -[mark]-> Q ;
\tQ[upos="SCONJ"] ; CAND << Q ; Q << CUR }'''
# e.g. Il sait que/si tu fais quoi ? ccomp(sait,fait)

# Additionnal marker locution
chp_2_5 = cl.Snippet("chp_2_5")
chp_2_5.pattern = '''pattern { CUR -[mark]-> Q ;
\tQ[ExtPos="SCONJ"] ; CAND << Q ; Q << CUR }'''
# e.g. Il sait que/si tu fais quoi ? ccomp(sait,fait)

# In situ or fronted WH word with xcomp complement
chp_2_6 = cl.Snippet("chp_2_6")
chp_2_6.pattern = '''pattern { CAND << CUR ; a.label = xcomp ;
\tCUR[VerbForm="Inf"] }
without { CUR -[cue:wh]-> WH2 }
without { CAND << WH ; WH << CUR }'''
# e.g. Il sait faire quoi ? xcomp(sait,faire)
# e.g. Elle est prête à les rejoindre où ? xcomp(prête, rejoindre)
# e.g. Il sait qui fait quoi. : no pull

# Idiomatic "pour quoi faire"
# -> falls under chp_2_1 now
# chp_2_4_0 = cl.Snippet("chp_2_4_0")
# chp_2_4_0.pattern = '''pattern { CUR[form="faire"] ; WH[form="quoi"] ;
# \tWH < CUR ; P < WH ; P[form="pour"] }'''

# Fronted WH word dependent on a xcomp'ed verbal infinitive complement
# -> falls under chp_2_3 now
# chp_2_5_0 = cl.Snippet("chp_2_5_0")
# chp_2_5_0.pattern = '''pattern { WH << CAND ; CAND << CUR ;
# \tCAND -[xcomp]-> CUR ; CUR[VerbForm="Inf"] }'''
# e.g. Que veut-elle faire ?



### Nominal relations: nsubj, obj, (iobj,) obl, nmod, (det)
chp_1_1 = cl.Snippet("chp_1_1_5") 
chp_1_1.pattern = '''pattern { CAND -[nsubj|obj|obl|nmod|det]-> CUR }
without { CAND[lemma="savoir"] ; CAND -[obj|obl]-> CUR }'''
# Exceptionnaly taken vocabulary into account
# cf ph_edge_b_2_3

# Globally, these relations are rare, and only occur with in-situ WH words,
# especially when the WH phrase cannot be extracted
# e.g. T'as acheté un jeans avec combien de trous ? obj(acheté,jean)

##### Adding edges

cl_head_pull.add_snippets([chp_1_0, chp_1_1], chp_0_0)

layer = [chp_2_0, chp_2_1, chp_2_2, chp_2_3, chp_2_4, chp_2_5, chp_2_6]
cl_head_pull.add_snippets(layer, chp_1_0)

