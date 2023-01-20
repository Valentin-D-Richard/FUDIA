import classes as cl

##### relprontype: Annotating some additional PronType=Rel
# By listing a reasonable number of relations between CL_HEAD and WH

# Root
relprontype_0_0 = cl.Snippet("relprontype")
relprontype_0_0.pattern = '''pattern {
\tWH[lemma="qui"|"que"|"quoi"|"où"|"lequel",!PronType] ;
\tANCHOR -[acl:relcl|advcl:cleft]-> CL_HEAD ; WH << CL_HEAD ; ANCHOR << WH }'''
# Adding PronType="Rel"
relprontype_0_0.command = '''WH.PronType="Rel"'''

relprontype = cl.DisjPat("relprontype", root=relprontype_0_0)

# Direct relation (1 intermediary)
relprontype_1_0 = cl.Snippet("relprontype_1_0")
relprontype_1_0.pattern = '''pattern { CL_HEAD -> WH }'''

# 2 intermediaries
relprontype_1_1 = cl.Snippet("relprontype_1_1")
relprontype_1_1.pattern = '''pattern { CL_HEAD -> I  ; I -> WH ; ANCHOR << I }'''

# 3 intermediaries with I1 << I2
relprontype_1_2 = cl.Snippet("relprontype_1_2")
relprontype_1_2.pattern = '''pattern { CL_HEAD -> I1 ; I1 -> I2 ;
\tI2 -> WH ; ANCHOR << I1 ; ANCHOR << I2 ;
\tI1 << I2 }'''

# 3 intermediaries with I2 << CL_HEAD and CL_HEAD << I1
relprontype_1_3 = cl.Snippet("relprontype_1_3")
relprontype_1_3.pattern = '''pattern { CL_HEAD -> I1 ; I1 -> I2 ;
\tI2 -> WH ; ANCHOR << I1 ; ANCHOR << I2 ;
\tI2 << CL_HEAD ; CL_HEAD << I1 }'''


layer = [relprontype_1_0, relprontype_1_1, relprontype_1_2, relprontype_1_3]
relprontype.add_snippets(layer, relprontype_0_0)



##### intprontype: Annotating all missed PronType="Int"

# Root
intprontype_0_0 = cl.Snippet("intprontype_0_0")
intprontype_0_0.pattern = '''pattern {
\tWH[lemma="qui"|"que"|"quoi"|"comment"|"où"|"quand"|"combien"|"pourquoi"|"lequel"|"quel",!PronType]}'''
# Adding PronType="Int"
intprontype_0_0.command = '''WH.PronType="Int"'''


intprontype = cl.DisjPat("intprontype", root=intprontype_0_0)


# quel
intprontype_1_0 = cl.Snippet("intprontype_1_0")
intprontype_1_0.pattern = '''pattern {
\tWH [lemma="quel",upos="ADJ"|"DET"|"PRON"] }
\twithout { Q [lemma="que"] ; WH < Q }
\twithout { A [form="n'"] ; B[form="importe"] ; A < B ; B < WH }
\twithout { T[lemma="tel"] ; T < WH }
\twithout { E[lemma="!"] }'''

# Only-interrogative adverbs: comment & combien
intprontype_1_1 = cl.Snippet("intprontype_1_1")
intprontype_1_1.pattern = '''pattern {
\tWH[lemma="comment"|"combien", upos="ADV"]}'''

# pourquoi
intprontype_1_2 = cl.Snippet("intprontype_1_2")
intprontype_1_2.pattern = '''pattern { WH[lemma="pourquoi", upos="ADV"]}
without { C[lemma="ce"] ; E[lemma="être"] ; C < E ; E < WH } % not "c'est pourquoi"
without { C[lemma="ce"] ; C < WH } % not "ce pourquoi"'''

# quand
intprontype_1_3 = cl.Snippet("intprontype_1_3")
intprontype_1_3.pattern = '''pattern { WH[lemma="quand", upos="ADV"]}
without { M[lemma="même"] ; WH < M } % not "quand même"
without { B[lemma="bien"] ; M[lemma="même"] ; WH < B ; B < M } % not "quand bien même"
without { G -[mark]-> WH } %% bad annotation of "quand" which should be SCONJ'''

# où
intprontype_1_4 = cl.Snippet("intprontype_1_4")
intprontype_1_4.pattern = '''pattern { WH[lemma="où", upos="ADV"]}
without { WH -[ccomp]-> V } % badly annotated relative clause'''

# lequel and related
intprontype_1_5 = cl.Snippet("intprontype_1_5")
intprontype_1_5.pattern = '''pattern { WH[lemma="lequel", upos="PRON"]}'''

# que, qui and quoi
intprontype_1_6 = cl.Snippet("intprontype_1_6")
intprontype_1_6.pattern = '''pattern {
\tWH[lemma="qui"|"que"|"quoi", upos="PRON"]}
without { C[lemma="ce"] ; WH[lemma="que"] ; C < WH } % no "ce que"
without { G -[discourse]-> WH ; WH[lemma="quoi"] } % no interjection "quoi" (should be INTJ)
without { N1[lemma="en"]; N2[lemma="ce"]; N3[form="concerne"];
\tN1 < N2; N2 < WH; WH < N3 } % no "en ce qui concerne"
without { E[lemma="!"] } % Not exclamative'''
# without { N1[lemma="que"]; N2[lemma="ce"]; N3[form="soit"];
# \tWH < N1 ; N1 < N2; N2 < N3; } % no "qui/quoi que ce soit"


layer =  [intprontype_1_0, intprontype_1_1, intprontype_1_2, intprontype_1_3]
layer += [intprontype_1_4, intprontype_1_5, intprontype_1_6]
intprontype.add_snippets(layer, intprontype_0_0)