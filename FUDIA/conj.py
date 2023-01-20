import classes as cl

##### conj: Adding coordinated WH phrases

conj_0_0 = cl.Snippet("conj_0_0")
conj_0_0.pattern = '''pattern { P1 -[conj]-> P2 ; C[IntClause="Yes"] }'''

conj = cl.DisjPat("conj", root = conj_0_0)

conj_1_0 = cl.Snippet("conj_1_0") # P1 is WH1
conj_1_0.pattern = '''pattern { P1[IntPhrase="Yes",PronType="Int"] ;
\tC -[cue:wh]-> P1 }'''

conj_1_1 = cl.Snippet("conj_1_1") # P1 is not WH1
conj_1_1.pattern = '''pattern { P1[IntPhrase="Yes"] ;
\tP1 -[cue:wh]-> WH1 ; C -[cue:wh]-> WH1 }'''


conj_2_0 = cl.Snippet("conj_2_0") # P2 is WH2
conj_2_0.pattern = '''pattern { P2[PronType="Int"] }
without { C -[cue:wh]-> P2 }'''
conj_2_0.command = '''add_edge C -[cue:wh]-> P2'''

conj_2_1 = cl.Snippet("conj_2_1") # P2 is not WH2
conj_2_1.pattern = '''pattern { P2[IntPhrase="Yes"] ; P2 -[cue:wh]-> WH2 }
without { C -[cue:wh]-> WH2 }'''
conj_2_1.command = '''add_edge C -[cue:wh]-> WH2'''


conj.add_snippets([conj_1_0, conj_1_1], conj_0_0)
conj.add_snippets([conj_2_0, conj_2_1], conj_0_0)


##### conjc: Distributing WH phrase over conjuncted sentences

# conjc_0_0 = cl.Snippet("conjc_0_0")
# conjc_0_0.pattern = '''pattern {C1[IntClause="Yes"] ;
# \tC2[IntClause="Yes"] ; C1 -[conj]-> C2 ;
# \tC1 -[cue:wh]-> WH}
# without { C2 -[cue:wh]-> WH }
# without { C2 -[cue:wh]-> WH2 } % C2 not already having a '''
# conjc_0_0.command = '''add_edge C2 -[cue:wh]-> WH'''

# conjc = cl.DisjPat("conjc", root = conjc_0_0)