"""
Credits: Rommel Artola
& Spotify for providing the API services to extract data! (Thank you Spotify!)


For this specific file, we're going to build a process or data a bit
and build some machine learning models to try and see if it can accurately predict
whether I (personally) would REALLY like a Kedrick Lamar song, or not so much.

This will be using manually imputted values of 1 on songs I really enjoy, and 
0 on songs I did not enjoy as much.

Though the above is a classification model, the same can be done using
regressions models using a "likeness" value from 0 to 100, for example!



Disclaimer:
According to Section IV.2.a.i  of Spotify's Policy Restrictions, machine learning models
 cannot be built using this data. However, this seems to be for the use in 
 specifics to commercial-type products or that is somehow connected with revenue. 
 This project is simply a hobbyist project and is in no way at all, 
 now or in the future, affiliated with any brand, commercial usage, or 
 anything more than an analytical project that may also be used as a way to 
 teach about Python and data science to early-career data scientists. 

"""


# We do not need the values we added for Analysis, since popularity will not
# be our target variable. We can just imported or original cleaned df.
from Step_02_Data_Cleaner import cleaned_df as df
import pandas as pd
from tkinter import simpledialog
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import (
                             classification_report, 
                             confusion_matrix, 
                             balanced_accuracy_score
                            )

# Let's first manually categorize whether we VERY MUCH like a Kendrick Lamar song
# or not so much.

favorites = {}

for index, row in df.iterrows():
    song = row['TRACK_NAME']
    is_favorite = simpledialog.askinteger('Song Categorizer', 
                            prompt=f'Do you like song: {song}: 0 or 1')
    favorites[song] = is_favorite


# To not have to cycle through again, I will hardcore the results below
""" Favorites Hardcoded: 
favorites =\
{'Alright': 1,
 'Silent Hill': 0,
 'Count Me Out': 0,
 'Not Like Us': 1,
 'meet the grahams': 1,
 'A.D.H.D': 1,
 'FEEL.': 1,
 'HiiiPower': 0,
 'Rich Spirit': 1,
 'ELEMENT.': 1,
 'euphoria': 1,
 'LOYALTY. FEAT. RIHANNA.': 1,
 'These Walls': 0,
 'N95': 1,
 'Father Time (feat. Sampha)': 1,
 'FEAR.': 1,
 'untitled 08 | 09.06.2014.': 0,
 'DUCKWORTH.': 1,
 'Savior': 1,
 'King Kunta': 1,
 'Purple Hearts': 0,
 'PRIDE.': 0,
 'LUST.': 1,
 'We Cry Together': 1,
 "Hol' Up": 0,
 'Die Hard': 1,
 'Chapter Six': 0,
 'XXX. FEAT. U2.': 0,
 'HUMBLE.': 1,
 "Wesley's Theory": 1,
 'YAH.': 1,
 'LOVE. FEAT. ZACARI.': 1,
 'Money Trees': 1,
 'DNA.': 1,
 'United In Grief': 1,
 'Mr. Morale': 0,
 'BLOOD.': 0,
 'm.A.A.d city': 1,
 'Bitch, Don’t Kill My Vibe': 1,
 'The Heart Part 5': 1,
 'Blow My High (Members Only)': 0,
 'u': 1,
 'Rigamortus': 0,
 'Mother I Sober (feat. Beth Gibbons of Portishead)': 1,
 'How Much A Dollar Cost': 0,
 'The Blacker The Berry': 1,
 'Hood Politics': 1,
 'untitled 02 | 06.23.2014.': 0,
 'untitled 03 | 05.28.2013.': 0,
 'Poe Mans Dreams (His Vice) (feat. GLC)': 0,
 'Institutionalized': 0,
 'Momma': 1,
 'Ronald Reagan Era': 0,
 'untitled 07 | 2014 - 2016': 1,
 "You Ain't Gotta Lie (Momma Said)": 1,
 'Complexion (A Zulu Love)': 0,
 'GOD.': 1,
 'i': 1,
 'untitled 06 | 06.30.2014.': 0,
 'Mirror': 0,
 'Mortal Man': 1,
 'For Free? - Interlude': 0,
 'Auntie Diaries': 0,
 'Rich - Interlude': 0,
 'untitled 05 | 09.21.2014.': 0,
 "Tammy's Song (Her Evils)": 1,
 'Crown': 0,
 'Worldwide Steppers': 0,
 'F*ck Your Ethnicity': 1,
 "Sing About Me, I'm Dying Of Thirst": 1,
 'Swimming Pools (Drank) - Extended Version': 1,
 'For Sale? - Interlude': 0,
 'Backseat Freestyle': 1,
 'Savior - Interlude': 1,
 'Poetic Justice': 1,
 'Opposites Attract (Tomorrow W/O Her)': 1,
 'Kush & Corinthians (feat. BJ The Chicago Kid)': 1,
 'Average Joe': 1,
 'Cut You Off (To Grow Closer)': 1,
 'She Needs Me (Remix)': 1,
 'Michael Jordan': 0,
 'P&P 1.5': 0,
 'Growing Apart (To Get Closer)': 1,
 'H.O.C': 0,
 'Ignorance Is Bliss': 0,
 "Keisha's Song (Her Pain) (feat. Ashtro Bot)": 1,
 'R.O.T.C (Interlude)': 0,
 'Chapter Ten': 0,
 'Barbed Wire': 1,
 'No Make-Up (Her Vice) (feat. Colin Munroe)': 1,
 'untitled 04 | 08.14.2014.': 0,
 'Alien Girl (Today W/ Her)': 1,
 'The Art of Peer Pressure': 1,
 'untitled 01 | 08.19.2014.': 1,
 'Ab-Souls Outro (feat. Ab-Soul)': 0,
 'Bitch, Don’t Kill My Vibe - Remix': 0,
 'good kid': 1,
 'Real': 1,
 'Compton': 1,
 'Sherane a.k.a Master Splinter’s Daughter': 1}

"""


df['IS_FAVORITE'] = favorites.values()

df.groupby('IS_FAVORITE').size()

""" 
Now, our target variable isn't grossly inbalaned, but there is some inbalance nonetheless.

Let's try and correct for that by manually some potentially repetitive songs (Remix versions), 
for example. Any additional differences, will have to be handled differently. 
Whether we use weights for the classes, undersampling, or SMOTE for oversampling. 

Though we will use some models that this inbalance does not matter as much (like random forest),
it should still be corrected for the best approaches.

We are also going to drop unneeded columns and scale all values for learning 
models before we begin.


"""

# Duplicated songs was just 1
songs_to_drop = ['Bitch, Don’t Kill My Vibe - Remix']


# Let's drop that row, and all unneeded columns now.
df_ML = df[~df['TRACK_NAME'].isin(songs_to_drop)]\
        .drop(columns=['ALBUM_ID', 'ALBUM_NAME', 'ALBUM_RELEASE_DATE',
                       'TRACK_ID', 'TRACK_POPULARITY', 'ALBUM_FRACTIONAL_DATE'])\
        .reset_index(drop=True)\
        .assign(**pd.get_dummies(data=df[['TRACK_KEY', 'TRACK_MODE', 
                                    'TRACK_TIME_SIGNATURE']], 
                                drop_first=True, 
                                 columns=['TRACK_KEY', 'TRACK_MODE', 
                                    'TRACK_TIME_SIGNATURE']))\
        .drop(columns=['TRACK_KEY', 'TRACK_MODE', 
                                    'TRACK_TIME_SIGNATURE'])

df_ML = df_ML.reindex(columns=['TRACK_NAME'] +\
                      [col for col in df_ML.columns if col not in ['IS_FAVORITE',
                                                                    'TRACK_NAME']] +\
                                                                 ['IS_FAVORITE']
                    )
df_og = df_ML.copy() #Will be used for index values later on.






####################################################################################################
# Let's try and proactive evaluate whether modeling with be useful or not. Though, we will still model.
# We'll do scatters of each pair-wise feature with hues for the target class.
####################################################################################################
sns.pairplot(df_ML.select_dtypes([int, float]), hue='IS_FAVORITE').add_legend()


"""
This pairplot was just usedd a quick spot-check analysis since we already performed an extensive
EDA on all of the features against the ranking of the song. 

So, what dop I infer from it? I would assume our predictive modeling abilities will be akin
to that of a coin flip, or perhaps a bit better, at most. However, we will still run through
several examples, I would feel relatively confident saying we would need more data or better 
features.

Why do I infer that? I do so because when looking at all the scatter plots, none have a very
clear seperation between the classes. Furthermore, when looking at the density plot (diagonals),
we can see that each class (0 and 1) can be very easily sub-sampled from the other in a random
sampling.

"""



















####################################################################################################
# Random Forest
####################################################################################################
best_rf = None
best_rf_accuracy = 0
best_rf_predict = None

for est in [50, 100, 150, 200, 250]:
    rf = RandomForestClassifier(n_estimators=est, 
                                class_weight='balanced', 
                                random_state=5)
    
    rf.fit(X_train_final, y_train_final.to_numpy().ravel())
    rf_predict = rf.predict(X_test_final)
    rf_balanced_accuracy = balanced_accuracy_score(y_test_final, rf_predict)
    if  rf_balanced_accuracy > best_rf_accuracy:
        best_rf_accuracy = rf_balanced_accuracy
        best_rf_predict = rf_predict
        best_rf = rf

print('Num of estimators: ', best_rf.n_estimators)
print('Best Score: ', best_rf_accuracy)


rf_conf_matrix = confusion_matrix(y_test_final, best_rf_predict)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(rf_conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Labels')
plt.ylabel('Actual Labels')
plt.title('Confusion Matrix')
plt.show()


# Create a dictionary of features and their importances
feature_importance_dict = dict(zip(best_rf.feature_names_in_, best_rf.feature_importances_))

# Sort the dictionary by importances in descending order
sorted_feature_importance = dict(sorted(feature_importance_dict.items(), key=lambda item: item[1], reverse=True))

# Plot the sorted feature importances
plt.bar(sorted_feature_importance.keys(), sorted_feature_importance.values(), color='steelblue')
plt.xticks(rotation=90)
plt.xlabel('Features')
plt.ylabel('Importance')
plt.title('Feature Importance Sorted')
plt.show()










####################################################################################################
# Logistics Regression
####################################################################################################
logit = LogisticRegression(class_weight='balanced', random_state=5)
logit.fit(X_train_final, y_train_final)
logit_predict = logit.predict(X_test_final)
conf_matrix = confusion_matrix(y_test_final, logit_predict)
print(classification_report(y_test, logit_predict))

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Labels')
plt.ylabel('Actual Labels')
plt.title('Confusion Matrix')
plt.show()









mlp = MLPClassifier(hidden_layer_sizes= (3, 20), activation='relu', random_state=5)
mlp.fit(X_train_final, y_train_final)
mlp_predict = mlp.predict(X_test_final)
conf_matrix = confusion_matrix(y_test_final, mlp_predict)
print(classification_report(y_test_final, mlp_predict))


balanced_accuracy_score(y_test_final, mlp_predict)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Labels')
plt.ylabel('Actual Labels')
plt.title('Confusion Matrix')
plt.show()







####################################################################################################
# KNN
####################################################################################################
neighbors_and_accuracy = {}

for i in np.arange(1, 20):
    knn = KNeighborsClassifier(n_neighbors=i, weights='uniform')
    knn.fit(X_train_final, y_train_final)
    knn_predict = knn.predict(X_test_final)
    knn_clf_score = balanced_accuracy_score(y_test_final, knn_predict)
    neighbors_and_accuracy.setdefault(i, knn_clf_score)



sns.lineplot(x=neighbors_and_accuracy.keys(), y=neighbors_and_accuracy.values())


####################################################################################################
# K-Means
####################################################################################################
clusters_and_accuracy = {}

for i in np.arange(1, 50):
    kmeans = KMeans(n_clusters=10, random_state=5)
    kmeans.fit(X_train_final)
    kmeans_predict = kmeans.predict(X_test_final)

sns.lineplot(x=clusters_and_accuracy.keys(), y=clusters_and_accuracy.values())


# Plotting the data points and cluster centers
plt.figure(figsize=(8, 6))
plt.scatter(X_train_final.iloc[:, 0], 
            X_train_final.iloc[:, 1], 
            c=kmeans.labels_, s=100, cmap='viridis', label='Training Data')

plt.scatter(X_test_final.iloc[:, 0], 
            X_test_final.iloc[:, 1], 
            c=kmeans_predict, s=200, cmap='coolwarm', 
            marker='X', edgecolors='k', 
            label='New Data')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red', marker='*', label='Cluster Centers')

plt.title('K-means Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.grid(True)
plt.show()






####################################################################################################
# Which songs did our best model get correct?
####################################################################################################
# Since KNN was our best model as far as balanced accuracy score, let's see exactly which songs
# it guess correctled/incorrectly, instead of just random indices and values.

song_analysis = df_og[['TRACK_NAME', 'IS_FAVORITE']].iloc[X_test_final.index,]\
                .assign(MLP_IS_FAVORITE = mlp_predict,
                        IS_MATCH = lambda df: df['MLP_IS_FAVORITE'] == df['IS_FAVORITE'])\
                .sort_values('IS_MATCH', ascending=False)


"""
What are my final thoughts? I'm actually relatively impressed that it performed
at ~ 60% which is a bit better than a coin-flip, though not substantially better.

What I am dissappointed in, is some of the songs it guessed as favorites when it 
wasn't a true favorite. However, those songs have A LOT of similarities with songs
I do love. 

This goes to show that it's not just the quantifiable features, but it may also
do with the words in the specific words. This would require a NLP lyrical-analysis
though, which is beyond the scope of this specific project. But perhaps something
for a future one.

Additionally, some songs I did like, but aren't a huge favorite. So, just as much
as the model "is the problem" I was also problem that was introduced into the equation
with perhaps a hard-to-reproduce scaling system. Perhaps if I retook my own song
questionnaire a month from now, all of my favorites would shuffle, which goes to
show my lack of reproducability in song classification is an issue, while the 
models will always perform the same (assuming a seed is set, anyway). I.e., 
human error!


"""



