import os
import numpy as np
import pandas as pd
#from PyConnect import TeradataConnect --Custom class to connect to Database
from datetime import datetime
import pyodbc
import time

class Data_Agg(TeradataConnect):
    """
    Data Processing and Management Script for Teradata Database.

    This script defines a class for managing data in a Teradata database. It provides methods for reading and processing data from external files (File1 and File2), merging, cleaning, and updating records in the Teradata database.

    Usage:
    1. Initialize an instance of the class with Teradata credentials and file paths.
    2. Execute a sequence of operations using the 'Run_All' method to process and update data in the Teradata database.

    This script contains the following methods and attributes:

    - 'read_File1': Reads the File1 data file and prepares it for further use.
    - 'read_File2': Reads the File2 data file and prepares it for further use.
    - 'merge_files': Merges the File1 and File2 data and handles duplicates.
    - 'prepare_records_for_database': Prepares records for insertion and deletion in the Teradata database.
    - 'Teradata_Delete': Deletes existing records in the Teradata database.
    - 'Teradata_Insert': Inserts new and updated records into the Teradata database.
    - 'Run_All': Orchestrates a sequence of operations to process and update data in the Teradata database.

    Class Attributes:
    - 'File1_filename' (str): Filepath to the File1 data file.
    - 'File2_filename' (str): Filepath to the File2 data file.
    - 'File1_df' (DataFrame): Data from the File1 file.
    - 'File2_df' (DataFrame): Data from the File2 file.
    - 'merged_df' (DataFrame): Merged and cleaned data.
    - 'Upload_Date' (str): Date of data upload in MM/DD/YYYY format.
    - 'Teradata_Order' (list): Column order from the Teradata current data.
    - 'records_to_add' (DataFrame): Records to be added to the Teradata database.
    - 'records_to_delete' (DataFrame): Records to be deleted from the Teradata database.

    Note: This script streamlines data management tasks for Teradata database integration, including reading, merging, and updating data.

    """
    
    #Class variables.
    source_table = 'SERVER.TABLE'
    source_table_query = f"SELECT * FROM {source_table}"
    
    
    def __init__(self, 
                 TD_uid, 
                 TD_pw,
                File1_filename,
                File2_filename):
        
        
        #Establish current Data in Teradata.
        super().__init__(teradata_uid=TD_uid,
                        teradata_password=TD_pw,
                        file_or_query=self.source_table_query)
        self.current_df = self.Run_SQL()
        self.current_df['Source_File'] = np.nan
    
    
        
        
        #Create class instance variables
        self.File1_filename    = File1_filename
        self.File2_filename    = File2_filename
        self.File1_df          = None
        self.File2_df          = None
        self.merged_df         = None
        self.Upload_Date       = datetime.now().strftime("%m/%d/%Y") #in MM/DD/YYYY format and string at the request of the users.
        self.Teradata_Order    = self.current_df.columns.tolist()
        self.records_to_add    = None
        self.records_to_delete = None


    def read_File1(self):
        """
        Reads a File1 file, which can be in .csv or .xlsx format,
        processes the data, and prepares it for further use.

        This method performs the following tasks:
        1. Reads the File1 file, proactively determining if it's in .csv or .xlsx format.
        2. Skips the first three rows during reading.
        3. Renames and drops columns, trims column names, and reorders columns.
        4. Sets default values for additional columns.
        5. Verifies the file format and raises an exception if the file is not found.

        Note: This method prepares the File1 data for use and proceeds to the next step in data processing.

        Args:
            None

        Returns:
            None: This method sets the 'File1_df' attribute of the instance to the processed DataFrame.

        Raises:
            FileNotFoundError: If the File1 file is not found, it prints a message and sets 'File1_df' to None.

        """

        print('Reading File1 file.')
        #Trying to read the file and proactively checking if it's a csv or xlsx
        try:
            #Notice it skips first three rows.
            if self.File1_filename.endswith('.xlsx'):
                self.File1_df = pd.read_excel(self.File1_filename, skiprows=3)
            elif self.File1_filename.endswith('.csv'):
                self.File1_df = pd.read_csv(self.File1_filename, skiprows=3)
            else:
                print('Please make sure File1 file is either .csv or .xlsx format')
            
            
            
            
            #Create the dictionary for renaming File1 columns
            File1_rename_dic ={'PartNumber': 'Part_no',
                              'Invoices': 'Col1',
                              'Quantity': 'Col2'
                             }
            #List of columns to be dropped in File1_df
            File1_drop_cols = ['List of columns to drop'
                             ]

            #Trim column names in case white File2ace exists
            self.File1_df.columns = self.File1_df.columns.str.strip() 
            
            #Rename and drop File1 columns
            self.File1_df.rename(columns=File1_rename_dic, inplace=True)
            self.File1_df.columns.values[6] = 'Price'
            self.File1_df.columns.values[7] = 'Cost'
            self.File1_df.drop(columns=File1_drop_cols, inplace=True)
            self.File1_df['Col3'] = 'EA'
            self.File1_df['Col4'] = np.nan
            self.File1_df['Upload_Date'] = self.Upload_Date
            self.File1_df['Source_File'] = 'File1'

            
            #Ordering Columns on Dataframes so it matches Teradata from the beginning
            self.File1_df = self.File1_df[self.Teradata_Order]
            print('File1 is read, proceeding to File2 file.')
            
        except FileNotFoundError:
            print('File1 file not found. If this was expected, no issue, the code will continue. Otherwise, please type the filename correctly or place it in the local working directory.')
            self.File1_df = None


    def read_File2(self):
        """
        Reads a File2 file, which can be in .csv or .xlsx format, processes the data,
        and prepares it for further use.

        This method performs the following tasks:
        1. Reads the File2 file, proactively determining if it's in .csv or .xlsx format.
        2. Renames and drops columns, trims column names, and reorders columns.
        3. Sets default values for additional columns.
        4. Verifies the file format and raises an exception if the file is not found.

        Note: This method prepares the File2 data for use and proceeds to the next step in data processing.

        Args:
            None

        Returns:
            None: This method sets the 'File2_df' attribute of the instance to the processed DataFrame.

        Raises:
            FileNotFoundError: If the File2 file is not found, it prints a message and sets 'File2_df' to None.

        """
        
        print('Reading File2 file.')
        #Trying to read the file and proactively checking if it's a csv or xlsx
        try:

            if self.File2_filename.endswith('.xlsx'):
                self.File2_df = pd.read_excel(self.File2_filename)
            elif self.File2_filename.endswith('.csv'):
                self.File2_df = pd.read_csv(self.File2_filename)
            else:
                print('Please make sure File2 file is either .csv or .xlsx format')
                
            
            
            
            #Create the dictionary for renaming File2 columns
            File2_rename_dic = {'Old Name': 'New Name'
                            }
            
            #List of columns to be dropped in File2_df
            File2_drop_cols = ['List of columns'
                           ]
            
            #Trimming column names
            self.File2_df.columns = self.File2_df.columns.str.strip()
        
            #Rename and drop File2 Columns
            self.File2_df.rename(columns=File2_rename_dic, inplace=True)
            self.File2_df.drop(columns=File2_drop_cols, inplace=True)
            self.File2_df['Upload_Date'] = self.Upload_Date
            self.File2_df['Source_File'] = 'File2'
            
            #Ordering Columns on Dataframes so it matches Teradata from the beginning
            self.File2_df = self.File2_df[self.Teradata_Order]
            print('File2 file is read, proceeding to merging the two files and cleaning them.')
            
        except FileNotFoundError:
            print('File2 file not found. If this was expected, no issue, the code will continue. Otherwise, please type the filename correctly or place it in the local working directory.')
            self.File2_df = None
       
    
    def merge_files(self):
         """
        Merges the File1 and File2 dataframes and handles duplicates.

        This method performs the following tasks:
        1. Checks if there are File1 or File2 data available. If one of them is missing, it uses the available data.
        2. Merges the two dataframes using 'Part_no' as the key, giving preference to File2.
        3. Sorts the merged dataframe by 'Part_no'.
        4. Drops duplicates based on the 'Part_no' column, keeping the first occurrence.

        Note: This method combines the data from both files, removing duplicates and preparing the merged data for further processing.

        Args:
            None

        Returns:
            None: This method sets the 'merged_df' attribute of the instance to the merged and cleaned DataFrame.

        """
        if self.File1_df is None:
            print('No File1 file, using only File2 data.')
            self.merged_df = self.File2_df 
        elif self.File2_df is None:
            print('No File2 file, using only File1 data.')
            self.merged_df = self.File1_df
        else:
            print('Beginning to merge the File1 and File2 File and dropping duplicates with preference on File2.')
            self.merged_df = pd.concat([self.File2_df, self.File1_df], #critical to keep self.File2_df as the first since pandas will drop the 2nd row of duplicates, not the first.
                                       ignore_index=True)
            
            self.merged_df.sort_values(by='Part_no', inplace=True) #sort values so parts are stacked with duplicates.
            
            self.merged_df = self.merged_df.drop_duplicates(subset='Part_no', keep='first') #subset focuses just on Part_no column for duplications, not the entire width of dataframe (since prices may be different)
            print('Both files are merged.')

   
    def final_parts(self):
        """
        Prepares the records to be added or deleted from the database table.

        This method performs the following tasks:
        1. Identifies records to delete by finding the intersection of 'Part_no' with the current database.
        2. Sets 'records_to_delete' as the 'Part_no' values to be deleted.
        3. Initializes 'records_to_add' with all records from the merged data.
        4. Truncates the 'Cost' column to a maximum of two decimal digits.
        5. Converts all 'np.nan' values to 'None' for compatibility with Teradata.

        Note: This method prepares the records to be added or deleted from the database table, ensuring data consistency and formatting.

        Args:
            None
            
        Returns:
            None: This method sets 'records_to_delete' and 'records_to_add' attributes of the instance.
        """
        
        
        self.records_to_delete = self.merged_df.merge(self.current_df, how='inner', on='Part_no')['Part_no']
        self.records_to_add = self.merged_df
        #Some issue with overflowing decimal digits in the BDSI_Cost column, so the below truncates it.
        self.records_to_add['Cost'] = self.records_to_add[['Cost']].applymap(lambda x: int(x * 100) / 100.0 if not np.isnan(x) else np.nan)
        #Lastly, since Teradata databases do not recognize np.nan or 'NULL' as actual NULL values, we convert all np.nan into a None value (which is an asbence of value), and is recognized as a NULL in Teradata.
        self.records_to_add = self.records_to_add.replace({np.nan: None})
        
    
    
    
    
    def Teradata_Delete(self):
        """
        Deletes records in a Teradata database that already exist in the merged data.

        This method performs the following tasks:
        1. Establishes a connection to the Teradata database.
        2. Deletes records from the Teradata table for 'Part_no' values in 'records_to_delete'.
        3. Commits the changes to the database.
        4. Measures the time taken for the batch deletions and prints the duration.

        Note: This method is responsible for removing existing records from the Teradata database, and it provides progress updates to the user.

        Args:
            None
            
        Returns:
            None: This method deletes records from the Teradata database table.

        """
        
        
        print('Beginning to delete the records in Teradata that already exist in the merged files. Changes are not committed until the last one is deleted.')
        print('This may take a while, depending on the number of parts. Go grab a coffee :)')
        delete_these_parts = self.records_to_delete.tolist()
        
        if len(delete_these_parts) == 0:
            return 'No parts to delete, proceeding to inserting parts'
        
        #else below takes place
        connection = pyodbc.connect(f'DSN={self.teradata_DSN};UID={self.teradata_uid};PWD={self.teradata_password}')
        try:
            #Time the query just for user info.
            start_time = time.time()

            # Create a cursor
            cursor = connection.cursor()

            delete_these_parts = self.records_to_delete.tolist()

            # SQL DELETE statement with a placeholder in part_no
            sql_delete = f"DELETE FROM {self.source_table} WHERE part_no = ?"

            # Execute batch deletions
            loops = 0
            loop_frequency = 1_000
            for part_number in delete_these_parts:
                loops += 1
                if loops % loop_frequency == 0: #Using this inner if as a way to show code is still working, to print every 1,000 parts.
                    print(f'Current loop: {loops} / {len(delete_these_parts)}')
                cursor.execute(sql_delete, part_number)

            # Commit the changes to the database
            connection.commit()
            
            # Stop the timer
            end_time = time.time()
            
            # Calculate and print the elapsed time
            elapsed_time = (end_time - start_time) / 60 #turn it into minutes instead of seconds
            print(f"Batch deletions successfully applied. This took {elapsed_time:.2f} minutes to run. Proceeding to inserting new values")

            
        except Exception as e:
            print("Error:", str(e))
            
        finally:
            # Close the cursor and the database connection
            cursor.close()
            connection.close()
            
            
            
            
            
    
    def Teradata_Insert(self, df_split:int=100):
        """
        Inserts records into a Teradata database table.

        This method performs the following tasks:
        1. Establishes a connection to the Teradata database.
        2. Splits the records to be inserted into DataFrame chunks for batch processing.
        3. Inserts the records into the Teradata table using batch processing with placeholders (the question marks).
        4. Measures the time taken for the batch insert and prints the duration.

        Note: This method is responsible for inserting new and previously-deleted records into the Teradata database, and it provides progress updates to the user.

        Args:
            df_split (int): The number of records to insert in each batch. Default is 100.

        Returns:
            None: This method inserts records into the Teradata database table.

        """
        
        
        print('Beginning to insert all of the values now (new and previously-deleted values).')
        print('This one will also take a while, depending on the number of parts. Maybe a snack to go alongside that coffee now...')
        
        # Sample data (replace this with your data)
        if len(self.records_to_add['Part_no'].tolist()) == 0:
               return 'No parts to insert.'
           

        
        #else the below takes place
        # Establish a connection to the Teradata database
        connection = pyodbc.connect(f'DSN={self.teradata_DSN};UID={self.teradata_uid};PWD={self.teradata_password}')

        try:
            #Time the query just for user info.
            start_time = time.time()
            
            
            # Create a cursor
            cursor = connection.cursor()

            chunks_insert_df = np.array_split(self.records_to_add, len(self.records_to_add) // df_split)

            
            # SQL INSERT statement with placeholders
            sql_insert = f"INSERT INTO {self.source_table} (Part_no, Col1, Col2, Col3, Col4, Col5, Col6, Source_File, Upload_Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

            # Iterate through the DataFrame chunks and execute batch inserts
            loops = 0
            loop_frequency = 100
            for chunk in chunks_insert_df:
                loops += 1
                if loops % loop_frequency == 0: #Using this inner if as a way to show code is still working, to print every 1,000 chunks.
                    print(f'Current chunk: {loops} / {len(chunks_insert_df)}')
                batch_data = [tuple(row) for row in chunk.values]
                cursor.executemany(sql_insert, batch_data)

            # Commit the changes to the database
            connection.commit()
            
            # Stop the timer
            end_time = time.time()
            
            # Calculate and print the elapsed time
            elapsed_time = (end_time - start_time) / 60 #turn it into minutes instead of seconds
            
            print(f"Batch insert successfully applied. This took {elapsed_time:.2f} minutes")
            print('Code completed. :)')

        except Exception as e:
            print("Error:", str(e))
            
        finally:
            # Close the cursor and the database connection
            cursor.close()
            connection.close()

        

        
    
    def Run_All(self):
        """
        Executes a sequence of operations to process and update data in a Teradata database.

        This method performs the following tasks in order:
        1. Reads the File1 data.
        2. Reads the File2 data.
        3. Merges and cleans the data.
        4. Finalizes the data for insertion.
        5. Deletes existing (matching) records in the Teradata database.
        6. Inserts new and updated records into the Teradata database.

        Note: This method sets forth a series of operations to prepare and update data in a Teradata database table.

        Args:
            None
            
        Returns:
            None: This method processes and updates data in the Teradata database.
        """
        
        self.read_File1()
        self.read_File2()
        self.merge_files()
        self.final_parts()
        self.Teradata_Delete()
        self.Teradata_Insert(df_split=100)



# Please create two .txt files with a single line each. One with your Teradata Password, and the other with your Teradata Username. 
# Store said files locally in the same working directory, and the code will read it with the below lines.
password = open('Teradata Password.txt', 'r').readline()
username = open('Teradata Username.txt', 'r').readline()

# When you are ready to commit to the code, this entire code cell and please wait patiently. It will take a while to delete and insert into Teradata.
Aggregation  = Data_Agg(username, password, 'File1 File.xlsx', 'File2 File.xlsx')
Aggregation.Run_All()