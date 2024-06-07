""" Credits: Rommel Artola
& Spotify for providing the API services to extract data! (Thank you Spotify!)

At this point in the journey, we've arrived at a very cleaned up dataframe.

Thankfully, we didn't have to aggregate any values once we cleaned up all the duplicates
in the album column, so that is good! Though we may still aggregate at the album
level for certain visuals. This is to be determined since the focal point is the track.


Important Note: 1) If you guessed that I also played Kendrick while doing this part of the analysis...
then you are absolutely correct.

 O       O//    \O/   \\O     \O/
/|\      |       |      |      | 
/ \     / \     / \    / \    / \ 
#StepThisWay, #StepThatWay



2) According to Spotify's Documentation:
    "Generally speaking, songs that are being played a lot now will have a higher 
    popularity than songs that were played a lot in the past. Duplicate tracks 
    (e.g. the same track from a single and an album) are rated independently. 
    Artist and album popularity is derived mathematically from track popularity. 
    Note: the popularity value may lag actual popularity by a few days: the 
    value is not updated in real time." "
 
 What this means for us is that we can reliably expect his latest songs to be higher
than his older hit records. For example, it is a VERY safe assumption that Not Like Us 
will be much higher in popularity than most other of this songs. So, total plays is not skewing this,
but recency is.

"""

# Import libraries
from Step_02_Data_Cleaner import cleaned_df as df
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.preprocessing import minmax_scale

from tabulate import tabulate




###############################################################################
# Boiling the Ocean
###############################################################################
sns.pairplot(df, kind='scatter', diag_kind='kde')#.savefig('Outputs/01_pairplot.png')
"""
The pairplot above has A LOT of information, so let's break down what it is that we are seeing.

Feature Analysis:
    TRACK_TIME_SIGNATURE: An overwhelming amount of K Dot's songs are in a value of 
        4 for this feature. Which the definition is:
            "An estimated time signature. The time signature (meter) is a 
            notational convention to specify how many beats are in each 
            bar (or measure). The time signature ranges from 3 to 7 
            indicating time signatures of "3/4", to "7/4"."

        For Kendrick, this means there are 4 beats in each measure 
        and a quarter note receives one count. According to https://www.skoove.com/,
        they say that a:
          Skoove: "4/4 time signature gives music a steady, marching rhythm, 
                    perfect for getting your foot tapping."
    
    TRACK_TEMPO: When looking at tempo and duration, it seems that the much
        longer songs of K Dot tend to be in lower tempo, which makes sense. His
        longer songs tend to be more poetically-inclined and are of spoken-word
        instead of something like Money Trees for example.

        For danceability, the middle ground of tempo seems to be the best.

        Overall, nothing too great here, even the aformentioned call outs, are sparse and not very 
        linear/direct. So, they are to be taken with a grain of salt. The biggest value is that,
        by looking at the kernel density plot, most of his songs are slower tempo, 
        hence the plot is right-skewed a bit.

    
    
    TRACK_VALENCE: I just want to call out, this is probably my favorite measure because
        it algorithmically places a valuue on how positive the song is based on the tone. As Spotify 
        calls out in the documentation: "Tracks with high valence sound more positive 
                                        (e.g. happy, cheerful, euphoric), while tracks 
                                        with low valence sound more negative 
                                        (e.g. sad, depressed, angry) "

        When looking at popularity it seems to have a relatively strong linear relationship
            with "happier" songs being more popular. With a couple songs being VERY popular and low
            valence.
        
        Valence distribution is overall pretty normal. But nothing else to note.


    TRACK_LOUDSNESS & TRACK_ENERGY: Both seem VERY positively correlated to each other.

    
    What is a little troublesome, is that popularity is a mathematical value that
    decreases over time. Let's see if we can reverse-engineer some of that logic
    after the plot below.

    Nothing else particularly interesting at a quick glance.
"""


# Let's now boil the ocean again, but instead of a graphical view, let's do a 
# numerical representation using a correlation matrix.

plt.figure(figsize=(20, 20))
sns.heatmap(df.corr(), annot=True, 
            linecolor='black', cmap='RdYlBu', 
            linewidths=0.5,  fmt=".2f",
            vmin=-1, vmax=1, center=0,        
            annot_kws={"size": 14})
plt.title('Correlation plot of K Dot')
#plt.savefig("Outputs/02_corrplot.png")
plt.show()


""" What is all of that mess even showing besides pretty squares..?

Well, in summary, it is showing that the below relationships are very strongly-related

ALBUM_FRACTIONAL_DATE and TRACK_POPULARITY: As we would expect with his most-recent drops
TRACK_ENERGY and TRACK_LOUDNESS: As we had called out earlier.
Both of the above are positive correlations.

Weaker, but worth calling out (negative) correlations:
TRACK_ENERGY and ALBUM_FRACTIONAL_DATE: Looks like K Dot has a negative trend on 'energy' (no pun intended)
TRACK_SPEACHINESS and TRACK_POPULARITY: Very 'speachie' tracks are less popular, BUT this makes A LOT
    of sense because his moire speachie songs are also much longer and tend to be more poetery/spoken word
    than a hype song.

    
Nothing else exceptional.

"""


# Let's reverse-engineer some of the algorithmicness of popularity.
# We will do this with the consideration that Money Trees and Not Like Us should
#   have a similar value in popularity, much closer than what is currently showing.
# This will be done using a modified anti-decay factor/function.

# Define a modified exponential decay function
def antidecay_function(decayed_value, rate_of_decrease, time):
    """
    Where:
        a = Initial Amount
        r = Rate of Decrease
        t = Time
        a = > 0
        r = between 0 and 1 (non-inclusive)
        d = output (decyaed value)

    Original function to give the decay value is:
        d = a(1 - r)**t
    
    For us, it'll be:
        a = d / ( (1 - r)**t )
    """
    return decayed_value / ( (1 - rate_of_decrease) ** time)



today = pd.to_datetime(datetime.now().date())
df['DAYS_SINCE_RELEASE'] = today - df['ALBUM_RELEASE_DATE']
df['SCALED_DAYS_SINCE_RELEASE'] = minmax_scale(df[['DAYS_SINCE_RELEASE']])


# Here we will use an iterative approach
best_rate = 0
lowest_RMSD = np.inf 
for i in np.arange(0, 1, .01):
    df['ANTI_DECAY_POPULARITY'] = antidecay_function(decayed_value=df['TRACK_POPULARITY'],
                                                     rate_of_decrease=i,
                                                     time=df['SCALED_DAYS_SINCE_RELEASE'])
    df['SCALED_ANTIDECAY_POPULARITY'] = minmax_scale(df[['ANTI_DECAY_POPULARITY']])

    #root mean square deviation (broken out for better reading)
    #grab mean value first for distance
    mean_val = df['SCALED_ANTIDECAY_POPULARITY'].mean()
    #square the distances
    squared_distances = (df['SCALED_ANTIDECAY_POPULARITY'] - mean_val)**2
    #Average distances and square root.
    #We want to minimize this value to find our ideal rate of decrease.
    RMSD = np.sqrt(squared_distances.mean())

    if RMSD < lowest_RMSD:
        lowest_RMSD = RMSD
        best_rate = i
        print(f'New best rate found! {best_rate}')


    plt.hist(df['SCALED_ANTIDECAY_POPULARITY'])
    plt.title(f'Rate of Decrease: {i}.\nRMSD: {RMSD}')
    plt.show()
    time.sleep(1)

print(f'Lowest RMSD: {lowest_RMSD}')
print(f'Best Rate of Decay: {best_rate}')


# Looks like we found our best rate of decay to reduce the room mean square difference
# from mean! Let's cement these findings in our columns now.

df['ANTI_DECAY_POPULARITY'] = antidecay_function(decayed_value=df['TRACK_POPULARITY'],
                                                     rate_of_decrease=best_rate, #.14
                                                     time=df['SCALED_DAYS_SINCE_RELEASE'])
df['SCALED_ANTIDECAY_POPULARITY'] = minmax_scale(df[['ANTI_DECAY_POPULARITY']]) * 100


# Let's take a look at how our songs were ranked with our new values.
with pd.option_context('display.max_rows', 100):
    display(df[['ALBUM_NAME', 'TRACK_NAME', 'TRACK_POPULARITY', 'SCALED_ANTIDECAY_POPULARITY']].sort_values(by='SCALED_ANTIDECAY_POPULARITY', ascending=False)
    )



""" Section Takeaway:

Though it reduces the score of Not Like Us, for example, by A LOT simply because 
it's much too new when compared to something like Money Trees, I can't say I entirely 
disagree with the new values. 

A similar metric could've been achieved with total play counts I believe, and arriving
to another mathematical way of popularity, but I think this way makes sense. 

What was surprising to me, was how his album "Mr. Morale & The Big Steppers"
was basically clusterd all the way to the bottom of lowest popularity. I imagine this 
must be, in part, because MMTBS is not very old when looking at albums like GKMC.
Additionally, some people hint at MMTBS having been "a flop" in commercial terms. 

What I certainly do not agree with (on the original popularity ranking) is how
albums were being clustered and sorted almost just by how old they were instead of their
actual popularity, grossly misidentifying the most-popular songs. I think the new 
value we've arrived at does a strong job of identifying truly popular songs, 
but harshly punishes songs that are relatively recent AND NOT highly popular.

This gives me confidence to preceed with our new popularity ranking.


"""


plt.figure(figsize=(20,20))
for num, i in enumerate(df.select_dtypes(include=['int', 'float']), start=1):
    plt.subplot(6, 3, num)
    plt.hist(df[i], density=True, label=str(i))
    plt.legend()
    plt.xlabel(str(i))

plt.show()


"""
Above is a simple histogram plot of each numeric column from the dataset.

Nothing ~too~ critical. Namely, Kendrick's track danceability seem to follow a 
relatively normal distribution, while his songs tend to lean towards loud and his
acousticness and liveness tend to not be very high.


Additionally, most of his songs fall between the 200K - 300K MS duration. Though,
a few songs have a much longer duration of more than double that.

However, now we can see the visual transformation from the raw (originall) track popularity 
to our anti-decay value, and finally our scaled anti-decay value to bring it back
into a range of 0-100. 

So, now it's worth calling out for consistency, that the SCALED_ANTIDECAY_POPULARITY
is not a relative value. I.e., a value of 0 is not that the song has never been listened to,
it's just showing:
     "This is the least popular song of K Dot's discography, when accounting
    for the amount of days the song has been released using the decay function."

"""












lm_plot = sns.lmplot(data=df, x='TRACK_DURATION_MS', 
                     y='SCALED_ANTIDECAY_POPULARITY',
                     hue='ALBUM_NAME', ci=10, robust=True)
lm_plot.set(title="Track's Duration Effect on Calculated Popularity\nWith Robust Regression Per Album")
plt.xticks(rotation=45)
plt.figtext(0.1, -0.1, 'Footnote: C.I. = 10', wrap=True, horizontalalignment='left', fontsize=10)
plt.show()
#lm_plot.savefig('Outputs/03_DurationEffect&RR.png')

"""
What are seeing in the plot above? Well, a lot of extraploation on very few data 
points, but an interesting extrapolation nonetheless. Naturally, there are going
to be outliers within-albums, so we use a Robust regression to de-weight 
those outliers a bit.

We also only use a very small confidence interval of 10 to not overcrowd the plot
with data.

What I find the most interesting is that the album "untitled unmastered." has an upward 
trend for track duration while "DAMN." has a negative fit for track duration. Now,
kee in mind "DAMN." was released mid 2017, while "untitled unmastered" was released
early 2016. So, not a whole lot of difference I would imagine for the popularity reversal
using the decay function to affect it. Even then, we are looking at the 
within-album trend instead of the between-album trend. 
Which should be controlling for that difference anyway since each album has the
same days since release, and the other difference would be the original popularity
we transformed.  



# Check the release dates here
#df[df['ALBUM_NAME'].str.contains('untitled|DAMN.')]\
#    .get(['ALBUM_NAME', 'ALBUM_RELEASE_DATE'])\
#    .drop_duplicates()


What is the opinion of this? 
    The "DAMN." album, having won the Pulitzer Prize, likely attracted A LOT of
    love from Kendrick's non-core audience. Likely some folks that just wanted to
    listen to the hottest songs, or at least not the longest ones. In the other hand,
    "untitled unmastered." targets K Dot's core audiance in the heart of hearts. 
    His poetic spoken-word approach with a grungy-type feeling filled with mystery appeals
    more to those folks, that want to stick around for the longer songs to learn
    about Kendrick.
    Additionally, just the fact alone that the album's name is "untitled unmastered"
    and all of the tracks are "untitled ## .." goes to show what audience he made it for,
    or at least had in mind.

    My theory above can also be best-shown by looking at the mean Acousticness, 
    Speachiness, Energy, and Danceability, over the two different albums
    using the code below:

    df[df['ALBUM_NAME'].str.contains('untitled|DAMN.')]\
        .groupby('ALBUM_NAME')\
        .aggregate('mean', numeric_only=True)\
        .filter(items=['TRACK_ACOUSTICNESS', 'TRACK_INSTRUMENTALNESS', 'TRACK_SPEACHINESS', 
                        'TRACK_ENERGY', 'TRACK_DANCEABILITY'])

"""








table_data = []
for feature in [feat_num for feat_num in df.select_dtypes(include=['int', 'float']).columns\
                if feat_num not in ['ALBUM_FRACTIONAL_DATE', 
                                    'TRACK_TIME_SIGNATURE', 
                                    'TRACK_KEY', 'TRACK_MODE', 
                                    'TRACK_TIME_SIGNATURE',
                                    'ANTI_DECAY_POPULARITY',
                                    'SCALED_DAYS_SINCE_RELEASE']]:
    max_track = df[df[feature] == df[feature].max()].get('TRACK_NAME').values[0]
    min_track = df[df[feature] == df[feature].min()].get('TRACK_NAME').values[0]

    max_album = df[df['TRACK_NAME'] == max_track].get('ALBUM_NAME').values[0]
    min_album = df[df['TRACK_NAME'] == min_track].get('ALBUM_NAME').values[0]


    # print(f"Song with Max {feature.lower().split(sep='_')[1]}: {max_track}")
    # print(f"Song with Min {feature.lower().split(sep='_')[1]}: {min_track}")
    # print("\n")
    # Decided to print out using a pretty tabulate format, instead of a general print statement.
    table_data.append([feature, 'Max', max_album, max_track])
    table_data.append([feature, 'Min', min_album, min_track])


print(tabulate(table_data, 
               headers=['Feature', 'Type', 'Album Name', 'Track Name'], 
               tablefmt='pretty', stralign='left'))

"""
There's quite a bit here, but nothing that we haven't quite already examined
in our plots of histograms. However, this is a good way to look at the
extreme ends of our data points in a qualitative standpoint, instead of
purely quantitatively.

"""







album_pop_and_length = df.groupby(['ALBUM_FRACTIONAL_DATE', 'ALBUM_NAME'])\
                        .aggregate(AVG_ALBUM_POPULARITY=('SCALED_ANTIDECAY_POPULARITY', 'mean'),
                                    AVG_ALBUM_DURATION=('TRACK_DURATION_MS', 'mean'))\
                        .reset_index()

lm_plot2 = sns.lmplot(data=album_pop_and_length, 
                      x='AVG_ALBUM_DURATION', y='AVG_ALBUM_POPULARITY', 
                      ci=25, robust=True, aspect=2, height=6)

lm_plot2.set(title="Track's Duration Effect on Album Mean Relative Popularity \nWith Robust Regression")
plt.figtext(0.5, -0.1, "Confidence Interval: 25", fontsize=10, ha='center')
plt.show()


"""
What do we see now? Simply, on average, we see that Kendrick's average album 
popularity tends to decrease as the average album duration increases. 
"""


lm_plot3 = sns.lmplot(data=album_pop_and_length, 
                      x='ALBUM_FRACTIONAL_DATE', y='AVG_ALBUM_POPULARITY', 
                      ci=25, robust=True, aspect=2, height=6)

lm_plot2.set(title="Mean Relative Album Popularity Over Time \nWith Robust Regression")
plt.figtext(0.5, -0.1, "Confidence Interval: 25", fontsize=10, ha='center')
plt.show()


"""
Now, this plot above is a bit misleading. If reading it at face value, one would
assume that over time, Kedrick is losing popularity. However, we must keep in mind 
that our y-value in this case, is relative. Moreover, a big part drving this decrease
is because of the last 3 songs not having a lot of time to really yet be established
as truly popular or not, given our anti-decay formula. Lastly, since the value is
relative, we also get the "negative" impact of 'Mr. Morale & The Big Steppers'
being the lowest and after 2022.




For reference, if I had plotted (not shown) the same plot but using the original
popularity value, the line was VERY linearly positive. 


With that, that concludes this section of our code, let's dive into some
machine learning algorithms now!

"""