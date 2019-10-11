import pandas as pd
import datetime as dt
import config
import praw
from psaw import PushshiftAPI
import matplotlib.pyplot as plt


def login():
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.personal,
                         client_secret=config.not_so_secret,
                         user_agent='github.com/UrosVuj')
    return reddit


# converts UNIX time to
# regular date-time format
def get_date(created):
    return dt.datetime.fromtimestamp(created)


main_reddit = login()
api = PushshiftAPI()

start_epoch = int(dt.datetime(2016, 1, 1).timestamp())

list_of_pushshift_data = list(api.search_submissions(after=start_epoch,
                                                     subreddit='serbia',
                                                     filter=['created_utc', 'num_comments', 'title']))

pushshift_data = pd.DataFrame(list_of_pushshift_data)

# drop unnecessary columns
pushshift_data.drop('created', axis=1, inplace=True)
pushshift_data.drop('d_', axis=1, inplace=True)

_timestamp_pushshift = pushshift_data['created_utc'].apply(get_date)
pushshift_data = pushshift_data.assign(timestamp=_timestamp_pushshift)

# cleaning up the DataFrame
pushshift_data.rename({"created_utc": "Time Of Creation",
                       "title": "Title",
                       "num_comments": "Number Of Comments",
                       }, axis=1, inplace=True)

# keep only the random discussion threads
# which have a simple title format
pushshift_data['Title'] = pushshift_data['Title'].str.slice(32, 47)
pushshift_data = pushshift_data[(pushshift_data['Title'].isin(['sredinu nedelje',
                                                               'početak nedelje',
                                                               'vikend (late we']))]

pushshift_data['Title'] = pushshift_data['Title'].str.replace('sredinu nedelje', 'Mid week')
pushshift_data['Title'] = pushshift_data['Title'].str.replace('početak nedelje', 'Early week')
pushshift_data['Title'] = pushshift_data['Title'].str.replace('vikend \(late we', 'Weekend')

pushshift_data.set_index('timestamp', inplace=True)

colors = {'Mid week': 'yellowgreen', 'Early week': 'darkcyan', 'Weekend': 'tomato'}

# Some invalid threads exist where there are 0 or less
# than 100 comments. These are usually the threads that were deleted.
# Pushshift doesn't sift through them correctly so we need to drop them
pushshift_data.drop(pushshift_data.loc[pushshift_data['Number Of Comments'] < 80].index, inplace=True)

# Creates one more dataframe used for plotting
# the second visualization
second_df = pushshift_data.copy()
second_df.drop('Time Of Creation', inplace=True, axis=1)

pushshift_data = pushshift_data.groupby('Title')['Number Of Comments']

# creating subplots for 2 visualizations
fig, (ax0, ax1) = plt.subplots(nrows=1, ncols=2)

# plot number 1
for key, grp in pushshift_data:
    grp.plot(ax=ax0, legend=True, color=colors[key])

# plot number 2
second_df = second_df.groupby(['Title']).mean().plot(ax=ax1, legend=False, kind='bar', color='forestgreen')

#  Tidying up everything
myLabels = ['Early week', 'Mid week', 'Weekend']
ax0.legend(labels=myLabels)
ax0.set_xlabel('Date of creation')
ax0.set_ylabel('Number of comments')
ax0.set_title('Over time')
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

ax1.set_xlabel('Type of thread')
ax1.set_ylabel('Number of comments')
ax1.set_title('Average')
ax1.tick_params(axis='x', rotation=90)

fig.suptitle("Comment distribution in /r/serbia 'random discussion' threads  \n \n 2017-")
plt.show()
