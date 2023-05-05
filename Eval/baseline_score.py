import csv

##### utils

def get_list(filename:str) -> list:
    """"Returns the list of all lines in filename"""
    file = open(filename, "r")
    l = []
    for line in file:
        l.append(line.strip('\n'))
    file.close()
    return l

##### Opening readers

CORPUS_DIR = "/home/varichar/Documents/PhD/Corpus/"
FUDIA_EVAL_DIR = "/home/varichar/Documents/PhD/FUDIA/Eval/"
baseline_ids_filenames =  [CORPUS_DIR + "FUDIA-eval/baseline1/positive_ids"]
baseline_ids_filenames += [CORPUS_DIR + "FUDIA-eval/baseline2/positive_ids"]

eval_ids_filename = FUDIA_EVAL_DIR + "eval_set_ids"
all_target_positive_ids_filename = FUDIA_EVAL_DIR + "all_target_positive_ids"

baseline_positives = []
for i, bl_f in enumerate(baseline_ids_filenames):
    baseline_positives.append(get_list(bl_f))

eval_ids = get_list(eval_ids_filename)
all_target_positive_ids = get_list(all_target_positive_ids_filename)


##### Computing scores

for i in range(len(baseline_positives)):

    true_positives =  [idx for idx in baseline_positives[i] if idx in all_target_positive_ids]
    false_postivies = [idx for idx in baseline_positives[i] if idx not in true_positives]
    true_negatives =  [idx for idx in eval_ids if idx not in baseline_positives[i] and idx not in all_target_positive_ids]
    false_negatives = [idx for idx in eval_ids if idx not in baseline_positives[i] and idx in all_target_positive_ids]

    tp = len(true_positives)
    fp = len(false_postivies)
    tn = len(true_negatives)
    fn = len(false_negatives)

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    print("##### Baseline ", i+1)
    print("True positives: ", tp)
    print("True negatives: ", tn)
    print("False positives: ", fp)
    print("False negatives: ", fn)
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)

