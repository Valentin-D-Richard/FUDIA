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

#### Note that, following the Grande Grammaire du Français, we do not consider sentences with final raising contour (2.) or similar disjunctive questions (3.) as syntactic interrogatives, but as question-raising declaratives.

(2.) Il vient quand-↑ ?

(3.) Vous voulez du thé-↑ ou du café-→ ?

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

(4.) La question suivante est : Peut-on y prendre épouse ? 

(5.) vous allez peut-être probablement avoir un débat en cette fin d'année avec vos amis ou votre famille sur [pause] faut-il séparer l'œuvre de l'artiste

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

The rules are based on linguistic literature, on personal knowledge or syntactic tests, and on observation of the corpus to see how phenomena have already been annotated.

Except for "quoted segments", we try to not base our rules on punctuation, and especially not on interrogation marks. Moreover, we try to base them only based on closed word class knowledge. In particular, there is not list of verbs embedding interrogatives.

Sometimes, the designed rules are however not sufficient to correctly capture a phenomenon. In that case, we resort to approximation rules and heuristics. When this is the case, we mention it using the symbol :construction:.

In the order of application, the python modules developped are:

 1. `constr`
 2. `prontype`
 3. `ecq`
 4. `quoted`
 5. `wh`
 6. `cl_head_pull`
 7. `conj`
 8. `mark`

Each class contains several disjunctive patterns (`DisjPat` object). We describe here the code used in the snippets making up the disjunctive patterns.

Each disjunctive pattern is turned into a `Onf(Seq(...))` strategy. `Onf` (one normal form) means that the disjunctive pattern is repeated until no more rule can be applied.

For reannotation, we create additional "copy" node (`T2`, `Q2`, etc.). We define their form, lemma and upos to be the same as their originals, and we append the resting features of the originals to the copies. We shifht all edges to the copies (usualy, only the head nodes) As said in UD guidelines, the head of the fixed expression is the first word. Some additional shifting may be performed, e.g. to handle consistently punctuation. We add `fixed` relations. Finally, we deleting the originals.

This method has the advantage to automatically erase the original relations between the lements of the expression.

In the programme, by "anchor" we usually mean the governer of the main head is question. In this description, by "follows", "after" and "before" we are talking about linear order of words. We employ the term "precede" to specify immediate follwing.

## 1. `constr`

The goal of this module is to reannotate some French fixed structures.

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

We detect the bigram WH lemma with undefined `PronType`, *que* lemma, and somewhere on the right :construction:, a node with `Mood="Sub"`.


## 2. `prontype`

The goal of this module is to add missing `PronType` annotations.

### `relprontype`

Adding some `PronType="Rel"` by listing a reasonable number of relations between CL_HEAD and WH.

We detect *qui*, *que*, *quoi*, *où* or *lequel* lemmas with undefined `PronType`, followed by a CL_HEAD and following an ANCHOR, which are related by a relative clause or cleft relation. We list three possible paths :construction: from CL_HEAD to WH:
 * 1 relation
 * 2 relations, with an intermediary I linearly after ANCHOR (e.g. WH is *quel*, the int. phrase head is not WH, or WH depends on a verbal complement of CL_HEAD)
 * 3 relations, with 2 intermediaries I1 and I2, linearly after ANCHOR, and such that `I1 << I2` or both `I2 << CL_HEAD` and `CL_HEAD << I1`

### `intprontype`

We detect lemma *qui*, *que*, *quoi*, *comment*, *où*, *quand*, *combien*, *pourquoi*, *lequel* or *quel* with undefined `PronType`. We assume the `relprontype` annotation has been performed and we assume that there is no annotation mistake.

*quel* as adjective, determiner or pronoun is interrogative if we are in no one of the follwoing cases:
 * it precedes lemma *que*
 * it precedes form *n'importe*
 * it succedes lemma *tel*
 * there is an exclamation mark :construction:

*comment* and *combien* are always interrogative as adverbs.

*pourquoi* is always interrogative as an adverb, except in the expressions (lemmas) *c'est quoi* and *ce pourquoi*.

*quand* is always interrogative as an adverb, except in expressions *quand même* and *quand bien même*.

*où* is always interrogative as an adverb.

*lequel* is always interrogative as a pronoun. Note that due to French UD guidelines, *au(x)quel(le)(s)* and *duquel* / *desquel(le)s* are decomposed into *à lequel* / *à lesquel(le)s* and *de lequel* / *de lesquel(le)s* respectively.

*qui*, *quoi* and *que* as pronouns are interrogative when we are no one of the follwing cases:
 * expression *ce que* (lemmas)
 * discourse marker *quoi*
 * expression *en ce qui concerne* (lemmas + form *concerne*)
 * there is an exclamation mark :construction:


## 3. `ecq`

The goal of this module is to reannotate *qu'est-ce que* and *est-ce que *expressions.

### `qecq`

Reannotating expression *qu'est-ce que/qui* as fixed. We do not reannotate cases where this expression precedes a NP, identified as a dislocation, e.g. *Qu'est-ce que Angiox*.

We detect the tetragram lemma *que* WH, form *est* E, form *ce* or *-ce* C and lemma *que* or *qui* Q.

We first treat as a special case the expression *qu'est-ce que c'est* (lemmas *ce+être*) as follows: we put *qu'* as head of the sentence, *c'* being its nominal subject and the second *est* being its copula.

We assume that the former head of the expression is on WH or E and that it formerly governed CL_HEAD by a `advcl`, `dislocated` or `ccomp` relation.

If Q is *que*, we add an object relation from CL_HEAD to the new WH (i.e. WH2). If CL_HEAD has a verbal complement (i.e. `xcomp`), we suppose that *qu'est-ce que* is the object of that complement :construction:.

If Q is *qui*, we add a nominal subject relation from CL_HEAD to the new WH.

In the complementary case where there is no `advcl`, `dislocated` or `ccomp` relation from WH or E, we do not add any relation :construction:.

### `ecq`

Reannotating expression *est-ce que/qui* as fixed.

We detect the trigram form *est* E, form *ce* or *-ce* C and lemma *que* or *qui* Q. We filter out cases where C is the object of E  (e.g. *Le ménage est ce que tu es en train de faire*.) or *c'est que ce* expressions.

We decided to try to list all the possible current annotations of est-ce que in the UD corpora in order to not overfit :construction:.

Case 1. there is a clause head CL_HEAD. We have two subcases (more detail is to be found in the source code):
 * *est* ist the former head, governing CL_HEAD with `advcl` or `ccomp`
 * CL_HEAD is the former head

Case 2. there is not clause head (*est-ce que* is isolated, e.g. unfinished sentence). We have two subcases (more detail is to be found in the source code):
 * *que/qui* is the former head
 * *est* is the former head


## 4. `quoted`

The goal of this module is to identify quoted segments.

In the following, by CL_HEAD we mean the head of the segment in question. It may not always be the head of a clause.

### quoted_a

Identifying a quoted segment using punctuation: case where the anchor is follwed by the clause head.

We detect a relation `ANCHOR -> CL_HEAD` with a punctuation P `:`, `«`, `"` or `-` between them. To be confident that the punctation is really linked to this relation, we add some constraints: :construction:
 * either ANCHOR or CL_HEAD governs P
 * P either unambiguously is an opening symbol (`:` or `«`), or CL_HEAD is located bewteen another occurrence of P (`"` or `-`).

#### Note 1.
These rules take for quoted clauses which could raher be analyses as "free indirect speech". In (a.), the interrogative is syntactically a subordinate, because the *si* surbordination conjunction cannot be used in independent clauses. However, the guillemots indicates the choice of the writer to categorize it as reported speech.

 (a.) Stéphanie Nicot et Eric Vial se posent la question de savoir « si l'uchronie peut faire l'économie de l'événement fondateur [...] ?

### quoted_b

Identifying reported speech: case where the clause head governs and is followed by an inserted clause (relation `parataxis`) headed by a reporting verb D.

We detect a relation `CL_HEAD -> D` with a punctuation P `»` or `"` between them. We use similar constraints as in `quoted_a`:
 * either CL_HEAD or D governs P
 * P either unambiguously is an opening symbol (`»`), or CL_HEAD is located bewteen another occurrence of P (`"`), or there is a comma just after P.

### quoted_c

Identifying reported speech: case where the head clause governs and follows a clause (relation `parataxis`) headed by a reported verb D.

We detect a relation `CL_HEAD -> D` with a comma between them and a dash before D. We use similar constraints as in `quoted_a`:
 * either CL_HEAD or D governs the comma

### quoted_d

Identifying title heads.

We detect a clause head having `Title="Yes"` or `InTitle="Yes"` anchored by a node having neither of theses fetures.

### quoted_e

Identifying parataxized parenthesized segments.

We detect clause heads governed by `parataxis` and governing a pair of `--` symbols or `(` and `)` around itself.


## 5. `wh`

The path of zero, one or more relations from the inerrogative clause head CL_HEAD to the interrogative phrase head is called the phrase path `ph_path`. The path from the interrogative phrase head PH_HEAD to the interrogative word WH is called the WH path `wh_path`.

The goal of this module is to identify PH_HEAD and CL_HEAD starting from WH and going up the direction of relations.
We first identify the first edge of `wh_path`. We then potentially pull the feature `IntPhrase="Yes"` (and the `cue:wh` relation) to find the right interrogative phrase head. We precede similarly wih `ph_phrase`. Pulling the feature `IntClause="Yes"` along relations is done in module 6 (`cl_head_pull`).

Some activations of the `cleft` strategy in between the other ones help handling clefted interrogative words.

### `wh_edge`

Finding the first edge of `wh_path` with PH_HEAD != WH.

We detect a word WH with `PronType="Int"` and a governer (excluding conjuction relation). There are three case were we are sure that the governer is part of the interrogative phrase:
 * WH is lemma *quel* (but not in *n'importe quel* expression)
 * the relation is `fixed`, e.g. *à quoi bon* (also excluding *n'importe + WH*)
 * the relation is a *de* nominal complement and the governer is before WH

We don't ask the governer to have a preposition to account for subject interrogative phrases, e.g. *Le chat de qui est parti ?*

### `ph_head_pull`

Pulling `IntPhrase="Yes"` and the `cue:wh` relation.

We detect a current word CUR with `IntPhrase="Yes"` and a candidate PH_HEAD governing CUR. We remove this feature from CUR and add it to PH_HEAD iff CUR is a *de* nominal complement following PH_HEAD and
 * either PH_HEAD has a preposition
 * or PH_HEAD is a nominal subject

As each disjunctive pattern is repeated until no more rule can be applied, we can handle any WH path length.

### `ph_edge_b`

Finding `ph_path` with WH != PH_HEAD, therefore supposing `wh_edge` (and potentially `ph_head_pull`) has been performed on PH_HEAD.

We detect a PH_HEAD with `IntPhrase="Yes"`.

In the first case, there is a governer CL_HEAD. CL_HEAD is part of the same clause iff the relation is oblique, nominal modifier or nominal subject.

Otherwise, CL_HEAD = PH_HEAD. More precisely, the cases where we add `IntPhrase="Yes"` to PH_HEAD are
 * when PH_HEAD is the root of the sentence, a parataxized segment or a reparendum (and other relations isolating a segment: `discourse`, `vocative`, `dislocated`, `list`, `orphan`)
 * when PH_HEAD is the head of a quoted segment
 * when PH_HEAD is the direct or oblique objet of an interrogative-embedding verb (elliptical interrogative clause). To avoid, listing all interrogative-embedding verbs, we choose to just test for one of the most common one in this situation: *savoir* (to know) :construction: :heavy_exclamation_mark:

### `ph_edge_a`

Finding the first edge of `ph_path` with WH = PH_HEAD, therefore supposing `wh_edge` did'nt apply.

We detect a word WH with `PronType="Int"` and a governer CL_HEAD which has no `IntPhrase` feature. We exclude other cases: *n'importe + WH* construction and alone WH (see next section).

We assume that the only relations between WH and a governing word in the same clause (but outside the interrogative phrase) are:
 * nominal subject, indirect object (certain occurrences of *où*), direct object, oblique object, adverbial modifier and `xcomp` (certain occurrences of *que*)
 * nominal modifier, supposing it is fronted wrt. CL_HEAD
 * `advcl` (adverbial clause) for clauses with a (present or past) participial, gerondival or infinitival copula (so WH is the head even if it's a clause) or auxiliary (but no passé composé) and introduced by a preposition, e.g. *Ils sont connus comme étant quoi ?*

### `wh_alone`

Identifying isolated WH = PH_HEAD = CL_HEAD.

We detect a word WH with `PronType="Yes"` and no `IntPhrase` feature. We add `IntPhrase="Yes"` and `IntClause="Yes"` iff:
 * when WH is the root of the sentence, a parataxized segment or a reparendum (and other relations isolating a segment: `discourse`, `vocative`, `dislocated`, `list`, `orphan`)
 * when WH is the head of a quoted segment
 * when WH is a direct or oblique objet of an interrogative-embedding verb (elliptical interrogative clause). We identify that with:
   * WH is an adverb (they are normally not objects)
   * WH is a pronoun and the governer is interrogative-embedding. To avoid, listing all interrogative-embedding verbs, we choose to just test for one of the most common one in this situation: *savoir* (to know) :construction: :heavy_exclamation_mark:

### `cleft`

Identifying clefted interrogative words.

We detect the lemma bigramm *ce + être*, followed by a head HEAD, then a subordination conjunction lemma *que*, *qui* or *dont*, and finally (in the linear order), a clause head, such that:
 * *ce* is the (expletive) subject of HEAD
 * *être* is the copula of HEAD
 * CL_HEAD is governed by HEAD as an adverbial clause (cleft is supposed to be annotated with `advcl:cleft`), adnominal clause, subject clause or clausal complement

In the first case, HEAD is a not-yet-annotated word with `PronType="Yes"` --Remember that `cleft` is run once before all disjunctive patterns of this module--. If so, We label HEAD with `IntPhrase="Yes"`, CL_HEAD with `IntClause="Yes"` and we add the edge `CL_HEAD -[cue:wh]-> HEAD`.

In the second case, HEAD is annotated with `IntPhrase="Yes"` --Remember that `cleft` is run just after `wh_edge` and just after `ph_head_pull`--. Similarly, we add `IntClause="Yes"` to CL_HEAD andthe edge `CL_HEAD -[cue:wh]-> HEAD`.


## 6. `cl_head_pull`

The goal of this module is to complete the module `wh` by getting the right node to be the clause head of the current interrogative. As explained in the previous module, we procede by going up relations until we can't.

### `chp`

We detect a node CUR currently having the feature `IntClause="Yes"`, relation `CUR -[cue:wh]-> WH` and its governer to be the candidate CAND. HEAD must also not have `Quoted="Yes"`.

Let us first discuss clausal relations between CAND and CUR (`csubj`, `ccomp`, `xcomp`, `advcl` and `acl`). There are three cases where we have to pull along such a relation:
  * when CUR is (or has a copula or auxiliary being) a (present or past) participle, gerondive or infinitive (but no passé composé) and is introduced by a preposition, e.g. *Ils a réussi en faisant quoi ?* *Il est venu pour faire quoi ?*
  * when a(nother) subordination conjunction is present bewteen CAND and CUR, e.g. *vous voulez que je fasse quoi*
  * with a verbal infinitival complement, when WH is fronted before CAND or in situ, e.g. *Que veut-elle faire ? Elle veut faire quoi ?*

Let us now consider the case where the relation between CAND and CUR is nominal (`nsubj`, `obj`, `obl`, `nmod` or `det`). This case is very rare because it only happens when the WH word is in situ, and particularly when it cannot be extracted, e.g. *T'as acheté un jeans avec combien de trous ?* `obj(acheté,jean)`. We assume that we can always pull along those relations. The only exception is when interrogative-embedding verbs have an interrogative phrase alone as complement. To filter out this case, we do as mentionned in `ph_edge_b` (last bullet point).

Note that each time we are searching for a preposition or a subordination conjunction, we also take into account the case of prepositional locutions or subsordination locutions.

As each disjunctive pattern is repeated until no more rule can be applied, we can handle any phrase path length.


## 7. `conj`

The goal of this module is to handle interrogative clauses with multiple WH words.

The conditions established in modules `wh` and `cl_head_pull` are supposed to make sure that whenever there are multiple WH words having the same interrogative clause head (resp. interrgoative phrase head), they all get an edge `cue:wh` from the latter. The remaining case is with conjoined WH words.

### `conj`

We detect two conjuncts P1 and P2 and a node CL_HEAD with `IntClause="Yes"`.

There are four cases depending on whether P1 (resp. P2) is a sole WH word or a PH_HEAD with a distinct WH word. We assume that CL_HEAD already has a `cue:wh` relation with P1 or its Wh word. We add a relation from CL_HEAD to P2 or its WH word.


## 8. `mark`

The goal of this module is to identify interrogative markers by adding an edge `CL_HEAD -[cue:mark]->` to them.

### `eske`

Annotating marker *est-ce que* or alternative forms *est-ce* or *ce que*.

Note that alternative non-standard garphies (e.g. *Ousque tu vas ?* *Kess tu fais ?*) are not taken into account :construction:. We only assume transcriptions using standard spelling and fixed analysis (e.g. *Où ce que tu vas ? Qu'est-ce tu fais ?*).

We detect fixed bi- or trigram forms *est-ce que*, *ce que* or *est-ce*. If it has a governer, we add `IntClause="Yes"` and the cue relation. If not, we simply add `IntClause="Yes"` to the first element of the bi or trigram.

### `que`

Annotating *que* marker.

*que* can also act like *est-ce que*, but only following a WH word, e.g. *Où qu'il va ?*

We detect a lemma *que* following a WH word.

If *que* is before its governer CL_HEAD as marker or `xcomp` and CL_HEAD has Wh as cue, we add `CL_HEAD -[cue:mark]-> Q`.

In the other case, *que* is alone, and we expect it to be governed by WH as marker or `xcomp`. We also add a cue edge.

### `si`

Annotating *si* marker.

There is no feature in UD which distinguished interrogative-*si* from conditional-*si*.

We detect a subordination conjunction lemma *si* marking a clause head CL_HEAD subordinated by a governer ANCHOR. We also include other constraints based on syntactic tests to **filter out conidtional-*si***:
 * interrogative *si* clauses must have a finite verb (or copula or auxiliary), e.g. *\**
 * as a consequence, interrogative *si* clauses cannot be infinitival, and so, cannot be `xcomp`'ed, e.g. *\*Elle sait si gagner.*
 * they cannot have a WH word, e.g. *\*Elle sait si combien elle peut gagner. \*Elle sait si elle peut gagner combien.*
 * they cannot be after another subordination conjunction in the same clause or parent clause, e.g. *\*Elle sait que si tu viens, elle part.* is conditional
 * if they are modifiers (`advcl` or `acl`), they only come with a preposition, e.g. (6.) and (7.) exhibit interrogatives, whereas (8.) and (9.) have conditional clauses instead.
 * mainly interrogative *si* clauses seem to be allowed as verb subjects :construction:, e.g. *S'il faut tout abandonner (ou pas) n'est pas la question.*
 * fixed expression *même si* (lemmas) is excluded

(6.) Suivant si elle vient (ou pas), on sera 3 ou 4.

(7.) C'est une vidéo sur si c'est une bonne idée ou pas de prendre l'avion.

(8.) Si elle vient *(ou pas), on sera 4.

(9.) C'est une belle vidéo si tu aimes le fantastique *(ou pas).

There seem to be some rare cases of *si* (with a similar use as *que*) in a declarative clausal subject, like in (10.). We do not know how to filter them out.

(10.) Ce n'est pas un hasard si le sensible Jean Anouilh, dans L'alouette, imagine une Jeanne qui ne meurt pas. [GSD]

### `spp`

Annotating suffixed personal pronoun (+ *ce*), also called interrogative subject-verb inversion or retrograde versational construction.

We detect a personal pronoun or *ce* lemma governed as subject or expletive subject by CL_HEAD such that it follows:
 * it is preceded by its finite verbal governer (except imperative mood)
 * it is preceded by a finite copula or auxiliary of its governer (except imperative mood)

The very difficult task is to **distinguish interrogative inversion from stylistic inversion**. We develop here several heuristics to filter out stylistic inversion :construction: :heavy_exclamation_mark:

The inversion is interrogative if we know there is already a WH word or there is an interrogation mark governed :heavy_exclamation_mark:. Otherwise, the inversion is most probably stylistic:
 * when CL_HEAD governs or is governed with parataxis by a quoted segment
 * when CL_HEAD is after an adverb (or adverbial locution) which is non-interrogative and not *ne*

If CL_HEAD is not governed with a parataxis relation, we can be quite confident the inversion is not stylistic. When it is, we have the following heuristics: the inversion is interrogative when:
 * CL_HEAD has an additional subject, object, oblique complement or clausal complement,
 * or CL_HEAD has a fronted WH word,
 * or CL_HEAD has a `xcomp` complement having an (oblique) object or clausal complement

In other words, we expect stylistic inversion, and more precisely speech reporting inversion, to be very short, contrary to interrogatives.

Unfortunately, some examples fail to be correctly annotated with these heuristics. In (11.), *poursuit* is parataxized and head of a quoted segment, but it is not sufficient to be sure it's not an interrogative.

(11.) c'est-à-dire--poursuit-il son argument--, " avant, le Maroc pensait [...] [GSD]

### `titu`

Annotating *-ti* / *-tu* markers.

As no example of regional *-ti* or québecois *-tu* is present in the current UD corpus, we have to imagine how people would annotate it.

We detect a form *-ti* or *-tu* (or without dash) and its governer. Either:
 * the relation between them is the expected `mark`
 * or the relation is (expletive) subject. In this case, we only add an edge if the form is *ti* or *-ti* because the *tu* / *-tu* form should have already been annotated by `spp`.



