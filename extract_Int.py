#!/usr/bin/env python3
import json
from grewpy import Request, Corpus, set_config

set_config("ud")


def prefix_conll(conll, corpus_name):
    """Adds the prefix 'corpus_name' to the sent_id of the conll 'conll'"""
    split_conll = conll.split("\n")
    sent_line   = split_conll[0].split("=")
    new_sent_id = " " + corpus_name + "_" + sent_line[1].strip()
    split_conll[0] = sent_line[0] + "=" + new_sent_id
    return "\n".join(split_conll)


corpora_path = "/home/varichar/Documents/PhD/Corpus/"

# We create three sets for FIB
sets = ["dev", "test", "train"]

for s in sets:
    print("***** Building " + s + " set")

    # Opening the list of input annotated corpora names used for set s
    corpus_list_name = corpora_path + "ud-" + s + "_Annotated.json"
    corpus_list = json.load(open(corpus_list_name, "r"))["corpora"]

    output_filename = corpora_path + "UD_French-FIB/fr_fib-ud-" + s + ".conll"
    output_file = open(output_filename, "w", encoding="utf-8")
    output_file.write("# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC\n")
    n_ids = 0 # Number of sentcences in set s

    for c in corpus_list:
        # Opening the corpus
        corpus_name = c["id"].split("-")[1]
        corpus = Corpus(corpora_path + c["directory"] + "/" + c["files"][0])
        print("* " + corpus_name + "...",end="")

        # Computing recognized sentences
        recog_sents = corpus.search(Request('CL_HEAD[ClauseType="Int"]'))
        
        # Retriving and writing the conll of every unique recognized sentence
        sent_ids = set()
        for sent in recog_sents:
            id = sent["sent_id"]

            if not id in sent_ids:
                sent_ids.add(id)

                # Retrieving the conll
                conll = corpus.get(id).to_conll()

                # Writing the conll
                output_file.write(prefix_conll(conll, corpus_name) + "\n")

        n_ids = n_ids + len(sent_ids)
        print(" done")

    # Finishing set s
    output_file.close()
    print("Finished " + s + " set: " + str(n_ids) + " sentences")

