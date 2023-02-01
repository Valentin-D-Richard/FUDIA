import classes as cl

##### conj: Adding coordinated WH phrases

conj_0_0 = cl.Snippet("conj_0_0")
conj_0_0.request = '''pattern { P1 -[conj]-> P2 ; CL_HEAD[IntClause="Yes"] }'''

conj = cl.DisjRule("conj", root = conj_0_0)

conj_1_0 = cl.Snippet("conj_1_0") # P1 is WH1
conj_1_0.request = '''pattern { P1[IntPhrase="Yes",PronType="Int"] ;
\tCL_HEAD -[cue:wh]-> P1 }'''

conj_1_1 = cl.Snippet("conj_1_1") # P1 is not WH1
conj_1_1.request = '''pattern { P1[IntPhrase="Yes"] ;
\tP1 -[cue:wh]-> WH1 ; CL_HEAD -[cue:wh]-> WH1 }'''


conj_2_0 = cl.Snippet("conj_2_0") # P2 is WH2
conj_2_0.request = '''pattern { P2[PronType="Int"] }
without { CL_HEAD -[cue:wh]-> P2 }'''
conj_2_0.command = '''add_edge CL_HEAD -[cue:wh]-> P2'''

conj_2_1 = cl.Snippet("conj_2_1") # P2 is not WH2
conj_2_1.request = '''pattern { P2[IntPhrase="Yes"] ; P2 -[cue:wh]-> WH2 }
without { CL_HEAD -[cue:wh]-> WH2 }'''
conj_2_1.command = '''add_edge CL_HEAD -[cue:wh]-> WH2'''


conj.add_snippets([conj_1_0, conj_1_1], conj_0_0)
conj.add_snippets([conj_2_0, conj_2_1], conj_0_0)



##### conjc: Distributing WH phrase over conjuncted sentences

# conjc_0_0 = cl.Snippet("conjc_0_0")
# conjc_0_0.request = '''pattern {C1[IntClause="Yes"] ;
# \tC2[IntClause="Yes"] ; C1 -[conj]-> C2 ;
# \tC1 -[cue:wh]-> WH}
# without { C2 -[cue:wh]-> WH }
# without { C2 -[cue:wh]-> WH2 } % C2 not already having a '''
# conjc_0_0.command = '''add_edge C2 -[cue:wh]-> WH'''

# conjc = cl.DisjRule("conjc", root = conjc_0_0)