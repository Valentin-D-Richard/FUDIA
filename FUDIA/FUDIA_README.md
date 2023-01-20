# French Universal Dependencies Interrogative Annotator (FUDIA)

FUDIA is a python programme able to add annotations about interrogatives on French UD-annotated corpora. FUDIA is based on [Grew](https://grew.fr/) and uses graph rewriting rules. It uses disjunctive patterns (DisjPat), written as python classes (file `classes.py`, see `DisjPat_README.md`).

## Use

In command line, you can use

```bash
./annotate.py
```

It creates a file `annotate.grs` which can be used to rewrite a conllu file using command line grew using the `main` strategy, e.g.

```bash
grew transform -grs annotate.grs -i corpus.conllu -o outputfile.conllu -strat "main"
```
---
## Added annotations

Take a French interrogatives like (1.).

(1.) À quelle heure vient-elle ?

We can identify the **interrogative word** (aka. WH word) *quelle*, the **head of the interrogative clause** *vient*, and the **head of** fronted **interrogative phrase** *[À quelle heure]* : *heure*. Moreover, the subject-verb inversion also indicates the interrogativeness of that clause.

FUDIA adds/changes the follwing annotations:

### Added features :
 * some missing `PronType="Rel"`
 * some missing `PronType="Int"`
 * `IntClause="Yes"` on interrogative clause heads
 * `IntPhrase="Yes"` on interrogative phrase heads
 * `Quoted="Yes"` on "quoted segments"

By "quoted segments", we mean segments which do not integrate nor get subordinated in the sentence. It could be
 * titles
 * expressions from another language
 * reported speech
 * complete independent sentences used as nominal blocks, which would typically be written using colons, e.g. 

(2.) La question suivante est : Peut-on y prendre épouse ? 

(3.) vous allez peut-être probablement avoir un débat en cette fin d'année avec vos amis ou votre famille sur [pause] faut-il séparer l'œuvre de l'artiste

### Added edges
 * `cue:wh` from the interrogative clause head to the interrogative word
 * `cue:wh` from the interrogative phrase head to the interrogative word
 * `cue:mark` from the interrogative clause head to a potential interrogative syntactic marker

When the interrogative word is also the head of the interrogative phrase (resp. clause), no such edge is added to avoid loops.

In French, the **interrogative markers** are:
 * the suffixed personnal (or *ce*) pronoun
 * the interrogative conjunction subordination *si* (embedded interrogatives only)
 * the interrogative expression *est-ce que* (see next session)
 * the regional interrogative particle *-ti* or *-tu*
 * the non-standard / regional conjunction *que*

Question-raising sentences using intonation raising are not considered syntactic interrogatives.

### Changed annotations
 * *tel quel* changed to fixed (with `ExtPos="ADJ"`) when it is not already the case
 * *n'importe + WH* changed to fixed: with `ExtPos="DET"` if `WH[lemma="quel"]`, `ExtPos="PRON"` if `WH[lemma="quoi"|"qui"|"lequel"]` and `ExtPos="ADV"` if `WH[lemma="comment"|"quand"|"où"]`, and with consequent head shift
 * *est-ce que* changed to fixed with `ExtPos="SCONJ"`, the head shifted to the interrogative clause head `CL_HEAD`, and the relations changed to `mark(CL_HEAD,est)`
 * *qu'est-ce que* changed to fixed with `ExtPos="PRON"`, the head shifted to the interrogative clause head `CL_HEAD`, and the relations changed to `obj(CL_HEAD,qu')` (see the corresponding section for more detail)

---
# Rules of the programme

The rules are based on linguistic literature, on personal knowledge or syntactic tests, and on observation of the corpus to see how phenomena have already been annotated. Sometimes, the designed rules are not sufficient to correctly capture a phenomenon. In that case, we resort to approximation rules and heuristics. When this is the case, we mention it using the symbol :construction:.

In the order of application, the python classes developped are:

 1. `constr`
 2. `prontype`
 3. `ecq`
 4. `quoted`
 5. `wh`
 6. `cl_head_pull`
 7. `conj`
 8. `mark`

Each class contains several disjunctive patterns (`DisjPat` object). We describe here the code used in the snippets making up the disjunctive patterns.

For reannotation, we create additional "copy" node (`T2`, `Q2`, etc.). We define their form, lemma and upos to be the same as their originals, and we append the resting features of the originals to the copies. We shifht all edges to the copies (usualy, only the head nodes) As said in UD guidelines, the head of the fixed expression is the first word. Some additional shifting may be performed, e.g. to handle consistently punctuation. We add `fixed` relations. Finally, we deleting the originals.

This method has the advantage to automatically erase the original relations between the lements of the expression.

In the programme, by "anchor" we usually mean the governer of the main head is question.

## 1. `constr`

### `telque`

Reannotating *tel quel* as fixed adjective.

### `nimporte`

Reannotating *n'importe + WH* ad fixed determiner, pronoun or adverb.

We detect the n-gram lemma *ne*, form *importe* and WH lemma.

When the WH is a pronoun:
 * if the anchoring relation is `advcl`, `ccomp` or `parataxis` we change it to `obj`, or `obl` when governing by a preposition
 * if it is `csubj`, we change it to `nsubj`

When the WH is *quel*, we change the edges so that the head is shifted to the noun governing *quel* and *n'importe quel* is the determiner of this noun. We do the same as above for object and subject relations.

When the WH is an adverb, we change the anchoring relation to `advmod` in the same conditions as above object.

### `whque`

Adding `PronType="Rel"` to *WH + que + S[Mood="Sub"]*.

We detect the bigram WH lemma with undefined `PronType`, *que* lemma, and somewhere on the right, a node with `Mood="Sub"`.



## 2. `prontype`

### `relprontype`

Adding some `PronType="Rel"` by listing a reasonable number of relations between CL_HEAD and WH.

We detect *qui*, *que*, *quoi*, *où* or *lequel* lemmas with undefined `PronType`, followed by a CL_HEAD and following an ANCHOR, which are related by a relative clause or cleft relation. We list for possible paths from CL_HEAD to WH:
 * 1 relation
 * 2 relations, with an intermediary I linearly after ANCHOR (e.g. WH is *quel*, the int. phrase head is not WH, or WH depends on a verbal complement of CL_HEAD)
 * 3 relations, with 2 intermediaries I1 and I2, linearly after ANCHOR, and such that I1 << I2 or both I2 << CL_HEAD and CL_HEAD << I1

### `intprontype`

We detect lemma *qui*, *que*, *quoi*, *comment*, *où*, *quand*, *combien*, *pourquoi*, *lequel* or *quel* with undefined `PronType`. We assume the `relprontype` annotation has been performed.

*quel* as adjective, determiner or pronoun is interrogative if we are not in one of the follwoing cases:
 * it precedes lemma *que*
 * it precedes form *n'importe*
 * it succedes form *tel*
 * there is an exclamation mark

## 3. `ecq`

## 4. `quoted`

## 5. `wh`

## 6. `cl_head_pull`

## 7. `conj`

## 8. `mark`