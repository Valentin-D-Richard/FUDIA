import classes as cl

# Identifying and adding annotation to the WH word,
# the WH phrase head PH_HEAD and the clause head CL_HEAD

##### wh_edge: Finding wh_path with PH_HEAD != WH

# Root :
wh_edge_0_0 = cl.Snippet("wh_edge_0_0")
wh_edge_0_0.pattern = '''pattern { WH [PronType="Int"] ; e : PH_HEAD -> WH ;
\tPH_HEAD[!IntPhrase] }
without { e.label = conj } % not conjuncted WH word'''
# Add IntPhrase=Yes to PH_HEAD and cue:wh
wh_edge_0_0.command = '''PH_HEAD.IntPhrase = "Yes" ;
add_edge PH_HEAD -[cue:wh]-> WH'''

wh_edge = cl.DisjPat("wh_edge", root=wh_edge_0_0)

# Determiner WH
wh_edge_1_0 = cl.Snippet("wh_edge_1_0")
wh_edge_1_0.pattern = '''pattern { e.label = det }
without { G1 [lemma="ne"] ; % n'importe quel constructions
\tG2 [form="importe"] ; G1 < G2 ; G2 < WH }'''

# Fixed WH locution
wh_edge_1_1 = cl.Snippet("wh_edge_1_1")
wh_edge_1_1.pattern = '''pattern { e.label = fixed }
without { PH_HEAD [lemma="ne"] ; % n'importe WH constructions
\tG2 [form="importe"] ; PH_HEAD < G2 ; G2 < WH }'''

# nmod "de" complement only if PH_HEAD also has a preposition
wh_edge_1_2 = cl.Snippet("wh_edge_1_2")
wh_edge_1_2.pattern = '''pattern { PH_HEAD -[nmod]-> WH ;
\tWH -[case]-> D ; D [lemma="de"] ; PH_HEAD << WH }'''

wh_edge.add_snippets([wh_edge_1_0, wh_edge_1_1, wh_edge_1_2], wh_edge_0_0)


##### ph_head_pull: Pulling IntPhrase="Yes"

# Root
ph_head_pull_0_0 = cl.Snippet("ph_head_pull_0_0")
ph_head_pull_0_0.pattern = '''pattern { R[IntPhrase="Yes"] ;
\te : R -[cue:wh]-> W ;
\tPH_HEAD -[nmod]->  R ; % maybe obl:mod is ok
\tR -[case]-> D ; D[lemma="de"] ; % only de complements
\tPH_HEAD << R ; PH_HEAD[!IntPhrase] }
without { R[Quoted="Yes"] }'''
ph_head_pull_0_0.command = '''del_feat R.IntPhrase ;
del_edge e ;
PH_HEAD.IntPhrase = "Yes" ;
add_edge PH_HEAD -[cue:wh]-> W'''

ph_head_pull = cl.DisjPat("ph_head_pull", root=ph_head_pull_0_0)

# PH_HEAD is has a preposition
ph_head_pull_1_0 = cl.Snippet("ph_head_pull_1_0")
ph_head_pull_1_0.pattern = '''pattern { PH_HEAD -[case]-> K }'''
# Only PP can be non-trivial WH-phrases

# PH_HEAD is a nominal subject
ph_head_pull_1_1 = cl.Snippet("ph_head_pull_1_1")
ph_head_pull_1_1.pattern = '''pattern { ANCHOR -[nsubj]-> PH_HEAD }'''

ph_head_pull.add_snippets([ph_head_pull_1_0, ph_head_pull_1_1], ph_head_pull_0_0)


##### ph_edge_b: Finding ph_path with WH != PH_HEAD

# Root
ph_edge_b_0_0 = cl.Snippet("ph_edge_b_0_0")
ph_edge_b_0_0.pattern = '''pattern {
\tPH_HEAD[IntPhrase="Yes"] ; PH_HEAD -[cue:wh]-> WH }'''

ph_edge_b = cl.DisjPat("ph_edge_b", root=ph_edge_b_0_0)


# Presence of CL_HEAD
ph_edge_b_1_0 = cl.Snippet("ph_edge_b_1_0")
ph_edge_b_1_0.pattern = '''pattern { f : CL_HEAD -[1=obl|nmod|nsubj]-> PH_HEAD }
without { CL_HEAD[IntClause] }'''
# Adding IntClause and cue
ph_edge_b_1_0.command = '''CL_HEAD.IntClause = "Yes" ;
\tadd_edge CL_HEAD -[cue:wh]-> WH'''


### Alone: CL_HEAD = PH_HEAD
ph_edge_b_1_1 = cl.Snippet("ph_edge_b_1_1")
ph_edge_b_1_1.pattern = '''without { PH_HEAD[IntClause] }'''
# Adding IntClause
ph_edge_b_1_1.command = '''PH_HEAD.IntClause = "Yes"'''

# Alone: Special dependency
ph_edge_b_2_1 = cl.Snippet("ph_edge_b_2_1")
ph_edge_b_2_1.pattern = '''pattern {
ANCHOR -[1=root|parataxis|discourse|vocative|reparandum|dislocated|list|orphan]-> PH_HEAD }'''

# Alone: quoted
ph_edge_b_2_2 = cl.Snippet("ph_edge_b_2_2")
ph_edge_b_2_2.pattern = '''pattern { PH_HEAD[Quoted="Yes"] }'''

# Alone: as object or oblique of "savoir"
ph_edge_b_2_3 = cl.Snippet("ph_edge_b_2_3")
ph_edge_b_2_3.pattern = '''pattern { ANCHOR -[1=obl|obj]-> PH_HEAD ;
\tANCHOR[lemma="savoir"] }'''
# Note: we should better take any interrogative-embedding predicate, rather
# than just "savoir"


ph_edge_b.add_snippets([ph_edge_b_1_0, ph_edge_b_1_1], ph_edge_b_0_0)
layer = [ph_edge_b_2_1, ph_edge_b_2_2, ph_edge_b_2_3]
ph_edge_b.add_snippets(layer, ph_edge_b_1_1)



##### ph_edge_a: Finding ph_path with WH = PH_HEAD

# Root:
ph_edge_a_0_0 = cl.Snippet("ph_edge_a_0_0")
ph_edge_a_0_0.pattern = '''pattern { WH [PronType="Int",!IntPhrase] ;
\te : CL_HEAD -[1=nsubj|iobj|obj|obl|advmod|nmod|xcomp|advcl]-> WH ;
\tCL_HEAD[!IntClause,!IntPhrase] }
without { N [lemma="ne"] ; N < CL_HEAD ; % n'importe WH constructions
\tCL_HEAD [form="importe"] ; CL_HEAD < WH }
without { WH[Quoted="Yes"] } % case wh_alone_1_1
without { CL_HEAD -[1=obl|obj]-> WH ;
\tCL_HEAD << WH ; WH[upos="ADV"] } % case wh_alone_1_3
without { CL_HEAD -[1=obl|obj]-> WH ; CL_HEAD [lemma="savoir"] ;
\tCL_HEAD << WH ; WH[upos="PRON"] } % case wh_alone_1_4'''
# Adds IntClause, IntPhrase and cue
ph_edge_a_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
WH.IntPhrase = "Yes" ;
add_edge CL_HEAD -[cue:wh]-> WH ;'''

ph_edge_a = cl.DisjPat("ph_edge_a", root=ph_edge_a_0_0)

# No other restriction (not nmod or advcl)
ph_edge_a_1_0 = cl.Snippet("ph_edge_a_1_0")
ph_edge_a_1_0.pattern = '''pattern {
\tCL_HEAD -[1=nsubj|iobj|obj|obl|advmod|xcomp]-> WH }'''

# nmod and fronted
ph_edge_a_1_1 = cl.Snippet("ph_edge_a_1_1")
ph_edge_a_1_1.pattern = '''pattern { e.label = nmod ; WH << CL_HEAD }'''

# advcl with participial copula
ph_edge_a_1_2 = cl.Snippet("ph_edge_a_1_2")
ph_edge_a_1_2.pattern = '''pattern { e.label = advcl ;
\tWH -[cop]-> E ; E.VerbForm = "Part"}'''
# ... comme étant quoi ?

ph_edge_a.add_snippets([ph_edge_a_1_0, ph_edge_a_1_1, ph_edge_a_1_2], ph_edge_a_0_0)


# Case with WH word isolated by conj : no IntPhrase="Yes" added

##### wh_alone: Isolated WH = PH_HEAD = CL_HEAD

# Root
wh_alone_0_0 = cl.Snippet("wh_alone_0_0")
wh_alone_0_0.pattern = '''pattern { WH [PronType="Int",!IntPhrase,!IntClause] }'''
# Adding IntClause and IntPhrase
wh_alone_0_0.command = '''WH.IntClause = "Yes" ;
WH.IntPhrase = "Yes"'''

wh_alone = cl.DisjPat("wh_alone", root=wh_alone_0_0)

# Alone: Special dependency
wh_alone_1_1 = cl.Snippet("wh_alone_1_1")
wh_alone_1_1.pattern = '''pattern {
ANCHOR -[1=root|parataxis|discourse|vocative|reparandum|dislocated|list|orphan]-> WH }'''

# Alone: quoted
wh_alone_1_2 = cl.Snippet("wh_alone_a_1_2")
wh_alone_1_2.pattern = '''pattern { WH[Quoted="Yes"] }'''

# Alone: adverb as object or oblique
wh_alone_1_3 = cl.Snippet("wh_alone_a_1_3")
wh_alone_1_3.pattern = '''pattern { ANCHOR -[1=obl|obj]-> WH ;
\tWH[upos="ADV"] ; ANCHOR << WH }'''

# Alone: pronoun as object or oblique of "savoir"
wh_alone_1_4 = cl.Snippet("wh_alone_a_1_4")
wh_alone_1_4.pattern = '''pattern { ANCHOR -[1=obl|obj]-> WH ;
\tANCHOR[lemma="savoir"] ; WH[upos="PRON"] ; ANCHOR << WH }'''
# Note: we should better take any interrogative-embedding predicate, rather
# than just "savoir"


layer = [wh_alone_1_1, wh_alone_1_2, wh_alone_1_3, wh_alone_1_4]
wh_alone.add_snippets(layer, wh_alone_0_0)


##### cleft: clefted wh phrases, to be applied before any other rule

cleft_0_0 = cl.Snippet("cleft_0_0")
cleft_0_0.pattern = '''pattern { C[lemma="ce"] ; E[lemma="être"] ;
\tQ[lemma="que"|"qui"|"dont", upos="SCONJ"] ; 
\tHEAD -[1=advcl|acl|csubj|ccomp]-> CL_HEAD ;
\tHEAD -[cop]-> E ; HEAD -[1=expl|nsubj]-> C ;
\tC < E ; E << HEAD ; HEAD << Q ; Q << CL_HEAD }'''

cleft = cl.DisjPat("cleft", root=cleft_0_0)


# HEAD is a wh word
cleft_1_0 = cl.Snippet("cleft_1_0")
cleft_1_0.pattern = '''pattern { HEAD[PronType="Int",!IntPhrase] ;
\tCL_HEAD[!IntClause] }'''
# Adding IntPhrase, IntClause and cue relation
cleft_1_0.command = '''HEAD.IntPhrase = "Yes" ;
CL_HEAD.IntClause = "Yes" ; add_edge CL_HEAD -[cue:wh]-> HEAD ;'''

# HEAD is PH_HEAD
cleft_1_1 = cl.Snippet("cleft_1_1")
cleft_1_1.pattern = '''pattern { HEAD[IntClause="Yes"] ;
\tCL_HEAD[!IntClause] }'''
# Adding IntClause and cue relation
cleft_1_1.command = '''CL_HEAD.IntClause = "Yes" ;
add_edge CL_HEAD -[cue:wh]-> HEAD ;'''

cleft.add_snippets([cleft_1_0, cleft_1_1], cleft_0_0)
