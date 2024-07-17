"""
Code authored by Rommel Artola

This simple file creates a class called SEC_API to perform some EDA on the SEC info. Please change the default value
of the email in the header of the innit parameter.

It has some built-in methods for automatic dataframe creation for the user, but it also gives full control to the user 
in some methods if they know the exact path they want to take, or are comfortable discovering and navigating the keys
of a JSON file-structure.

"""


import requests
import pandas as pd
import matplotlib.pyplot as plt



class SEC_API(object):

    def __init__(self, 
                 headers={'User-Agent': 'rartolalaiz@seattleu.edu'},
                 url="https://www.sec.gov/files/company_tickers.json",
                 ) -> None:
        self.headers = headers
        self.url = url


        # Attempt to connect to API upon instance creation of class that has all CIK data.
        cik_df = requests.get("https://www.sec.gov/files/company_tickers.json", headers=self.headers)
        if cik_df.status_code == 200:
            print('Successful Connection to the API')
        else:
            raise 'Connection to API not successful, please check headers and URL'

        # Create dataframe of tickers and format 'cik_str' with leading zeros as requested for API call
        self.ticker_df = pd.DataFrame.from_dict(cik_df.json(), orient='index')
        self.ticker_df['cik_str'] = self.ticker_df['cik_str'].astype(str).str.zfill(10)


        self.keys_df = None

    def read_keys(self, filename='EDGARApiKeys.txt') -> pd.DataFrame:
        """
        This method is used to read a provided .txt file with keys for the SEC API connection request
        """
        keyList = open(filename, 'r').read().split(sep=',')
        self.keys_df = list(map(lambda key: key.replace("'", '').strip(), keyList))
        self.keys_df = pd.DataFrame({'Keys Available': self.keys_df})

    def cik_from_ticker(self, 
                        ticker_symbol:str) -> str:
        """
        Returns the company CIK number in string format based on the
        string ticker symbol inputted into the function.
        Mostly a helper function, but also useful on its own, so not hidden.
        """
        ret = self.ticker_df['cik_str'][self.ticker_df['ticker'] == ticker_symbol][0]
        return ret

    def company_facts_EDA(self, ticker_symbol:str) -> dict:
        """
        Used as a supporting function for some pre-built analysis
        However, can be used by user, where method turns over all EDA (Exploratory Data Analysis) 
            aspects over to the user 
            instead of providing pre-manipulated analysis. 
        Will require user to either know the exact path they want within the companyfacts.json or 
            cycle through the .keys() to find 'new_key' and then drill down using ['new_key'] and using .keys() 
            once again.
        """ 
        cik = self.cik_from_ticker(ticker_symbol)
        facts_eda = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json', headers=self.headers)
        return facts_eda.json()


    def submission_EDA(self, ticker_symbol:str) -> dict:
        """
        Used as a supporting function for some pre-built analysis
        However, can be used by user, where method turns over all EDA (Exploratory Data Analysis) 
            aspects over to the user  
        Will require user to either know the exact path they want within the submission.json or 
            cycle through the .keys() to find 'new_key' and then drill down using ['new_key'] and using .keys() 
            once again.
        """ 
        cik = self.cik_from_ticker(ticker_symbol)
        subs_eda = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers=self.headers)
        return subs_eda.json()
    

    def get_all_filing(self, ticker_symbol:str) -> pd.DataFrame:
        """
        Using default URL formatting of: https://data.sec.gov/submission/CIK##########.json
        Pulls all the recent filings of your desired company
        This was used as a follow-through for an example.
        """
        cik = self.cik_from_ticker(ticker_symbol)
        filing_request = self.submission_EDA(ticker_symbol=ticker_symbol)
        filing_data = filing_data['filings']['recent']
        filing_df = pd.DataFrame.from_dict(filing_data)
        return filing_df
    
    def revenue_and_assets(self, ticker_symbol:str, choice:str=['Revenues', 'Assets']):
        """
        Using default URL formatting of companyfacts: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
        Method specififically built to extract either Revenues or Assets data from desired company using Ticker Symbol
        """
        assert choice!=str, 'choice parameter must be string of either Revenues or Assets value'

        if choice.capitalize().strip() not in ['Revenues', 'Assets']:
            raise 'Choice must be Revenues or Assets values only.'
        
        fact_request = self.company_facts_EDA(ticker_symbol=ticker_symbol)
        fact_data = fact_request['facts']['us-gaap'][choice.capitalize()]['units']['USD']
        fact_df = pd.DataFrame.from_dict(fact_data)
        return fact_df

    def gaap_info(self, ticker_symbol:str, key:str) -> pd.DataFrame:
        """
        This method assumes that the user is going directly into companyfacts and will choose one of the many keys available
            under facts > us-gaap > 'key' -> units -> USD. 
            The key string MUST be in PascalCase.
        When this combination does not work, the user will be informed via an error.
        This method is very similar to the revenue_and_assets, with the exception that it gives freedom to the user
            to enter any field instead of just revenue or assets. 
        This method could replace self.revenue_and_assets if the user is well informed.
        """
        info_request = self.company_facts_EDA(ticker_symbol=ticker_symbol)
        try:
            info_data = info_request['facts']['us-gaap'][key]['units']['USD']
            info_df = pd.DataFrame.from_dict(info_data)
            return info_df
        except KeyError as err:
            raise ValueError (f'Key {key} is not a valid option in the SEC API. Please make sure that the key is in PascalCase and '+
                        'that it is found in the self.keys_df after running read_keys() method.') from err

    

# Instance Class
SEC = SEC_API()

# Part 1/5: Extract Revenues from your desired Ticker Symbol Company.
SEC.revenue_and_assets('AAPL', 'Revenues')

# Part 2/5: Extract Assets from your desired Ticket Symbol Company.
SEC.revenue_and_assets('AAPL', 'Assets')

# Part 3/5:
# For this part we're going to explore company facts and look at the common stock shares data
# Instead of using a pre-built method, we'll do this one more manually.
part3 = SEC.company_facts_EDA('AAPL')['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares']
# Let's get a count of how many different forms AAPL has filed.
part3_df = pd.DataFrame(part3)
# The below code shows that we have history of up to 15 10-K which are filed annually, and 43 10-Q which are quarterly. 
# This would make it seem that after a certain number of years, either the data deletes, OR the data did not exist, thus
#   cannot be in the API. Let's find the first report.
part3_df.groupby(by='form').size()

# First filing available o the 10-K
# The earliest filing of the 10-K we have available for Apple is from 2009-10-27. 
part3_df[part3_df['form'] == '10-K'].sort_values(by='filed')[0:1]




#Part 4/5:
# Let's find information related to Net Income for Boeing
# This one uses the pre-built method that automatically goes into the US-GAAP info. Read the provided docstring.
part4_df = SEC.gaap_info('BA', 'ComprehensiveIncomeNetOfTax')

# Let's plot the val(ue) of ComprehensiveIncomeNetofTax on filed date (timeseries).
part4_ts = part4_df[['filed', 'val']].sort_values(by='filed')
# Little messy and the x-axis can be definitely cleaned up, but we're just exploring data and trend for now. 
# Seems like Boeing has been on the negative (general) trend, as far as ComprehensiveIncomeNetOfTax is concerned.
plt.plot(part4_ts['filed'], part4_ts['val'])
plt.show()


#Part 5/5:
# Let's do a similar one to above, but now let's look at AccountsPayableCurrent, or, what the trend is on how much money Boeing
#   is owing over time.
part5_df = SEC.gaap_info('BA', 'AccountsPayableCurrent')
part5_ts = part5_df[['filed', 'val']].sort_values(by='filed')
plt.plot(part5_ts['filed'], part5_ts['val'])
plt.show()
# Cool stuff! Based on the group, Boeing had a constantly-increasing amount of AccountsPayableCurrent and then had a drastic
#   decrease in said amount at some point. It has began to start accruing up the current debts though!
