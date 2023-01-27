#!/usr/bin/env python3

import sys

USAGE = '''./generate_grs.py [-o FILENAME]
Creates a grs file with can be used with grew to annotate French interrogatives.
To run the annotation, use:
  grew transform -grs GRS_FILE -i CORPUS -o OUTPUT_FILE -strat main

Options:
-o FILENAME     Specifies output file name. Default is fudia.grs'''

# Argument handling
FILENAME = "fudia.grs"

if len(sys.argv) > 1 and sys.argv[1] == "--help":
    print(USAGE)
    exit()

elif len(sys.argv) > 1 and sys.argv[1] == "-o": # -o option
    if len(sys.argv) != 3:
        message = "Error: missing -o argument or too many parameters. See --help"
        print(message,file=sys.stderr)
        exit(2)
    else:
        FILENAME = sys.argv[2]

else:
    if len(sys.argv) != 1:
        message = "Error: too many parameters. See --help"
        print(message,file=sys.stderr)
        exit(1)



# Importing classes

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


# Main routine
cl.gen_grs(seq, FILENAME)

