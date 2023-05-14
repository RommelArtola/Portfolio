"""
This project was a guided project in Machine Learning to be used as a soft 
introduction to ML for myself. 

All credits for an extensive write-up are to be given to the origianl author, who
is Yvon Dalat, and whoever they also mention in their footer: 
https://www.kaggle.com/code/ydalat titanic-a-step-by-step-intro-to-machine-learning


Some code did need editing for it to run properly and those edits were done by me.
Additionally, some minor edits were performed in certain instances were 
hard-coded values were being passed/assigned, instead of choosing
random values from np.random.choice(). 

Thank you!
"""

# Load libraries for analysis and visualization
import pandas as pd 
import numpy as np  
import re           # Regular expression operations
import matplotlib.pyplot as plt 
#import plotly.offline as py     
from collections import Counter

# Machine learning libraries
import xgboost as xgb  # Implementation of gradient boosted decision trees designed for speed and performance that is dominative competitive machine learning
import seaborn as sns 

import sklearn         # Collection of machine learning algorithms
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier, 
                              GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier)
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report, precision_recall_curve, confusion_matrix

import warnings
warnings.filterwarnings('ignore')



# Load in the train and test datasets from the CSV files using relative paths.
train = pd.read_csv('Raw Data/train.csv')
test = pd.read_csv('Raw Data/test.csv')

# We'll seperate our passanger ID for easy access
PassengerId = test['PassengerId']

# Display the first 5 rows of the dataset, a first look at our data
train.head(5)


train.sample(5)

# Overview of the data using describe.
train.describe()


#Our outcome/dependant variable is whether a passanger survived or not, and it is a binary value
# All other columns may serve as a predictor variable.


#Create subplots of 3 rows 4 columns, and 20x16 sizes.
f,ax = plt.subplots(3,4,figsize=(15,16))


#A countplot counting Pclass in our train dataset, and placing on top left chart.
sns.countplot(x = 'Pclass',data=train,ax=ax[0,0])

#A countplot to show count of sex, and placing on the right of our hist above.
sns.countplot(x = 'Sex',data=train,ax=ax[0,1])

#Boxplot distribution of age across Pclasses, placing on the next right.
sns.boxplot(x='Pclass',y='Age',data=train,ax=ax[0,2])

#Countplot of the count of individuals survived by the number of sibilings/spouse aboard with them
sns.countplot(x = 'SibSp',hue='Survived',data=train,ax=ax[0,3],palette='husl')

#A distribution plot on our Fare column with an overlayed kernel density estimator curve
sns.distplot(train['Fare'].dropna(),ax=ax[2,0],kde=True,color='b')

#A countplot of where passangers embarked from with their code where:
#{C:Cherbourg, Q: Queenstown, S: Southampton}
sns.countplot(x = 'Embarked',data=train,ax=ax[2,2])

#A countplot of our passanger classes and split up by whether or not they survived.
sns.countplot(x = 'Pclass',hue='Survived',data=train,ax=ax[1,0],palette='husl')

#A countplot of the sex of our passangers and whether or not they survived
sns.countplot(x = 'Sex',hue='Survived',data=train,ax=ax[1,1],palette='husl')

#Filtering train dataset to select the Age where the column survived == 0 to show a distplot of age by survival count

#Same as above applies for the below, but this one is for those who did survived, or survived == 1. 
#Where red is for those who did not survived, and green is for those who did. 
sns.distplot(train[train['Survived']==0]['Age'].dropna(),ax=ax[1,2],kde=False,color='r',bins=5, label = '0')
sns.distplot(train[train['Survived']==1]['Age'].dropna(),ax=ax[1,2],kde=False,color='g',bins=5, label = '1')
# Add legend to the plot
ax[1, 2].legend(title = 'Survived')


#A countplot of passangers that survived based on the number of parents/children aboard.
sns.countplot(x = 'Parch',hue='Survived',data=train,ax=ax[1,3],palette='husl')

#A swarmplot that shows distribution and density of whether a passanger survived and their fare cost split by passanger class
sns.swarmplot(x='Pclass',y='Fare',hue='Survived',data=train,palette='husl',ax=ax[2,1])

#And finally, a countplot of the count of passangers that survived split by their location of embarkment, again where:
#{C:Cherbourg, Q: Queenstown, S: Southampton}
sns.countplot(x = 'Embarked',hue='Survived',data=train,ax=ax[2,3],palette='husl')






# Outlier detection 
def detect_outliers(df,n,features):
    outlier_indices = []
    # iterate over features(columns)
    for col in features:
        # 1st quartile (25%)
        Q1 = np.percentile(df[col],25)
        # 3rd quartile (75%)
        Q3 = np.percentile(df[col],75)
        # Interquartile range (IQR)
        IQR = Q3 - Q1
        # outlier step
        outlier_step = 1.5 * IQR
        # Determine a list of indices of outliers for feature col
        #Need to compare using the vertical bar to work directly for element-wise boolean operations.
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step )].index       
        # extend the found outlier indices for col to the list of outlier indices 
        outlier_indices.extend(outlier_list_col)
        
    # select observations containing more than n outliers
    outlier_indices = Counter(outlier_indices)        
    multiple_outliers = list( k for k, v in outlier_indices.items() if v > n )
    return multiple_outliers   

# detect outliers from Age, SibSp , Parch and Fare using index values on a list
Outliers_to_drop = detect_outliers(train,2,["Age","SibSp","Parch","Fare"])
len(Outliers_to_drop) #We have 10 outliers
train.loc[Outliers_to_drop] # Show the outliers rows

#Removal of outliers lowers the predictions, so they will be kept, however, they can be dropped using the below commented code
# Drop outliers
# train = train.drop(Outliers_to_drop, axis = 0).reset_index(drop=True)

#Data is split roughly into 2/3 for train, and 1/3 for test.
train.info()
print('_'*40)
test.info()


#Let's start doing some descriptive analytics on this.
full_data = [train, test]
Survival = train['Survived']
Survival.describe()

#Feature Engineering to convert variables into numerical values
#{C:Cherbourg, Q: Queenstown, S: Southampton}
#Below we will look at the rate of survivial by gender and Embarked area
sns.barplot(x="Embarked", y="Survived", hue="Sex", data=train)


#Let's determine wheteher we can remove this predictor or not from our model
#Adding name length column to train and test dataset.
for dataset in full_data:
    dataset['Name_length'] = train['Name'].apply(len)
    # Qcut is a quantile based discretization function to automatically create categories
    # dataset['Name_length'] = pd.qcut(dataset['Name_length'], 6, labels=False)
    # train['Name_length'].value_counts()

#Getting a length of Name
sum_Name = train[["Name_length", "Survived"]].groupby(['Name_length'],as_index=False).sum()
#Getting the mean of survival rate by name length
average_Name = train[["Name_length", "Survived"]].groupby(['Name_length'],as_index=False).mean()

fig, (axis1,axis2) = plt.subplots(2,1,figsize=(18,6))
#Plotting survivability grouped by length of name
## First plot is absolute count of survivalists by name length
sns.barplot(x='Name_length', y='Survived', 
            data=sum_Name, ax = axis1, color='#efc0fe')
## Second plot is mean survival by name length
sns.barplot(x='Name_length', y='Survived', 
            data=average_Name, ax = axis2, color='#82cafc')
## Last plot is the same as above but in pointplot format. I prefer the top, so I will leave commented out.
# sns.pointplot(x = 'Name_length', y = 'Survived', 
#               data=train, ax = axis3)





for dataset in full_data:
    #Assigning value of 0 where name_lenght <= 23
    dataset.loc[ dataset['Name_length'] <= 23, 'Name_length'] = 0
    #Value of 1 given the range
    dataset.loc[(dataset['Name_length'] > 23) & (dataset['Name_length'] <= 28), 'Name_length']  = 1
    #Value of 2 given the range
    dataset.loc[(dataset['Name_length'] > 28) & (dataset['Name_length'] <= 40), 'Name_length']  = 2
    #Value of 3 given teh range
    dataset.loc[ dataset['Name_length'] > 40, 'Name_length'] = 3
train['Name_length'].value_counts()


#Mapping and overriding values of sex from categorical to numeric/binary.
for dataset in full_data:# Mapping Gender
    dataset['Sex'] = dataset['Sex'].map( {'female': 0, 'male': 1} ).astype(int)   


#plot distributions of age of passengers who survived or did not survive
a = sns.FacetGrid(train, hue = 'Survived', aspect=6 )
a.map(sns.kdeplot, 'Age', shade= True )
#X limits by age of 0 and max value in column age.
a.set(xlim=(0 , train['Age'].max()))
a.add_legend()


#Seems like the best categories for survival in age are about:
# 1: 0-14,
# 2: 30-40,
# 3: 50-57



for dataset in full_data:
    age_avg = dataset['Age'].mean()
    age_std = dataset['Age'].std()
    age_null_count = dataset['Age'].isnull().sum()
    #Will fill in empty ages based on the mean and std values.
    age_null_random_list = np.random.randint(age_avg - age_std, age_avg + age_std, size=age_null_count)
    dataset['Age'][np.isnan(dataset['Age'])] = age_null_random_list
    dataset['Age'] = dataset['Age'].astype(int)
# Qcut is a quantile based discretization function to autimatically create categories (not used here)
# dataset['Age'] = pd.qcut(dataset['Age'], 6, labels=False)
# Using categories as defined above
    dataset.loc[ dataset['Age'] <= 14, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 14) & (dataset['Age'] <= 30), 'Age'] = 5
    dataset.loc[(dataset['Age'] > 30) & (dataset['Age'] <= 40), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 40) & (dataset['Age'] <= 50), 'Age'] = 3
    dataset.loc[(dataset['Age'] > 50) & (dataset['Age'] <= 60), 'Age'] = 2
    dataset.loc[ dataset['Age'] > 60, 'Age'] = 4
train['Age'].value_counts()


#Survival Rate by age.
train[["Age", "Survived"]].groupby(['Age'], as_index=False).mean().sort_values(by='Survived', ascending=False)




for dataset in full_data:
# Create new feature FamilySize as a combination of SibSp and Parch
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch']+1
# Create new feature IsAlone from FamilySize
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1
    
# Create new feature Boys from FamilySize
#Where "boys" are male that are 14 years old or less.
    dataset['Boys'] = 0
    dataset.loc[(dataset['Age'] == 0) & (dataset['Sex']==1), 'Boys'] = 1
    
fig, (axis1,axis2) = plt.subplots(1,2,figsize=(18,6))
sns.barplot(x="FamilySize", y="Survived", hue="Sex", data=train, ax = axis1)
sns.barplot(x="IsAlone", y="Survived", hue="Sex", data=train, ax = axis2)

#Being alone doesn't seem to be a good predictor of likeliness of survival.
#However, seems like having a family size of 5 or greater, greatly impacts rate
## of survival.

# Interactive chart using cufflinks
import cufflinks as cf
cf.go_offline()
train['Fare'].iplot(kind='hist', bins=30)



# Remove all NULLS in the Fare column and create a new feature Categorical Fare
for dataset in full_data:
    #Filling the NAs with the median fare to avoid skewness in 
    # fare paid by using mean.
    dataset['Fare'] = dataset['Fare'].fillna(train['Fare'].median())

# Explore Fare distribution 
#Very left-skewed histogram
g = sns.distplot(dataset["Fare"], color="m", label="Skewness : %.2f"%(dataset["Fare"].skew()))
g = g.legend(loc="best")


#Let's handle the skewness by using logarithmic conversion of the Fare paid.
for dataset in full_data:
    dataset["Fare"] = dataset["Fare"].map(lambda x: np.log(x) if x > 0 else 0)
fig, ax = plt.subplots(figsize=(20,6))
g = sns.distplot(train["Fare"][train["Survived"] == 0], color="r", label="Skewness : %.2f"%(train["Fare"].skew()), ax=ax)
g = sns.distplot(train["Fare"][train["Survived"] == 1], color="b", label="Skewness : %.2f"%(train["Fare"].skew()))
#g = g.legend(loc="best")
g = g.legend(["Not Survived","Survived"])


#We've observed that log fare of 2.7 to 0, we find less survivors, and we find
#more survivors where log fare > 2.7
for dataset in full_data:
    dataset.loc[ dataset['Fare'] <= 2.7, 'Fare'] = 0
#    dataset.loc[(dataset['Fare'] > 2.7) & (dataset['Fare'] <= 3.2), 'Fare'] = 1
#    dataset.loc[(dataset['Fare'] > 3.2) & (dataset['Fare'] <= 3.6), 'Fare'] = 2
    dataset.loc[ dataset['Fare'] > 2.7, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int)
train['Fare'].value_counts()


#Let's analyze the Cabin feature
# Feature that tells whether a passenger had a cabin on the Titanic 
# (O if no cabin number, 1 otherwise)
for dataset in full_data:
    #np.nan is a datatype float.
    dataset['Has_Cabin'] = dataset["Cabin"].apply(lambda x: 0 if type(x) == float else 1)

#Sum counter
train[["Has_Cabin", "Survived"]].groupby(['Has_Cabin'], as_index=False).sum().sort_values(by='Survived', ascending=False)

#Mean value
train[["Has_Cabin", "Survived"]].groupby(['Has_Cabin'], as_index=False).mean().sort_values(by='Survived', ascending=False)


#Let's analyze the embarked feature
for dataset in full_data:
# Remove all NULLS in the Embarked column
    dataset['Embarked'] = dataset['Embarked'].fillna(np.random.choice(['S', 'C', 'Q']))
# Mapping Embarked
    dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)
    
train_pivot = pd.pivot_table(train, values= 'Survived',
                             index=['Embarked'],columns='Pclass',
                             aggfunc=np.mean, margins=True)

def color_negative_red(val):
    # Takes a scalar and returns a string with the css property 'color: red' if below 0.4, green otherwise.
    color = 'red' if val < 0.4 else 'green'
    return 'color: %s' % color


train_pivot = train_pivot.style.applymap(color_negative_red)
train_pivot

#Seems like regardless of where someone Embarks from, all 3rd class suffer from
#low probability of survival. 
#Likewise, regardless of class, embarking from S has the lowest survival rate.
for dataset in full_data:
    dataset['Pclass'] = dataset['Pclass'].replace(3, 0)

train['Pclass'].value_counts()






#Let's Analyze Titles:
# Define function to extract titles from passenger names
def get_title(name):
    title_search = re.search(' ([A-Za-z]+)\.', name)
 # If the title exists, extract and return it.
    return title_search.group(1) if title_search else ""

for dataset in full_data:
# Create a new feature Title, containing the titles of passenger names
    dataset['Title'] = dataset['Name'].apply(get_title)

fig, (axis1) = plt.subplots(1,figsize=(18,6))
sns.barplot(x="Title", y="Survived", data=train, ax=axis1)


# There are 4 types of title groups:
# 0. Mme, Ms, Lady, Sir, Mlle, Countess: 100%. 
# 1. Mrs, Miss: around 70% survival
# 2. Master: around 60%
# 3. Don, Rev, Capt, Jonkheer: no data
# 4. Dr, Major, Col: around 40%
# 5. Mr: below 20%


for dataset in full_data:
    dataset['Title'] = dataset['Title'].replace(['Mrs', 'Miss'], 'MM')
    dataset['Title'] = dataset['Title'].replace(['Dr', 'Major', 'Col'], 'DMC')
    dataset['Title'] = dataset['Title'].replace(['Don', 'Rev', 'Capt', 'Jonkheer'],'DRCJ')
    dataset['Title'] = dataset['Title'].replace(['Mme', 'Ms', 'Lady', 'Sir', 'Mlle', 'Countess'],'MMLSMC' )
# Mapping titles
    title_mapping = {"MM": 1, "Master":2, "Mr": 5, "DMC": 4, "DRCJ": 3, "MMLSMC": 0}
    dataset['Title'] = dataset['Title'].map(title_mapping)
    #Added random here.
    dataset['Title'] = dataset['Title'].fillna(np.random.choice([i for i in title_mapping.values()]))
    

train[["Title", "Survived"]].groupby(['Title'], as_index=False).mean().sort_values(by='Survived', ascending=False)





#Let's extract deck from cabin
deck_map = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}
for dataset in full_data:
    dataset['Cabin'] = dataset['Cabin'].fillna("U0")
    dataset['Deck'] = dataset['Cabin'].map(lambda x: re.compile("([a-zA-Z]+)").search(x).group())
    dataset['Deck'] = dataset['Deck'].map(deck_map)
    dataset['Deck'] = dataset['Deck'].fillna(0)
    dataset['Deck'] = dataset['Deck'].astype(int) 
train['Deck'].value_counts()

#Let's plot deck info
sns.barplot(x ='Deck', y = 'Survived', data=train.loc[train["Deck"] != 0])#, ci=None)


for dataset in full_data:
    dataset.loc[ dataset['Deck'] <= 1, 'Deck'] = 1
    dataset.loc[(dataset['Deck'] > 1) & (dataset['Deck'] <= 6), 'Deck']  = 3
    dataset.loc[ dataset['Deck'] > 6, 'Deck'] = 0
train[["Deck", "Survived"]].groupby(['Deck'], as_index=False).mean().sort_values(by='Survived', ascending=False)


train.head(5), test.head(5)



#Descriptive Stats
train.describe()
#Only 38% of the passangers survived
train[['Pclass', 'Sex', 'Age', 'Parch', 'Fare', 'Embarked', 'Has_Cabin', 'FamilySize', 'Title', 'Survived']].groupby(['Survived'], as_index=False).mean().sort_values(by='Pclass', ascending=False)


#Correlation Analysis
fig, (axis1,axis2) = plt.subplots(1,2,figsize=(18,6))
sns.barplot(x="Embarked", y="Survived", hue="Sex", data=train, ax = axis1);
sns.barplot(x="Age", y="Survived", hue="Sex", data=train, ax = axis2);

#Family size and survival rates
train[["FamilySize", "Survived"]].groupby(['FamilySize'], as_index=False).mean().sort_values(by='Survived', ascending=False)


for dataset in full_data:
    dataset['Gender_Embarked'] = 0
    dataset.loc[(dataset['Sex']==0) & (dataset['Embarked']==0), 'Gender_Embarked'] = 0
    dataset.loc[(dataset['Sex']==0) & (dataset['Embarked']==2), 'Gender_Embarked'] = 1
    dataset.loc[(dataset['Sex']==0) & (dataset['Embarked']==1), 'Gender_Embarked'] = 2
    dataset.loc[(dataset['Sex']==1) & (dataset['Embarked']==2), 'Gender_Embarked'] = 3
    dataset.loc[(dataset['Sex']==1) & (dataset['Embarked']==0), 'Gender_Embarked'] = 4
    dataset.loc[(dataset['Sex']==1) & (dataset['Embarked']==1), 'Gender_Embarked'] = 5
train[["Gender_Embarked", "Survived"]].groupby(['Gender_Embarked'], as_index=False).mean().sort_values(by='Survived', ascending=False)


train_pivot = pd.pivot_table(train, values= 'Survived',index=['Title', 'Pclass'],columns='Sex',aggfunc=np.mean, margins=True)


train_pivot = train_pivot.style.applymap(color_negative_red)
train_pivot

#grid = sns.FacetGrid(train_df, col='Pclass', hue='Survived')
grid = sns.FacetGrid(train, col='Survived', row='Pclass', aspect=3)
grid.map(plt.hist, 'Age', alpha=.5, bins=8)
grid.add_legend();


#graph distribution of qualitative data: Pclass
fig, (axis1,axis2,axis3) = plt.subplots(1,3,figsize=(18,8))

sns.boxplot(x = 'Pclass', y = 'Fare', hue = 'Survived', data = train, ax = axis1)
axis1.set_title('Pclass vs Fare Survival Comparison')

sns.violinplot(x = 'Pclass', y = 'Age', hue = 'Survived', data = train, split = True, ax = axis2)
axis2.set_title('Pclass vs Age Survival Comparison')

sns.boxplot(x = 'Pclass', y ='FamilySize', hue = 'Survived', data = train, ax = axis3)
axis3.set_title('Pclass vs Family Size Survival Comparison')


fig, saxis = plt.subplots(2, 3,figsize=(20,10))

sns.barplot(x = 'Embarked', y = 'Survived', data=train, ax = saxis[0,0])
sns.barplot(x = 'Pclass', y = 'Survived', order=[1,2,3], data=train, ax = saxis[0,1])
sns.barplot(x = 'Deck', y = 'Survived', order=[1,0], data=train, ax = saxis[0,2])

sns.pointplot(x = 'Fare', y = 'Survived',  data=train, ax = saxis[1,0])
sns.pointplot(x = 'Age', y = 'Survived',  data=train, ax = saxis[1,1])
sns.pointplot(x = 'FamilySize', y = 'Survived', data=train, ax = saxis[1,2])

# grid = sns.FacetGrid(train_df, col='Embarked')
grid = sns.FacetGrid(train, row='Has_Cabin', aspect=1.2)
grid.map(sns.pointplot, 'Parch', 'Survived', 'Sex', palette='deep')
grid.add_legend(title='Sex')


#Let's begin dropping features
# Feature selection
drop_elements = ['PassengerId', 'Name', 'Ticket', 'Cabin', 'SibSp', 'Boys', 'IsAlone', 'Embarked']

train = train.drop(drop_elements, axis = 1)
test  = test.drop(drop_elements, axis = 1)

#Pearson Correlation Heatmap
colormap = plt.cm.seismic.reversed()
plt.figure(figsize=(14,12))
plt.title('Pearson Correlation of Features', y=1.05, size=15)
sns.heatmap(train.astype(float).corr(),linewidths=0.1,vmax=1.0, square=True, cmap=colormap, linecolor='black', annot=True)

#Values of about 0.5 to 0.7 are at least moderately correlated.



g = sns.pairplot(train[['Survived', 'Pclass', 'Sex', 'Age', 'Fare',
       'FamilySize', 'Title']], hue='Survived', palette = 'seismic', size=1.2,
       diag_kind = 'kde',
       diag_kws={'shade':True},
       plot_kws={'s': 10})

g.set(xticklabels=[])

#Clustering of red dots in combinations indicate higher survival rates, 
#whereas blue clustering shows the opposite.

# X_train (all features for training purpose but excluding Survived),
# Y_train (survival result of X-Train) and test are our 3 main datasets for the next sections
X_train = train.drop("Survived", axis=1)
Y_train = train["Survived"]
X_train.shape, Y_train.shape, test.shape

X_train, x_test, Y_train, y_test = train_test_split(X_train, Y_train, test_size=0.3, random_state=101)

#X_test = test.copy() # test data for Kaggle submission
#std_scaler = StandardScaler()
#X_train = std_scaler.fit_transform(X_train)
#X_test = std_scaler.transform(X_test)

#Logistics Regression
logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
Y_pred1 = logreg.predict(x_test)
acc_log = round(logreg.score(x_test, y_test) * 100, 2)
acc_log

print(classification_report(y_test, Y_pred1))
cm = pd.DataFrame(confusion_matrix(y_test, Y_pred1), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)



#Support Vector Machines 
svc=SVC()
svc.fit(X_train, Y_train)
Y_pred2 = svc.predict(x_test)
acc_svc = round(svc.score(x_test, y_test) * 100, 2)
acc_svc

print(classification_report(y_test, Y_pred2))
cm = pd.DataFrame(confusion_matrix(y_test, Y_pred2), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)


#k-Nearest Neighbors Algorithm
knn = KNeighborsClassifier(algorithm='auto', leaf_size=26, metric='minkowski', 
                           metric_params=None, n_jobs=1, n_neighbors=10, p=2, 
                           weights='uniform')
knn.fit(X_train, Y_train)
knn_predictions = knn.predict(x_test)
acc_knn = round(knn.score(x_test, y_test) * 100, 2)

# Preparing data for Submission 1
test_Survived = pd.Series(knn_predictions, name="Survived")
Submission1 = pd.concat([PassengerId,test_Survived],axis=1)
acc_knn

print(classification_report(y_test, knn_predictions))
cm = pd.DataFrame(confusion_matrix(y_test, knn_predictions), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)


Submission1.head(5)



## Selecting the right n_neighbors for the k-NN classifier
x_trainknn, x_testknn, y_trainknn, y_testknn = train_test_split(X_train,Y_train,test_size = .33, random_state = 0)
nn_scores = []
best_prediction = [-1,-1]
for i in range(1,100):
    knn = KNeighborsClassifier(n_neighbors=i, 
                               weights='distance', 
                               metric='minkowski',
                               p=2)
    knn.fit(x_trainknn, y_trainknn)
    score = accuracy_score(y_testknn, knn.predict(x_testknn))
    #print i, score
    if score > best_prediction[1]:
        best_prediction = [i, score]
    nn_scores.append(score)
print (best_prediction)
plt.plot(range(1,100),nn_scores)



#Naive Bayes Classifier
gaussian = GaussianNB()
gaussian.fit(X_train, Y_train)
Y_pred3 = gaussian.predict(x_test)
acc_gaussian = round(gaussian.score(x_test, y_test) * 100, 2)
acc_gaussian

print(classification_report(y_test, Y_pred3))
cm = pd.DataFrame(confusion_matrix(y_test, Y_pred3), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)


#Perceptron
perceptron = Perceptron()
perceptron.fit(X_train, Y_train)
Y_pred4 = perceptron.predict(x_test)
acc_perceptron = round(perceptron.score(x_test, y_test) * 100, 2)
acc_perceptron


print(classification_report(y_test, Y_pred4))
cm = pd.DataFrame(confusion_matrix(y_test, Y_pred4), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)


#Linear SVC
linear_svc = LinearSVC()
linear_svc.fit(X_train, Y_train)
Y_pred5 = linear_svc.predict(x_test)
acc_linear_svc = round(linear_svc.score(x_test, y_test) * 100, 2)
acc_linear_svc

print(classification_report(y_test, Y_pred5))
cm = pd.DataFrame(confusion_matrix(y_test, Y_pred5), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)


#Stochastic Gradient Descent (SGD)
sgd = SGDClassifier()
sgd.fit(X_train, Y_train)
Y_pred6 = sgd.predict(x_test)
acc_sgd = round(sgd.score(x_test, y_test) * 100, 2)
acc_sgd

print(classification_report(y_test, Y_pred6))
cm = pd.DataFrame(confusion_matrix(y_test, Y_pred6), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)


#Decision Tree
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, Y_train)
Y_pred7 = decision_tree.predict(x_test)
acc_decision_tree = round(decision_tree.score(x_test, y_test) * 100, 2)
acc_decision_tree

print(classification_report(y_test, Y_pred7))
cm = pd.DataFrame(confusion_matrix(y_test, Y_pred7), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)



#Random Forest
random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, Y_train)
random_forest_predictions = random_forest.predict(x_test)
acc_random_forest = round(random_forest.score(x_test, y_test) * 100, 2)


# Preparing data for Submission 2
test_Survived = pd.Series(random_forest_predictions, name="Survived")
Submission2 = pd.concat([PassengerId,test_Survived],axis=1)
acc_random_forest

print(classification_report(y_test, random_forest_predictions))
cm = pd.DataFrame(confusion_matrix(y_test, random_forest_predictions), ['Actual: NOT', 'Actual: SURVIVED'], ['Predicted: NO', 'Predicted: SURVIVED'])
print('-'*50)
print(cm)



#Model Summary
objects = ['Logistic Regression', 'SVC', 'KNN', 'Gaussian', 'Perceptron', 'linear SVC', 'SGD', 'Decision Tree', 'Random Forest']
x_pos = np.arange(len(objects))
accuracies1 = [acc_log, acc_svc, acc_knn, acc_gaussian, acc_perceptron, acc_linear_svc, acc_sgd, acc_decision_tree, acc_random_forest]
    
plt.bar(x_pos, accuracies1, align='center', alpha=0.5, color='r')
plt.xticks(x_pos, objects, rotation='vertical')
plt.ylabel('Accuracy')
plt.title('Classifier Outcome')
plt.axhline(max(accuracies1), color = 'purple')
plt.show()



# Cross validate model with Kfold stratified cross validation
kfold = StratifiedKFold(n_splits=10)
# Modeling step Test differents algorithms 
random_state = 2

classifiers = []
classifiers.append(LogisticRegression(random_state = random_state))
classifiers.append(SVC(random_state=random_state))
classifiers.append(KNeighborsClassifier())
classifiers.append(GaussianNB())
classifiers.append(Perceptron(random_state=random_state))
classifiers.append(LinearSVC(random_state=random_state))
classifiers.append(SGDClassifier(random_state=random_state))
classifiers.append(DecisionTreeClassifier(random_state = random_state))
classifiers.append(RandomForestClassifier(random_state = random_state))

cv_results = []
for classifier in classifiers :
    cv_results.append(cross_val_score(classifier, X_train, y = Y_train, scoring = "accuracy", cv = kfold, n_jobs=4))

cv_means = []
cv_std = []
for cv_result in cv_results:
    cv_means.append(cv_result.mean())
    cv_std.append(cv_result.std())

cv_res = pd.DataFrame({"CrossValMeans":cv_means,
                       "CrossValerrors": cv_std,
                       "Algorithm":['Logistic Regression',
                                    'KNN', 
                                    'Gaussian', 
                                    'Perceptron', 
                                    'linear SVC', 
                                    'SGD', 
                                    'Decision Tree',
                                    'SVMC', 
                                    'Random Forest'
                                    ]
                        })

g = sns.barplot(x = "CrossValMeans", y = "Algorithm", data = cv_res, palette="Set3",orient = "h",**{'xerr':cv_std})
g.set_xlabel("Mean Accuracy")
g = g.set_title("Cross validation scores")



#Hyperparameter Tuning & Learning Curves
# Adaboost
DTC = DecisionTreeClassifier()
adaDTC = AdaBoostClassifier(DTC, random_state=7)
ada_param_grid = {"base_estimator__criterion" : ["gini", "entropy"],
              "base_estimator__splitter" :   ["best", "random"],
              "algorithm" : ["SAMME","SAMME.R"],
              "n_estimators" :[1,2],
              "learning_rate":  [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3,1.5]}
gsadaDTC = GridSearchCV(adaDTC,param_grid = ada_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)
gsadaDTC.fit(X_train,Y_train)
adaDTC_best = gsadaDTC.best_estimator_
gsadaDTC.best_score_



# ExtraTrees 
ExtC = ExtraTreesClassifier()
ex_param_grid = {"max_depth": [None],
              "max_features": [1, 3, 7],
              "min_samples_split": [2, 3, 7],
              "min_samples_leaf": [1, 3, 7],
              "bootstrap": [False],
              "n_estimators" :[300,600],
              "criterion": ["gini"]}
gsExtC = GridSearchCV(ExtC,param_grid = ex_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)
gsExtC.fit(X_train,Y_train)
ExtC_best = gsExtC.best_estimator_
gsExtC.best_score_



# Gradient boosting tunning
GBC = GradientBoostingClassifier()
gb_param_grid = {'loss' : ["deviance"],
              'n_estimators' : [100,200,300],
              'learning_rate': [0.1, 0.05, 0.01],
              'max_depth': [4, 8],
              'min_samples_leaf': [100,150],
              'max_features': [0.3, 0.1] }
gsGBC = GridSearchCV(GBC,param_grid = gb_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)
gsGBC.fit(X_train,Y_train)
GBC_best = gsGBC.best_estimator_
gsGBC.best_score_




# SVC classifier
SVMC = SVC(probability=True)
svc_param_grid = {'kernel': ['rbf'], 
                  'gamma': [ 0.001, 0.01, 0.1, 1],
                  'C': [1,10,50,100,200,300, 1000]}
gsSVMC = GridSearchCV(SVMC,param_grid = svc_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)
gsSVMC.fit(X_train,Y_train)
SVMC_best = gsSVMC.best_estimator_
# Best score
gsSVMC.best_score_



# Random Forest
rf_param_grid = {"max_depth": [None],
              "max_features": [1, 3, 7],
              "min_samples_split": [2, 3, 7],
              "min_samples_leaf": [1, 3, 7],
              "bootstrap": [False],
              "n_estimators" :[300,600],
              "criterion": ["gini"]}
gsrandom_forest = GridSearchCV(random_forest,param_grid = rf_param_grid, cv=kfold, scoring="accuracy", n_jobs= 4, verbose = 1)
gsrandom_forest.fit(X_train,Y_train)
# Best score
random_forest_best = gsrandom_forest.best_estimator_
gsrandom_forest.best_score_



def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
        n_jobs=-1, train_sizes=np.linspace(.1, 1.0, 5)):
    """Generate a simple plot of the test and training learning curve"""
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")
    plt.legend(loc="best")
    return plt
g = plot_learning_curve(gsadaDTC.best_estimator_,"AdaBoost learning curves",X_train,Y_train,cv=kfold)
g = plot_learning_curve(gsExtC.best_estimator_,"ExtC ExtraTrees learning curves",X_train,Y_train,cv=kfold)
g = plot_learning_curve(gsGBC.best_estimator_,"GBC Gradient Boost learning curves",X_train,Y_train,cv=kfold)
g = plot_learning_curve(gsrandom_forest.best_estimator_,"RandomForest learning curves",X_train,Y_train,cv=kfold)
g = plot_learning_curve(gsSVMC.best_estimator_,"SVMC learning curves",X_train,Y_train,cv=kfold)



test_Survived_AdaDTC = pd.Series(adaDTC_best.predict(x_test), name="AdaDTC")
test_Survived_ExtC = pd.Series(ExtC_best.predict(x_test), name="ExtC")
test_Survived_GBC = pd.Series(GBC_best.predict(x_test), name="GBC")
test_Survived_SVMC = pd.Series(SVMC_best.predict(x_test), name="SVMC")
test_Survived_random_forest = pd.Series(random_forest_best.predict(x_test), name="random_forest")

# Concatenate all classifier results
ensemble_results = pd.concat([test_Survived_AdaDTC, test_Survived_ExtC, test_Survived_GBC,test_Survived_SVMC,test_Survived_random_forest],axis=1)
g= sns.heatmap(ensemble_results.corr(),annot=True)


#Ensembling
VotingPredictor = VotingClassifier(estimators=[('ExtC', ExtC_best), 
                                               ('GBC',GBC_best),
                                               ('SVMC', SVMC_best), 
                                               ('random_forest', random_forest_best)
                                               ], 
                                    voting='soft', 
                                    n_jobs=4
                                    )
VotingPredictor = VotingPredictor.fit(X_train, Y_train)
VotingPredictor_predictions = VotingPredictor.predict(test)
test_Survived = pd.Series(VotingPredictor_predictions, name="Survived")

# Preparing data for Submission 3
test_Survived = pd.Series(VotingPredictor_predictions, name="Survived")
Submission3 = pd.concat([PassengerId,test_Survived],axis=1)
Submission3.head(15)



nrows = ncols = 2
fig, axes = plt.subplots(nrows = nrows, ncols = ncols, sharex="all", figsize=(15,7))
names_classifiers = [("AdaBoosting", adaDTC_best),("ExtraTrees",ExtC_best),
("GradientBoosting",GBC_best), ("RandomForest",random_forest_best)]

nclassifier = 0
for row in range(nrows):
    for col in range(ncols):
        name = names_classifiers[nclassifier][0]
        classifier = names_classifiers[nclassifier][1]
        indices = np.argsort(classifier.feature_importances_)[::-1][:40]
        g = sns.barplot(y=train.columns[indices][:40],x = classifier.feature_importances_[indices][:40] , orient='h',ax=axes[row][col])
        g.set_xlabel("Relative importance",fontsize=11)
        g.set_ylabel("Features",fontsize=11)
        g.tick_params(labelsize=9)
        g.set_title(name + " feature importance")
        nclassifier += 1


# # Final File
# Submission3.to_csv("PassangerSurvival.csv", index=False)
# print("Completed.")