import classes as cl

##### eske: Annotating marker "est-ce que" or alternative forms
# "est-ce" or "ce que", supposed to be well annotated as fixed
# Alternative graphies are not taken into account

eske = cl.DisjPat("eske")

# fixed "est-ce que" or "est-ce" without qu'
eske_1_0 = cl.Snippet("eske_1_0")
eske_1_0.pattern = '''pattern { N1[form="est"|"Est"|"EST"] ;
\tN2[form="ce"|"-ce"|"CE"|"-CE"] ;
\tN1 < N2 ; N1 -[fixed]-> N2  }
without { Q [form="qu'"|"Qu'"|"QU'"] ; Q < N1 }'''
# we could have "c'est-à-dire que" preceding

# fixed "c'que"
eske_1_1 = cl.Snippet("eske_1_1")
eske_1_1.pattern = '''pattern { N1[form="ce"|"-ce"|"CE"|"-CE"] ;
\tN2 [form="que"|"QUE"] ; N1 < N2 ; N1 -[fixed]-> N2 }'''

# Presence of CL_HEAD
eske_2_0 = cl.Snippet("eske_2_0")
eske_2_0.pattern = '''pattern { CL_HEAD -[mark]-> N1 ; }
without { CL_HEAD -[cue:mark]-> N1 } % no loop '''
# Adding IntClause = "Yes" and cue relation
eske_2_0.command = '''CL_HEAD.IntClause = "Yes" ;
\tadd_edge CL_HEAD -[cue:mark]-> N1 ; '''

# Alone: no CL_HEAD
eske_2_1 = cl.Snippet("eske_2_1")
eske_2_1.pattern = '''without { CL_HEAD -[mark]-> N1 ; N1[!IntClause] }
without { N1.IntClause = "Yes"} % no loop '''
# Adding IntClause = "Yes" only
eske_2_1.command = '''N1.IntClause = "Yes" ;'''


eske.add_snippets([eske_1_0, eske_1_1], eske.root)
eske.add_snippets([eske_2_0, eske_2_1], eske.root)



##### que: Annotating "que" marker

# Root
que_0_0 = cl.Snippet("que_0_0")
que_0_0.pattern = '''pattern { Q[lemma="que"] ; WH[PronType="Int"] ;
\tWH << Q }'''

que = cl.DisjPat("que", root=que_0_0)

# Presence of CL_HEAD marking que
que_1_0 = cl.Snippet("que_1_0")
que_1_0.pattern = '''pattern { CL_HEAD -[mark|xcomp]-> Q ;
\tCL_HEAD -[cue:wh]-> WH ; Q << CL_HEAD }
without { CL_HEAD -[cue:mark]-> Q } % no loop'''
# Adding cur relation
que_1_0.command = '''add_edge CL_HEAD -[cue:mark]-> Q ;'''

# Alone: no CL_HEAD
que_1_1 = cl.Snippet("que_1_1")
que_1_1.pattern = '''pattern { WH -[mark|xcomp|dep]-> Q ; WH[IntClause="Yes"] }
without { WH -[cue:mark]-> Q }'''
# Adding cue relation from the WH word
que_1_1.command = '''add_edge WH -[cue:mark]-> Q ;'''

# Presence of CL_HEAD but governed by WH
que_1_2 = cl.Snippet("que_1_2")
que_1_2.pattern = '''pattern { d: WH -[dep|mark|xcomp]-> Q ;
\tCL_HEAD -[cue:wh]-> WH ; Q << CL_HEAD }
without { CL_HEAD -[cue:mark]-> Q } % no loop'''
# Changing governer and adding cue relation
que_1_2.command = '''add_edge CL_HEAD -[mark]-> Q ; del_edge d ;
add_edge CL_HEAD -[cue:mark]-> Q ;'''


que.add_snippets([que_0_0, que_1_1, que_1_2], que_0_0)


##### si: Annotating "si" marker

# Root
si_0_0 = cl.Snippet("si_0_0")
si_0_0.pattern = '''pattern {a: ANCHOR -[advcl|acl|ccomp|csubj]-> CL_HEAD ;
\tm: CL_HEAD -[mark]-> S ; S[lemma="si",upos="SCONJ"] ; CL_HEAD[!IntClause] }
without { M[lemma="même"] ; M < S }
without { Q[upos=SCONJ,!ExtPos] ; Q << S ; CL_HEAD -[mark]-> Q }
without { Q[ExtPos=SCONJ] ; Q << S ; CL_HEAD -[mark]-> Q }
without { Q[upos=SCONJ,!ExtPos] ; Q << S ; ANCHOR -[mark]-> Q }
without { Q[ExtPos=SCONJ] ; Q << S ; ANCHOR -[mark]-> Q }
without { CL_HEAD -[cue:mark]-> S  } % no loop'''
# Adding IntClause= "Yes" and cue relation
si_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
\tadd_edge CL_HEAD -[cue:mark]-> S ;'''

si = cl.DisjPat("si", root=si_0_0)

# Finite verb
si_1_0 = cl.Snippet("si_1_0")
si_1_0.pattern = '''pattern { CL_HEAD[upos="VERB"|"AUX",VerbForm="Fin"] }'''

# Finite copula or auxiliary
si_1_1 = cl.Snippet("si_1_1")
si_1_1.pattern = '''pattern { CL_HEAD -[1=aux|cop]-> V ;
\tV[VerbForm="Fin"] }'''

# ccomp
si_2_0 = cl.Snippet("si_2_0")
si_2_0.pattern = '''pattern { ANCHOR -[ccomp]-> CL_HEAD }'''

# acl or advcl with a preposition preceding
si_2_1 = cl.Snippet("si_2_1")
si_2_1.pattern = '''pattern { ANCHOR -[advcl|acl]-> CL_HEAD ; C[upos="ADP",!ExtPos] ;
\tCL_HEAD -[case|mark]-> C ; C < S }'''

# acl or advcl with a prepositional locution preceding
si_2_2 = cl.Snippet("si_2_2")
si_2_2.pattern = '''pattern { ANCHOR -[advcl|acl]-> CL_HEAD ; C[ExtPos="ADP"] ;
\tCL_HEAD -[case|mark]-> C ; C < S }'''

# csubj
si_2_3 = cl.Snippet("si_2_3")
si_2_3.pattern = '''pattern { a.label = csubj }'''

si.add_snippets([si_1_0, si_1_1], si_0_0)
si.add_snippets([si_2_0, si_2_1, si_2_2, si_2_3], si_0_0)


##### spp: Annotating suffixed personal pronoun + ce

# Root
spp_0_0 = cl.Snippet("spp_0_0")
spp_0_0.pattern = '''pattern { S[upos="PRON"] ;
\tS[lemma="ce"|"je"|"tu"|"il"|"elle"|"on"|"nous"|"vous"|"ils"|"elles"] ;
\ts: CL_HEAD -[1=expl|nsubj]-> S ; }
% Negative patterns
without { CL_HEAD -[1=parataxis]-> G ; G[Quoted="Yes"] } % no verb-reporting stylistic inversion
without { G -[1=parataxis]-> CL_HEAD ; G[Quoted="Yes"] } % no verb-reporting stylistic inversion
without { CL_HEAD -[expl:comp]-> S } % no expletive object S
without { CL_HEAD -[cue:mark]-> S } % no loop
'''
# Adding IntClause=Yes and cue relation
spp_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
add_edge CL_HEAD -[cue:mark]-> S ;'''

spp = cl.DisjPat("spp", root=spp_0_0)

# Inverted subject wrt. verbal finite CL_HEAD
spp_1_0 = cl.Snippet("spp_1_0")
spp_1_0.pattern = '''pattern { CL_HEAD[upos="VERB"|"AUX", VerbForm="Fin"] ;
\tCL_HEAD < S ; }
without { CL_HEAD[Mood="Imp"] } % not imperative'''

# Inverted subject wrt. the finite copula or auxiliary of CL_HEAD
spp_1_1 = cl.Snippet("spp_1_1")
spp_1_1.pattern = '''pattern { CL_HEAD -[1=cop|aux]-> V ;
\tV[upos="VERB"|"AUX", VerbForm="Fin"] ; V < S }
without { V[Mood="Imp"] } % not imperative'''

### Filtering out extra-short stylistic inversions

# Presence of a WH word
spp_2_0 = cl.Snippet("spp_2_0")
spp_2_0.pattern = '''pattern { CL_HEAD -[cue:wh]-> WH }'''

# Presence of an interrogation point
spp_2_1 = cl.Snippet("spp_2_1")
spp_2_1.pattern = '''pattern { CL_HEAD -[punct]-> IP ;
\tIP[lemma="?"] }'''

# No additional subject or WH word, and no preceding adverb (locution)
spp_2_2 = cl.Snippet("spp_2_2")
spp_2_2.pattern = '''without { CL_HEAD -[cue:wh]-> WH }
without { A[upos="ADV",!ExtPos,lemma <> "ne"|"pourquoi"|"où"|"comment"|"quand"] ;
\tCL_HEAD -[advmod]-> A ; A << CL_HEAD } % No non-interrogative preceding adverb
without { A[ExtPos="ADV",lemma <> "ne"|"pourquoi"|"où"|"comment"|"quand"] ;
\tCL_HEAD -[advmod]-> A ; A << CL_HEAD } % No non-interrogative preceding adverbial phrase'''


# No parataxis
spp_3_0 = cl.Snippet("spp_3_0")
spp_3_0.pattern = '''without { ANCHOR -[1=parataxis]-> CL_HEAD }'''

# Paraxtaxis + presence of an additional subject, or of an (oblique) object,
# or clausal complement
spp_3_1 = cl.Snippet("spp_3_1")
spp_3_1.pattern = '''pattern { ANCHOR -[1=parataxis]-> CL_HEAD ;
\tCL_HEAD -[1=nsubj|obj|obl|ccomp]-> U }
without { CL_HEAD -[obl:mod]-> U }'''

# Paraxtaxis + presence of a verbal complement having an (oblique) object
spp_3_2 = cl.Snippet("spp_3_2")
spp_3_2.pattern = '''pattern { ANCHOR -[1=parataxis]-> CL_HEAD ;
\tCL_HEAD -[xcomp]-> U ; U[upos="VERB"|"AUX"] ;
\tU -[1=obj|obl|ccomp]-> W }
without { U -[obl:mod]-> W }'''

spp.add_snippets([spp_1_0, spp_1_1], spp_0_0)
spp.add_snippets([spp_2_0, spp_2_1, spp_2_2], spp_0_0)
spp.add_snippets([spp_3_0, spp_3_1, spp_3_2], spp_2_2)



##### titu: Annotating "-ti"/"-tu" markers

titu_0_0 = cl.Snippet("titu_0_0")
titu_0_0.pattern = '''pattern { CL_HEAD -[1=mark|nsubj|expl]-> T ;
\tT[form="tu"|"-tu"|"ti"|"-ti"|"TU"|"-TU"|"TI"|"-TI"] }
without { CL_HEAD -[cue:mark]-> T } % no loop'''
# Adding IntClause= "Yes" and cue relation
titu_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
add_edge CL_HEAD -[cue:mark]-> T'''

titu = cl.DisjPat("titu", root=titu_0_0)

# Expected marker relation
titu_1_0 = cl.Snippet("titu_1_0")
titu_1_0.pattern = '''pattern { CL_HEAD -[1=mark]-> T }'''

# subject relation with -ti
titu_1_1 = cl.Snippet("titu_1_1")
titu_1_1.pattern = '''pattern { CL_HEAD -[1=nsubj|expl]-> T ;
\tT[form="ti"|"-ti"|"TI"|"-TI"] }'''

titu.add_snippets([titu_1_0, titu_1_1], titu_0_0)



##### Disjunctive ?

##### Raising intonation ?