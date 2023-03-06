# FUDIA

French UD Interrogative Annotator

## Introduction

FUDIA (French UD Interrogative Annotator) is a programme able to identify and extract interrogative clauses in French UD-annotated sentences. This programme is based on graph rewriting rules. It builds on the [Grew](https://grew.fr/) software.

Python was used as a meta-language to be able to create disjunctive rules (`DisjRule`). See `DisjRule_README.md` for more about that package.

Extra scripts were used to extract the corpus into the French Interrogative Bank [UD_French-FIB](https://github.com/Valentin-D-Richard/UD_French-FIB) and evaluated the programme.


## FUDIA annotator

Given a French UD corpus, FUDIA identify sentences having an interrogative clause by adding the feature `ClauseType="Int"`.

Several other changes are done wrt. the input corpus. For exemple, it adds some missing `PronType` features, reannotate *est-ce que* as fixed, etc. All these changes are documented in `FUDIA_README.md`.

The rules of FUDIA are written in python micro-packages: `cl_head_pull`, `conj`, `constr`, `ecq`, `marker`, `prontype`, `quoted` and `wh`.

The `DisjRule` class of `classes.py`  is used to creat disjunctive rules. See `DisjRule_README.md` for more about that package.

### Use

In command line, you can use

```bash
./generate_grs.py -o fudia.grs
```

It creates a file `fudia.grs` which can be used to rewrite a conll(u) file using command line grew (using the `main` strategy), e.g.

```bash
grew transform -grs fudia.grs -i corpus.conllu -o outputfile.conllu -strat "main"
```

## Extraction

We extracted the sentences having a word with `ClauseType="Int"` from French UD corpora (see the list in `corpus_list`) to create the French Interrogative Bank [UD_French-FIB](https://github.com/Valentin-D-Richard/UD_French-FIB).

We used the Grew python wrapper `grewpy` (version 0.2.0) to retrieve matching sentences and paste them into a conlu file: `extract_Int.py`. See the UD_French-FIB repository for more detail about extraction.

## Evaluation

Evaluation was performed on the train sets (+ FQB test and PUD test) of our corpora.

We 

=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: Grew 
License: CC-BY
Contributors: Valentin D. Richard
Contact: valentin.d.richard@gmail.com
===============================================================================