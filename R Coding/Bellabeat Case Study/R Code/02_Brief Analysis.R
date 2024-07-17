# Performing Analysis
#Quick view at the tables
skim(daily_activity)
skim(daily_sleep)
skim(daily_weight)


### SUMMARY ####

### daily_activity ###
#Average steps walked per day is about 8,330
#Average distance traveled is almost 6 (I assume miles)
#The average individual burned 2,360 calories a day, according to the trackers.


## daily_weight & daily_sleep ##
#Average time in bed per individual was 458 minutes (or about 7.60 hours)
#Average individual had a body weight of around 159 lbs and a BMI of 25.2.
#Weight and BMI both look very right-skewed. We'll be plotting that.



#Average BMI of 25.2 which classifies as "Healthy Weight" accorsing to CDC:
#https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html



#Counting distinct user ids:
dplyr::n_distinct(daily_activity$Id) #33
dplyr::n_distinct(daily_calories$Id) #33
dplyr::n_distinct(daily_intensities$Id) #33
dplyr::n_distinct(daily_sleep$Id) #24
dplyr::n_distinct(daily_weight$Id) #8


#8 participants is not very representative of much, but I will do some analysis on that still. But it is an important limitation to note.






#Let's merge datasets:
Daily_Data <- dplyr::left_join(x = daily_activity, y = daily_sleep, by = "Id")
Daily_Data <- dplyr::left_join(x = Daily_Data, y = daily_weight, by = "Id")


#We'll remove some columns that we won't use to make the table not as bulky.
Daily_Data <- Daily_Data %>%
  dplyr::select(-LogId, 
         -WeightKg, 
         -TotalSleepRecords)


str(Daily_Data)
dplyr::n_distinct(Daily_Data$Id) #33






### Graphing ###
ggplot(data = Daily_Data, aes(x=WeightPounds, y=BMI)) + 
  geom_smooth(method = lm, se = FALSE) + 
  geom_point() + 
  labs(title="Body Weight vs BMI", 
       caption="", 
       x="Weight (lbs)", 
       y="Body Mas Index (BMI)")


#Let's filter out that outlier for our purposes and regraph
Daily_Data_Filtered <- Daily_Data %>%
  filter(WeightPounds <= 250)


ggplot(data = Daily_Data_Filtered, aes(x=WeightPounds, y=BMI)) + 
  geom_smooth(method = lm, se = FALSE) + 
  geom_point() + 
  labs(title="Body Weight vs BMI", 
       caption="", 
       x="Weight (lbs)", 
       y="Body Mas Index (BMI)")




#Let's look at distance vs calories burned by self reporting or not
ggplot(data = Daily_Data_Filtered, aes(x=TotalDistance, y=Calories_Burned)) + 
  geom_jitter(aes(color=IsManualReport)) + 
  geom_smooth(method = lm, se = FALSE) + 
  labs(title="Distance VS Calories Burned", 
       subtitle="Seperated by whether entry was self-logged or automatically generated", 
       caption="Longer distances tend to result in more calories burned", 
       x="Distance (miles)", 
       y="Calories Burned", 
       color = "Manually Reported?")

#The above graphs is telling me that more calories were burned as distance traveled increased. 






#Daily Activity Graph on Calories Burned
ggplot(data = daily_activity, aes(x=TotalMinutesActive, y=Calories_Burned)) + 
  geom_jitter(color="red", alpha=.5) + 
  geom_smooth(color="black", method = lm, se = FALSE) + 
  labs(title="Minutes Being Active VS Calories Burned", 
       caption="Longer times of activity tends to results in more calories burned", 
       x="Total Minutes Spent Being Active", 
       y="Calories Burned")




#Last sets of graph:
#1) daily_activity for total minutes active and date
daily_activity %>% 
  ggplot(aes(x=ActivityDate, y=TotalMinutesActive)) + 
  geom_smooth() + 
  labs(title="#1 Length of Activity by Date", 
       subtitle="When were people most active?", 
       caption="Decline in activity after May", 
       x="Date", 
       y="Minutes Spent Being Active")



#2) daily_calories for activity day and calories burned
daily_calories %>% 
  ggplot(aes(x=ActivityDay, y=Calories_Burned)) + 
  geom_smooth() + 
  labs(title="#2 Amount of Calories Burned by Date", 
       subtitle="When were people burning the most calories?", 
       caption="Rapid decline in burned calories after May", 
       x="Date", 
       y="Amount of Calories Burned")


#3) daily_sleep for total time asleep and sleep day
daily_sleep %>% 
  ggplot(aes(x=SleepDay, y=TotalMinutesAsleep)) + 
  geom_smooth() + 
  labs(title="#3 Time Spent Sleeping by Date", 
       subtitle="When were people sleeping the most?", 
       caption="Increase in time spent sleeping after May", 
       x="Date", 
       y="Minutes Spent Sleeping")


#4) daily_steps for total steps and date
daily_steps %>% 
  ggplot(aes(x=ActivityDay, y=StepTotal)) + 
  geom_smooth() + 
  labs(title="#4 Amount of Steps by Date", 
       subtitle="When were people walking the most?", 
       caption="Decline in steps after May", 
       x="Date",
       y="Number of Steps in a Day")



#5) daily_weight for weight(lbs) and date.
daily_weight %>% 
  ggplot(aes(x=Date, y=WeightPounds)) + 
  geom_smooth() + 
  labs(title="#5 Body Weight by Date", 
       subtitle="Trends in body weight by date", 
       caption="Overall decreasing, but potential trend for increase after May", 
       x="Date", 
       y="Body Weight (lbs)")
