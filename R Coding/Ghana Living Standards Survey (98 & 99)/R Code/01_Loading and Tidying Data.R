

## Library
library(haven)
library(tidyverse)



####################################### CREATION OF INDIVIDUAL DATASETS BELOW ONLY##################################
##### Load Raw Data #####

#Individual Infos
sec1 <- read_dta('Original Datasets/sec1.dta')


#Agricultre profits
agg2 <- read_dta('Original Datasets/aggregates/agg2.dta')


#Farmland size
sec8b <- read_dta('Original Datasets/sec8b.dta')




#Ecological zones
sec0a <- read_dta('Original Datasets/sec0a.dta')


#Education Information
sec2a <- read_dta('Original Datasets/sec2a.dta')
sec2a <- read_dta('Original Datasets/sec2a.dta')




#Community Demographic Info (Religion, Ethnicity)
cs1 <- read_dta('Original Datasets/community/cs1.dta')



#Community Economy and Infrastructure Dataset (Water, Banking, Public Transportation)
cs2 <- read_dta('Original Datasets/community/cs2.dta')



#Community Education Dataset
cs3 <- read_dta('Original Datasets/community/cs3.dta')

#Community Health-Related Dataset.
cs4b<- read_dta('Original Datasets/community/cs4b.dta')


#Debt
sec12a2 <- read_dta('Original Datasets/sec12a2.dta')
sec12a1 <- read_dta('Original Datasets/sec12a1.dta')


#Savings
sec12c <- read_dta('Original Datasets/sec12c.dta')



#Other datasets. Not used here.
# sec7 <- read_dta('Original Datasets/sec7.dta')
# sec8a1 <- read_dta('Original Datasets/sec8a1.dta')
# sec8a2 <- read_dta('Original Datasets/sec8a2.dta')
# sec8a3 <- read_dta('Original Datasets/sec8a3.dta')
# sec8c1 <- read_dta('Original Datasets/sec8c1.dta')
# sec8c2 <- read_dta('Original Datasets/sec8c2.dta')
# sec8d <- read_dta('Original Datasets/sec8d.dta')
# sec8e <- read_dta('Original Datasets/sec8e.dta')
# sec8f <- read_dta('Original Datasets/sec8f.dta')
# sec8g <- read_dta('Original Datasets/sec8g.dta')
# sec8h <- read_dta('Original Datasets/sec8h.dta')
# sec8hid <- read_dta('Original Datasets/sec8hid.dta')
# sec9a2 <- read_dta('Original Datasets/sec9a2.dta')
# sec9a11 <- read_dta('Original Datasets/sec9a11.dta')
# sec9a12 <- read_dta('Original Datasets/sec9a12.dta')
# sec9b <- read_dta('Original Datasets/sec9b.dta')
# sec9b0 <- read_dta('Original Datasets/sec9b0.dta')
# sec9c <- read_dta('Original Datasets/sec9c.dta')
# sec0a <- read_dta('Original Datasets/sec0a.dta')
# cs0 <- read_dta('Original Datasets/community/cs0.dta')
# sec0 <- read_dta('Original Datasets/sec0b.dta')
# sec0c <- read_dta('Original Datasets/sec0c.dta')
# agg1 <- read_dta('Original Datasets/aggregates/agg1.dta')
# subagg13 <- read_dta('Original Datasets/aggregates/subagg13.dta')
# agg8 <- read_dta('Original Datasets/aggregates/agg8.dta')
# cs0 <- read_dta('Original Datasets/community/cs0.dta')
# cs4a <- read_dta('Original Datasets/community/cs4a.dta')
# cs4c <- read_dta('Original Datasets/community/cs4c.dta')
# cs5a <- read_dta('Original Datasets/community/cs5a.dta')
# cs5b <- read_dta('Original Datasets/community/cs5b.dta')





##### Unique Key Table (used later) #####
#Let's make a unique table to query off of the other tables. This table is from sec0a that has nh_clust and region_dis_eanum as the only columns so we can merge others on it
Unique_Key_Table <- sec0a %>%
  unite("clust_nh", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  unite('reg_dis_eanum', c('region', 'district', 'eanum'), sep = "-", remove = FALSE) %>%
  select(c('clust_nh', 'reg_dis_eanum')) %>%
  rename(House_ID = clust_nh)





#### Agg Profit ####
#let's start making a smaller dataset for agriculture income per household.
#Assuming all profits are in the same currency, so no conversion done on currency amounts.
Agg_Profit_HH <- agg2 %>%
  unite("clust_nh", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  select(clust_nh, agri1c) %>%
  #Mutate_at converts values instead of creating a new column like mutate does. Similar to a CAST() on SQL.
  #Needed to convert because it was in scientific notation, and could not arrive at a useful profit per acre with it, had to convert and work my way down again.
  mutate_at(vars(agri1c), as.integer) %>%
  rename(House_ID = clust_nh,
         Agg_Profit = agri1c)





##### Next, let's get farmland size with unit of measurement for each household. We can worry about converting units later ####
#Only selecting the maximum farm size answer per household because duplicates existed.
Farm_Land_Size_Per_HH <- sec8b %>%
  unite("clust_nh", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  #unite("clust_nh_pid", c('clust', 'nh', 'pid'), sep = "-", remove = FALSE) %>% #If we want per person we can uncomment this line to break it out that way
  select(clust_nh, s8bq4a, s8bq4b) %>%
  rename("Farm_Size" = 's8bq4a',
         "Unit_Of_Measurement" = "s8bq4b") %>%
  mutate(Unit_Convert = case_when(
    Unit_Of_Measurement == 1 ~ 1,
    Unit_Of_Measurement == 2 ~ 1,
    Unit_Of_Measurement == 3 ~ (1/9)) #if 4 or anything else besides 1,2,3 it'll return NA.
  ) %>%
  mutate(Farm_Land_Size_Norm = Farm_Size * Unit_Convert) %>%
  select(-c('Farm_Size', 'Unit_Of_Measurement', 'Unit_Convert')) %>%
  group_by(clust_nh) %>%
  summarise(Max_Farm_Land_Size_Norm = max(Farm_Land_Size_Norm)) %>%
  rename(House_ID = clust_nh)





#### Next question is profit per acre of farm. We answer this one with the two datasets above. ####
Agg_Profit_Per_Acre <- merge(x = Farm_Land_Size_Per_HH, y = Agg_Profit_HH, by = 'House_ID') %>%
  mutate(Profit_Per_Acre = Agg_Profit / Max_Farm_Land_Size_Norm)
#We can drop general profit column now since we've joined.  
rm(Agg_Profit_HH, Farm_Land_Size_Per_HH)





###### Ecozone #####
#Let's look at ecological zones next.
#Below is the binary dataset just for linear regression modeling.
EcoZone_of_HH_Binary <- sec0a %>%
  unite("clust_nh", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  select(clust_nh, ez) %>%
  mutate(is_Coastal = case_when(ez == 1 ~ 1)) %>%
  mutate(is_Forest = case_when(ez == 2 ~ 1)) %>%
  mutate(is_Savannah = case_when(ez == 3 ~ 1)) %>%
  select(-ez) %>%
  rename(House_ID = clust_nh) %>%
  mutate_at(c('is_Coastal', 'is_Forest', 'is_Savannah'), ~replace_na(.,0))

#Categorical representation of the same dataset for easier graphing.
EcoZone_of_HH_Categorical <- sec0a %>%
  unite("clust_nh", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  select(clust_nh, ez) %>%
  mutate(Eco_Zone = case_when(ez == 1 ~ 'Coastal',
                              ez == 2 ~ 'Forest',
                              ez == 3 ~ 'Savannah')) %>%
  select(-ez) %>%
  rename(House_ID = clust_nh)



##### Education ####
##### The below section will give us a unique dataset that shows us the max level of education completed and education qualification by each head of household and their partners.

##### Additionally, we removed all the respondents that had "Other" (or value 96) as the answer to their education, in addition to dropping NAs.
#Selecting just the household individuals
Head_of_HH_ID <- sec1 %>%
  unite("House_ID_Person", c('clust', 'nh', 'pid'), sep = "-", remove = FALSE) %>%
  unite("House_ID", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  select(House_ID_Person, House_ID, rel) %>%
  filter(rel == 1) %>%
  select(-rel)


#Selecting partner of head of household
Partner_of_Head_ID <- sec1 %>%
  unite("House_ID_Person", c('clust', 'nh', 'pid'), sep = "-", remove = FALSE) %>%
  unite("House_ID", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  select(House_ID_Person, House_ID, rel) %>%
  filter(rel == 2) %>%
  select(-rel)



#Selecting max education qualification of all individuals in household and whether they had any shcooling or not as binary.
Education_Per_HH_and_Indiv <- sec2a %>%
  unite("House_ID_Person", c('clust', 'nh', 'pid'), sep = "-", remove = FALSE) %>%
  unite("House_ID", c('clust', 'nh'), sep = "-", remove = FALSE) %>%
  select(House_ID_Person, House_ID, s2aq1, s2aq2) %>%
  rename("Max_Educ_Cmpl" = 's2aq2') %>%
  mutate_at(c('Max_Educ_Cmpl'), ~replace_na(.,0)) %>%
  mutate(Attended_School_TF = case_when(s2aq1 == 1 ~ 1,
                                     s2aq1 == 2 ~ 0)) %>%
  filter(Max_Educ_Cmpl != 96) %>%
  select(-s2aq1)




#### Merging the previous three datasets to show highest education of the head of household. #####

##Let's start with the head of household.
Head_HH_Max_Educ <- left_join(x = Head_of_HH_ID, y = Education_Per_HH_and_Indiv, by = c('House_ID_Person', 'House_ID'), all.x = T)

#Further cleaning by dropping NA and renaming columns for post-join.
Head_HH_Max_Educ <-  Head_HH_Max_Educ %>%
  drop_na() %>%
  rename(Max_Educ_Cmpl_Head = Max_Educ_Cmpl,
         House_ID_Person_Head = House_ID_Person,
         Attended_School_TF_Head = Attended_School_TF)



#Let's get the same now for the partner of head of HH.
Partner_HH_Max_Educ <- left_join(x = Partner_of_Head_ID, y = Education_Per_HH_and_Indiv, by = c('House_ID_Person', 'House_ID'), all.x = TRUE)

Partner_HH_Max_Educ <- Partner_HH_Max_Educ %>%
  drop_na() %>%
  rename(Max_Educ_Cmpl_Partn = Max_Educ_Cmpl,
         House_ID_Person_Partn = House_ID_Person,
         Attended_School_TF_Partner = Attended_School_TF)


#Now let's merge it all together via house id and see max education per head of HH and per partner of head of HH. 
Max_Educ_Of_House <- left_join(x = Head_HH_Max_Educ, y = Partner_HH_Max_Educ, by = 'House_ID', all.x = TRUE)

#We can remove the intermediary datasets
rm(Partner_HH_Max_Educ, Head_HH_Max_Educ, Partner_of_Head_ID, Head_of_HH_ID)




#### NetWorth ####


#Creating Debt Dataframe.
#First we select the unique House_ID keys that currently owe money AND have not been fully repaid.
HH_ID_with_Debt <- sec12a1 %>%
  unite(House_ID, clust, nh, sep="-", remove = TRUE) %>%
  #q1 = Does anyone owe money in Household? 1 = Yes.
  #q2 = Has loan been fully paid. 2 = No.
  filter(s12aq1 == 1,
         s12aq2 == 2) %>%
  select(House_ID)

#Check distinct count
n_distinct(HH_ID_with_Debt$House_ID)

#Then, we create a dataframe with all House_ID and the total of loan amount.
Tot_House_Debt <- sec12a2 %>%
  unite(House_ID, c(clust, nh), sep="-", remove = TRUE) %>%
  select(House_ID, s12aq6) %>%
  group_by(House_ID) %>%
  summarise(Tot_Debt = sum(s12aq6))

#Finally, we merge the two previous datasets using inner join (if no debt exists, row is dropped, likewise, if no house_id exist, row is also dropped.)
HH_debt <- inner_join(x = HH_ID_with_Debt, y = Tot_House_Debt, by = 'House_ID')
#Then we remove the two intermediary datasets.
rm(HH_ID_with_Debt, Tot_House_Debt)



#Creating Savings Dataframe
#Savings
HH_Savings <- sec12c %>%
  unite(House_ID, clust, nh, sep="-", remove = TRUE) %>%
  select(House_ID, s12cq4) %>%
  group_by(House_ID) %>%
  summarise(Tot_Savings = sum(s12cq4))


#Merging of the two previous datasets to get a net-worth column (can further relate this with income, but let's not for the time being)
#Net Worth of HH
HH_Net_Worth <- left_join(x = HH_Savings, y = HH_debt, by = 'House_ID', all.x = TRUE)
HH_Net_Worth <- HH_Net_Worth %>%
  #VERY CLOSE Attention to the below. We are assuming that "NA" in debt means 0 debt, and NA in Savings means 0 in savings.
  #Understanding that NA COULD just mean lack of answer, but we will interpret at 0 for out analysis.
  mutate_at(c('Tot_Savings', 'Tot_Debt'), ~replace_na(.,0)) %>%
  mutate(Net_Worth = Tot_Savings - Tot_Debt)

#Now we can drop the savings and debt column
rm(HH_Savings, HH_debt)











#### Community Health #####

#Below are the community dataset answers, with one final merged dataset.
Health_Related_Binary <- cs4b %>%
  #We make a unique coloumn
  unite("reg_dis_eanum", c('region', 'district', 'eanum'), sep = "-", remove = TRUE) %>%
  #We make the values of the column s4bq0 more descriptive since we will only look at this column, we can spend a little more time cleaning it up
  mutate(is_There = case_when(s4bq0 == 10 ~ 'Hospital_Avail',
                              s4bq0 == 11 ~ 'Drugstore_Avail',
                              s4bq0 == 12 ~ 'Pharmacy_Avail',
                              s4bq0 == 13 ~ 'MaternityHome_Avail',
                              s4bq0 == 14 ~ 'Clinic_Avail',
                              s4bq0 == 15 ~ 'FamilyPlanning_Avail')) %>%
  #Same for this oclumn, since I was going to analyze using sum, I wnated the "NO" answers to be 0 instead of 2, which was the survey original value.
  mutate(Yes_No = case_when(s4bq5 == 1 ~ 1,
                            s4bq5 == 2 ~ 0)) %>%
  #Reducing our dataset.
  select(reg_dis_eanum, is_There, Yes_No) %>%
  #Needed a unique key column in the dataset for the spread to work properly
  rownames_to_column() %>%
  #Spreading the is_There column into seperate columns and carrying over the binary Yes_No value.
  spread(is_There, Yes_No) %>%
  #Reducing dataset. We can drop the rownumber now, as well as an empty "<NA>" column that was generated, assumingly, from the spread post-case statements.
  select(-c('rowname', '<NA>')) %>%
  #Grouping by our key to summarise
  group_by(reg_dis_eanum) %>%
  #Summarising by sum so each row only has values of 0 or 1 instead of NAs.
  summarise(Hospital_Avail = sum(Hospital_Avail, na.rm = TRUE),
            Drugstore_Avail = sum(Drugstore_Avail, na.rm = TRUE),
            Pharmacy_Avail = sum(Pharmacy_Avail, na.rm = TRUE),
            MaternityHome_Avail = sum(MaternityHome_Avail, na.rm = TRUE),
            Clinic_Avail = sum(Clinic_Avail, na.rm = TRUE),
            FamilyPlanning_Avail = sum(FamilyPlanning_Avail, na.rm = TRUE)) %>%
  #The below filter drops a total of 5 observations that had a sum answer of 2. Meaning wrongful entries from the data entry operator, or multiple answers per survey for those surveys.
  filter(Hospital_Avail < 2,
         Drugstore_Avail < 2,
         Pharmacy_Avail < 2,
         MaternityHome_Avail < 2,
         Clinic_Avail < 2,
         FamilyPlanning_Avail < 2)






#### Electricity ####
#Let's do a small dataset to see if a lot of households in community have electricity or only a few.
Household_Electricity_Binary <- cs2 %>%
  unite("reg_dis_eanum", c('region', 'district', 'eanum'), sep = "-", remove = TRUE) %>%
  select(reg_dis_eanum, s2q8) %>%
  #converting 2 to 0 belows because 1 is Yes and 2 is No electricity.
  mutate(Community_Electricity = case_when(s2q8 == 1 ~ 1,
                                           s2q8 == 2 ~ 0)) %>%
  select(-s2q8) %>%
  drop_na() %>%
  #dropping duplicates again. Went from 64 to 61 after having dropped NAs.
  group_by(reg_dis_eanum) %>%
  filter(row_number(reg_dis_eanum) == 1)






#### Household Water ####

#Let's do a small dataset to see where most of the households get the water during dry season.
Household_Water_Source_Dry_Szn <- cs2 %>%
  unite("reg_dis_eanum", c('region', 'district', 'eanum'), sep = "-", remove = TRUE) %>%
  select(reg_dis_eanum, s2q12) %>%
  #Let's conver survey answers to categorical values, exluding option 6 which is "other".
  mutate(Dry_Season_Water_Source = case_when(s2q12 == 1 ~ 'Private tap',
                                             s2q12 == 2 ~ 'Public tap',
                                             s2q12 == 3 ~ 'Well without pump',
                                             s2q12 == 4 ~ 'Well with pump',
                                             s2q12 == 5 ~ 'Spring, river, lake, rain water')) %>%
  #Dropping na, or answers 6 basically
  drop_na() %>%
  select(-s2q12) %>%
  #dropping duplicates again. Went from 210 to 178 after having dropped NAs.
  group_by(reg_dis_eanum) %>%
  filter(row_number(reg_dis_eanum) == 1) 






##### Banking Availability ####
#Let's do an analysis to see if the communities have a bank nearby.
Bank_in_Community_Binary <- cs2 %>%
  unite("reg_dis_eanum", c('region', 'district', 'eanum'), sep = "-", remove = TRUE) %>%
  select(reg_dis_eanum, s2q17) %>%
  mutate(Bank_Available = case_when(s2q17 == 1 ~ 1,
                                    s2q17 == 2 ~ 0)) %>%
  select(-s2q17) %>%
  drop_na() %>%
  #Went from 223 without NAs to 190 after removing duplicates.
  group_by(reg_dis_eanum) %>%
  filter(row_number(reg_dis_eanum) == 1) 


#### Transportation ####
#Let's do an analysis to see if the communities have public transport available to them in ANY capacity (i.e., does it pass by the community in any frequency?)
Public_Trans_Avail_Binary <- cs2 %>%
  unite("reg_dis_eanum", c('region', 'district', 'eanum'), sep = "-", remove = TRUE) %>%
  select(reg_dis_eanum, s2q23) %>%
  mutate(Public_Trans_In_Community = case_when(s2q23 == 1 ~ 1,
                                               s2q23 == 2 ~ 0)) %>%
  select(-s2q23) %>%
  drop_na() %>%
  #Went from 223 without NAs to 190 after removing duplicates.
  group_by(reg_dis_eanum) %>%
  filter(row_number(reg_dis_eanum) == 1) 


##### Primary School #####



#lastly, let's do an analysis to see if the communities have primary school available.
Primary_School_In_Community_Binary <- cs3 %>%
  unite("reg_dis_eanum", c('region', 'district', 'eanum'), sep = "-", remove = TRUE) %>%
  select(reg_dis_eanum, s3q1) %>%
  mutate(Primary_School_Available = case_when(s3q1 == 1 ~ 1,
                                              s3q1 == 2 ~ 0)) %>%
  select(-s3q1) %>%
  drop_na() %>%
  #Went from 223 without NAs to 190 after removing duplicates.
  group_by(reg_dis_eanum) %>%
  filter(row_number(reg_dis_eanum) == 1) 








########################################## RENAMING AND MERGING OF DATASETS BELOW #####################################################
#Removing bulk from Datasets by eliminating the default/raw datasets from our environment
rm(agg2, 
   cs1, 
   cs2, 
   cs3, 
   sec0a, 
   sec1, 
   sec2a, 
   sec8b, 
   cs4b, 
   sec12a1, 
   sec12a2, 
   sec12c)





#Let's start merging datasets to household ID:
Main_Dataset_Household <- left_join(x = Agg_Profit_Per_Acre, y = EcoZone_of_HH_Categorical, by = 'House_ID', all.x = TRUE)
Main_Dataset_Household <- left_join(x = Main_Dataset_Household, y = Max_Educ_Of_House, by = 'House_ID', all.x = TRUE)
Main_Dataset_Household <- left_join(x = Main_Dataset_Household, y = HH_Net_Worth, by = 'House_ID', all.x = TRUE)
Main_Dataset_Household <- left_join(x = Main_Dataset_Household, y = Unique_Key_Table, by = 'House_ID', all.x = TRUE)
Main_Dataset_Household <- left_join(x = Main_Dataset_Household, y = Household_Water_Source_Dry_Szn, by = 'reg_dis_eanum', all.x = TRUE)



#We can drop all the datasets that makeup the main dataset now. 
rm(Agg_Profit_Per_Acre, 
   EcoZone_of_HH_Categorical,
   Max_Educ_Of_House,
   HH_Net_Worth)















#As a last step, we can add some continuous numeric values by reg_dis_eanum to make binary set a little more helpful for predicting
binary_temp_df <- Main_Dataset_Household %>%
  select(reg_dis_eanum
         ,House_ID
         ,Max_Farm_Land_Size_Norm           #Will be max
         ,Agg_Profit                        #will be max
         ,Profit_Per_Acre                   #will be max
         ,Net_Worth) %>%                        #also max
  group_by(reg_dis_eanum, House_ID) %>%
  summarise(across(everything(), max = max))








#Let's merge all the binary datasets now.
#Need to add reg_dis_eanum to EcoZone Binary to make it useful.
EcoZone_of_HH_Binary <- left_join(x = EcoZone_of_HH_Binary, y = Unique_Key_Table, by = 'House_ID', all.x = TRUE)
Binary_Main_Dataset <- left_join(x = Bank_in_Community_Binary, y = EcoZone_of_HH_Binary, by = 'reg_dis_eanum', all.x = TRUE)
Binary_Main_Dataset <- left_join(x = Binary_Main_Dataset, y = Household_Electricity_Binary, by = 'reg_dis_eanum', all.x = TRUE)
Binary_Main_Dataset <- left_join(x = Binary_Main_Dataset, y = Primary_School_In_Community_Binary, by = 'reg_dis_eanum', all.x = TRUE)
Binary_Main_Dataset <- left_join(x = Binary_Main_Dataset, y = Public_Trans_Avail_Binary, by = 'reg_dis_eanum', all.x = TRUE)
Binary_Main_Dataset <- left_join(x = Binary_Main_Dataset, y = Health_Related_Binary, by = 'reg_dis_eanum', all.x = TRUE)
Binary_Main_Dataset <- left_join(x = Binary_Main_Dataset, y = binary_temp_df, by = c('reg_dis_eanum', 'House_ID'), all.x = TRUE) 






#We can drop all the datasets that makeup the binary main dataset now. 
rm(Bank_in_Community_Binary, 
   EcoZone_of_HH_Binary, 
   Household_Electricity_Binary, 
   Household_Water_Source_Dry_Szn, 
   Primary_School_In_Community_Binary, 
   Public_Trans_Avail_Binary,
   Health_Related_Binary)





#Reorganizing columns on both main datasets to something that makes more sense.
Main_Dataset_Household <- Main_Dataset_Household %>%
  select(reg_dis_eanum
         ,House_ID
         ,House_ID_Person_Head
         ,Attended_School_TF_Head
         ,Max_Educ_Cmpl_Head         
         ,House_ID_Person_Partn
         ,Attended_School_TF_Partner
         ,Max_Educ_Cmpl_Partn
         ,Max_Farm_Land_Size_Norm
         ,Agg_Profit
         ,Profit_Per_Acre
         ,Eco_Zone
         ,Dry_Season_Water_Source
         ,Tot_Savings
         ,Tot_Debt
         ,Net_Worth
  )


Binary_Main_Dataset <- Binary_Main_Dataset %>%
  select(reg_dis_eanum
         ,House_ID
         ,is_Coastal
         ,is_Forest
         ,is_Savannah
         ,Hospital_Avail
         ,Drugstore_Avail
         ,Pharmacy_Avail
         ,MaternityHome_Avail
         ,Clinic_Avail
         ,FamilyPlanning_Avail
         ,Bank_Available
         ,Community_Electricity
         ,Primary_School_Available
         ,Public_Trans_In_Community
         ,Max_Farm_Land_Size_Norm
         ,Agg_Profit
         ,Profit_Per_Acre
         ,Net_Worth)




#We can drop the other excess datasets now.
rm(Education_Per_HH_and_Indiv
   ,Unique_Key_Table
   ,binary_temp_df)







