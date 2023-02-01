import classes as cl

# Direct (or emphasized) speech or words

##### quoted_a: Identified by punctuation, after a governer
# e.g. <ANCHOR> ... :/«/-/" ... <CL_HEAD>

# Root
quoted_a_0_0 = cl.Snippet("quoted_a_0_0")
quoted_a_0_0.request = '''pattern { e : ANCHOR -> CL_HEAD ; CL_HEAD[!Quoted] ;
\tP[lemma=":"|"«"|"\\\""|"-"] ; ANCHOR << P ; P << CL_HEAD ; }
without { CL_HEAD[upos="PUNCT"] }
without { P[lemma="\\\""] ; PP << ANCHOR ; PP[lemma="\\\""] } % " as final quote mark (may restrict a little more than necessary)'''
# Adding Quoted="Yes"
quoted_a_0_0.command = '''CL_HEAD.Quoted = "Yes"'''

quoted_a = cl.DisjRule("quoted_a", root=quoted_a_0_0)

# Punctuation attached on the frame
quoted_a_1_0 = cl.Snippet("quoted_a_1_0")
quoted_a_1_0.request = '''pattern { ANCHOR -[punct]-> P }'''

# Punctuation attached on the reported part
quoted_a_1_1 = cl.Snippet("quoted_a_1_1")
quoted_a_1_1.request = '''pattern { CL_HEAD -[punct]-> P }'''

# unambiguaous punctuation
quoted_a_2_0 = cl.Snippet("quoted_a_2_0")
quoted_a_2_0.request = '''pattern { P[lemma="«"|":"] }'''

# succeding "
quoted_a_2_1 = cl.Snippet("quoted_a_2_1")
quoted_a_2_1.request = '''pattern { P[lemma="\\\""] ;
\tCL_HEAD << P2 ; P2[lemma="\\\""] }'''

# succeding -
quoted_a_2_2 = cl.Snippet("quoted_a_2_2")
quoted_a_2_2.request = '''pattern { P[lemma="-"] ;
\tCL_HEAD << P2 ; P2[lemma="-"] }'''

quoted_a.add_snippets([quoted_a_1_0, quoted_a_1_1], quoted_a_0_0)
quoted_a.add_snippets([quoted_a_2_0, quoted_a_2_1, quoted_a_2_2], quoted_a_0_0)



##### quoted_b: Reported speech preceding with partaxis, 
# e.g. <CL_HEAD> ... "/» ... <D>

# Root
quoted_b_0_0 = cl.Snippet("quoted_b_0_0")
quoted_b_0_0.request = '''pattern { e : CL_HEAD -[1=parataxis]-> D ;
\tP[lemma="»"|"\\\""] ; CL_HEAD << P ; P << D ; CL_HEAD[!Quoted] ; }
without { CL_HEAD[upos="PUNCT"] }
without { P[lemma="\\\""] ; D << PP ; PP[lemma="\\\""] } % " as initial quote mark (may retrict a little more than necessary)'''
# Adding Quoted="Yes"
quoted_b_0_0.command = '''CL_HEAD.Quoted = "Yes"'''

quoted_b = cl.DisjRule("quoted_b", root=quoted_b_0_0)

# Punctuation attached on the frame
quoted_b_1_0 = cl.Snippet("quoted_b_1_0")
quoted_b_1_0.request = '''pattern { D -[punct]-> P }'''

# Punctuation attached on the reported part
quoted_b_1_1 = cl.Snippet("quoted_b_1_1")
quoted_b_1_1.request = '''pattern { CL_HEAD -[punct]-> P }'''

# unambiguaous punctuation
quoted_b_2_0 = cl.Snippet("quoted_b_2_0")
quoted_b_2_0.request = '''pattern { P[lemma="»"] }'''

# preceeding "
quoted_b_2_1 = cl.Snippet("quoted_b_2_1")
quoted_b_2_1.request = '''pattern { P[lemma="\\\""] ;
\tP2 << P ; P2[lemma="\\\""] }'''

# additional comma
quoted_b_2_2 = cl.Snippet("quoted_b_2_2")
quoted_b_2_2.request = '''pattern { P < P2 ; P2[lemma=","] }'''


quoted_b.add_snippets([quoted_b_1_0, quoted_b_1_1], quoted_b_0_0)
quoted_b.add_snippets([quoted_b_2_0, quoted_b_2_1, quoted_b_2_2], quoted_b_0_0)



##### quoted_c: Succeding reported speech with partaxis and no quotation marks,
# e.g. - ... <D> ... , <CL_HEAD> 

# Root
quoted_c_0_0 = cl.Snippet("quoted_c_0_0")
quoted_c_0_0.request = '''pattern { e : CL_HEAD -[1=parataxis]-> D ;
\tP1[lemma="-"] ; P1 << CL_HEAD ; CL_HEAD -[punct]-> P1 ;
\tP2[lemma=","] ; CL_HEAD << P2 ; P2 << D ; CL_HEAD[!Quoted] ; }
without { CL_HEAD[upos="PUNCT"] }'''
# Adding Quoted="Yes"
quoted_c_0_0.command = '''CL_HEAD.Quoted = "Yes"'''

quoted_c = cl.DisjRule("quoted_c", root=quoted_c_0_0)

# Punctuation attached on the frame
quoted_c_1_0 = cl.Snippet("quoted_c_1_0")
quoted_c_1_0.request = '''pattern { G -[punct]-> P2 }'''

# Punctuation attached on the reported part
quoted_c_1_1 = cl.Snippet("quoted_c_1_1")
quoted_c_1_1.request = '''pattern { CL_HEAD -[punct]-> P2 }'''

quoted_c.add_snippets([quoted_c_1_0, quoted_c_1_1], quoted_c_0_0)



##### quoted_d: InTitle

# Root
quoted_d_0_0 = cl.Snippet("quoted_d_0_0")
quoted_d_0_0.request = '''pattern { e : ANCHOR -> CL_HEAD ; CL_HEAD[!Quoted] }
without { ANCHOR[InTitle="Yes"] }
without { ANCHOR[Title="Yes"] }
without { e.label = reparandum }'''
# Adding Quoted="Yes"
quoted_d_0_0.command = '''CL_HEAD.Quoted = "Yes"'''

quoted_d = cl.DisjRule("quoted_d", root=quoted_d_0_0)

# CL_HEAD annotated Title
quoted_d_1_0 = cl.Snippet("quoted_d_1_0")
quoted_d_1_0.request = '''pattern { CL_HEAD[Title="Yes"] }'''

# CL_HEAD annotated InTitle
quoted_d_1_1 = cl.Snippet("quoted_d_1_1")
quoted_d_1_1.request = '''pattern { CL_HEAD[InTitle="Yes"] }'''

quoted_d.add_snippets([quoted_d_1_0, quoted_d_1_1], quoted_d_0_0)



# quoted_e: parataxed parenthesis with '(' and ')' or '--' and '--'

# Root
quoted_e_0_0 = cl.Snippet("quoted_e_0_0")
quoted_e_0_0.request = '''pattern { e : ANCHOR -[1=parataxis]-> CL_HEAD ;
\tP1[lemma="--"|"("] ; P2[lemma="--"|")"] ;
\tP1 << CL_HEAD ; CL_HEAD << P2 ; CL_HEAD[!Quoted] ;
\tCL_HEAD -> P1 ; CL_HEAD -> P2 }
without { CL_HEAD[upos="PUNCT"] }'''
# Adding Quoted="Yes"
quoted_e_0_0.command = '''CL_HEAD.Quoted = "Yes"'''

quoted_e = cl.DisjRule("quoted_e", root=quoted_e_0_0)

# Two parentheses
quoted_e_1_0 = cl.Snippet("quoted_c_1_0")
quoted_e_1_0.request = '''pattern { P1[lemma="("] ; P2[lemma=")"] }'''

# Two '--'
quoted_e_1_1 = cl.Snippet("quoted_c_1_1")
quoted_e_1_1.request = '''pattern { P1[lemma="--"] ; P2[lemma="--"] }'''

quoted_e.add_snippets([quoted_e_1_0, quoted_e_1_1], quoted_e_0_0)