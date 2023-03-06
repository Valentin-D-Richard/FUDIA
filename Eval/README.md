# Evaluation of the FUDIA annotator

## Evaluation method

For each corpus and each set, we extract, from the FUDIA-annotated corpus, 3 mutually distinct subsets:
 1. Sentences having a `IntClause="Yes"` feature
 2. Sentences having a `IntPhrase="Yes"` feature but no `IntClause="Yes"` feature
 3. Sentences having a `PronType="Int"` feature but no `IntClause="Yes"` or `IntPhrase="Yes"` feature

A priori, sentences of type 2 are not considered well-annotated. Except fixed expressions like `n'importe + WH`, sentences of type 3 are not considered well-annotated.

## Mistake categories

Categories:

 0. Well-annotated

 1. Original UD annotation mistake
  a. Wrong PronType (subset 3)
  b. Wrong analysis as `ANCHOR -[obj]-> PH_HEAD ; PH_HEAD -[acl|advcl]-> CL_HEAD` or similar (subset 1 or 2)
  c. Grammatically dubious sentence (subset 3)
  d. Other wrong relation
  e. Missing `(In)Title="Yes"` feature
  f. Missing `relcl` or `cleft` subspecification

 2. Actual mistake of FUDIA
  - a. Due to unexpected segmentation, feature, relation or structure
    - i. Unexpected segmentation with euphonic *-t-* :heavy_check_mark:
    - ii. conjuncted WH phrase with interrogative marker: should be analzed as isolated for simplicity :heavy_check_mark:

  - b. Some FUDIA rule does not implement the specification correctly
    - i. *quel + NP* as `obj` (fronted, in-situ or alone): phrase path not detected (subset 1 or 2) :heavy_check_mark:
    - ii. *quel* as adjectival head with copula: `IntClause` feature not added (subset 3) :heavy_check_mark: 
    - iii. adverbial non-finite adjunct: phrase path not detected (subset 3) :heavy_check_mark:
    - iv. in situ `nmod`: phrase path not detected (subset 3) :heavy_check_mark:
    - v. copular WH embedded: `IntClause` not added (subset 3) :heavy_check_mark:
    - vi. *quel + NP* as head with copula (subset 2) :heavy_check_mark:
    - vii. *comme si* and *sauf si* subordination locution: `IntClause=Yes` added (subset 1) :heavy_check_mark:
    - viii. pronoun *quel* as head and having a `nsubj`: `IntClause` not added (subset 3) :heavy_check_mark:
    - ix. *quel* as `amod`: phrase relation not detected (subset 3) :heavy_check_mark:
    - x. isolated WH phrase with `conj` or `appos`: `IntClause` not added (subset 2) :heavy_check_mark:
    - xi. fixed WH locution as `advmod`: phrase path not detected (subset 2) :heavy_check_mark:
    - xii. *qu'est-ce* expression: not reannotated as fixed :heavy_check_mark:
    - xiii. finite adverbial clause: pulled clause head :heavy_check_mark: (It was actually an issue in the heuristics of `cl_head_pull`, which was solved by considering *par exemple* as a cue for quoted segments.)
   
  - c. FUDIA heuristic fail
    - i. aborted relative construction: PronType="Yes" added (subset 3) :heavy_check_mark:
    - ii. relative clause: `PronType="Int"` added (subset 1) :heavy_check_mark:
    - iii. speech-reporting subject-verb inversion: `IntClause` added (subset 1) :heavy_check_mark:
    - iv. fixed *ne + être + -ce que*: `IntClause` added (subset 1) :heavy_check_mark:
    - v. parenthesized segment with 1 parenthesis missing: pull clause head because missing quoted (subset 1)
    - vi. paratactic speech-reporting subject-verb inversion with oblique argument
    - vii. reported segment with guillemots attached to the first element: quoted feature missed (subset 2)

 3. Clause not considered as interrogative
  - a. No question-raising clause (FQB diff)
  - b. Question-raising declarative (FQB diff)
  - c. Fixed expreession *n'importe + WH* (subset 3)

Missed clauses:
 * GSD:fr-ud-train_07658 due to `conj`

Heuristics were added to solve partially issue 2ciii. But remaining cases are hard to handle if we want to avoid overfitting. Here is the only example where we were not able to annotate correctly (2cvi):
 * fr-ud-train_05325 (2cvii)

Remaining problems du to "quoted" heuristics:
 * fr-ud-train_12149 (2cvi)
 * fr-ud-train_09783 (2cv)


## Evaluation files

We created a csv file for each corpus. There is a sheet for each evaluated subset.

 * Column 1: sentence id
 * Column 2: category
 * Column 3: remarks