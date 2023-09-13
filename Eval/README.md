
List of commands to create the corpus files, example with `written` (similar for `spoken`, but with files `maya`, `ofrom` and ...):

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
cut written.csv -d',' -f3- | sed -E -e 's/^.//' -e 's/.$//' | sed 's/\\"/"/g' > written_buffer.txt
# Tokenization
python3 tokenizer.py written_buffer.txt > written_tokenized.txt
```