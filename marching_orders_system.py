#arguments: mass_messenger.py usernames_to_message.csv marching_orders.csv team_members_with_stars.csv
import sys
import csv
import time
import pandas as pd
import datetime

#reads CSV file of names passed in as first argument
with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f)
    users = list(reader)

#reads marching orders
orders = pd.read_csv(sys.argv[2], header=None)
#orders['cumsum'] = 1.0
orders['cumsum'] = orders[1].cumsum()

#reassigns users to straight list of names
users = [user[0].lower() for user in users]

#creates reddit instance
#reddit = praw.Reddit(client_id='CLIENT ID HERE', client_secret='CLIENT SECRET HERE', user_agent='USER AGENT HERE', username = 'USERNAME HERE', password = 'PASSWORD HERE')

#grabs names of teammates
df = pd.read_csv(sys.argv[3])
df['user'] = df['user'].str.lower() #converts usernames to lowercase
df = df[df['user'].isin(users)] #filters out people who did not opt in
new_users = [user for user in users if user not in list(df['user'])] #grabs list of new people
ones = [1] * len(new_users) #assumes one star user
df2 = pd.DataFrame([ones, new_users]).transpose()
df2 = df2.rename(index=str, columns={0: 'max(stars)', 1:'user'})
df = df.append(df2)
df = df.sample(frac=1) #shuffles usernames
df['cumsum'] = df['max(stars)'].cumsum() #adds up all of the stars for iterating
total_stars = sum(df['max(stars)'])

#sets thresholds
orders['cumsum'] = orders['cumsum']*total_stars

#sets up looping
n = 0
today = datetime.date.today()
for user in df['user']:
    try:
        if (int(df[df['user'] == user]['cumsum']) >= int(orders['cumsum'].loc[n])) and n <= len(orders):
            n = n + 1 #increments to next set of orders
    except:
        print('Ran out of orders! Using last order...')

    try:
        order = 'marching orders for {}'.format(str(today)),'{}, Your orders are to {} territory. To make your move, go [here!](https://vote.redditcfb.com/cfbrisk.php) If you wish to be removed from this mailing list, please contact INSERT USERNAME HERE.'.format(user,orders[0].loc[n])
    except:
        print "oops"

    print order

'''
#main iteration loop
for user in df['user']:
    try:
        if (int(df[df['user'] == user]['cumsum']) >= int(orders['cumsum'].loc[n])) and n <= len(orders):
            n = n + 1 #increments to next set of orders
    except:
        print('Ran out of orders! Using last order...')
    print('Messaging ' + user + ' to ' + orders[0].loc[n])
    try:
        reddit.redditor(user).message('marching orders for {}'.format(str(today)),'{}, Your orders are to {} territory. To make your move, go [here!](https://vote.redditcfb.com/cfbrisk.php) If you wish to be removed from this mailing list, please contact INSERT USERNAME HERE.'.format(user,orders[0].loc[n]),from_subreddit='INSERT SUBREDDIT HERE')
    except:
        print('Unable to message ' + user)
    time.sleep(3)
'''
