import classes as cl

### telquel: reannotating tel quel as fixed adjective

# Root
telquel_0_0 = cl.Snippet("telquel_0_0")
telquel_0_0.pattern = '''pattern { T[lemma="tel"] ; Q[lemma="quel"] ;
\tT < Q }
without { T -[fixed]-> Q } % no loop'''
# Recreating fixed nodes
telquel_0_0.command = '''add_node T2 :< T ; add_node Q2 :< Q ; 
append_feats T ==> T2 ;
T2.form = T.form ; T2.lemma = T.lemma ; T2.upos = "ADJ" ;
append_feats Q ==> Q2 ;
Q2.form = Q.form ; Q2.lemma = Q.lemma ; Q2.upos = "ADJ" ;
shift Q ==> T2 ; shift T ==> T2 ;
T2.ExtPos = "ADJ" ; add_edge T2 -[fixed]-> Q2 ;
del_node T ; del_node Q'''

telquel = cl.DisjPat("telquel", root=telquel_0_0)



### nimporte: reannotating n'importe + WH ad fixed DET, PRON or ADV

# Root
nimporte_0_0 = cl.Snippet("nimporte_0_0")
nimporte_0_0.pattern = '''pattern { N[lemma="ne"] ; I[form="importe"] ;
\tWH[lemma="qui"|"quoi"|"quel"|"où"|"quand"|"comment"|"lequel"] ;
\tN < I ; I < WH }
without { N -[fixed]-> I ;  N -[fixed]-> WH } % no loop'''
# Recreating fixed nodes
nimporte_0_0.command = '''add_node N2 :< N ; add_node I2 :< I ;
add_node WH2 :< WH ;
append_feats N ==> N2 ;
N2.form = N.form ; N2.lemma = N.lemma ; N2.upos = N.upos ;
append_feats I ==> I2 ;
I2.form = I.form ; I2.lemma = I.lemma ; I2.upos = I.upos ;
append_feats WH ==> WH2 ;
WH2.form = WH.form ; WH2.lemma = WH.lemma ; WH2.upos = WH.upos ;
shift N ==> N2 ; shift I ==> N2 ; shift WH ==> N2 ;
add_edge N2 -[fixed]-> I2 ; add_edge N2 -[fixed]-> WH2 ;
del_node N ; del_node I ; del_node WH ;'''

nimporte = cl.DisjPat("nimporte", root=nimporte_0_0)

# Note: edges recognized in the pattern are not shifted by shift command


#  WH is quoi, lequel or qui
nimporte_1_0 = cl.Snippet("nimporte_1_0")
nimporte_1_0.pattern = '''pattern  { WH[lemma="quoi"|"qui"|"lequel"] }'''
# Adding ExtPos PRON
nimporte_1_0.command = '''N2.ExtPos = "PRON" ;'''

#  WH is quel
nimporte_1_1_3 = cl.Snippet("nimporte_1_1_3")
nimporte_1_1_3.pattern = '''pattern  { WH[lemma="quel"] ;
\tI -[1=nsubj|obj]-> S }'''
# Adding ExtPos DET
nimporte_1_1_3.command = '''N2.ExtPos = "DET" ;
del_edge N2 -[obj]-> S ; del_edge S -[nsubj]-> N2 ; shift N2 =[^fixed]=> S ;
add_edge S -[det]-> N2 ;'''

#  WH is an adverb
nimporte_1_2_5 = cl.Snippet("nimporte_1_2_5")
nimporte_1_2_5.pattern = '''pattern  { WH[lemma="quand"|"où"|"comment"] }'''
# Adding ExtPos PRON
nimporte_1_2_5.command = '''N2.ExtPos = "ADV" ;'''


# No regular anchor (complement case)
nimporte_2_0 = cl.Snippet("nimporte_2_0")
nimporte_2_0.pattern = '''without { ANCHOR -[1=advcl|ccomp|parataxis|csubj]-> I }'''

# PRON + Anchor relation to object NP 
nimporte_2_1 = cl.Snippet("nimporte_2_1")
nimporte_2_1.pattern = '''pattern { ANCHOR -[1=advcl|ccomp|parataxis]-> I }
without { I -[case|mark]-> C }'''
# Replacing by obj
nimporte_2_1.command = '''add_edge ANCHOR -[obj]-> N2'''

# PRON + Anchor relation to PP
nimporte_2_2 = cl.Snippet("nimporte_2_2")
nimporte_2_2.pattern = '''pattern { ANCHOR -[1=advcl|ccomp|parataxis]-> I ;
\tI -[case|mark]-> C ; C[upos="ADP"] }'''
# Replacing by obl
nimporte_2_2.command = '''add_edge ANCHOR -[obl]-> N2 ;
add_edge N2 -[case]-> C'''

# PRON + Anchor relation to PP (prep locution)
nimporte_2_3 = cl.Snippet("nimporte_2_3")
nimporte_2_3.pattern = '''pattern { ANCHOR -[1=advcl|ccomp|parataxis]-> I ;
\tI -[case|mark]-> C ; C[ExtPos="ADP"] }'''
# Replacing by obl
nimporte_2_3.command = '''add_edge ANCHOR -[obl]-> N2 ;
add_edge N2 -[case]-> C'''

# PRON + Anchor relation to subject NP
nimporte_2_4 = cl.Snippet("nimporte_2_4")
nimporte_2_4.pattern = '''pattern { ANCHOR -[1=csubj]-> I }'''
# Replacing by obl
nimporte_2_4.command = '''add_edge ANCHOR -[nsubj]-> N2 '''


# DET + Anchor relation to object NP 
nimporte_2_1_3 = cl.Snippet("nimporte_2_1_3")
nimporte_2_1_3.pattern = '''pattern { ANCHOR -[1=advcl|ccomp|parataxis]-> I }
without { I -[case|mark]-> C }'''
# Replacing by obj
nimporte_2_1_3.command = '''add_edge ANCHOR -[obj]-> S'''

# DET + Anchor relation to PP
nimporte_2_2_3 = cl.Snippet("nimporte_2_2_3")
nimporte_2_2_3.pattern = '''pattern { ANCHOR -[1=advcl|ccomp|parataxis]-> I ;
\tI -[case|mark]-> C ; C[upos="ADP"] }'''
# Replacing by obl
nimporte_2_2_3.command = '''add_edge ANCHOR -[obl]-> S ;
add_edge S -[case]-> C'''

# DET + Anchor relation to PP
nimporte_2_3_3 = cl.Snippet("nimporte_2_3_3")
nimporte_2_3_3.pattern = '''pattern { ANCHOR -[1=advcl|ccomp|parataxis]-> I ;
\tI -[case|mark]-> C ; C[upos="ADP"] }'''
# Replacing by obl
nimporte_2_3_3.command = '''add_edge ANCHOR -[obl]-> S ;
add_edge S -[case]-> C'''

# DET + Anchor relation to object NP 
nimporte_2_4_3 = cl.Snippet("nimporte_2_4_3")
nimporte_2_4_3.pattern = '''pattern { ANCHOR -[1=csubj]-> I }'''
# Replacing by obj
nimporte_2_4_3.command = '''add_edge ANCHOR -[nsubj]-> S'''


# Anchor relation to ADV
nimporte_2_1_5 = cl.Snippet("nimporte_2_1_5")
nimporte_2_1_5.pattern = '''pattern { ANCHOR -[1=advcl|ccomp|parataxis]-> I ;
\tWH[lemma="quand"|"où"|"comment"] }'''
# Replacing by obj
nimporte_2_1_5.command = '''add_edge ANCHOR -[advmod]-> N2'''


layer = [nimporte_1_0, nimporte_1_1_3, nimporte_1_2_5]
nimporte.add_snippets(layer, nimporte_0_0)
layer1 = [nimporte_2_0, nimporte_2_1, nimporte_2_2, nimporte_2_3, nimporte_2_4]
nimporte.add_snippets(layer1, nimporte_1_0)
layer2 = [nimporte_2_0, nimporte_2_1_3, nimporte_2_2_3, nimporte_2_4_3]
nimporte.add_snippets(layer2, nimporte_1_1_3)
nimporte.add_snippets([nimporte_2_0, nimporte_2_1_5], nimporte_1_2_5)


### whque: adding PronType=Rel to WH + que + S[Mood=Sub]

whque_0_0 = cl.Snippet("whque_0_0")
whque_0_0.pattern = '''pattern {
\tWH[lemma="quel"|"qui"|"quoi"|"lequel"|"où"|"quand",!PronType] ;
\tQ[lemma="que"] ; WH < Q ; Q << S ; S[Mood="Sub"] }'''
# Adding PronType = Rel
whque_0_0.command = '''WH.PronType = "Rel"'''

whque = cl.DisjPat("whque", root=whque_0_0)

# # WH + que + ce
# whque_1_0 = cl.Snippet("whque_1_0")
# whque_1_0.pattern = '''pattern { C[lemma="ce"] ; Q < C }'''

# # Quel + que
# whque_1_1 = cl.Snippet("whque_1_1")
# whque_1_1.pattern = '''pattern { WH[lemma="quel"] }'''

# whque.add_snippets([whque_1_0, whque_1_1], whque_0_0)