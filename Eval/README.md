# Evaluation of FUDIA

## Evaluation corpus

FUDIA is evaluated on the corpus `Eval`, split up in `written.csv` and `spoken.csv`.

Content of `Eval`

|Subcorpus|Corpus of origin|Genre(s)|Number of sentences|
|-----|-----|-----|-----|
|written|Annodis|newspaper, Wikipedia, scientific, administrative|50|
|written|ten_novels|questions (novel)|25|
|written|Defrancq_written|embedded interrogatives (newspaper, novel)|25|
|spoken|OFROM|spontaneous spoken (interview)|50|
|spoken|Maya|questions (TV cartoon)|25|
|spoken|Defrancq_spoken|embedded interrogatives (conversation, radio, TV show)|25|

## Annotation task

We asked 12 French native speakers to annotate the 200 sentences of `Eval` according to the guidelines `fudia_task_guidelines.pdf` (in French). The two labels are

 * **0**: the sentence has no interrogative
 * **1**: the sentence has at least one interrogative (sub)clause

We are concerned with syntatic interrogatives, i.e. the clauses (or infinitival or elliptic phrases) containing an interrogative marker: an interrogative word or another marker specific to French (e.g. *est-ce que*, *si*, subject-verb inversion,...).

We take the majority judgement as gold standard (see `gold.csv`). We add the standard derivation of annotations for each sentence as third column of `gold.csv`. The inter-annotator agreement table is printed in `report.txt`.

## Prediction computation

We parsed `Eval` with ArboratorGrew. To ensure an efficient parsing on the corpus, we selected French UD corpora close to target data genres to fine-tune a pretrained parser. The subcorpus `written` was parsed using a training on GSD `dev` (1476 sentences, obtaining LAS=0.922), and `spoken` using a training on Rhapsodie `train` + ParisStories `train` (total: 2675 sentences, LAS=0.818).

We run FUDIA and the two baselines QUECQ? and SimpleFUDIC on the parsed subcorpora. We retrieved the sentences having a node with label `ClauseType=Int`. We compute the accuracy, precision and recall of the programs using `compute_scores.py`. The scores are available in `report.txt`.

## Appendix

### Commands used to create the corpus and the predictions

Here is the list of commands used to create the corpus files, example with `written`:

```bash
# Adding origin metadata and formatting into csv
python3 add_metadata.py -o Sentences/annodis.txt > annodis.csv
python3 add_metadata.py -o Sentences/ten_novels.txt > ten_novels.csv
python3 add_metadata.py -o Sentences/defrancq_written.txt > defrancq_written.csv
# Merging and suffling
(cat annodis.csv ; cat ten_novels.csv ; cat defrancq_written.csv ) | shuf > written.txt
# Adding unique id
python3 add_metadata.py -n -i written.txt -p written > written.csv
## Creating the file for UD parser:
# Removing origin and id, and deformatting from csv
cut written.csv -d',' -f3- | sed -e 's/^.//' -e 's/.$//' | sed 's/\\"/"/g' > written_buffer.txt
# Tokenization
python3 tokenizer.py written_buffer.txt > written_tokenized.txt
```

The sequence is similar for `spoken`, but with files `maya`, `ofrom` and `defrancq_spoken`. The temporary files have been removed.

Here is the list of commands used to extract the list of positives of FUDIA / a baseline, case with FUDIA and corpus `written`:

```bash
# Annotation of the corpus
./annotate.sh -g ../fudia.grs -c written.conllu
mv written_Annotated.conllu Annotated/written_fudia.conllu
# Extraction of the sentences containing a node with ClauseType=Int
./extract.sh -g ../fudia.grs -c Annotated/written_fudia.conllu --no-png > Annotated/written_fudia.json
# Getting simple list format
grep "sent_id" Annotated/written_fudia.json | sed -E 's/^.*sent_id": "(.*)".*$/\1/' | tac > Annotated/written_fudia.txt
```

Other example with baseline1 (QUECQ?) on `spoken`:

```bash
./annotate.sh -g quecq.grs -c spoken.conllu
mv spoken_quecq.conllu Annotated/
./extract.sh -g quecq.grs -c Annotated/spoken_quecq.conllu --no-png > Annotated/spoken_quecq.json
grep "sent_id" Annotated/spoken_quecq.json | sed -E 's/^.*sent_id": "(.*)".*$/\1/' | tac > Annotated/spoken_quecq.txt
```

Adding the results to a csv file:

```bash
python3 add_results.py
```

Then we copy and paste each annotators' judgment into `results.csv` and run

```bash
python3 compute_scores.py
```