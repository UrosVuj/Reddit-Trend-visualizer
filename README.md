# Reddit comment visualizer script

A Reddit script written in Python using PRAW, Pushshift RESTful API, Pandas and Matplotlib.

-[PRAW](https://github.com/praw-dev/praw) - Python Reddit API Wrapper

-[Pushshift](https://github.com/pushshift/api)

## What it does and how it does it 

The script is used for visualizing the amount of comments certain threads in a subreddit have (in this example, /r/serbia and its random discussions) in a set timeframe.
It uses PRAW to communicate with the Reddit API and Pushshift to surpass the limitations of it, the main being downloading small amounts of data per request. The data downloaded in a JSON format. 
_Note_ that Pushshift doesn't misuse or abuse a flaw in the Reddit API, it runs in compliance with it.

EDIT: Pushshift API is replaced with PSAW (Pushshift API Wrapper), the reason being code simplicity for readers. The project realization is the same, while some parts are just being hidden behind a wrapper. 

All of the data is then loaded inside a  Pandas DataFrame for manipulation purposes. Columns which are not needed are dropped and submissions are then filtered by title. If a submission has a title corresponding to a random discussion, it is kept and renamed for the sake of convenience. 

After the data selection, a line graph and a bar plot are created as 2 different subplots. The line graph is perfect for displaying the comment amount growth over time. Meanwhile the bar plot is used to show the average comment amount of these threads and with that, which ones are more popular during the week.

## Conclusion

The script, while looking specialized for a certain type of subreddit and submission title, is a great base for building similar reddit scripts. Examples can be something like visualizing NBA Game Threads in /r/nba and their popularity in the regular season vs playoff time, or displaying certain trends and their life cycles in pop culture by using the number of times they are mentioned in all of reddit.

## Example

[Image](https://github.com/UrosVuj/Reddit-comment-visualizer/blob/master/Scraper_visualization.png?raw=true)








