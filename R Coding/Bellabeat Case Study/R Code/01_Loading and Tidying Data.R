library(tidyverse)
library(skimr)
library(janitor)
library(here)
library(lubridate)


# Loading The Data
#Since we've uploaded all of our datasets we may use by uploading it via a .zip file into the files window, 
#we can now read and import them. We'll only be examining the *daily* datasets (including weight log) in this study, 
#so the other dataset reads have been commented out.

OG_daily_activity <- read_csv("dailyActivity_merged.csv")
OG_daily_calories <- read_csv("dailyCalories_merged.csv")
OG_daily_intensities <- read_csv("dailyIntensities_merged.csv")
OG_daily_steps <- read_csv("dailySteps_merged.csv")
OG_sleep_day <- read_csv("sleepDay_merged.csv")
OG_weight_log <- read_csv("weightLogInfo_merged.csv")
## heartrate_seconds <- read_csv("heartrate_seconds_merged.csv")
### hourly_calories <- read_csv("hourlyCalories_merged.csv")
## hourly_intensities <- read_csv("hourlyIntensities_merged.csv")
## hourly_steps <- read_csv("hourlySteps_merged.csv")
## minute_calories <- read_csv("minuteCaloriesNarrow_merged.csv")
## minute_intensities <- read_csv("minuteIntensitiesNarrow_merged.csv")
## minute_MET <- read_csv("minuteMETsNarrow_merged.csv")
## minute_sleep <- read_csv("minuteSleep_merged.csv")



#### Cleaning & Transforming Data ####
#I first want to start with some removal of data that I find to not be needed for my analysis on one dataset, 
#then we'll do all the others separately.

# Let's first examine daily activity
skim_without_charts(OG_daily_activity)
summary(OG_daily_activity)




#We'll begin with some cleaning of OG_Daily_Activity. OG_Daily_Activity has some columns/rows that don't make too much sense or don't add value to my analysis such as... 
###LoggedActivitiesDistance being mostly 0 values. 
## We'll be removing the rows where Calories = 0. I interpret this as tracker was simply not used that day, or it malfunctioned. 
## We'll check for and remove duplicates
## We'll rename Calories column to Calories_Burned


# Let's first filter out the rows where Calories = 0.
# Removing where TotalSteps = 0 because no tracker used that day.
# Remove Where SedentaryMinutes = 1440
daily_activity <- OG_daily_activity %>%  
  filter(Calories != 0,
         TotalSteps != 0,
         SedentaryMinutes < 1440) %>%
  # Then, we can remove the column LoggedActivitiesDistance
  # LoggedActivtiesDistance was mostly 0 values, and I will not be using this column for my analysis.
  select(-LoggedActivitiesDistance) %>%
  #removing duplicates if any
  unique()


#Next steps of tidying data:
#Let's also rename Calories to Calories_Burned. My assumption is that since the tracker can't track calories consumed, then it must mean that Calories == Calories Burned.
daily_activity <- daily_activity %>%
  rename(Calories_Burned = Calories) %>%
  #Let's add a total column to add all minutes spent being active (not including sedentary activity)
  mutate(TotalMinutesActive = (VeryActiveMinutes + 
                                 FairlyActiveMinutes + 
                                 LightlyActiveMinutes))

#Let's format the date column
daily_activity$ActivityDate <- as.Date(daily_activity$ActivityDate , format = "%m/%d/%y")


#We've cleaned this dataset.
head(daily_activity)





#Let's proceed and do the rest with all other datasets.
# OG_Daily_Calories
#Removing Calories = 0 rows from OG_daily_calories
daily_calories <- OG_daily_calories %>%  
  filter(Calories != 0) %>%
  #Let's rename Calories to Calories Burned
  rename(Calories_Burned = Calories) %>%
  #Let's remove duplicates
  unique()
  

#Transform Date Column.
daily_calories$ActivityDay <- as.Date(daily_calories$ActivityDay , format = "%m/%d/%y")




# OG_daily_intensities
#Removing rows from OG_daily_intensities where SedentaryMinutes=1440 because that's 24 hrs hours, which means tracker was not used. Although I see some values as 1439 minutes on SedentaryMinutes, I am keeping those because tracker report some level of activity. Important limitation to note.
daily_intensities <- OG_daily_intensities %>%  
  filter(SedentaryMinutes != 1440) %>%
  #Let's remove duplicates
  unique()

#Transform Date Column.
daily_intensities$ActivityDay <- as.Date(daily_intensities$ActivityDay , format = "%m/%d/%y")




# OG_daily_steps

#Remove rows from OG_daily_steps where StepTotal = 0. Although it does not mean the tracker was not used that day, that is an assumption I will be making on this analysis.
daily_steps <- OG_daily_steps %>% 
  filter(StepTotal != 0) %>%
  #Let's remove duplicates
  unique()

#Transform Date Column.
daily_steps$ActivityDay <- as.Date(daily_steps$ActivityDay , format = "%m/%d/%y")




# OG_sleep_day
#OG_sleep_day data seems good. Will only convert name for consistency and removing duplicates.
daily_sleep <- OG_sleep_day %>%
  unique()
#Transform Date Column removing time.
daily_sleep$SleepDay <-gsub(" 12:00:00 AM","",as.character(daily_sleep$SleepDay))
daily_sleep$SleepDay <- as.Date(daily_sleep$SleepDay , format = "%m/%d/%y")




# OG_weight_log
#We'll remove the Fat column from the OG_weight_log dataset, remove duplicates, and rename dataset as we've done with the others. Not enough data in Fat column and fitness trackers are not reliable measures of body fat. Additionally, if body fat was self-reported, those numbers are also very likely to not be representative.
daily_weight <- OG_weight_log %>%
  select(-Fat) %>%
  #Let's remove duplicates
  unique()


#Transform Date Column removing time.
daily_weight$Date <-gsub(" 11:59:59 PM","",as.character(daily_weight$Date))
daily_weight$Date <- as.Date(daily_weight$Date , format = "%m/%d/%y")
