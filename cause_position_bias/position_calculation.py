import numpy as np
import random


dic_position = {}
dic_length = {}
#annotated_cause = 2167
#proposed_cause = 210 #2105


dic_probability = {
    "-10": 0.0004,
    "-9": 0.0004,
    "-7": 0.0013,
    "-6": 0.0032,
    "-5": 0.0032,
    "-4": 0.0059,
    "-3": 0.0170,
    "-2": 0.0812,
    "-1": 0.5445,
    "0": 0.2357,
    "1": 0.0747,
    "2": 0.0221,
    "3": 0.0050,
    "4": 0.0018,
    "5": 0.0009,
    "7": 0.0004,
    "8": 0.0009,
    "12": 0.0004,
}

def instance(lst):
    global dic_position
    flag = 0
    for item in lst:
        if item.split(",")[-2] == "yes":
            flag = 1
            if item.split(",")[-3] in dic_position.keys():
                dic_position[item.split(",")[-3]] += 1
            else:
                dic_position[item.split(",")[-3]] = 1
    if flag == 0:
        print("Wrong!", item.split(",")[0])


def instance_length(lst):
    global dic_length
    length = len(lst)
    if length in dic_length.keys():
        dic_length[length] += 1
    else:
        dic_length[length] = 1


def assign_prob(lst):
    label, prob = get_none_exist_prob(lst)
    prob_lst = []
    id_lst = []
    true_label_lst = []
    for item in lst:
        id_lst.append(item.split(",")[4])
        if item.split(",")[5] == "yes":
            true_label_lst.append(item.split(",")[4])
        if item.split(",")[4] in dic_probability.keys():
            if label == True:
                if item.split(",")[4] == "0":
                    prob_lst.append(dic_probability[item.split(",")[4]] + prob)
                else:
                    prob_lst.append(dic_probability[item.split(",")[4]])
            else:
                prob_lst.append(dic_probability[item.split(",")[4]] + prob)
        else:
            if label == False:
                prob_lst.append(prob)
    return (prob_lst, id_lst, true_label_lst)


def get_none_exist_prob(lst):
    sum_prob = 0
    cnt = 0
    for item in lst:
        if item.split(",")[4] in dic_probability.keys():
            sum_prob += dic_probability[item.split(",")[4]]
        else:
            cnt += 1

    if cnt == 0:
        return(True, 1-sum_prob)
    else:
        #return(False, ((1-sum_prob) / cnt))
        return(False, (1-sum_prob) / len(lst))


def predict(prob_lst, id_lst, k):
    np.random.seed(k)
    p = np.array(prob_lst)
    index = np.random.choice(id_lst, p=p.ravel())
    return index


def test_all(k):
    annotated_cause = 0
    correct_cause = 0
    proposed_cause = 2105
    with open("../data/clause_keywords_emotion.txt") as fp:
        line = fp.readline()
        cnt = 1
        lst = []
        while line:

            if line.split(",")[0] == str(cnt):
                lst.append(line.strip())
            else:

                instance(lst)
                instance_length(lst)
                prob_lst, id_lst, true_label_lst = assign_prob(lst)
                annotated_cause += len(true_label_lst)

                pred_val = predict(prob_lst, id_lst, k)
                if pred_val in true_label_lst:
                    correct_cause += 1

                #print(prob_lst, id_lst, pred_val)

                lst = []
                lst.append(line.strip())
                cnt += 1
            #print(line.strip())
            line = fp.readline()
    fp.close()
    prec = correct_cause / proposed_cause
    recall = correct_cause / annotated_cause
    f1 = (2 * prec * recall) / (prec + recall)
    print("Test on all data:")
    print("precision:", prec)
    print("recall:", recall)
    print("f1:", f1)
    return(prec, recall, f1)



def test():
    annotated_cause = 0
    correct_cause = 0
    proposed_cause = 0

    test_id_lst = [random.randint(1, 2106) for _ in range(210)]
    with open("../data/clause_keywords_emotion.txt") as fp:
        line = fp.readline()
        cnt = 1
        lst = []
        while line:

            if line.split(",")[0] == str(cnt):
                lst.append(line.strip())
            else:
                if cnt in test_id_lst:
                    proposed_cause += 1
                    instance(lst)
                    instance_length(lst)
                    prob_lst, id_lst, true_label_lst = assign_prob(lst)
                    annotated_cause += len(true_label_lst)
                    pred_val = predict(prob_lst, id_lst, 1)
                    if pred_val in true_label_lst:
                        correct_cause += 1
                    #print(prob_lst, id_lst, pred_val)

                lst = []
                lst.append(line.strip())
                cnt += 1
            #print(line.strip())
            line = fp.readline()
    fp.close()

    print("-----------------------------------------")
    print("The summary of cause position:", dic_position)
    result_dic = {}
    total = sum(dic_position.values())
    print("Total number of the emotion causes:", total)
    for key, val in dic_position.items():
        result_dic[key] = val / total


    print("The sum of prob:", sum(dic_probability.values()))
    result_dic_position = sorted(result_dic.items(), key=lambda item: item[1], reverse=True)
    print(result_dic_position)


    result_dic_length = sorted(dic_length.items(), key=lambda item: item[1], reverse=True)
    print(result_dic_length)

    print("-------------------------------------------")
    prec = correct_cause / proposed_cause
    recall = correct_cause / annotated_cause
    f1 = (2*prec*recall) / (prec + recall)
    print("precision:", prec)
    print("recall:", recall)
    print("f1:", f1)
    return (prec, recall, f1)



if __name__ == "__main__":
    prec_all_total = 0
    recall_all_total = 0
    f1_all_total = 0
    for i in range(1, 26):
        prec_all, recall_all, f1_all = test_all(1)
        prec_all_total += prec_all
        recall_all_total += recall_all
        f1_all_total += f1_all
    print("Test on all dataset:")
    print("After running 25 times: \n")
    print("precision:", prec_all_total / 25)
    print("recall:", recall_all_total / 25)
    print("f1:", f1_all_total / 25)



    prec_total = 0
    recall_total =0
    f1_total = 0
    for i in range(25):
        prec, recall, f1 = test()
        prec_total += prec
        recall_total += recall
        f1_total += f1
    print("After running 25 times: \n")
    print("precision:", prec_total/25)
    print("recall:", recall_total/25)
    print("f1:", f1_total/25)


