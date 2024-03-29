import classes as cl

##### eske: Annotating marker "est-ce que" or alternative forms
# "est-ce" or "ce que", supposed to be well annotated as fixed
# Alternative graphies are not taken into account

eske = cl.DisjRule("eske")

# fixed "est-ce que" or "est-ce" without qu'
eske_1_0 = cl.Snippet("eske_1_0")
eske_1_0.request = '''pattern { N1[form="est"|"Est"|"EST"] ;
\tN2[form="ce"|"-ce"|"CE"|"-CE"] ;
\tN1 < N2 ; N1 -[fixed]-> N2  }
without { Q [form="qu'"|"Qu'"|"QU'"] ; Q < N1 }'''
# we could have "c'est-à-dire que" preceding

# fixed "c'que"
eske_1_1 = cl.Snippet("eske_1_1")
eske_1_1.request = '''pattern { N1[form="ce"|"-ce"|"CE"|"-CE"] ;
\tN2 [form="que"|"QUE"] ; N1 < N2 ; N1 -[fixed]-> N2 }'''

# Presence of CL_HEAD
eske_2_0 = cl.Snippet("eske_2_0")
eske_2_0.request = '''pattern { CL_HEAD -[mark]-> N1 ; }
without { CL_HEAD -[cue:mark]-> N1 } % no loop '''
# Adding IntClause = "Yes" and cue relation
eske_2_0.command = '''CL_HEAD.IntClause = "Yes" ;
\tadd_edge CL_HEAD -[cue:mark]-> N1 ; '''

# Alone: no CL_HEAD
eske_2_1 = cl.Snippet("eske_2_1")
eske_2_1.request = '''without { CL_HEAD -[mark]-> N1 ; N1[!IntClause] }
without { N1.IntClause = "Yes"} % no loop '''
# Adding IntClause = "Yes" only
eske_2_1.command = '''N1.IntClause = "Yes" ;'''


eske.add_snippets([eske_1_0, eske_1_1], eske.root)
eske.add_snippets([eske_2_0, eske_2_1], eske.root)



##### que: Annotating "que" marker

# Root
que_0_0 = cl.Snippet("que_0_0")
que_0_0.request = '''pattern { Q[lemma="que"] ; WH[PronType="Int"] ;
\tWH << Q }'''

que = cl.DisjRule("que", root=que_0_0)

# Presence of CL_HEAD marking que
que_1_0 = cl.Snippet("que_1_0")
que_1_0.request = '''pattern { CL_HEAD -[mark|xcomp]-> Q ;
\tCL_HEAD -[cue:wh]-> WH ; Q << CL_HEAD }
without { CL_HEAD -[cue:mark]-> Q } % no loop'''
# Adding cur relation
que_1_0.command = '''add_edge CL_HEAD -[cue:mark]-> Q ;'''

# Alone: no CL_HEAD
que_1_1 = cl.Snippet("que_1_1")
que_1_1.request = '''pattern { WH -[mark|xcomp|dep]-> Q ; WH[IntClause="Yes"] }
without { WH -[cue:mark]-> Q }'''
# Adding cue relation from the WH word
que_1_1.command = '''add_edge WH -[cue:mark]-> Q ;'''

# Presence of CL_HEAD but governed by WH
que_1_2 = cl.Snippet("que_1_2")
que_1_2.request = '''pattern { d: WH -[dep|mark|xcomp]-> Q ;
\tCL_HEAD -[cue:wh]-> WH ; Q << CL_HEAD }
without { CL_HEAD -[cue:mark]-> Q } % no loop'''
# Changing governer and adding cue relation
que_1_2.command = '''add_edge CL_HEAD -[mark]-> Q ; del_edge d ;
add_edge CL_HEAD -[cue:mark]-> Q ;'''


que.add_snippets([que_0_0, que_1_1, que_1_2], que_0_0)


##### si: Annotating "si" marker

# Root
si_0_0 = cl.Snippet("si_0_0")
si_0_0.request = '''pattern {a: ANCHOR -[advcl|acl|ccomp|csubj]-> CL_HEAD ;
\tm: CL_HEAD -[mark]-> S ; S[lemma="si",upos="SCONJ"] ; CL_HEAD[!IntClause] }
without { M[lemma="même"|"comme"|"sauf"] ; M < S } % subordination locutions
without { Q[upos=SCONJ,!ExtPos] ; Q << S ; CL_HEAD -[mark]-> Q }
without { Q[ExtPos=SCONJ] ; Q << S ; CL_HEAD -[mark]-> Q }
without { Q[upos=SCONJ,!ExtPos] ; Q << S ; ANCHOR -[mark]-> Q ; ANCHOR << Q }
without { Q[ExtPos=SCONJ] ; Q << S ; ANCHOR -[mark]-> Q ; ANCHOR << Q }
without { CL_HEAD -[cue:mark]-> S  } % no loop'''
# Adding IntClause= "Yes" and cue relation
si_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
\tadd_edge CL_HEAD -[cue:mark]-> S ;'''

si = cl.DisjRule("si", root=si_0_0)

# Finite verb
si_1_0 = cl.Snippet("si_1_0")
si_1_0.request = '''pattern { CL_HEAD[upos="VERB"|"AUX",VerbForm="Fin"] }'''

# Finite copula or auxiliary
si_1_1 = cl.Snippet("si_1_1")
si_1_1.request = '''pattern { CL_HEAD -[1=aux|cop]-> V ;
\tV[VerbForm="Fin"] }'''

# ccomp
si_2_0 = cl.Snippet("si_2_0")
si_2_0.request = '''pattern { ANCHOR -[ccomp]-> CL_HEAD }'''

# acl or advcl with a preposition preceding
si_2_1 = cl.Snippet("si_2_1")
si_2_1.request = '''pattern { ANCHOR -[advcl|acl]-> CL_HEAD ; C[upos="ADP",!ExtPos] ;
\tCL_HEAD -[case|mark]-> C ; C < S }
without { C[lemma="même"|"comme"|"sauf"] }'''

# acl or advcl with a prepositional locution preceding
si_2_2 = cl.Snippet("si_2_2")
si_2_2.request = '''pattern { ANCHOR -[advcl|acl]-> CL_HEAD ; C[ExtPos="ADP"] ;
\tCL_HEAD -[case|mark]-> C ; C < S }'''

# csubj
si_2_3 = cl.Snippet("si_2_3")
si_2_3.request = '''pattern { a.label = csubj }'''

si.add_snippets([si_1_0, si_1_1], si_0_0)
si.add_snippets([si_2_0, si_2_1, si_2_2, si_2_3], si_0_0)


##### spp: Annotating suffixed personal pronoun + ce

# Root
spp_0_0 = cl.Snippet("spp_0_0")
spp_0_0.request = '''pattern { S[upos="PRON"] ;
\tS[] ;
\ts: CL_HEAD -[1=expl|nsubj]-> S ; }
% Negative filtering
without { CL_HEAD -[1=parataxis]-> G ; G[Quoted="Yes"] } % no verb-reporting stylistic inversion
without { G -[1=parataxis]-> CL_HEAD ; G[Quoted="Yes"] } % no verb-reporting stylistic inversion
without { CL_HEAD -[1=parataxis]-> G ; G << CL_HEAD } % heuristics on verb-reporting
without { CL_HEAD -[expl:comp]-> S } % no expletive object S
without { N[lemma="ne"] ; Q[lemma="que"] ; N << CL_HEAD ; CL_HEAD -> N ;
\tCL_HEAD -[advmod]-> Q ; CL_HEAD << Q } % no graft "ne + V + S + que + ... " graft
without { CL_HEAD -[cue:mark]-> S } % no loop
'''
# Adding IntClause=Yes and cue relation
spp_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
add_edge CL_HEAD -[cue:mark]-> S ;'''

spp = cl.DisjRule("spp", root=spp_0_0)

# Subject identified by its lemma: 1st case
spp_00_0 = cl.Snippet("spp_00_0")
spp_00_0.request = ''' pattern {
\tS[lemma="ce"|"je"|"tu"|"il"|"elle"|"on"|"nous"|"vous"|"ils"|"elles"|
\t"-ce"|"-je"|"-tu"|"-il"|"-elle"|"-on"|"-nous"|"-vous"|"-ils"|"-elles"|
\t"t-il"|"t-elle"|"t-ils"|"t-elles"|"-t-il"|"-t-elle"|"-t-ils"|"-t-elles"] }
'''

# Subject identified by its lemma: 2nd case (GSD and Sequoia)
spp_00_1 = cl.Snippet("spp_00_1")
spp_00_1.request = ''' pattern {
\tS[lemma="moi"|"toi"|"lui"|"elle"|"on"|"nous"|"vous"|"eux"|"elles",
\tPronType="Prs"] }'''

# Inverted subject wrt. verbal finite CL_HEAD
spp_1_0 = cl.Snippet("spp_1_0")
spp_1_0.request = '''pattern { CL_HEAD[upos="VERB"|"AUX", VerbForm="Fin"] ;
\tCL_HEAD < S ; }
without { CL_HEAD[Mood="Imp"] } % not imperative'''

# Inverted subject wrt. the finite copula or auxiliary of CL_HEAD
spp_1_1 = cl.Snippet("spp_1_1")
spp_1_1.request = '''pattern { CL_HEAD -[1=cop|aux]-> V ;
\tV[upos="VERB"|"AUX", VerbForm="Fin"] ; V < S }
without { V[Mood="Imp"] } % not imperative'''

### Filtering out extra-short stylistic inversions

# Presence of a WH word
spp_2_0 = cl.Snippet("spp_2_0")
spp_2_0.request = '''pattern { CL_HEAD -[cue:wh]-> WH }'''

# Presence of an interrogation point
spp_2_1 = cl.Snippet("spp_2_1")
spp_2_1.request = '''pattern { CL_HEAD -[punct]-> IP ;
\tIP[lemma="?"] }'''

# No additional subject or WH word, no preceding adverb (or locution)
# no special parataxis subrelation (insert, parenthesis)
spp_2_2 = cl.Snippet("spp_2_2")
spp_2_2.request = '''without { CL_HEAD -[cue:wh]-> WH }
without { A[upos="ADV",!ExtPos,lemma <> "ne"|"pourquoi"|"où"|"comment"|"quand"] ;
\tCL_HEAD -[advmod]-> A ; A << CL_HEAD } % No non-interrogative preceding adverb
without { A[ExtPos="ADV",lemma <> "ne"|"pourquoi"|"où"|"comment"|"quand"] ;
\tCL_HEAD -[advmod]-> A ; A << CL_HEAD } % No non-interrogative preceding adverbial phrase
without { ANCHOR -[parataxis:insert|parataxis:parenth]-> CL_HEAD }'''


# No parataxis
spp_3_0 = cl.Snippet("spp_3_0")
spp_3_0.request = '''without { ANCHOR -[1=parataxis]-> CL_HEAD }'''

# Paraxtaxis + presence of an additional subject, or of an (oblique) object,
# or clausal complement
spp_3_1 = cl.Snippet("spp_3_1")
spp_3_1.request = '''pattern { ANCHOR -[1=parataxis]-> CL_HEAD ;
\tCL_HEAD -[1=nsubj|obj|obl|ccomp]-> U }
without { CL_HEAD -[obl:mod]-> U }'''

# Paraxtaxis + presence of a verbal complement having an (oblique) object
spp_3_2 = cl.Snippet("spp_3_2")
spp_3_2.request = '''pattern { ANCHOR -[1=parataxis]-> CL_HEAD ;
\tCL_HEAD -[xcomp]-> U ; U[upos="VERB"|"AUX"] ;
\tU -[1=obj|obl|ccomp]-> W }
without { U -[obl:mod]-> W }'''

spp.add_snippets([spp_00_0, spp_00_1], spp_0_0)
spp.add_snippets([spp_1_0, spp_1_1], spp_0_0)
spp.add_snippets([spp_2_0, spp_2_1, spp_2_2], spp_0_0)
spp.add_snippets([spp_3_0, spp_3_1, spp_3_2], spp_2_2)



##### titu: Annotating "-ti"/"-tu" markers

titu_0_0 = cl.Snippet("titu_0_0")
titu_0_0.request = '''pattern { CL_HEAD -[1=mark|nsubj|expl]-> T ;
\tT[form="tu"|"-tu"|"ti"|"-ti"|"TU"|"-TU"|"TI"|"-TI"] }
without { CL_HEAD -[cue:mark]-> T } % no loop'''
# Adding IntClause= "Yes" and cue relation
titu_0_0.command = '''CL_HEAD.IntClause = "Yes" ;
add_edge CL_HEAD -[cue:mark]-> T'''

titu = cl.DisjRule("titu", root=titu_0_0)

# Expected marker relation
titu_1_0 = cl.Snippet("titu_1_0")
titu_1_0.request = '''pattern { CL_HEAD -[1=mark]-> T }'''

# subject relation with -ti
titu_1_1 = cl.Snippet("titu_1_1")
titu_1_1.request = '''pattern { CL_HEAD -[1=nsubj|expl]-> T ;
\tT[form="ti"|"-ti"|"TI"|"-TI"] }'''

titu.add_snippets([titu_1_0, titu_1_1], titu_0_0)



##### final: finishing touch
final = cl.DisjRule("final")

final_1_0 = cl.Snippet("final_1_0")
final_1_0.request = '''pattern { PH_HEAD[IntPhrase="Yes"] }'''
final_1_0.command = '''del_feat PH_HEAD.IntPhrase ;
PH_HEAD.PhraseType = "Int"'''

final_1_1 = cl.Snippet("final_1_1")
final_1_1.request = '''pattern { CL_HEAD[IntClause="Yes"] }'''
final_1_1.command = '''del_feat CL_HEAD.IntClause ;
CL_HEAD.ClauseType = "Int"'''

final.add_snippets([final_1_0, final_1_1], final.root)