import numpy as np
import pandas as pd
import seaborn as sns


#from PyConnect import TeradataConnect --Custom class I made to connect up to Teradata server, not shown here.
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

#Password and username string.
password = open('password.txt', 'r').readline()
username = open('username.txt', 'r').readline()
sql_file = open('Part Characteristics.sql', 'r').read()

df = TeradataConnect(teradata_uid=username,
                     teradata_password=password,
                     file_or_query=sql_file).Run_SQL()
df


# Create the Analysis class
class Cost_Estimator(object):
    
    # Define a grid of hyperparameter values to search
    # Based on testing outside of the class, the initial value of each dictionary key was the best.
    param_grid = {
        'n_estimators':         [300, 800],
        'max_depth':            [None],     
        'min_samples_split':    [5, 10],
        'min_samples_leaf':     [1],
        'max_features':         [0.25, 0.50, 'auto']
        }

    
    def __init__(self, dataframe,
                 random_state,
                 test_size):
        
        self.all_data = dataframe
        
        self.part_index = self.all_data[['PART_NUMBER']]
        self.df = self.all_data.drop('PART_NUMBER', axis=1)
        
        
        self.Y_var          = 'COST_ONE'
        self.seed           = random_state
        self.test_size      = test_size
        
        # Variables that will be created later        
        self.df_encoded         = None
        self.X                  = None
        self.Y                  = None
        self.string_cols        = None
        self.numeric_cols       = None
        self.X_train            = None
        self.X_test             = None
        self.Y_train            = None
        self.Y_test             = None
        self.default_rf         = None
        self.grid_search        = None
        self.Y_pred             = None
        self.mse                = None
        self.r_squared          = None
        self.important_features = None
        self.max_pred           = None
        self.pred_diff_df       = None
        
        #The default best parameters for the RandomForestRegressor.
        self.best_params = {'max_depth': None,
                   'max_features': 0.25,
                   'min_samples_leaf': 1,
                   'min_samples_split': 5,
                   'n_estimators': 300}
        
    
    def value_checker(self):
        df = self.df if self.df_encoded is None else self.df_encoded
        print('NA Count:\n', df.isna().sum())
        print('End of NA counts\n')
        for colname in df.columns:
            print(df[colname].value_counts()) 
    
    def transform_dummies(self):
        # # Handle NaNs using SimpleImputer (replace NaNs with median)
        # imputer = SimpleImputer(strategy='median')
        # imputed_OPPOSITE_COST = pd.DataFrame(imputer.fit_transform(self.all_data[['OPPOSITE_COST']]), columns=['OPPOSITE_COST'])
        # #Fill missing OP prime cost with medians.
        # self.df_encoded['OPPOSITE_COST'] = imputed_OPPOSITE_COST['OPPOSITE_COST']
        
        #Let's convert the numeric 0/1 columns to match pandas get_dummies of T/F bool datatypes.
        self.numeric_cols = self.df.select_dtypes(include=['int64']).columns.tolist()
        self.df[self.numeric_cols] = self.df[self.numeric_cols].astype(bool)
        
        
        self.string_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        self.df_encoded = pd.get_dummies(self.df, columns=self.string_cols, prefix_sep='*')
        # Identify columns with NaN values
        #columns_with_nan = self.df_encoded.columns[self.df_encoded.isna().any()].tolist()
        # Drop columns with NaN values
        #self.df_encoded = self.df_encoded.drop(columns=columns_with_nan)
        self.df_encoded = self.df_encoded.reindex(sorted(self.df_encoded.columns), axis=1) #sorting by column names
        
    def split_variables(self, Y_var:str='COST_ONE'):
        self.Y_var = Y_var
        self.X = self.df_encoded.drop(self.Y_var, axis=1)
        self.Y = self.df_encoded[self.Y_var]    
    
    
    def split_data(self):
        #Only used for residuals/testing, but all data will be fed into model due to cross-validation folding.
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=self.test_size, random_state=self.seed)
        
    
    def param_tuning(self):
        
        #using Random/Default hyperparameters for now.
        default_rf = RandomForestRegressor(n_estimators=128,         # Number of trees in the forest (Max ideal might be 128)
                                            max_depth=None,              # Maximum depth of the tree (None means unlimited)
                                            min_samples_split=2,         # Minimum samples required to split an internal node
                                            min_samples_leaf=1,          # Minimum number of samples required to be at a leaf node                  (tweak this one to avoid some noise from outliers)
                                            max_features='auto',         # Number of features to consider for the best split (auto=sqrt(n_features))
                                            random_state=self.seed)      # Seed for random number generator (for reproducibility)
    
        #Hyperparameter Tuning Now.
        self.grid_search = GridSearchCV(estimator=default_rf, 
                                   param_grid=self.param_grid, 
                                   cv=5,                                #5 due to relatively smaller dataset.
                                   scoring='neg_mean_squared_error',    #Using negative MSE as the scoring metric in scikit-learn is a common practice because grid search aims to maximize the score, and minimizing negative MSE is equivalent to minimizing MSE.
                                   n_jobs=-1)                           #all available CPU cores will be used for parallel processing when using -1
        
        self.grid_search.fit(self.X, self.Y)
        self.best_params = self.grid_search.best_params_
        
        print(f'The best params were {self.best_params}')

    def create_model(self):
        self.best_rf = RandomForestRegressor(**self.best_params, random_state=self.seed)
        self.best_rf.fit(self.X, self.Y)

    def predict(self):
        self.Y_pred = self.best_rf.predict(self.X_test)
        return self.Y_pred
    
    
    def residuals(self):
        self.resids = (self.Y_test - self.Y_pred )
        return self.resids
    
    def MSE(self):
        self.mse = mean_squared_error(self.Y_test, self.Y_pred)
        return self.mse
    
    def r2(self):
        self.r_squared= r2_score(self.Y_test, self.Y_pred)
        return self.r_squared
    
    def print_performance(self):
        resid = self.residuals()
        MSE = self.MSE()
        r_sqrd = self.r2()
        print(f"Max Residual: {max(resid)}\n"
              f"Min Residual: {min(resid)}")
        print(f"Mean Squared Error (MSE): {MSE}")
        print(f"R-squared (R2): {r_sqrd}")
        
        
    def feature_importance(self):
        feature_importances = pd.DataFrame({'Feature': self.X.columns, 'Importance': self.best_rf.feature_importances_})
        self.important_features = feature_importances.sort_values(by='Importance', ascending=False)
        
        print("Feature Importances:")
        print(self.important_features)

    
    
    
    def calc_pred_diff(self):
        pred_diff_df = self.part_index.merge(pd.DataFrame(self.Y_test), how='inner',
                                            left_index=True, right_index=True)

        pred_diff_df = pred_diff_df.merge(pd.DataFrame({'RF_COST': self.Y_pred}), how='inner',
                                        left_index=True, right_index=True)

        pred_diff_df['COST_DIFF'] = (pred_diff_df['COST_ONE'] - pred_diff_df['RF_COST']).fillna(pred_diff_df['RF_COST'])
    
        self.pred_diff_df = pred_diff_df
        
        diff = self.pred_diff_df['COST_DIFF']
        plt.hist(diff)
        plt.xlabel('Amount Difference')
        plt.ylabel('Frequency')
        plt.title('Histogram of Residuals\n'
                'Resid = Cost One - Predicted')
        
        print(self.pred_diff_df)
    
    
    def test_new_part(self, new_parts_df:str):
        
        new_parts_X_df = new_parts_df.drop(['PART_NUMBER', 'COST_ONE'], axis=1)
        numeric_cols = new_parts_X_df.select_dtypes(include=['int64']).columns.tolist() #select the numeric columns
        new_parts_X_df[numeric_cols] = new_parts_X_df[numeric_cols].astype(bool)        #converts 1/0 to T/F.

        string_cols = new_parts_X_df.select_dtypes(include=['object']).columns.tolist() #select string columns
        new_parts_df_encoded = pd.get_dummies(new_parts_X_df, columns=string_cols, prefix_sep='*') #gets the dummies from these by unpivot and converting to T/F.

        # Identify columns with NaN values
        #columns_with_nan = new_parts_df_encoded.columns[new_parts_df_encoded.isna().any()].tolist()
        # Drop columns with NaN values
        #new_parts_df_encoded = new_parts_df_encoded.drop(columns=columns_with_nan)

        new_parts_columns = new_parts_df_encoded.columns.tolist()

        full_model_columns = [i for i in self.df_encoded.drop('COST_ONE', axis=1).columns.tolist() if i not in new_parts_columns]

        new_parts_final = pd.DataFrame(columns=new_parts_columns + full_model_columns)
        new_parts_final[new_parts_columns] = new_parts_df_encoded

        # Iterate through column names and set values
        for column_name in full_model_columns:
            if '*IS_NULL' in column_name:
                new_parts_final[column_name] = True
            else:
                new_parts_final[column_name] = False

       

        new_parts_final = new_parts_final.reindex(sorted(self.df_encoded.drop('COST_ONE', axis=1).columns.to_list()), axis=1)

        new_parts_pred_Y = self.best_rf.predict(new_parts_final)

        final_predict_df = pd.DataFrame({'PART_NUMBER': new_parts_df['PART_NUMBER'],
                        'COST_ONE': new_parts_df['COST_ONE'],
                        'RF_COST': new_parts_pred_Y})
        final_predict_df['COST_DIFF'] = (final_predict_df['COST_ONE'] - final_predict_df['RF_COST'])#.fillna(final_predict_df['RF_COST'])
        
        return final_predict_df
        
        
        
    def Run_All(self):
        #self.value_checker()
        self.transform_dummies()
        self.split_variables()
        self.split_data()
        #self.param_tuning() #Only needed to run on a as-needed basis due to computational requirements
        self.create_model()
        self.predict()
        self.residuals()
        self.MSE()
        self.r2()
        self.feature_importance()
        self.print_performance()
        self.calc_pred_diff()
        

cost_class = Cost_Estimator(dataframe=df,
                            random_state=777,
                            test_size=0.20)
cost_class.Run_All()
#cost_class.transform_dummies()
#cost_class.split_variables()
#cost_class.split_data() #used to calculate residuals, but not build the model
#cost_class.create_model() #uses the best params
#cost_class.predict()
#cost_class.feature_importance()
#cost_class.residuals()
#cost_class.r2()
#cost_class.MSE()
#cost_class.print_performance()



new_parts = """  
                Query here
            
            """
predict_part_query = open('New Part Test.sql', 'r').read().replace("'CHANGE_THIS_PART_NUMBER_HERE'", new_parts)

new_parts_df = TeradataConnect(teradata_uid=username,
                     teradata_password=password,
                     file_or_query=predict_part_query).Run_SQL()
 
new_parts_df




y = cost_class.test_new_part(new_parts_df)
plt.hist(y['COST_DIFF'])



print(min(y['COST_DIFF']), max(y['COST_DIFF']))



plt.scatter(x=y['COST_ONE'], y=y['COST_DIFF'], alpha=0.7)
plt.xlabel('Actuals')
plt.ylabel('Residuals')
plt.title('RF Model')
plt.axline((0,-2500), slope=1, color='red', linestyle='--')
plt.show()
