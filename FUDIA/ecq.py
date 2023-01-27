import classes as cl

##### qecq: Reannotating expressions containing "qu'est-ce que/qui"

### Root
qecq_0_0 = cl.Snippet("qecq_0_0")
qecq_0_0.pattern = '''pattern { WH[lemma="que"] ; E[form="est"|"EST"] ;
\tC[form="ce"|"-ce"|"CE"|"-CE"] ; Q[lemma="que"|"qui"] ;
\tWH < E ; E < C ; C < Q }
without { WH -[fixed]-> E ; WH -[fixed]-> C ; WH -[fixed]-> Q } % Avoiding looping'''
# Rearranging by getting the expression as fixed
qecq_0_0.command = '''add_node WH2 :< WH ; add_node E2 :> WH ;
add_node C2 :> E2 ; add_node Q2 :> C2 ;
append_feats WH ==> WH2 ; shift WH ==> WH2 ; WH2.ExtPos = "PRON" ;
shift E ==> E2 ;
WH2.form = WH.form ; WH2.lemma = WH.lemma ; WH2.upos = WH.upos ;
append_feats E ==> E2 ;
E2.form = E.form ; E2.lemma = E.lemma ; E2.upos = E.upos ;
append_feats C ==> C2 ;
C2.form = C.form ; C2.lemma = C.lemma ; C2.upos = C.upos ;
append_feats Q ==> Q2 ;
Q2.form = Q.form ; Q2.lemma = Q.lemma ; Q2.upos = Q.upos ;
add_edge WH2 -[fixed]-> E2 ; add_edge WH2 -[fixed]-> C2 ;
add_edge WH2 -[fixed]-> Q2 ;
del_node WH ; del_node E ; del_node C ; del_node Q ;'''

qecq = cl.DisjPat("qecq", root=qecq_0_0)


# Special case of "qu'est-ce que c'est"
qecq_1_0 = cl.Snippet("qecq_1_0")
qecq_1_0.pattern = '''pattern { CE [lemma="ce"]; COP [lemma="être"];
\tQ < CE ; CE < COP }'''
# Adding "c'" and "est" as nsubj and cop
qecq_1_0.command = '''add_node CE2 :> Q2 ; add_node COP2 :> CE2 ;
append_feats CE ==> CE2 ;
CE2.form = CE.form ; CE2.lemma = CE.lemma ; CE2.upos = CE.upos ;
append_feats COP ==> COP2 ;
COP2.form = COP.form ; COP2.lemma = COP.lemma ; COP2.upos = COP.upos ;
add_edge WH2 -[nsubj]-> CE2 ; add_edge WH2 -[cop]-> COP2 ;
del_node CE ; del_node COP ; '''

# "qu'est-ce que S'"
qecq_1_1 = cl.Snippet("qecq_1_1")

# Other uses of "qu'est-ce que", complementary case
qecq_1_2 = cl.Snippet("qecq_1_2")
qecq_1_2.pattern = '''without { CE [lemma="ce"]; COP [lemma="être"];
\tQ < CE ; CE < COP }
without { WH -[1=advcl|dislocated]-> CL_HEAD }
without { E -[1=advcl|dislocated]-> CL_HEAD }'''
# Nothing to add


# "qu'est-ce que S'" with head on qu'
qecq_2_0_1 = cl.Snippet("qecq_2_0_1")
qecq_2_0_1.pattern = '''pattern { h: WH -[1=advcl|dislocated|ccomp]-> CL_HEAD ;
\tWH << CL_HEAD }'''
# Deleting h and shifting WH2 to CL_HEAD (except fixed)
qecq_2_0_1.command = '''shift WH2 =[^fixed]=> CL_HEAD ;'''

# "qu'est-ce que S'" with head on est
qecq_2_1_1 = cl.Snippet("qecq_2_1_1")
qecq_2_1_1.pattern = '''pattern { h: E -[1=advcl|dislocated|ccomp]-> CL_HEAD ;
\tWH << CL_HEAD }'''
# Shifting the head from qu' to the head of S'
qecq_2_1_1.command = '''shift E2 ==> CL_HEAD ;'''


# Q = que (objet)
qecq_3_0_1 = cl.Snippet("qecq_3_0_1")
qecq_3_0_1.pattern = '''pattern { Q[lemma="que"] }'''


# CL_HEAD is a nominal group without copula or auxiliary
qecq_4_0_1 = cl.Snippet("qecq_4_0_1")
qecq_4_0_1.pattern = '''pattern { CL_HEAD[upos="NOUN"|"PRON"|"PROPN",!ExtPos] }
without { CL_HEAD -[1=cop|aux]-> A }'''
# Adding nsubj
qecq_4_0_1.command = '''add_edge CL_HEAD -[nsubj]-> WH2 ;'''

# CL_HEAD is a nominal locution without copula or auxiliary
qecq_4_1_1 = cl.Snippet("qecq_4_1_1")
qecq_4_1_1.pattern = '''pattern { CL_HEAD[ExtPos="NOUN"|"PRON"|"PROPN"] }
without { CL_HEAD -[1=cop|aux]-> A }'''
# Adding nsubj
qecq_4_1_1.command = '''add_edge CL_HEAD -[nsubj]-> WH2 ;'''

# CL_HEAD is a nominal group (ExtPos) without copula or auxiliary
qecq_4_2_1 = cl.Snippet("qecq_4_2_1")
qecq_4_2_1.pattern = '''pattern { CL_HEAD[ExtPos="NOUN"|"PRON"|"PROPN"] }
without { CL_HEAD -[1=cop|aux]-> A }'''
# Adding nsubj
qecq_4_2_1.command = '''add_edge CL_HEAD -[nsubj]-> WH2 ;'''

# xcomp'ed verb (heuristics)
qecq_4_3_1 = cl.Snippet("qecq_4_3_1")
qecq_4_3_1.pattern = '''pattern { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }'''
# Addin3 object relation from the xcomp'ed verb
qecq_4_3_1.command = '''add_edge V -[obj]-> WH2 ;'''

# No xcomp'ed verb and not NP
qecq_4_4_1 = cl.Snippet("qecq_4_4_1")
qecq_4_4_1.pattern = '''without { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }
without { CL_HEAD[upos="NOUN"|"PRON"|"PROPN"] }
without { CL_HEAD[ExtPos="NOUN"|"PRON"|"PROPN"] }'''
# Adding object relation from CL_HEAD
qecq_4_4_1.command = '''add_edge CL_HEAD -[obj]-> WH2 ;'''

# No xcomp'ed verb with copula or auxiliary
qecq_4_5_1 = cl.Snippet("qecq_4_5_1")
qecq_4_5_1.pattern = '''pattern { CL_HEAD -[1=cop|aux]-> COP }
without { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }
without { CL_HEAD[ExtPos="NOUN"|"PRON"|"PROPN"] }'''
# Adding object relation from CL_HEAD
qecq_4_5_1.command = '''add_edge CL_HEAD -[obj]-> WH2 ;'''



# Q = qui (subjet)
qecq_3_1_1 = cl.Snippet("qecq_3_1_1")
qecq_3_1_1.pattern = '''pattern { Q[lemma="qui"] }'''
# Adding subject relation
qecq_3_1_1.command = '''add_edge CL_HEAD -[nsubj]-> WH2 ;'''

qecq.add_snippets([qecq_1_0, qecq_1_1, qecq_1_2], qecq_0_0)
qecq.add_snippets([qecq_2_0_1, qecq_2_1_1], qecq_1_1)
qecq.add_snippets([qecq_3_0_1, qecq_3_1_1], qecq_1_1)
layer = [qecq_4_0_1, qecq_4_1_1, qecq_4_2_1, qecq_4_3_1, qecq_4_4_1, qecq_4_5_1]
qecq.add_snippets(layer, qecq_3_0_1)
# Note1: qecq_1_1 fails to capture cases where WH should be
# the objet of the xcomp'ed verb
# Note2: I think that Note1 is not up to date



##### ecq: Reannotating expressions containing "est-ce que/qui" (without "que")

### Root: "est-ce que/qui" trigram
ecq_0_0 = cl.Snippet("ecq_0_0")
ecq_0_0.pattern = '''pattern { E[form="est"|"Est"|"EST"] ; C[form="ce"|"-ce"|"CE"|"-CE"] ;
\tQ[lemma="que"|"qui"] ; E < C ; C < Q }
without { E -[fixed]-> C ; E -[fixed]-> C } % Avoiding looping
without { WH[form="qu'"|"Qu'"|"QU'"] ; WH < E }
without { E -[1=obj]-> C } % ignoring sent. like Le ménage est ce que tu es en train de faire.
without { C -[1=nsubj|expl]-> CE ; CE < E } % ignoring sent. like Le ménage c'est ce que tu es en train de faire.'''
# Copying and replacing E, C, Q as fixed
ecq_0_0.command = '''add_node E2 :< E ; add_node C2 :> E2 ; add_node Q2 :> C2 ;
append_feats E ==> E2 ; E2.ExtPos = "SCONJ" ;
E2.form = E.form ; E2.lemma = E.lemma ; E2.upos = E.upos ;
append_feats C ==> C2 ;
C2.form = C.form ; C2.lemma = C.lemma ; C2.upos = C.upos ;
append_feats Q ==> Q2 ;
Q2.form = Q.form ; Q2.lemma = Q.lemma ; Q2.upos = Q.upos ;
add_edge E2 -[fixed]-> C2 ; add_edge E2 -[fixed]-> Q2 ;'''

ecq = cl.DisjPat("ecq", root=ecq_0_0)


### CL_HEAD is present
ecq_1_0_0 = cl.Snippet("ecq_1_0_0")
# Shifting the head to CL_HEAD
ecq_1_0_0.command = '''shift E ==> CL_HEAD ;
add_edge CL_HEAD -[mark]-> E2 ;'''

# Head is "est"
ecq_2_0_0 = cl.Snippet("ecq_2_0_0")
ecq_2_0_0.pattern = '''pattern { a : ANCHOR -> E ;
\ts : E -[1=nsubj|expl]-> C ;
\td : E -[1=advcl|ccomp]-> CL_HEAD ;
\tm : CL_HEAD -[1=mark|obj|xcomp|nsubj]-> Q }'''

# Head is CL_HEAD
ecq_2_1_0 = cl.Snippet("ecq_2_1_0")
ecq_2_1_0.pattern = '''pattern { c : CL_HEAD -[cop]-> E ;
\ts : CL_HEAD -[1=nsubj|expl]-> C ;
\tm : CL_HEAD -[1=mark|obj|xcomp|nsubj|case]-> Q }'''

# Head is "est" with xcomp("est","que")
ecq_2_2_0 = cl.Snippet("ecq_2_2_0")
ecq_2_2_0.pattern = '''pattern { a : ANCHOR -> E ;
\ts : E -[1=nsubj|expl]-> C ; m : E -[xcomp]-> Q ;
\td : E -[1=advcl|ccomp]-> CL_HEAD }'''


### Alone, i.e. no CL_HEAD
ecq_1_1_3 = cl.Snippet("ecq_1_1_3")

# Head is "que" and alone (eg. reparandum)
ecq_2_0_3 = cl.Snippet("ecq_2_0_3")
ecq_2_0_3.pattern = '''pattern { a : ANCHOR -> Q ;
\ts : Q -[1=nsubj|expl]-> C ; c : Q -[cop]-> E }'''
# Shifting Q (and E) to E2
ecq_2_0_3.command = '''shift Q ==> E2 ; shift E ==> E2 ;'''

# Head is "est" with xcomp("est","que") alone
ecq_2_1_3 = cl.Snippet("ecq_2_1_3")
ecq_2_1_3.pattern = '''pattern { a : ANCHOR -> E ;
\ts : E -[1=nsubj|expl]-> C ; m : E -[xcomp]-> Q }
without { d : E -[1=advcl|ccomp]-> CL_HEAD }'''
# Shifting E to E2
ecq_2_1_3.command = '''shift E ==> E2 ;'''


### Last node for E, C, Q erasure
ecq_3_0 = cl.Snippet("ecq_3_0")
ecq_3_0.command = '''del_node E ; del_node C ; del_node Q ;'''


### Adding edges
ecq.add_snippets([ecq_1_0_0, ecq_1_1_3], ecq_0_0)
ecq.add_snippets([ecq_2_0_0, ecq_2_1_0, ecq_2_2_0], ecq_1_0_0)
ecq.add_snippets([ecq_2_0_3, ecq_2_1_3], ecq_1_1_3)

ecq.add_snippets([ecq_3_0], ecq_0_0)
