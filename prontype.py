import classes as cl

##### relprontype: Annotating some additional PronType=Rel

# Root
relprontype_0_0 = cl.Snippet("relprontype")
relprontype_0_0.request = '''pattern {
\tWH[lemma="qui"|"que"|"quoi"|"où"|"lequel",!PronType] }'''
# Adding PronType="Rel"
relprontype_0_0.command = '''WH.PronType="Rel"'''

relprontype = cl.DisjRule("relprontype", root=relprontype_0_0)

# Pronouns
relprontype_1_0 = cl.Snippet("relprontype_1_0")
relprontype_1_0.request = '''pattern { WH[lemma="qui"|"que"|"quoi"|"lequel", upos="PRON"] }'''

# Adverb
relprontype_1_1 = cl.Snippet("relprontype_1_1")
relprontype_1_1.request = '''pattern { WH[lemma="où", upos="ADV"|"PRON"] }'''

# Adjective
relprontype_1_2 = cl.Snippet("relprontype_1_2")
relprontype_1_2.request = '''pattern { WH[lemma="lequel", upos="ADJ"] }'''


# Listing a reasonable number of relations between CL_HEAD
relprontype_2_0 = cl.Snippet("relprontype_2_0")

# In a relative clause: fronted WH
relprontype_3_0 = cl.Snippet("relprontype_3_0")
relprontype_3_0.request = '''pattern { WH << CL_HEAD ;
\tANCHOR -[acl:relcl|advcl:cleft]-> CL_HEAD ; ANCHOR << WH }'''

# Conj of a relative clause
relprontype_3_1 = cl.Snippet("relprontype_3_1")
relprontype_3_1.request = '''pattern { C -[conj]-> CL_HEAD ; ANCHOR << C ;
\tANCHOR -[acl:relcl|advcl:cleft]-> C ; ANCHOR << WH ; ANCHOR << CL_HEAD }'''

# Direct relation (1 intermediary)
relprontype_4_0 = cl.Snippet("relprontype_4_0")
relprontype_4_0.request = '''pattern { CL_HEAD -> WH }'''

# 2 intermediaries
relprontype_4_1 = cl.Snippet("relprontype_4_1")
relprontype_4_1.request = '''pattern { CL_HEAD -> I  ; I -> WH ; ANCHOR << I }'''

# 3 intermediaries with I1 << I2
relprontype_4_2 = cl.Snippet("relprontype_4_2")
relprontype_4_2.request = '''pattern { CL_HEAD -> I1 ; I1 -> I2 ;
\tI2 -> WH ; ANCHOR << I1 ; ANCHOR << I2 ;
\tI1 << I2 }'''

# 3 intermediaries with I2 << CL_HEAD and CL_HEAD << I1
relprontype_4_3 = cl.Snippet("relprontype_4_3")
relprontype_4_3.request = '''pattern { CL_HEAD -> I1 ; I1 -> I2 ;
\tI2 -> WH ; ANCHOR << I1 ; ANCHOR << I2 ;
\tI2 << CL_HEAD ; CL_HEAD << I1 }'''


# Reparandum of a PronType="Rel"
relprontype_2_1 = cl.Snippet("reprontype_2_1")
relprontype_2_1.request = '''pattern { N -[reparandum]-> WH ; N[PronType="Rel"] }'''

relprontype.add_snippets([relprontype_1_0, relprontype_1_1, relprontype_1_2], relprontype_0_0)
relprontype.add_snippets([relprontype_2_0, relprontype_2_1], relprontype_0_0)
relprontype.add_snippets([relprontype_3_0, relprontype_3_1], relprontype_2_0)
layer = [relprontype_4_0, relprontype_4_1, relprontype_4_2, relprontype_4_3]
relprontype.add_snippets(layer, relprontype_2_0)



##### intprontype: Annotating all missed PronType="Int"

# Root
intprontype_0_0 = cl.Snippet("intprontype_0_0")
intprontype_0_0.request = '''pattern {
\tWH[lemma="qui"|"que"|"quoi"|"comment"|"où"|"quand"|"combien"|"pourquoi"|"lequel"|"quel"|"quid"]}
without { ANCHOR -[reparandum]-> WH ; ANCHOR[PronType<>"Int"] }
without { ANCHOR -[reparandum]-> WH ; ANCHOR[!PronType] }
without { ANCHOR -[dep]-> WH } % uncomplete constructions
without { ANCHOR -[reparandum]-> N ; N -> WH }'''
# with reparandum, we cannot be sure, or there are too many possible cases
# Adding PronType="Int"
intprontype_0_0.command = '''WH.PronType="Int"'''


intprontype = cl.DisjRule("intprontype", root=intprontype_0_0)


# no PronType
intprontype_1_0 = cl.Snippet("intprontype_1_0")
intprontype_1_0.request = '''pattern {WH[!PronType]}'''

# PronType=Rel, but followed by "est-ce que/qui"
intprontype_1_1 = cl.Snippet("intprontype_1_1")
intprontype_1_1.request = '''pattern {WH[PronType="Rel"] ;
\tXE[lemma="être"] ; XC[lemma="ce"] ; XQ[lemma="que"|"qui"] ;
\tWH < XE ; XE < XC ; XC < XQ}'''


# quel
intprontype_2_0 = cl.Snippet("intprontype_2_0")
intprontype_2_0.request = '''pattern {
\tWH [lemma="quel",upos="ADJ"|"DET"|"PRON"] }
\twithout { Q [lemma="que"] ; WH < Q }
\twithout { A [lemma="ne"] ; B[form="importe"|"IMPORTE"] ; A < B ; B < WH }
\twithout { T[lemma="tel"] ; T < WH }
\twithout { E[lemma="!"] }'''

# Only-interrogative adverbs: comment,  combien & quid (if not exclamative)
intprontype_2_1 = cl.Snippet("intprontype_2_1")
intprontype_2_1.request = '''pattern {
\tWH[lemma="comment"|"combien"|"quid", upos="ADV"]}'''

# pourquoi
intprontype_2_2 = cl.Snippet("intprontype_2_2")
intprontype_2_2.request = '''pattern { WH[lemma="pourquoi", upos="ADV"]}
without { C[lemma="ce"] ; E[lemma="être"] ; C < E ; E < WH } % not "c'est pourquoi"
without { C[lemma="ce"] ; C < WH } % not "ce pourquoi"'''

# quand
intprontype_2_3 = cl.Snippet("intprontype_2_3")
intprontype_2_3.request = '''pattern { WH[lemma="quand", upos="ADV"]}
without { M[lemma="même"] ; WH < M } % not "quand même"
without { B[lemma="bien"] ; M[lemma="même"] ; WH < B ; B < M } % not "quand bien même"
without { G -[mark]-> WH } %% bad annotation of "quand" which should be SCONJ'''

# où
intprontype_2_4 = cl.Snippet("intprontype_2_4")
intprontype_2_4.request = '''pattern { WH[lemma="où", upos="ADV"|"PRON"]}
without { WH -[ccomp]-> V } % badly annotated relative clause'''

# lequel and related
intprontype_2_5 = cl.Snippet("intprontype_2_5")
intprontype_2_5.request = '''pattern { WH[lemma="lequel", upos="PRON"]}'''

# que, qui and quoi
intprontype_2_6 = cl.Snippet("intprontype_2_6")
intprontype_2_6.request = '''pattern {
\tWH[lemma="qui"|"que"|"quoi", upos="PRON"] }
without { C[lemma="ce"] ; WH[lemma="que"] ; C < WH } % no "ce que"
without { G -[discourse]-> WH ; WH[lemma="quoi"] } % no interjection "quoi" (should be INTJ)
without { N1[lemma="en"]; N2[lemma="ce"]; N3[form="concerne"|"CONCERNE"] ;
\tN1 < N2; N2 < WH; WH < N3 } % no "en ce qui concerne"
without { E[lemma="!"] } % Not exclamative'''
# without { N1[lemma="que"]; N2[lemma="ce"]; N3[form="soit"];
# \tWH < N1 ; N1 < N2; N2 < N3; } % no "qui/quoi que ce soit"

# Reparadum of a PronType="Int"
intprontype_2_7 = cl.Snippet("intprontype_2_7")
intprontype_2_7.request = '''pattern { ANCHOR -[reparandum]-> WH ;
\tANCHOR[PronType="Int"] }'''


intprontype.add_snippets([intprontype_1_0, intprontype_1_1], intprontype_0_0)

layer =  [intprontype_2_0, intprontype_2_1, intprontype_2_2, intprontype_2_3]
layer += [intprontype_2_4, intprontype_2_5, intprontype_2_6, intprontype_2_7]
intprontype.add_snippets(layer, intprontype_0_0)