# BoardGameGeek BoardGames Web Scraping

I made this project to learn how to use [Scrapy](https://scrapy.org/) framework with Python to perform web scraping.
The developed spider extracts all the board games from BoardGameGeek [website](https://boardgamegeek.com/) and exported into a csv file with the following data:

- Id
- Rank
- Name
- Url
- Rating
- Number of Votes
- Year
- Description

## Web Scrape date from an online boardgaming store [Jugamosotra](https://jugamosotra.com/es/)

After collecting the data from the boardgamegeek website, I'm using an online boardgaming store to get data about the games, more specifically:

- Id
- Name
- Price
- Availability (In Stock, Out of Stock)
- Url
- Url from Boardgamegeek
- Date

The goal is to track prices from the games in a daily basis to check if there are discounts in games that I'm interested on buying.

### Mail Notification when game reaches the target price
The final step is to define my shortlist of games that I'm interested and the respective target price.
With those parameters defined, then I use the collected data from the online store to check if the games are below the target price.
If the conditions are met, then it sends an email automatically with a personalized message to make it easier to buy the game. 
You can check this code [here](https://github.com/FilipeTheAnalyst/BoardGames/blob/master/boardgames/boardgames/PriceTracker.ipynb)

