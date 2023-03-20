# Evaluation of the FUDIA annotator

## Evaluation method

For each corpus and each set, we extract, from the FUDIA-annotated corpus, 3 mutually non-intersecting subsets:
 * Cl: Sentences having a `IntClause="Yes"` feature
 * Phr: Sentences having a `IntPhrase="Yes"` feature but no `IntClause="Yes"` feature
 * Pr: Sentences having a `PronType="Int"` feature but no `IntClause="Yes"` or `IntPhrase="Yes"` feature

A priori, sentences of type Phr are not considered well-annotated. Except fixed expressions like `n'importe + WH`, sentences of type Pr are not considered well-annotated.

We looked at the sets that ware not part of the development phase to assess whether the sentences of their subsets Cl, Phr and Pr were correctly annotated:
 * FQB (test, only subsets Phr, Pr and Diff)
 * GSD train
 * ParisStories train
 * ParTUT train
 * PUD (test)
 * Rhapsodie train
 * Sequoia train

As the French Question Bank (FQB) was designed to train parsers on interrogative, we also collected the list of FQB sentences that does not belong to any subset after FUDIA annotation, and we call it the diff subset.

The file `statistics.ods` lists the sentences of subsets Cl, Phr or Pr and the mistake category we assigned them.

## "Mistake" categories

Categories:

 0. Well-annotated

 1. Original UD annotation mistake
  a. Wrong PronType (Pr)
  b. Wrong analysis as `ANCHOR -[obj]-> PH_HEAD ; PH_HEAD -[acl|advcl]-> CL_HEAD` or similar (Cl or Phr)
  c. Grammatically dubious sentence (Pr)
  d. Other wrong relation
  e. Missing `(In)Title="Yes"` feature
  f. Missing `relcl` or `cleft` subspecification

 2. Actual mistake of FUDIA
  - a. Due to unexpected segmentation, feature, relation or structure
    - i. Unexpected segmentation with euphonic *-t-* :heavy_check_mark:
    - ii. conjuncted WH phrase with interrogative marker: should be analzed as isolated for simplicity :heavy_check_mark:

  - b. Some FUDIA rule does not implement the specification correctly
    - i. *quel + NP* as `obj` (fronted, in-situ or alone): phrase path not detected (Cl or Phr) :heavy_check_mark:
    - ii. *quel* as adjectival head with copula: `IntClause` feature not added (Pr) :heavy_check_mark: 
    - iii. adverbial non-finite adjunct: phrase path not detected (Pr) :heavy_check_mark:
    - iv. in situ `nmod`: phrase path not detected (Pr) :heavy_check_mark:
    - v. copular WH embedded: `IntClause` not added (Pr) :heavy_check_mark:
    - vi. *quel + NP* as head with copula (Phr) :heavy_check_mark:
    - vii. *comme si* and *sauf si* subordination locution: `IntClause=Yes` added (Cl) :heavy_check_mark:
    - viii. pronoun *quel* as head and having a `nsubj`: `IntClause` not added (Pr) :heavy_check_mark:
    - ix. *quel* as `amod`: phrase relation not detected (Pr) :heavy_check_mark:
    - x. isolated WH phrase with `conj` or `appos`: `IntClause` not added (Phr) :heavy_check_mark:
    - xi. fixed WH locution as `advmod`: phrase path not detected (Phr) :heavy_check_mark:
    - xii. *qu'est-ce* expression: not reannotated as fixed :heavy_check_mark:
    - xiii. finite adverbial clause: pulled clause head :heavy_check_mark: (It was actually an issue in the heuristics of `cl_head_pull`, which was solved by considering *par exemple* as a cue for quoted segments.)
   
  - c. FUDIA heuristic
    - i. aborted relative construction: IntClause="Yes" added (Pr) :heavy_check_mark:
    - ii. relative clause: `PronType="Int"` added (Cl) :heavy_check_mark:
    - iii. speech-reporting subject-verb inversion: `IntClause` added (Cl) :heavy_check_mark:
    - iv. fixed *ne + être + -ce que*: `IntClause` added (Cl) :heavy_check_mark:
    - v. parenthesized segment with 1 parenthesis missing: pull clause head because missing quoted (Cl)
    - vi. paratactic speech-reporting subject-verb inversion with oblique argument
    - vii. reported segment with guillemots attached to the first element: quoted feature missed (Phr)
    - viii. embedded exclamative pronoun: `PronType="Int"` added (Cl)

 3. Clause not considered as interrogative
  - a. No question-raising clause (FQB Diff)
  - b. Question-raising declarative (FQB Diff)
  - c. Fixed expreession *n'importe + WH* (Pr)

Missed clauses:
 * GSD:fr-ud-train_07658 due to `conj`

Heuristics were added to solve partially issue 2ciii. But remaining cases are hard to handle if we want to avoid overfitting. Here is the only example where we were not able to annotate correctly (2cvi):
 * fr-ud-train_05325 (2cvii)

Remaining problems du to "quoted" heuristics:
 * fr-ud-train_12149 (2cvi)
 * fr-ud-train_09783 (2cv)

Remaining weak heuristics for missing `PronType=Exc`
 * fr-ud-train_08302
 * Rhap_M2004-6

## Results

663 sentnences were detected over all evaluation subsets. We looked at each of them and assigned them a mistake category.
 * 490 sentences were well-annotated
 * 16 sentneces were ill-annotated due to an original annotation mistake
 * 86 sentences were ill-annotated due to a FUDIA mistake
 * 66 sentences were excluded (mistake category 3)

The accurracy of FUDIA before fix is computed as #{sent. of cat. 0} / #{sent. of cat. 0 + 2}, which is 0.8507.

Most mistakes of category 2 were actually easily fixable. Only mistakes 2cv, 2cvi and 2cvii were not fixed because they go beyond the limits of our heuristic approach.

The **accurracy of FUDIA** after fix is estimated as #{sent. of cat. 0 + 2a + 2b + 2ci-2civ} / #{sent. of cat. 0 + 2}, which is **0.9931**.