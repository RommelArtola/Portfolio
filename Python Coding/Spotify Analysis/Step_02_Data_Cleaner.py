""" Credits: Rommel Artola
& Spotify for providing the API services to extract data! (Thank you Spotify!)

There are countless ways to clean this data, namely when referring to duplicated songs.

We know that artists sometimes drop the same song on multiple albums, or "tease" a
special song before dropping the whole album, but leave both entries of the songs
on their discography. 


Since data cleaning is not a straight-forward process with many iterative steps,
I've chosen that the best way to simplify this is by creating a class (shouts out to K Dot)
which will have a method for each step that I used for cleaning the data 
and finding what could be dropped. 

The final method wil be the one that will return the cleaned dataframe, while 
all others should return nothing and simply be print statements.



Important Note: Yes, Kendrick was playing on loop while coding this entire project

 O      \O/      O      \O/
/|\      |      /|\      | 
/ \     / \     / \     / \
#TheyNotLikeUs
"""


from Step_01_Data_Getter import df
import pandas as pd
from IPython.display import display


class K_Dot():
    def __init__(self, df) -> None:
        self.df = df

        self.tracks_df = pd.DataFrame()
        self.albums_df = pd.DataFrame()
        self.final_df = pd.DataFrame()

    def basics(self) -> None:
        """
        This basics methods just displays (on jupyter interactive notebook)
        very high-level summary data. 

        Of prime importance is that no null values exist anywhere on any row/columns.
        This is a great starting point since we do not have to worry about 
        dropping data or data imputation which can oft be hugely
        time-consuming.


        """
        display(self.df.info())
        display(self.df.describe())


    def col_duplicates(self) -> None:
        """Another simple summary method that shows the sum of duplicate value 
        per columns (axis=1) since the dataframe does not have row-long (axis=0)
        duplicates due to specific track IDs.
        
        Here, we are fully expect many duplicates on SOME columns, while expecting
        no (or very few) duplicates on other columns. For example, we expect MANY
        duplicates on albums, but NO duplicates on Track IDs but some duplicates 
        on track names, for example. (See docstring as to why this is).

        """

        # Grab the max string character count of the df
        max_len = max(len(col) for col in self.df.columns)

        for col in self.df.columns:
            print(f"{col.ljust(max_len)} contains\t" f"{self.df[col].duplicated().sum()} duplicates")

    
    def count_duplicates(self, columns:list[str]) -> pd.DataFrame:
        """
        This method groups by the desired columns and returns a counter of how
        how many duplicates exist with max rows shown in the pandas display
        option value.

        This method was used over various columns and combinations to try and
        visually identify a pattern of duplicates and see what potentially
        can be dropped or addressed differently.

        """

        with pd.option_context('display.max_rows', None):
            ret = self.df.groupby(columns)\
                    .size()\
                    .reset_index(name='Counter')\
                    .sort_values(by='Counter', ascending=False)
            #display(ret)

        return(ret)

    
    def multi_query(self, 
                       columns:list[str], 
                       operators:list[str],
                       search_val:list) -> pd.DataFrame:
        """
        This method was put together more as a challenge than anything. 
        It would've been easier to manually type these string query by hand,
        but I saw a lot of value in creating this function I hadn't seen before
        since I see applicability in my day-to-day work for analysis as well.

        With that said, this method takes 3 lists of strings which are:
        columns: The columns in the dataframe you want to pd.query()
        operators: The matching operators that will be used on the columns
        search_val: The value you will be looking for in the columns. 

        For example, say you had an infinite dataframe with at least day of week
        like (Sunday - Saturday), weather forecast (Sunny, Rainy, etc...)
        and how many miles (int) you drove your vehicle that day.. then:

        >> columns = ['DAY_OF_WEEK', 'FORECAST', 'MILES_DRIVEN]
        >> operators = ['==', '==', '>=']
        >> search_val = ['Sunday', 'Sunny', 30]

        >> self.multi_query(columns=columns, operators=operators, search_val=search_val)

        It would return the rows where it was Sunday, Sunny, and you drove 30 miles or more.
        """

        assert len(columns) == len(operators) == len(search_val), (
                "All parameters must be equal in length\n"
                f"Length columns: {len(columns)}\n"
                f"Length operators: {len(operators)}\n"
                f"Length search_val: {len(search_val)}"
        )

        conditions = []

        for col, op, search in zip(columns, operators, search_val):
            if isinstance(search, str):
                conditions.append(f"{col} {op} \"{search}\"")
            else:
                conditions.append(f"{col} {op} {search}")

        query_str = " and ".join(conditions)

        return self.df.query(query_str)


    def drop_non_explicits(self) -> None:
        """
        It seems like the prime issues are duplicated albums (like collector's editions),
        and other entries like "Best of 2017 Hip Hop" for example, that house the same track.
        For this, we will have to aggregate our values. Additionally, it seems that
        storing the track as an explicit version and non-explicit version of course also
        create two different entries. The latter is what we will address in this method.

        For simplicity, and because I'm relatively familiar with Kendrick's "true" music,
        I will remove all non-explicit songs.
        """
        self.df = self.df.query('EXPLICIT_TRACK == True').reset_index(drop=True)
    
    def seperate_albums_and_tracks(self) -> None:
        """
        The easiest way to address the issue of random album names (not the True names),
        we are going to: 
            1) Split album names from track names as two seperate dfs,
            2) clean up album dataframe by manually dropping the non-original ones
            3) Cleaning up track df by aggregating where it makes sense (manual)
            4) Joining back together.
        """
        self.albums_df = self.df[['ALBUM_ID', 'ALBUM_NAME', 'ALBUM_RELEASE_DATE',
                                      'ALBUM_RELEASE_DATE_PRECISION', 'TRACK_ID']]
        
        self.tracks_df = self.df.iloc[:, 4:]

    def clean_albums(self, keep_these_albums:list[str], 
                     drop_column:list[str] = ['ALBUM_RELEASE_DATE_PRECISION']) -> None:

        self.albums_df = self.albums_df[self.albums_df['ALBUM_NAME'].isin(keep_these_albums)]

        #Everything looks good at this point for albums, when I ran the below
        #kdot.albums_df[['ALBUM_NAME', 'ALBUM_RELEASE_DATE']].drop_duplicates()
        # The issue is that GKMC is missing the full release date, so I will manually
        # override that with the correct date.

        # Default column dropped because the value would become a constant value of 'day'

        self.albums_df.loc[self.albums_df['ALBUM_NAME'] == 'good kid, m.A.A.d city', 'ALBUM_RELEASE_DATE'] = '2012-10-22'
        self.albums_df['ALBUM_RELEASE_DATE'] = pd.to_datetime(self.albums_df['ALBUM_RELEASE_DATE'])

        # Below we want to convert the album release date as a fractional (decimal)
        # value so we can perform regression on it as a continuous variable.
        # 365.25 is used to account for leap year.
        
        # For easier coding, we're going to make the column into a variable instead of calling it 
        # several times
        date_col = self.albums_df['ALBUM_RELEASE_DATE']

        self.albums_df['ALBUM_FRACTIONAL_DATE'] =\
                    date_col.dt.year +\
                    (date_col - pd.to_datetime(date_col.dt.year, format='%Y')).dt.days / 365


        self.albums_df = self.albums_df.drop(columns=drop_column)
        # I believe albums are cleaned up at this point. Let's head to tracks now.

    def clean_tracks(self, col_drops:list[str] = ['EXPLICIT_TRACK', 'TRACK_TYPE']) -> None:
        
        #The default columns are dropped because they're constant values
        self.tracks_df = self.tracks_df.drop(columns=col_drops)

        #Looks like after cleaning up the albums, nothing really needs to be
        # cleaned up in the tracks AFTER we inner join. Let's do that now as
        # a seperate method.
    
    def join_albums_and_tracks(self, how:str='inner') -> pd.DataFrame:
        self.final_df = pd.merge(left=self.albums_df,
                                 right=self.tracks_df,
                                    on='TRACK_ID',
                                    how=how)



    

kdot = K_Dot(df)
kdot.drop_non_explicits()
kdot.df.shape #This now brings us to a shape of (195, 22), down from (297,22)

# With that said, it looks like HUMBLE. has 8 duplicates, as our most-reapeated one, 
#for example. Let's dig into that particular one a bit more using the count duplica
duplicated_songs = list(kdot.count_duplicates('TRACK_NAME').query("Counter > 1")['TRACK_NAME'])
duplicated_songs


kdot.seperate_albums_and_tracks()

og_albums = ['To Pimp A Butterfly',
                'Mr. Morale & The Big Steppers', 'meet the grahams',
                'Not Like Us', 'Section.80', 'DAMN.', 'euphoria',
                'untitled unmastered.', 'good kid, m.A.A.d city',
                'Overly Dedicated']
kdot.clean_albums(keep_these_albums=og_albums)


kdot.clean_tracks()


kdot.join_albums_and_tracks()


cleaned_df = kdot.final_df.copy()