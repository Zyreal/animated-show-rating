# animated-show-rating

Allows user to find the ratings of an anime using multiple sources

The app uses beautifulsoup in order to scrape the scores of MyAnimeList, Anillist, and Livechart, supplemented with selenium for any dynamic loaded sites
Any searches are then stored in a cache using Redis to decrease wait times
