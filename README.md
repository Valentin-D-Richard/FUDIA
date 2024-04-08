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

FUDIA was designed using some searches on the online Grew match interface (all French corpora and sets). Then, a developpement phase consisted in checking that the programme performed as expected on a subset of the French corpora:
 * GSD test and dev
 * ParisStories test and dev
 * ParTUT test and dev
 * Rhapsodie test and dev
 * Sequoia test and dev
by extracting all the sentences having `ClauseType="Int"` and verifying that there were correctly annotated. Badly annotated sentences led to fixes on FUDIA.

Fianlly, an evaluation phase was run to asses the potential flaws and weaknesses of this program. More in `Eval/READMED.md`

## References

> Valentin D. Richard. Est-ce que l'extraction des interrogatives du français peut-elle être automatisée ?. 5èmes journées du Groupement de Recherche CNRS « Linguistique Informatique, Formelle et de Terrain » (LIFT 2023), Nov 2023, Nancy, France. pp.69-76. [⟨hal-04359947⟩](https://hal.science/hal-04359947)

=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: Grew 1.11, grewpy 0.2.0
License: CC-BY 4.0
COntributors: Richard, Valentin D.
===============================================================================