# What do you have to consider when scraping websites

Over the last years I scraped many websites to get data for my data science projects, because I am neither Google nor Facebook with a ton of data. Scraping data from websites is often the only way to get data for
your analysis project or for training a model. However, we all know it's a grey zone area. There are a few things you need to be aware of:

The first step in every scraping project is a non-technical one: __Check the legal stuff__. Always check the Terms Of Service and the robots.txt to check what data you are allowed to fetch and what you can do with. It's essentiell as you don't want to get sued by a big player in the market.

A major issue with scraping data is that you often get blocked. On the one hand you don't want to wait for hours for the data, therefore you have to parallize your scraper code, on other hand if you send too many requests you get blocked. You have to take measures for not being blocked. Either __use proxies__ or try to send less requests. Forget about free proxies, instead use first class proxies. However, a high-quality proxy service comes as it's price, that's a bitter truth for a scraper.

__Always keep the raw files__. This is important, because you don't want to fetch the same page over and over again. __Separate the logic for fetching the raw data and the data parsing__. Save the raw data in a database (MongoDB's GridFS is my favourite). Once the raw data is there, you can concentrate on the logic, that extracts the data without being worried about getting blocked. Maybe you need to extract more data later, then you still have the raw data available.

Last year I wrote an detalied article ["10 Lessons Learned from Scraping Websites"](https://jenslaufer.com/data%20retrieval/10_lessons_learned_from_scraping_websites.html) about the topic.
