import pandas as pd
import csv
import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
from sklearn.metrics import cohen_kappa_score

##### utils

def scores(tp:int, fp:int, tn: int, fn:int) -> tuple:
    """"Returns the accuracy, precision and recall"""
    accuracy = float(tp + tn) / float(tp + tn + fp + fn)
    precision = float(tp) / float(tp + fp)
    recall = float(tp) / float(tp + fn)
    return accuracy, precision, recall

##### Loading annotations and predictions

programs = ["fudia", "quecq", "simplefudic"]
results = pd.read_csv("results.csv")

preds = {name:{} for name in programs}
gold = {} # list of gold category
number_ann = results.shape[1] - 4 # Number of annotators

for row in results.iterrows():
    id = row[1][0]
    annotations = [row[1][4+i] for i in range(number_ann)]

    # Taking the most occurring element as gold
    gold[id] = int(max(set(annotations), 
                   key = annotations.count))
    
    # Loading predictions
    for i, name in enumerate(programs):
        preds[name][id] = int(row[1][i+1])


##### Compiting inter-annotator agreement
anns = [list(results["ann"+str(1+i)]) 
        for i in range(number_ann)]

anns = np.array(anns)
matrix = aggregate_raters(anns.T)[0]
fleiss = fleiss_kappa(matrix)
print("Fleiss's kappa:", fleiss)

cohen_table = np.zeros((number_ann, number_ann), 
                       dtype=float)
for i in range(number_ann):
    for j in range(number_ann - i):
        cohen_table[i][i+j] = \
            cohen_kappa_score(anns[i], anns[i+j])

print("Cohen kappa matrix:")
print(cohen_table)
print()       

##### Writing gold labels in a file

gold_file = open("gold.csv", "w")
gold_output = csv.writer(gold_file)

for id in gold.keys():
    gold_output.writerow([id, gold[id]])

gold_file.close()

##### Computing scores

for name in programs:

    true_pos_written =  [id for id in gold.keys() 
                         if id.split("_")[0] == "written"
                           and preds[name][id] == 1 
                            and gold[id] == 1]
    false_pos_written = [id for id in gold.keys() 
                         if id.split("_")[0] == "written"
                           and preds[name][id] == 1 
                           and gold[id] == 0]
    true_neg_written =  [id for id in gold.keys() 
                         if id.split("_")[0] == "written"
                           and preds[name][id] == 0 
                           and gold[id] == 0]
    false_neg_written = [id for id in gold.keys() 
                         if id.split("_")[0] == "written"
                           and preds[name][id] == 0 
                           and gold[id] == 1]
    
    true_pos_spoken =  [id for id in gold.keys() 
                         if id.split("_")[0] == "spoken"
                           and preds[name][id] == 1 
                           and gold[id] == 1]
    false_pos_spoken = [id for id in gold.keys() 
                         if id.split("_")[0] == "spoken"
                           and preds[name][id] == 1 
                           and gold[id] == 0]
    true_neg_spoken =  [id for id in gold.keys() 
                         if id.split("_")[0] == "spoken"
                           and preds[name][id] == 0 
                           and gold[id] == 0]
    false_neg_spoken = [id for id in gold.keys() 
                         if id.split("_")[0] == "spoken"
                           and preds[name][id] == 0 
                           and gold[id] == 1]

    tpw = len(true_pos_written)
    fpw = len(false_pos_written)
    tnw = len(true_neg_written)
    fnw = len(false_neg_written)

    tps = len(true_pos_spoken)
    fps = len(false_pos_spoken)
    tns = len(true_neg_spoken)
    fns = len(false_neg_spoken)

    tp = tpw + tps
    fp = fpw + fps
    tn = tnw + tns
    fn = fnw + fns

    print("##### Program "+ name)
    print("### On written:")
    accuracy, precision, recall = scores(tpw, fpw, tnw, fnw)
    print("True positives: ", tpw)
    print("True negatives: ", tnw)
    print("False positives: ", fpw)
    print("False negatives: ", fnw)
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)

    print("### On spoken:")
    accuracy, precision, recall = scores(tps, fps, tns, fns)
    print("True positives: ", tps)
    print("True negatives: ", tns)
    print("False positives: ", fps)
    print("False negatives: ", fns)
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)

    print("### Total:")
    accuracy, precision, recall = scores(tp, fp, tn, fn)
    print("True positives: ", tp)
    print("True negatives: ", tn)
    print("False positives: ", fp)
    if name == "fudia":
        print("\t",false_pos_written+false_pos_spoken)
    print("False negatives: ", fn)
    if name == "fudia":
        print("\t",false_neg_written+false_neg_spoken)
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print()

