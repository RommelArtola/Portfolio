
############ GRAPHING, PLOTTING, AND LM BELOW ONLY #############################

#Density of net worth in eco zones
ggplot(drop_na(Main_Dataset_Household), aes(x = Eco_Zone, y = Net_Worth/100000, color = Eco_Zone)) + 
  geom_violin(fill = "midnightblue") + 
  geom_jitter(position = position_jitter(.2)) +
  ylim(-5,5) + 
  theme(axis.text.y = element_blank()
        ,axis.title.y = element_blank()
        ,legend.position = "bottom") +
  labs(x = "Ecological Zone" 
       ,y = "Net Worth (in 100K)"
       ,title = "Net Worth Density in Households by Ecological Zone"
       ,subtitle = "Net Worth Shown in 100K units"
       ,caption = "Net Worth is defined as Total Savings - Total Debt only"
       ,fill = "Ecological Zones:") + 
  coord_flip()







#Count of water sources for all households, wrapped by eco zone
ggplot(drop_na(Main_Dataset_Household), aes(x = Dry_Season_Water_Source, fill = Dry_Season_Water_Source)) + 
  geom_bar() +
  geom_text(stat='count', aes(label=after_stat(count)), hjust=2)+
  facet_wrap(vars(Eco_Zone), scales = "free_x") +   
  theme(axis.text.y = element_blank()
        ,axis.title.y = element_blank()
        ,legend.position = "bottom") +
  labs(y = "Count"
       ,title = "Count of Water Source (during dry season only)"
       ,subtitle = "Sub-sectioned by ecological zone"
       ,caption = "Note that count labels are not not standardized to better show distribution between zones"
       ,fill="Water Sources:"
  ) +
  #Below function where x is the x variable called above
  scale_x_discrete(labels = function(x) str_wrap(x, width = 10)) +
  coord_flip()








#Scatter of Net Worth to Profit Per Acre
ggplot(drop_na(Main_Dataset_Household), aes(x = Profit_Per_Acre/10000, y = Net_Worth/10000)) +
  geom_jitter(color = "midnightblue") + 
  labs(y = "Net Worth (in 10K)"
       ,x = "Profit Per Acre (in 10K)"
       ,title = "Relationship of Total Agricultural Profit and Net Worth"
  ) + 
  xlim(0,200) + 
  ylim(0,200)



#Distribution of max education completed between head and partner.
ggplot(drop_na(Main_Dataset_Household), aes(x = Max_Educ_Cmpl_Head, y = Max_Educ_Cmpl_Partn)) + 
  geom_jitter(aes(color = Eco_Zone), size = 3) + 
  geom_smooth(fill = "midnightblue", color = "red") +
  labs(x = "Max Education (Head of Household)" 
       ,y = "Max Education (Partner of Head of Household)"
       ,title = "Education Correlation Between Head of Household and Partner"
       ,color = "Ecological Zone:") +
  theme(legend.position = "top")



#As a last interesting plot of education, we can look at a "matrix" (4 square) of the relationship between when 1 goes to school, and the result of the other
ggplot(drop_na(Main_Dataset_Household), aes(x = Attended_School_TF_Head, y = Attended_School_TF_Partner)) + 
  geom_jitter(aes(color = Eco_Zone), size = 3) + 
  labs(x = "Head of House Attended School (T/F)" 
       ,y = "Partner of Head of House Attended School (T/F)"
       ,title = "Education Correlation Between Head of Household and Partner"
       ,color = "Ecological Zone:") +
  theme(legend.position = "top")

