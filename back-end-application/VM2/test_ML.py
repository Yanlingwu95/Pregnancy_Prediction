import sendemail_attachment
import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def ML_prediction(filename, classifier):
    data = pd.read_csv(filename)
    trn = data.iloc[:,1:-1]
    pickle_file = open(classifier,'rb')
    clf = pickle.load(pickle_file)
    label = clf.predict(trn)
    with open("pre_result.txt","w") as f:
        f.write("pregnant_cow_ID \t Group_ID\n")
        f.close()
    with open("pre_result.txt","a") as f:
        for i in range(len(label)):
            if label[i] == 0:
                f.write(str(i)+"\t"+str(i+10)+"\n")
        f.close()

ML_prediction('real_time_data2.csv','ML_Model_DecisionTree.pickle')
sendemail_attachment.sendemail()

