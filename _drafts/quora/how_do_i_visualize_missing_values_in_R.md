To visualize missing values in R I would use the Tidyverse ecosystem with dplyr and ggplot2 for the visualisation.

First of all you can aggregate the number of missing values in a very generic way with dplyr. The "gather" function is your friend here:

missing.values <- data %>% 
   gather(key = "feature", value = "val") %>%
   mutate(is.missing = http://is.na(val)) %>%
   group_by(feature, is.missing) %>%
   summarise(num.missing = n()) %>%
   select(-is.missing) %>%
   ungroup()
You have different options to visualize empty values. In it's simplest version you check the number of empty values with a barchart:

missing.values %>%
  ggplot() +
  geom_bar(aes(x=key, y=num.missing), stat = 'identity') +
  labs(x='variable', y="number of missing values", title='Number of missing values') +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

A more sophisticated way to visualise missing values is a stacked barchart and chart that visualises in which row values are missing. This way you can identify patterns:


Last year I wrote a blog article with code samples about the topic: Missing value visualization with tidyverse in R

