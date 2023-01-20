#!/usr/bin/env python3

import classes as cl
import constr as cs     # Reannotating constructions involving WH proforms
import prontype as p    # Reannotating some relative and interrogative pronouns
import ecq as e         # Reannotating "est-ce que" expressions
import quoted as q      # Adding annotations about reported speech or titles
import wh as w          # Annotating wh words ans phrases
import cl_head_pull as c # Recursive operation on wh clause head
import conj as co       # Conjuncted wh words
import marker as m      # Annotating interrogative markers

# The next list provides the sequence of disjunctive patterns (DisjPat)
# (and their strategy) in orer to annotate French interrogative clauses
# Default stategy is Onf (One normal form)

seq =  [cs.telquel, cs.nimporte, cs.whque]
seq += [p.relprontype, p.intprontype]
seq += [e.qecq, e.ecq]
seq += [q.quoted_a, q.quoted_b, q.quoted_c, q.quoted_d, q.quoted_e]
seq += [w.cleft, w.wh_edge, w.cleft, w.ph_head_pull, w.cleft]
seq += [w.ph_edge_b, w.ph_edge_a, w.wh_alone]
seq += [c.cl_head_pull]
seq += [co.conj]
seq += [m.eske, m.que, m.si, m.titu, m.spp]


cl.gen_grs(seq, "annotate")

