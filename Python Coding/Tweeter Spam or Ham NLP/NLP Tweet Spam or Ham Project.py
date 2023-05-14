"""
This project was a guided project in Natural Language Processing (NLP) to be 
used as a soft introduction to NLP for myself. 

All credits for the walk-through and original code write-up are to be given to 
the origianl author, who is Fares Sayah at:
https://www.kaggle.com/code/faressayah/natural-language-processing-nlp-for-beginners


Some code did need editing for it to run properly and those edits were done by me.
Additionally, several bits of code were changed to match my preferred notation
(primarily referencing pandas columns with square brackets over dot notation).
Lastly, a helper function was added to visualize the Confusion Matrix (cm_plotter)


Thank you!
"""


#importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
import warnings
import string
from nltk.corpus import stopwords
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
warnings.filterwarnings('ignore')

final_scores = {}

#Stylized settings
sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")

# example text for model training (SMS messages)
simple_train = ['call you tonight', 'Call me a cab', 'Please call me... PLEASE!']



#Converting text into a matrix of token counts using CountVectorizer
vect = CountVectorizer()
#Below code learns the vocabulary of the data
vect.fit(simple_train)
vect.get_feature_names_out()

# transform training data into a 'document-term matrix' (dtm)
#Below uses fitted vocabulary to build documentation-term matrix from training data
simple_train_dtm = vect.transform(simple_train)
simple_train_dtm

# convert sparse matrix to a dense matrix
simple_train_dtm.toarray()

# examine the vocabulary and document-term matrix together
pd.DataFrame(simple_train_dtm.toarray(), columns=vect.get_feature_names())


# check the type of the document-term matrix and examine the sparse matrix contents
#   print(type(simple_train_dtm))
#   print(simple_train_dtm)


# example text for model testing
simple_test = ["please don't call me"]

# transform testing data into a document-term matrix (using existing vocabulary)
#Below uses fitted vocabulary to build documentation-term matrix from testing data
# and ignores new words (or tokens) it hasn't encountered before.

simple_test_dtm = vect.transform(simple_test)
simple_test_dtm.toarray()

# examine the vocabulary and document-term matrix together
pd.DataFrame(simple_test_dtm.toarray(), columns=vect.get_feature_names_out())


# read file into pandas using a relative path
sms = pd.read_csv("Raw Data/spam.csv", encoding='latin-1')
#Drop any NAs in the entire dataset inplace.
sms.dropna(how="any", inplace=True, axis=1)
#Rename the columns from v1 and v2 to label and message
sms.columns = ['label', 'message']

#EDA
sms.head()
sms.describe()

sms.groupby('label').describe()
#4825 non-spam (or ham) messages, and 747 spam messages.

# convert label to a numerical variable
spam_mapping = {'ham':0, 
                'spam': 1}
sms['label_num'] = sms.label.map(spam_mapping)
sms.head()
#Mapped correctly

sms['message_len'] = sms['message'].apply(len)
sms.head()


plt.figure(figsize=(10, 6))
sns.histplot(data = sms, x='message_len',
             hue='label', hue_order=['spam', 'ham'],
             bins=35, alpha=0.6)
plt.xlabel('Message Length')
plt.show()

#Looking at the histograms, non-spam messages tend to have many fewer characters,
# while spam messages tend to be many more characters in length.
sms.groupby('label').describe()

#The highest message is 910 characters, and it is not marked as spam!
sms[sms['message_len'] == 910]['message'].iloc[0]


def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    STOPWORDS = stopwords.words('english') + ['u', 'ü', 'ur', '4', '2', 'im', 'dont', 'doin', 'ure']
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    
    # Now just remove any stopwords
    return ' '.join([word for word in nopunc.split() if word.lower() not in STOPWORDS])

sms.head()
sms['clean_msg'] = sms['message'].apply(text_process)
sms.head()

#Ham word counter
words = sms[sms['label']=='ham'].clean_msg.apply(lambda x: [word.lower() 
                                                         for word in x.split()])
ham_words = Counter()
for msg in words:
    ham_words.update(msg)
print(ham_words.most_common(50))

#Spam word counter
words = sms[sms.label=='spam'].clean_msg.apply(lambda x: [word.lower() for word in x.split()])
spam_words = Counter()
for msg in words:
    spam_words.update(msg)
print(spam_words.most_common(50))


# split X and y into training and testing sets 
# how to define X and y (from the SMS data) for use with COUNTVECTORIZER
X = sms['clean_msg']
y = sms['label_num']
# print(X.shape)
# print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# print(X_train.shape)
# print(X_test.shape)
# print(y_train.shape)
# print(y_test.shape)


#Function for plotting confusion matrix
def cm_plotter(cm_variable, title:str, ax=None):

    sns.heatmap(cm_variable, annot=True, cmap='Blues', fmt='g', 
            xticklabels=['Predicted Negative', 'Predicted Positive'], 
            yticklabels=['Actual Negative', 'Actual Positive'],
            ax=ax)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(title +' Confusion Matrix')
    #plt.show()






# instantiate the vectorizer
vect = CountVectorizer()
vect.fit(X_train)

# learn training data vocabulary, then use it to create a document-term matrix
X_train_dtm = vect.transform(X_train)

# equivalently: combine fit and transform into a single step
X_train_dtm = vect.fit_transform(X_train)


# examine the document-term matrix
print(type(X_train_dtm), X_train_dtm.shape)

# transform testing data (using fitted vocabulary) into a document-term matrix
X_test_dtm = vect.transform(X_test)
print(type(X_test_dtm), X_test_dtm.shape)


tfidf_transformer = TfidfTransformer()
tfidf_transformer.fit(X_train_dtm)
tfidf_transformer.transform(X_train_dtm)

#Building Multinomial Naive Bayes Model & Evaluation
nb = MultinomialNB()
# train the model using X_train_dtm (timing it with an IPython "magic command")
%time nb.fit(X_train_dtm, y_train)

# make class predictions for X_test_dtm
y_pred_class = nb.predict(X_test_dtm)

# calculate accuracy of class predictions
print("=======Accuracy Score===========")
nb_score = metrics.accuracy_score(y_test, y_pred_class)
print(nb_score)

final_scores['NB'] = nb_score

# print the confusion matrix
print("=======Confision Matrix===========")
cm_tfidf = metrics.confusion_matrix(y_test, y_pred_class)
cm_plotter(cm_tfidf, 'TFIDF')
plt.show()

# print message text for false positives (ham incorrectly classifier)
# X_test[(y_pred_class==1) & (y_test==0)]
X_test[y_pred_class > y_test]

# print message text for false negatives (spam incorrectly classifier)
X_test[y_pred_class < y_test]

# calculate predicted probabilities for X_test_dtm (poorly calibrated)
y_pred_prob = nb.predict_proba(X_test_dtm)[:, 1]
y_pred_prob


# calculate Area Under the Curve (AUC)
metrics.roc_auc_score(y_test, y_pred_prob)




pipe = Pipeline([('bow', CountVectorizer()), 
                 ('tfid', TfidfTransformer()),  
                 ('model', MultinomialNB())])

pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

# calculate accuracy of class predictions
print("=======Accuracy Score===========")
pipe_score = metrics.accuracy_score(y_test, y_pred)
print(pipe_score)
final_scores['Pipe'] = pipe_score

cm_pipe = metrics.confusion_matrix(y_test, y_pred)
cm_plotter(cm_pipe, 'Pipeline')
plt.show()



#Comparing Models
logreg = LogisticRegression(solver='liblinear')

# train the model using X_train_dtm
%time logreg.fit(X_train_dtm, y_train)


# make class predictions for X_test_dtm
y_pred_class = logreg.predict(X_test_dtm)

# calculate predicted probabilities for X_test_dtm (well calibrated)
y_pred_prob = logreg.predict_proba(X_test_dtm)[:, 1]
y_pred_prob

# calculate accuracy of class predictions
print("=======Accuracy Score===========")
logreg_score = metrics.accuracy_score(y_test, y_pred_class)
print(logreg_score)
final_scores['LogReg'] = logreg_score

# print the confusion matrix
print("=======Confision Matrix===========")
cm_LR = metrics.confusion_matrix(y_test, y_pred_class)
cm_plotter(cm_LR, 'LogReg')
plt.show()


# calculate AUC
print("=======ROC AUC Score===========")
logreg_auc = metrics.roc_auc_score(y_test, y_pred_prob)
print(logreg_auc)
print(metrics.roc_auc_score(y_test, y_pred_prob))


vect = CountVectorizer(stop_words='english')

# include 1-grams and 2-grams
vect = CountVectorizer(ngram_range=(1, 2))
vect = CountVectorizer(max_df=0.5)


print("="*40, "Final Scores", "="*40)
print(pd.DataFrame(final_scores.items(), columns=['Model', 'Score']))
print("="*40, "Plots", "="*47)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

cm_plotter(cm_tfidf, 'TFIDF', ax=ax[0])
cm_plotter(cm_pipe, 'Pipeline', ax=ax[1])
cm_plotter(cm_LR, 'LogReg', ax=ax[2])
ax[0].set_title('TFIDF Confusion Matrix')
ax[1].set_title('Pipeline Confusion Matrix')
ax[2].set_title('LogReg Confusion Matrix')
plt.show()

#Without further tuning, looks like LogReg performed the best based on accuracy score.