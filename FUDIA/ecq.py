import classes as cl

##### qecq: Reannotating expressions containing "qu'est-ce que/qui"

### Root
qecq_0_0 = cl.Snippet("qecq_0_0")
qecq_0_0.request = '''pattern { WH[lemma="que"] ; E[form="est"|"EST"] ;
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

qecq = cl.DisjRule("qecq", root=qecq_0_0)


# Special case of "qu'est-ce que c'est"
qecq_1_0 = cl.Snippet("qecq_1_0")
qecq_1_0.request = '''pattern { CE [lemma="ce"]; COP [lemma="être"];
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
qecq_1_2.request = '''without { CE [lemma="ce"]; COP [lemma="être"];
\tQ < CE ; CE < COP }
without { WH -[1=advcl|dislocated]-> CL_HEAD }
without { E -[1=advcl|dislocated]-> CL_HEAD }'''
# Nothing to add


# "qu'est-ce que S'" with head on qu'
qecq_2_0_1 = cl.Snippet("qecq_2_0_1")
qecq_2_0_1.request = '''pattern { h: WH -[1=advcl|dislocated|ccomp]-> CL_HEAD ;
\tWH << CL_HEAD }'''
# Deleting h and shifting WH2 to CL_HEAD (except fixed)
qecq_2_0_1.command = '''shift WH2 =[^fixed]=> CL_HEAD ;'''

# "qu'est-ce que S'" with head on est
qecq_2_1_1 = cl.Snippet("qecq_2_1_1")
qecq_2_1_1.request = '''pattern { h: E -[1=advcl|dislocated|ccomp]-> CL_HEAD ;
\tWH << CL_HEAD }'''
# Shifting the head from qu' to the head of S'
qecq_2_1_1.command = '''shift E2 ==> CL_HEAD ;'''


# Q = que (objet)
qecq_3_0_1 = cl.Snippet("qecq_3_0_1")
qecq_3_0_1.request = '''pattern { Q[lemma="que"] }'''


# CL_HEAD is a nominal phrase without copula or auxiliary
qecq_4_0_1 = cl.Snippet("qecq_4_0_1")
qecq_4_0_1.request = '''pattern { CL_HEAD[upos="NOUN"|"PRON"|"PROPN",!ExtPos] }
without { CL_HEAD -[1=cop|aux]-> A }'''
# Adding nsubj
qecq_4_0_1.command = '''add_edge CL_HEAD -[nsubj]-> WH2 ;'''

# CL_HEAD is a nominal locution without copula or auxiliary
qecq_4_1_1 = cl.Snippet("qecq_4_1_1")
qecq_4_1_1.request = '''pattern { CL_HEAD[ExtPos="NOUN"|"PRON"|"PROPN"] }
without { CL_HEAD -[1=cop|aux]-> A }'''
# Adding nsubj
qecq_4_1_1.command = '''add_edge CL_HEAD -[nsubj]-> WH2 ;'''

# xcomp'ed verb (heuristics)
qecq_4_3_1 = cl.Snippet("qecq_4_3_1")
qecq_4_3_1.request = '''pattern { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }'''
# Addin3 object relation from the xcomp'ed verb
qecq_4_3_1.command = '''add_edge V -[obj]-> WH2 ;'''

# No xcomp'ed verb and not NP
qecq_4_4_1 = cl.Snippet("qecq_4_4_1")
qecq_4_4_1.request = '''without { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }
without { CL_HEAD[upos="NOUN"|"PRON"|"PROPN"] }
without { CL_HEAD[ExtPos="NOUN"|"PRON"|"PROPN"] }
without { CL_HEAD -[mark]-> M ; M[upos="SCONJ",!ExtPos] ; h.label = advcl }
without { CL_HEAD -[mark]-> M ; M[ExtPos="SCONJ"] ; h.label = advcl } % real advcl'''
# Adding object relation from CL_HEAD
qecq_4_4_1.command = '''add_edge CL_HEAD -[obj]-> WH2 ;'''

# No xcomp'ed verb with copula or auxiliary
qecq_4_5_1 = cl.Snippet("qecq_4_5_1")
qecq_4_5_1.request = '''pattern { CL_HEAD -[1=cop|aux]-> COP }
without { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }'''
# Adding object relation from CL_HEAD
qecq_4_5_1.command = '''add_edge CL_HEAD -[obj]-> WH2 ;'''



# Q = qui (subjet)
qecq_3_1_1 = cl.Snippet("qecq_3_1_1")
qecq_3_1_1.request = '''pattern { Q[lemma="qui"] }'''
# Adding subject relation
qecq_3_1_1.command = '''add_edge CL_HEAD -[nsubj]-> WH2 ;'''

qecq.add_snippets([qecq_1_0, qecq_1_1, qecq_1_2], qecq_0_0)
qecq.add_snippets([qecq_2_0_1, qecq_2_1_1], qecq_1_1)
qecq.add_snippets([qecq_3_0_1, qecq_3_1_1], qecq_1_1)
layer = [qecq_4_0_1, qecq_4_1_1, qecq_4_3_1, qecq_4_4_1, qecq_4_5_1]
qecq.add_snippets(layer, qecq_3_0_1)




##### qec: Reannotating expression "qu'est-ce + S"

### Root, supposing it is object
qec_0_0 = cl.Snippet("qec_0_0")
qec_0_0.request = '''pattern { WH[lemma="que"] ; E[form="est"|"EST"] ;
\tC[form="ce"|"-ce"|"CE"|"-CE"] ; WH < E ; E < C }
without { Q[lemma="que"|"qui"] ; C < Q }
without { WH -[fixed]-> E ; WH -[fixed]-> C } % Avoiding looping'''
# Rearranging by getting the expression as fixed
qec_0_0.command = '''add_node WH2 :< WH ; add_node E2 :> WH ;
add_node C2 :> E2 ; add_node Q2 :> C2 ;
append_feats WH ==> WH2 ; shift WH ==> WH2 ; WH2.ExtPos = "PRON" ;
shift E ==> E2 ;
WH2.form = WH.form ; WH2.lemma = WH.lemma ; WH2.upos = WH.upos ;
append_feats E ==> E2 ;
E2.form = E.form ; E2.lemma = E.lemma ; E2.upos = E.upos ;
append_feats C ==> C2 ;
C2.form = C.form ; C2.lemma = C.lemma ; C2.upos = C.upos ;
add_edge WH2 -[fixed]-> E2 ; add_edge WH2 -[fixed]-> C2 ;
del_node WH ; del_node E ; del_node C ;'''

qec = cl.DisjRule("qec", root=qec_0_0)


# "qu'est-ce que S'" with head on qu'
qec_1_0 = cl.Snippet("qec_1_0")
qec_1_0.request = '''pattern { h: WH -[1=advcl|dislocated|ccomp]-> CL_HEAD ;
\tWH << CL_HEAD }'''
# Deleting h and shifting WH2 to CL_HEAD (except fixed)
qec_1_0.command = '''shift WH2 =[^fixed]=> CL_HEAD ;'''

# "qu'est-ce que S'" with head on est
qec_1_1 = cl.Snippet("qec_1_1")
qec_1_1.request = '''pattern { h: E -[1=advcl|dislocated|ccomp]-> CL_HEAD ;
\tWH << CL_HEAD }'''
# Shifting the head from qu' to the head of S'
qec_1_1.command = '''shift E2 ==> CL_HEAD ;'''


# xcomp'ed verb (heuristics)
qec_2_0 = cl.Snippet("qec_2_0")
qec_2_0.request = '''pattern { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }'''
# Addin3 object relation from the xcomp'ed verb
qec_2_0.command = '''add_edge V -[obj]-> WH2 ;'''

# No xcomp'ed verb and not NP
qec_2_1 = cl.Snippet("qec_2_1")
qec_2_1.request = '''without { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }
without { CL_HEAD[upos="NOUN"|"PRON"|"PROPN"] }
without { CL_HEAD[ExtPos="NOUN"|"PRON"|"PROPN"] }'''
# Adding object relation from CL_HEAD
qec_2_1.command = '''add_edge CL_HEAD -[obj]-> WH2 ;'''

# No xcomp'ed verb with copula or auxiliary
qec_2_2 = cl.Snippet("qec_2_2")
qec_2_2.request = '''pattern { CL_HEAD -[1=cop|aux]-> COP }
without { CL_HEAD -[xcomp]-> V ; V[upos="VERB"|"AUX"] }'''
# Adding object relation from CL_HEAD
qec_2_2.command = '''add_edge CL_HEAD -[obj]-> WH2 ;'''

qec.add_snippets([qec_1_0, qec_1_1], qec_0_0)
layer = [qec_2_0, qec_2_1, qec_2_2]
qec.add_snippets(layer, qec_0_0)




##### ecq: Reannotating expressions containing "est-ce que/qui" (without "que")

### Root: "est-ce que/qui" trigram
ecq_0_0 = cl.Snippet("ecq_0_0")
ecq_0_0.request = '''pattern { E[form="est"|"Est"|"EST"] ; C[form="ce"|"-ce"|"CE"|"-CE"] ;
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

ecq = cl.DisjRule("ecq", root=ecq_0_0)


### CL_HEAD is present
ecq_1_0_0 = cl.Snippet("ecq_1_0_0")
# Shifting the head to CL_HEAD
ecq_1_0_0.command = '''shift E ==> CL_HEAD ;
add_edge CL_HEAD -[mark]-> E2 ;'''

# Head is "est"
ecq_2_0_0 = cl.Snippet("ecq_2_0_0")
ecq_2_0_0.request = '''pattern { a : ANCHOR -> E ;
\ts : E -[1=nsubj|expl]-> C ;
\td : E -[1=advcl|ccomp]-> CL_HEAD ;
\tm : CL_HEAD -[1=mark|obj|xcomp|nsubj]-> Q }'''

# Head is CL_HEAD
ecq_2_1_0 = cl.Snippet("ecq_2_1_0")
ecq_2_1_0.request = '''pattern { c : CL_HEAD -[cop]-> E ;
\ts : CL_HEAD -[1=nsubj|expl]-> C ;
\tm : CL_HEAD -[1=mark|obj|xcomp|nsubj|case]-> Q }'''

# Head is "est" with xcomp("est","que")
ecq_2_2_0 = cl.Snippet("ecq_2_2_0")
ecq_2_2_0.request = '''pattern { a : ANCHOR -> E ;
\ts : E -[1=nsubj|expl]-> C ; m : E -[xcomp]-> Q ;
\td : E -[1=advcl|ccomp]-> CL_HEAD }'''


### Alone, i.e. no CL_HEAD
ecq_1_1_3 = cl.Snippet("ecq_1_1_3")

# Head is "que" and alone (eg. reparandum)
ecq_2_0_3 = cl.Snippet("ecq_2_0_3")
ecq_2_0_3.request = '''pattern { a : ANCHOR -> Q ;
\ts : Q -[1=nsubj|expl]-> C ; c : Q -[cop]-> E }'''
# Shifting Q (and E) to E2
ecq_2_0_3.command = '''shift Q ==> E2 ; shift E ==> E2 ;'''

# Head is "est" with xcomp("est","que") alone
ecq_2_1_3 = cl.Snippet("ecq_2_1_3")
ecq_2_1_3.request = '''pattern { a : ANCHOR -> E ;
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
