import csv

##### utils

def scores(tp:int, fp:int, tn: int, fn:int) -> tuple:
    """"Returns the accuracy, precision and recall"""
    accuracy = float(tp + tn) / float(tp + tn + fp + fn)
    precision = float(tp) / float(tp + fp)
    recall = float(tp) / float(tp + fn)
    return accuracy, precision, recall

##### Loading annotations and predictions

programs = ["fudia", "quecq", "simplefudic"]
results_file = open("results.csv")
results = csv.reader(results_file)

preds = {name:{} for name in programs}
gold = {}
header = True

for row in results:
    id = row[0]
    annotations = row[4:]

    # Ignoring header
    if header:
        header = False
        continue

    # Taking the most occurring element as gold
    gold[id] = int(max(set(annotations), 
                   key = annotations.count))
    
    # Loading predictions
    for i, name in enumerate(programs):
        preds[name][id] = int(row[i+1])

results_file.close()

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

