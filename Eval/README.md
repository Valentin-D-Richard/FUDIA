


List of commands used to create the corpus files, example with `written`:

```bash
# Adding origin metadata and formatting into csv
python3 add_metadata.py -o annodis.txt > annodis.csv
python3 add_metadata.py -o ten_novels.txt > ten_novels.csv
python3 add_metadata.py -o defrancq_written.txt > defrancq_written.csv
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

The sequence is similar for `spoken`, but with files `maya`, `ofrom` and `defrancq_spoken`.

List of commands used to extract the list of positives of FUDIA / a baseline, case with FUDIA and corpus `written`:

```bash
./annotate.sh -g ../fudia.grs -c written.conllu
mv written_Annotated.conllu Annotated/written_fudia.conllu
./extract.sh -g ../fudia.grs -c Annotated/written_fudia.conllu --no-png > Annotated/written_fudia.json
grep "sent_id" Annotated/written_fudia.json | sed -E 's/^.*sent_id": "(.*)".*$/\1/' | tac > Annotated/written_fudia.txt
```

Other example with baseline1 (QUECQ?) on `spoken`:

```bash
./annotate.sh -g quecq.grs -c spoken.conllu
mv spoken_quecq.conllu Annotated/
./extract.sh -g quecq.grs -c Annotated/spoken_quecq.conllu --no-png > Annotated/spoken_quecq.json
grep "sent_id" Annotated/spoken_quecq.json | sed -E 's/^.*sent_id": "(.*)".*$/\1/' | tac > Annotated/spoken_quecq.txt
```