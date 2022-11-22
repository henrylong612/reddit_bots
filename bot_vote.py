import praw
import argparse
from textblob import TextBlob
import pickle

filename2 = 'mypickle2.pk'
filename3 = 'mypickle3.pk'

with open(filename2, 'rb') as f:
    submissions_already_voted = pickle.load(f)
print('len(submissions_already_voted)=',len(submissions_already_voted))

with open(filename2, 'rb') as f:
    comments_already_voted = pickle.load(f)
print('len(comments_already_voted)=',len(comments_already_voted))

parser = argparse.ArgumentParser()
parser.add_argument('--bot_number',default='0')
args = parser.parse_args()
reddit = praw.Reddit('bot'+args.bot_number)
bot_name='botbombdotcom'+args.bot_number

for submission in list(reddit.subreddit("cs40_2022fall").hot(limit=None)):
    print('len(submissions_already_voted)=',len(submissions_already_voted))
    print('len(comments_already_voted)=',len(comments_already_voted))
    if submission not in submissions_already_voted:
        if "yang" in submission.title.lower():
                textblob=TextBlob(submission.title)
                polarity=textblob.sentiment.polarity
                print('polarity=',polarity)
                if polarity>=0.0:
                    submission.upvote()
                    print('upvote: ',submission.title)
                else:
                    submission.downvote()
                    print('downvote: ',submission.title)
        submissions_already_voted.append(submission)
        with open(filename2, 'wb') as f:
            pickle.dump(submissions_already_voted, f)
    print('before .replace_more')
    submission.comments.replace_more(limit=None)
    print('after .replace_more')
    for comment in submission.comments.list():
        if comment not in comments_already_voted:
            if "yang" in comment.body.lower():
                textblob=TextBlob(comment.body)
                polarity=textblob.sentiment.polarity
                print('polarity=',polarity)
                if polarity>=0.0:
                    comment.upvote()
                    print('upvote: ',comment.body)
                else:
                    comment.downvote()
                    print('downvote: ',comment.body)
            comments_already_voted.append(comment)
            with open(filename3, 'wb') as f:
                pickle.dump(comments_already_voted, f)




