from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC  
import itertools
import matplotlib.pyplot as plt
import pandas 
import pickle

def get_all_data():
    root = "Data/"
    
    with open(root + "yelp_labelled.txt", "r") as text_file:
        data = text_file.read().split('\n')
    with open(root + "amazon_cells_labelled.txt", "r") as text_file:
        data += text_file.read().split('\n')

    with open(root + "imdb_labelled.txt", "r") as text_file:
       data += text_file.read().split('\n')
    
       

    return data

def preprocessing_data(data):
    processing_data = []
    for single_data in data:
        if len(single_data.split("\t")) == 2 and single_data.split("\t")[1] != "":
            processing_data.append(single_data.split("\t"))

    return processing_data
def split_data(data):
    total = len(data)//3 #sadece yelp yorumlarından test secmek icin
    training_ratio = 0.25
    training_data = []
    evaluation_data = []
    
    for indice in range(0, total):
        if indice < total * training_ratio:
            training_data.append(data[indice])
        else:
            evaluation_data.append(data[indice])
    
    for indice in range(1001,total*3):
            training_data.append(data[indice])
           

    return training_data, evaluation_data


def preprocessing_step():
    data = get_all_data()
    processing_data = preprocessing_data(data)

    return split_data(processing_data)


def training_step(data, vectorizer):
    training_text = [data[0] for data in data]
    training_result = [data[1] for data in data] 
    training_text = vectorizer.fit_transform(training_text) 
 
    return BernoulliNB().fit(training_text, training_result)

def analyse_text(classifier, vectorizer, text):
    return text, classifier.predict(vectorizer.transform([text]))
  
def print_result(result):
    text, analysis_result = result
    print_text = "Positive" if analysis_result[0] == '1' else "Negative"
    print(text, ":", print_text)
    
def simple_evaluation(evaluation_data):
    evaluation_text     = [evaluation_data[0] for evaluation_data in evaluation_data]
    evaluation_result   = [evaluation_data[1] for evaluation_data in evaluation_data]

    total = len(evaluation_text)
    corrects = 0
    for index in range(0, total):
        analysis_result = analyse_text(classifier, vectorizer, evaluation_text[index])
        text, result = analysis_result
        corrects += 1 if result[0] == evaluation_result[index] else 0
        print (corrects * 100 / total)
    return corrects * 100 / total

def create_confusion_matrix(evaluation_data):
    evaluation_text     = [evaluation_data[0] for evaluation_data in evaluation_data]
    actual_result       = [evaluation_data[1] for evaluation_data in evaluation_data]
    prediction_result   = []
    for text in evaluation_text:
        analysis_result = analyse_text(classifier, vectorizer, text)
        prediction_result.append(analysis_result[1][0])
    
    matrix = confusion_matrix(actual_result, prediction_result)
    return matrix

from sklearn.feature_extraction.text import TfidfVectorizer 

def training_step2(data, vectorizer,comm):
    training_text2 = [data[0] for data in data]
    training_result2 = [data[1] for data in data]
    testing_text2 = [evaluation_data[0] for evaluation_data in evaluation_data]
    testing_result2 =[evaluation_data[1] for evaluation_data in evaluation_data]
 
        
    training_text2 = vectorizer.fit_transform(training_text2)
    testing_text2 = vectorizer.transform(testing_text2)
         
    svc=SVC(kernel="rbf")
   
    svc.fit(training_text2, training_result2)
   
    stahmin=svc.predict(testing_text2)

    
    dbfile = open('SupportVectorvectorizer', 'ab') 
    pickle.dump(vectorizer, dbfile)
    dbfile.close() 

    
    dbfile = open('svc', 'ab') 
    pickle.dump(svc, dbfile)
    dbfile.close()
    
    
    print("SVC")
    cm=confusion_matrix(testing_result2,stahmin)
    dbfile = open('confusionMatrix', 'ab') 
    pickle.dump(cm, dbfile)
    dbfile.close()
    
    
    print(cm)
    accu2=(cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1])
    print("SVC Accuracy")
    print(accu2) 
            
    return svc.predict(vectorizer.transform([comm]))
    
    
training_data, evaluation_data = preprocessing_step()
vectorizer = CountVectorizer(binary = 'true') 
classifier = training_step(training_data, vectorizer)

training_data2, evaluation_data2 = preprocessing_step() 
vectorizer2 = TfidfVectorizer(min_df = 5,
                             max_df = 0.8,
                             sublinear_tf = True,
                             use_idf = True)


confusion_matrix_result=create_confusion_matrix(evaluation_data)

dbfile = open('BayesConfusionMatrix', 'ab') 
pickle.dump(confusion_matrix_result, dbfile)
dbfile.close()
accu=(confusion_matrix_result[0][0]+confusion_matrix_result[1][1])/(confusion_matrix_result[0][0]+confusion_matrix_result[0][1]+confusion_matrix_result[1][0]+confusion_matrix_result[1][1])
print("Bayes Accuracy")
print(accu)

#cm=confusion_matrix(ytest,training_step2)
 

dbfile = open('Bayesvectorizer', 'ab') 
pickle.dump(vectorizer, dbfile)
dbfile.close() 

dbfile = open('BayesClassifier', 'ab') 
pickle.dump(classifier, dbfile)
dbfile.close() 
 
def BayesPredict(comm): 
    result = classifier.predict(vectorizer.transform([comm]))
    if result[0]=='0':
        a=0 
    else:
        a=1  
    return a  
def SVCPredict(comm): 
    result=training_step2(training_data2, vectorizer2,comm)
    if result[0]=='0':
        a=0 
    else:
        a=1  
    return a   
a=SVCPredict("Good Place")