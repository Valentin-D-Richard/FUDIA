import classes as cl

# Identifying and adding annotation to the WH word,
# the WH phrase head PH_HEAD and the clause head CL_HEAD

##### wh_edge: Finding wh_path with PH_HEAD != WH

# Root :
wh_edge_0_0 = cl.Snippet("wh_edge_0_0")
wh_edge_0_0.request = '''pattern { WH [PronType="Int"] ; e : PH_HEAD -> WH }
without { PH_HEAD -[cue:wh]-> WH } % no loop
without { e.label = conj } % not conjuncted WH word'''
# Add IntPhrase=Yes to PH_HEAD and cue:wh
wh_edge_0_0.command = '''PH_HEAD.IntPhrase = "Yes" ;
add_edge PH_HEAD -[cue:wh]-> WH'''

wh_edge = cl.DisjRule("wh_edge", root=wh_edge_0_0)

# Determiner or adjectival WH
wh_edge_1_0 = cl.Snippet("wh_edge_1_0")
wh_edge_1_0.request = '''pattern { PH_HEAD -[det|amod]-> WH }
without { G1 [lemma="ne"] ; % n'importe quel constructions
\tG2 [form="importe"|"IMPORTE"] ; G1 < G2 ; G2 < WH }'''

# Fixed WH locution
wh_edge_1_1 = cl.Snippet("wh_edge_1_1")
wh_edge_1_1.request = '''pattern { e.label = fixed }
without { PH_HEAD [lemma="ne"] ; % n'importe WH constructions
\tG2 [form="importe"|"IMPORTE"] ; PH_HEAD < G2 ; G2 < WH }'''
# e.g. À quoi bon

# nmod "de" complement only if PH_HEAD is a subject
wh_edge_1_2 = cl.Snippet("wh_edge_1_2")
wh_edge_1_2.request = '''pattern { PH_HEAD -[nmod|obl|obl:nmod]-> WH ;
\tWH -[case]-> D ; D [lemma="de"] ; PH_HEAD << WH ; ANCHOR -[nsubj]-> PH_HEAD }'''

# nmod "de" complement only if PH_HEAD also has a preposition
wh_edge_1_3 = cl.Snippet("wh_edge_1_3")
wh_edge_1_3.request = '''pattern { PH_HEAD -[nmod|obl|obl:nmod]-> WH ;
\tWH -[case]-> D ; D [lemma="de"] ; PH_HEAD << WH ; PH_HEAD -[case]-> K  }'''


layer = [wh_edge_1_0, wh_edge_1_1, wh_edge_1_2, wh_edge_1_3]
wh_edge.add_snippets(layer, wh_edge_0_0)


##### ph_head_pull: Pulling IntPhrase="Yes"

# Root
ph_head_pull_0_0 = cl.Snippet("ph_head_pull_0_0")
ph_head_pull_0_0.request = '''pattern { CUR[IntPhrase="Yes"] ;
\te : CUR -[cue:wh]-> WH ; CAND << CUR }
without { CAND -[cue:wh]-> WH } % no loop
without { CUR[Quoted="Yes"] }'''
ph_head_pull_0_0.command = '''del_feat CUR.IntPhrase ;
del_edge e ;
CAND.IntPhrase = "Yes" ;
add_edge CAND -[cue:wh]-> WH'''

ph_head_pull = cl.DisjRule("ph_head_pull", root=ph_head_pull_0_0)

# CAND is a nominal subject
ph_head_pull_1_0 = cl.Snippet("ph_head_pull_1_0")
ph_head_pull_1_0.request = '''pattern { ANCHOR -[1=nsubj]-> CAND ;
\tCAND -[nmod|obl:mod]->  CUR ;
\tCUR -[case]-> D ; D[lemma="de"] } % only de complements }'''

# CAND has a preposition + de complement
ph_head_pull_1_1 = cl.Snippet("ph_head_pull_1_1")
ph_head_pull_1_1.request = '''pattern { CAND -[case]-> P ;
\tCAND -[nmod|obl:mod]->  CUR ;
\tCUR -[case]-> D ; D[lemma="de"] } % only de complements }'''

layer = [ph_head_pull_1_0, ph_head_pull_1_1]
ph_head_pull.add_snippets(layer, ph_head_pull_0_0)


##### ph_edge_b: Finding ph_path with WH != PH_HEAD

# Root
ph_edge_b_0_0 = cl.Snippet("ph_edge_b_0_0")
ph_edge_b_0_0.request = '''pattern {
\tPH_HEAD[IntPhrase="Yes"] ; PH_HEAD -[cue:wh]-> WH }'''

ph_edge_b = cl.DisjRule("ph_edge_b", root=ph_edge_b_0_0)


# Presence of CL_HEAD
ph_edge_b_1_0 = cl.Snippet("ph_edge_b_1_0")
ph_edge_b_1_0.request = '''pattern {
\tf : CL_HEAD -[1=obl|nmod|nsubj|obj|advmod|xcomp]-> PH_HEAD }
without { CL_HEAD -[cue:wh]-> WH } % no loop'''
# Adding IntClause and cue
ph_edge_b_1_0.command = '''CL_HEAD.IntClause = "Yes" ;
\tadd_edge CL_HEAD -[cue:wh]-> WH'''

# oblique, modifier, subject or xcomp (e.g. "de quelle couleur devient ...")
ph_edge_b_2_0 = cl.Snippet("ph_edge_b_2_0")
ph_edge_b_2_0.request = '''pattern { CL_HEAD -[1=obl|nmod|nsubj|xcomp]-> PH_HEAD }'''

# with determiner "quel"
ph_edge_b_2_1 = cl.Snippet("ph_edge_b_2_1")
ph_edge_b_2_1.request = '''pattern { WH[lemma="quel"] }'''

# fixed WH expression
ph_edge_b_2_2 = cl.Snippet("ph_edge_b_2_2")
ph_edge_b_2_2.request = '''pattern { PH_HEAD -[fixed]-> WH }'''


### Alone: CL_HEAD = PH_HEAD
ph_edge_b_1_1_2 = cl.Snippet("ph_edge_b_1_1_2")
ph_edge_b_1_1_2.request = '''without { PH_HEAD[IntClause="Yes"] } % no loop'''
# Adding IntClause
ph_edge_b_1_1_2.command = '''PH_HEAD.IntClause = "Yes"'''

# Alone: Special dependency
ph_edge_b_2_1_2 = cl.Snippet("ph_edge_b_2_1_2")
ph_edge_b_2_1_2.request = '''pattern {
ANCHOR -[1=root|parataxis|discourse|reparandum|dislocated|appos]-> PH_HEAD }'''

# Alone: quoted
ph_edge_b_2_2_2 = cl.Snippet("ph_edge_b_2_2_2")
ph_edge_b_2_2_2.request = '''pattern { PH_HEAD[Quoted="Yes"] }'''

# Alone: as object or oblique of "savoir"
ph_edge_b_2_3_2 = cl.Snippet("ph_edge_b_2_3_2")
ph_edge_b_2_3_2.request = '''pattern { ANCHOR -[1=obl|obj]-> PH_HEAD ;
\tANCHOR[lemma="savoir"|"demander"] ; ANCHOR << PH_HEAD }'''
# Note: we should better take any interrogative-embedding predicate, rather
# than just "savoir"


ph_edge_b.add_snippets([ph_edge_b_1_0, ph_edge_b_1_1_2], ph_edge_b_0_0)
layer = [ph_edge_b_2_0, ph_edge_b_2_1, ph_edge_b_2_2]
ph_edge_b.add_snippets(layer, ph_edge_b_1_0)
layer = [ph_edge_b_2_1_2, ph_edge_b_2_2_2, ph_edge_b_2_3_2]
ph_edge_b.add_snippets(layer, ph_edge_b_1_1_2)



##### ph_edge_a: Finding ph_path with WH = PH_HEAD

# Root:
ph_edge_a_0_0 = cl.Snippet("ph_edge_a_0_0")
ph_edge_a_0_0.request = '''pattern { WH[PronType="Int",!IntPhrase] ;
\te : CL_HEAD -[1=nsubj|iobj|obj|obl|advmod|nmod|xcomp|advcl]-> WH }
% Negative clauses:
without { CL_HEAD -[cue:wh]-> WH }
without { N [lemma="ne"] ; N < CL_HEAD ; % n'importe WH constructions
\tCL_HEAD [form="importe"|"IMPORTE"] ; CL_HEAD < WH }
without { WH[Quoted="Yes"] } % case wh_alone_1_1
without { CL_HEAD -[1=obj]-> WH ; CL_HEAD[lemma<>"appeler"|"aller"] ;
\tCL_HEAD << WH ; WH[upos="ADV"] ; WH[lemma<>"combien"] } % case wh_alone_1_3
without { CL_HEAD -[1=obl|obj]-> WH ; CL_HEAD [lemma="savoir"|"demander"] ;
\tCL_HEAD << WH ; WH[upos="ADV"] } % case wh_alone_1_4
without { CL_HEAD -[1=obl|obj]-> WH ; CL_HEAD [lemma="savoir"|"demander"] ;
\tCL_HEAD << WH ; WH[upos="PRON"] } % case wh_alone_1_5'''
# Adds IntClause, IntPhrase and cue
ph_edge_a_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
WH.IntPhrase = "Yes" ;
add_edge CL_HEAD -[cue:wh]-> WH ;'''

ph_edge_a = cl.DisjRule("ph_edge_a", root=ph_edge_a_0_0)

# No other restriction (not nmod or advcl)
ph_edge_a_1_0 = cl.Snippet("ph_edge_a_1_0")
ph_edge_a_1_0.request = '''pattern {
\tCL_HEAD -[1=nsubj|iobj|obj|obl|advmod|xcomp]-> WH }'''

# nmod and fronted
ph_edge_a_1_1 = cl.Snippet("ph_edge_a_1_1")
ph_edge_a_1_1.request = '''pattern { e.label = nmod ; WH << CL_HEAD }'''

# nmod of a NP without preposition
ph_edge_a_1_1 = cl.Snippet("ph_edge_a_1_1")
ph_edge_a_1_1.request = '''pattern { e.label = nmod }
without { CL_HEAD -[case|mark]-> P ; P[upos="ADP"]}
without { CL_HEAD -[case|mark]-> P ; P[ExtPos="ADP"]}'''

# advcl with participial or infinitival copula and a preposition
ph_edge_a_1_3 = cl.Snippet("ph_edge_a_1_3")
ph_edge_a_1_3.request = '''pattern { e.label = advcl ;
\ta: WH -[cop|aux]-> E ; E[VerbForm="Part"|"Inf"] ; WH -[case|mark]-> P ;
\tP[upos="ADP"] }
without { WH -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''
# ... comme étant quoi ?

# advcl with participial or infinitival copula and a prepositional locution
ph_edge_a_1_4 = cl.Snippet("ph_edge_a_1_4")
ph_edge_a_1_4.request = '''pattern { e.label = advcl ;
\ta: WH -[cop|aux]-> E ; E[VerbForm="Part"|"Inf"] ; WH -[case|mark]-> P ;
\tP[ExtPos="ADP"] }
without { WH -[1=aux]-> AUX ; AUX[VerbForm="Fin"] }'''

layer = [ph_edge_a_1_0, ph_edge_a_1_1, ph_edge_a_1_3, ph_edge_a_1_4]
ph_edge_a.add_snippets(layer, ph_edge_a_0_0)


# Case with WH word isolated by conj : no IntPhrase="Yes" added


##### wh_alone: Isolated WH = PH_HEAD = CL_HEAD

# Root
wh_alone_0_0 = cl.Snippet("wh_alone_0_0")
wh_alone_0_0.request = '''pattern { WH [PronType="Int",!IntPhrase,!IntClause] }'''
# Adding IntClause and IntPhrase
wh_alone_0_0.command = '''WH.IntClause = "Yes" ;
WH.IntPhrase = "Yes"'''

wh_alone = cl.DisjRule("wh_alone", root=wh_alone_0_0)


# adjectival "quel" with copula
wh_alone_1_0 = cl.Snippet("wh_alone_1_0")
wh_alone_1_0.request = '''pattern { WH[lemma="quel",upos="ADJ"] ;
\tWH -[cop]-> C }'''

# Special dependency
wh_alone_1_1 = cl.Snippet("wh_alone_1_1")
wh_alone_1_1.request = '''pattern {
ANCHOR -[1=root|parataxis|discourse|reparandum|dislocated|appos]-> WH }'''

# Quoted
wh_alone_1_2 = cl.Snippet("wh_alone_a_1_2")
wh_alone_1_2.request = '''pattern { WH[Quoted="Yes"] }'''

# Adverb as object or ccomp
wh_alone_1_3 = cl.Snippet("wh_alone_a_1_3")
wh_alone_1_3.request = '''pattern { ANCHOR -[1=obj|ccomp]-> WH ;
\tWH[upos="ADV"] ; ANCHOR << WH }
without { ANCHOR[lemma="appeler"|"aller"] }
without { ANCHOR -[1=obj]-> WH ; WH[lemma="combien"] }'''
# e.g. "s'appeler comment", or "aller où" using obj sometimes
# obliques adverbs are rarely oblique object in a different clause

# Adverb as oblique or direct object object of "savoir" or "(se) demander"
wh_alone_1_4 = cl.Snippet("wh_alone_a_1_4")
wh_alone_1_4.request = '''pattern { ANCHOR -[1=obl|obj|ccomp]-> WH ;
\tWH[upos="ADV"] ; ANCHOR << WH ; ANCHOR[lemma="savoir"|"demander"] }'''
# e.g. Ça va s'arrêter mais je sais pas à partir de quand.

# Pronoun as object or oblique of "savoir" or "(se) demander"
wh_alone_1_5 = cl.Snippet("wh_alone_a_1_5")
wh_alone_1_5.request = '''pattern { ANCHOR -[1=obl|obj|ccomp]-> WH ;
\tANCHOR[lemma="savoir"|"demander"] ; WH[upos="PRON"] ; ANCHOR << WH }'''
# Note: we should better take any interrogative-embedding predicate, rather
# than just "savoir"

# Pronoun as ccomp
wh_alone_1_6 = cl.Snippet("wh_alone_1_6")
wh_alone_1_6.request = '''pattern { ANCHOR -[1=ccomp]-> WH ; WH[upos="PRON"] }'''

layer =  [wh_alone_1_0, wh_alone_1_1, wh_alone_1_2, wh_alone_1_3]
layer += [wh_alone_1_4, wh_alone_1_5, wh_alone_1_6]
wh_alone.add_snippets(layer, wh_alone_0_0)


##### cleft: clefted wh phrases, to be applied before any other rule

cleft_0_0 = cl.Snippet("cleft_0_0")
cleft_0_0.request = '''pattern { C[lemma="ce"] ; E[lemma="être"] ;
\tQ[lemma="que"|"qui"|"dont", upos="SCONJ"] ; 
\tHEAD -[1=advcl|acl|csubj|ccomp]-> CL_HEAD ;
\tHEAD -[cop]-> E ; HEAD -[1=expl|nsubj]-> C ;
\tC < E ; E << HEAD ; HEAD << Q ; Q << CL_HEAD }
without { CL_HEAD -[cue:wh]-> HEAD } % no loop'''

cleft = cl.DisjRule("cleft", root=cleft_0_0)


# HEAD is a wh word
cleft_1_0 = cl.Snippet("cleft_1_0")
cleft_1_0.request = '''pattern { HEAD[PronType="Int",!IntPhrase] }'''
# Adding IntPhrase, IntClause and cue relation
cleft_1_0.command = '''HEAD.IntPhrase = "Yes" ;
CL_HEAD.IntClause = "Yes" ; add_edge CL_HEAD -[cue:wh]-> HEAD ;'''

# HEAD is PH_HEAD
cleft_1_1 = cl.Snippet("cleft_1_1")
cleft_1_1.request = '''pattern { HEAD[IntPhrase="Yes"] ;
\tHEAD -[cue:wh]-> WH }'''
# Adding IntClause and cue relation
cleft_1_1.command = '''CL_HEAD.IntClause = "Yes" ;
add_edge CL_HEAD -[cue:wh]-> WH ;'''

cleft.add_snippets([cleft_1_0, cleft_1_1], cleft_0_0)
