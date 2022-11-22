import praw
import time
import argparse
import random
import pickle

filename = 'mypickle.pk'

with open(filename, 'rb') as f:
    already_submitted = pickle.load(f)
print(already_submitted)

parser = argparse.ArgumentParser()
parser.add_argument('--bot_number',default='0')
args = parser.parse_args()
reddit = praw.Reddit('bot'+args.bot_number)

while True:
    try:
        print('len(already_submitted)=',len(already_submitted))
        yang_submission=random.choice(list(reddit.subreddit("YangForPresidentHQ").hot(limit=None)))
        if yang_submission not in already_submitted:
            link=random.choice([0,1])
            if link:
                reddit.subreddit("cs40_2022fall").submit(yang_submission.title, url=yang_submission.url)
                print('url submitted: ', yang_submission.url)
                already_submitted.append(yang_submission)
                with open(filename, 'wb') as f:
                    pickle.dump(already_submitted, f)
            else:
                reddit.subreddit("cs40_2022fall").submit(yang_submission.title, selftext=yang_submission.selftext)
                print('selftext submitted: ', yang_submission.selftext)
                already_submitted.append(yang_submission)
                with open(filename, 'wb') as f:
                    pickle.dump(already_submitted, f)
    except praw.exceptions.RedditAPIException as e:
        for subexception in e.items:
            if subexception.error_type=='RATELIMIT':
                error_str=str(subexception)
                print(error_str)
                if 'minute' in error_str:
                    delay_str=error_str.split('for ')[-1].split(' minute')[0]
                    delay_int=int(delay_str)*60
                else:
                    delay_str=error_str.split('for ')[-1].split(' second')[0]
                    delay_int=int(delay_str)
                while delay_int:
                    mins, secs = divmod(delay_int, 60)
                    timer = '{:02d}:{:02d}'.format(mins, secs)
                    print(timer, end="\r")
                    time.sleep(1)
                    delay_int-=1

