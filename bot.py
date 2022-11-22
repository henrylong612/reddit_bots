import praw
import random
import datetime
import time
import argparse
import bot_counter
import requests
from bs4 import BeautifulSoup
import markovify

# FIXME:
# copy your generate_comment function from the madlibs assignment here
madlibs = [
    "**American [BUSINESSMAN] Andrew Yang, [FLAWS], [REPRESENTS] [ESSENTIAL] [DEPARTURE] from the [NORM]. Yang's rise to [FAME] began in the 2020 Democratic primaries. Yang [PROMOTED] [SEVERAL] [UNORTHODOX] [PROPOSALS] including a universal basic income [UBI] funded by a value-added tax [VAT].**",
    "**Andrew Yang is a [SPECIAL] politcian. [HIS] 2020 campaign centered around a universal basic income [UBI] proposal in which every [CITIZEN] would receive $1000/month regardless of their income. This [PROPOSAL], though not a panacea, would be a major improvement on our [INEFFICIENT] current welfare [SYSTEM].**",
    "**Andrew Yang recently [STARTED] the Forward Party. While this party may ultimately be counterproductive and [INEFFECTIVE], it does [PROMOTE] common-sense voting reform, including measures like [PRIMARY]. It also [REPRESENTS] a commitment to moving beyond the [LEFT] [BINARY].**",
    "**Andrew Yang hosts a podcast called Yang Speaks. On this podcast, Yang [TALKS] with people across the political [AISLE] about pressing [POLITICAL] issues. My personal favorite episode is when he [TALKS] with NYU Professor Jonathan Haidt about the [DETERMINANTS] what makes [SOMEONE] a [LIBERAL].**",
    "**Andrew Yang [PROMOTES] [MANY] of [UNORTHODOX] [PROPOSALS]. For example, he [PROMOTES] universal basic income [UBI], [PAYING] [COLLEGE] athletes, and automatic tax filing. Many of these [PROPOSALS] are overlooked simply because [MAINSTREAM].**",
    "**Andrew Yang [REPRESENTS] a [DEPARTURE] from the [LEFT] [BINARY]. His new party, the Forward Party, [AIMS] to bring [AMERICANS] together under common sense [PROPOSALS]. Hopefully, this kind of thinking will [QUELL] partisan [STRIFE].**"
    ]

replacements = {
    'BUSINESSMAN' : ['businessman', 'entrepreneur', 'tycoon'],
    'FLAWS' : ['while he has his flaws', 'although not perfect', 'despite his limitations'],
    'ESSENTIAL' : ['an essential', 'a much-needed', 'an important'],
    'NORM' : ['norm', 'status-quo', 'traditional politician'],
    'FAME' : ['fame', 'stardom', 'prominence'],
    'PROMOTED' : ['promoted', 'advocated for', 'supported'],
    'SEVERAL' : ['several', 'a number of', 'multiple'],
    'UBI' : ['(UBI)', '(also known as UBI)'],
    'VAT' : ['(also known as a VAT)', '(VAT)', '(or VAT)'],
    'SPECIAL' : ['special', 'unique'],
    'HIS' : ['his', 'Yang\'s'],
    'CITIZEN' : ['U.S. citizen', 'American'],
    'PROPOSAL' : ['proposal', 'idea', 'policy'],
    'INEFFICIENT' : ['inefficient', 'bureaucratic', 'red-tape ridden'],
    'SYSTEM' : ['system', 'regime', 'programs'],
    'STARTED' : ['founded', 'created', 'started'],
    'INEFFECTIVE' : ['ineffective', 'unhelpful'],
    'PROMOTE' : ['promote', 'support', 'advocate for'],
    'PRIMARY' : ['ranked-choice voting', 'open primaries'],
    'REPRESENTS' : ['represents', 'symbolizes', 'relfects'],
    'BINARY' : ['binary', 'dichotomy', 'paradigm'],
    'TALKS' : ['talks', 'discusses', 'chats'],
    'AISLE' : ['aisle', 'spectrum'],
    'POLITICAL' : ['political', 'social and economic'],
    'DETERMINANTS' : ['determinants of', 'factors contributing to', 'contributing factors for'],
    'SOMEONE' : ['someone', 'a person'],
    'LIBERAL' : ['liberal or conservative', 'Republican or a Democrat'],
    'UNORTHODOX' : ['unorthodox', 'unconventional', 'out of the ordinary'],
    'PROMOTES' : ['promotes', 'advocates for', 'supports'],
    'PROPOSALS' : ['proposals', 'ideas', 'policies'],
    'PAYING' : ['paying', 'compensating'],
    'COLLEGE' : ['college', 'collegiate', 'NCAA'],
    'MAINSTREAM' : ['they are not mainstream', 'many deem the issues unimportant', 'they are not often discussed on the news'],
    'DEPARTURE' : ['departure', 'break', 'shift'],
    'LEFT' : ['left-right', 'liberal-conservative', 'Republican-Democrat'],
    'AIMS' : ['aims', 'is an attempt'],
    'AMERICANS' : ['Americans', 'people'],
    'QUELL' : ['quell', 'calm'],
    'STRIFE' : ['strife', 'tensions'],
    'MANY' : ['many', 'several', 'a lot']
    }


def generate_comment_madlibs():
    '''
    This function generates random comments according to the patterns specified in the `madlibs` variable.

    To implement this function, you should:
    1. Randomly select a string from the madlibs list.
    2. For each word contained in square brackets `[]`:
        Replace that word with a randomly selected word from the corresponding entry in the `replacements` dictionary.
    3. Return the resulting string.

    For example, if we randomly selected the madlib "I [LOVE] [PYTHON]",
    then the function might return "I like Python" or "I adore Programming".
    Notice that the word "Programming" is incorrectly capitalized in the second sentence.
    You do not have to worry about making the output grammatically correct inside this function.
    Instead, you should ensure that the madlibs that you create will all be grammatically correct when this substitution procedure is followed.
    '''
    madlib=random.choice(madlibs)
    for replacement in replacements.keys():
        madlib=madlib.replace('['+replacement+']',random.choice(replacements[replacement]))
    return madlib

def generate_comment_markovify():

    url="https://en.wikipedia.org/wiki/Andrew_Yang"

    r = requests.get(url)
    html = r.text

    soup=BeautifulSoup(html,'html.parser')

    text=''
    tags=soup.select('.mw-parser-output > p')
    for tag in tags:
        text+=tag.text

    accumulator=''
    in_bracket=False
    for i,c in enumerate(text):
        if c=='[':
            in_bracket=True
        elif in_bracket==False:
            accumulator+=c
        elif c==']':
            in_bracket=False

    text_model = markovify.Text(accumulator)

    sentence='**'+text_model.make_sentence()+' '+text_model.make_sentence()+' '+text_model.make_sentence()+'**'

    return sentence



# FIXME:
# connect to reddit 
parser = argparse.ArgumentParser()
parser.add_argument('--bot_number',default='3')
parser.add_argument('--markovify',action='store_true')
args = parser.parse_args()
reddit = praw.Reddit('bot'+args.bot_number)
bot_name='botbombdotcom'+args.bot_number

if args.markovify:
    post=generate_comment_markovify()
else:
    post=generate_comment_madlibs()

# FIXME:
# select a "home" submission in the /r/cs40_2022fall subreddit to post to,
# and put the url below
#
# HINT:
# The default submissions are going to fill up VERY quickly with comments from other students' bots.
# This can cause your code to slow down considerably.
# When you're first writing your code, it probably makes sense to make a submission
# that only you and 1-2 other students are working with.
# That way, you can more easily control the number of comments in the submission.
submission_url = 'https://old.reddit.com/r/cs40_2022fall/comments/yz0j52/kanye_buying_parler/'
submission = reddit.submission(url=submission_url)

# each iteration of this loop will post a single comment;
# since this loop runs forever, your bot will continue posting comments forever;
# (this is what makes it a deamon);
# recall that you can press CTRL-C in the terminal to stop your bot
#
# HINT:
# while you are writing and debugging your code, 
# you probably don't want it to run in an infinite loop;
# you can change this while loop to an if statement to make the code run only once
while True:

    # printing the current time will help make the output messages more informative
    # since things on reddit vary with time
    print()
    print('new iteration at:',datetime.datetime.now())
    print('submission.title=',submission.title)
    print('submission.url=',submission.url)

    # FIXME (task 0): get a list of all of the comments in the submission
    # HINT: this requires using the .list() and the .replace_more() functions

    print('before .replace_more')
    submission.comments.replace_more(limit=None)
    print('after .replace_more')

    all_comments = []

    for comment in submission.comments.list():
        all_comments.append(comment)

    # HINT: 
    # we need to make sure that our code is working correctly,
    # and you should not move on from one task to the next until you are 100% sure that 
    # the previous task is working;
    # in general, the way to check if a task is working is to print out information 
    # about the results of that task, 
    # and manually inspect that information to ensure it is correct; 
    # in this specific case, you should check the length of the all_comments variable,
    # and manually ensure that the printed length is the same as the length displayed on reddit;
    # if it's not, then there are some comments that you are not correctly identifying,
    # and you need to figure out which comments those are and how to include them.
    print('len(all_comments)=',len(all_comments))

    # FIXME (task 1): filter all_comments to remove comments that were generated by your bot
    # HINT: 
    # use a for loop to loop over each comment in all_comments,
    # and an if statement to check whether the comment is authored by you or not
    not_my_comments = []
    
    for comment in all_comments:
        if comment.author!=bot_name:
            not_my_comments.append(comment)
        

    # HINT:
    # checking if this code is working is a bit more complicated than in the previous tasks;
    # reddit does not directly provide the number of comments in a submission
    # that were not gerenated by your bot,
    # but you can still check this number manually by subtracting the number
    # of comments you know you've posted from the number above;
    # you can use comments that you post manually while logged into your bot to know 
    # how many comments there should be. 
    print('len(not_my_comments)=',len(not_my_comments))

    # if the length of your all_comments and not_my_comments lists are the same,
    # then that means you have not posted any comments in the current submission;
    # (your bot may have posted comments in other submissions);
    # your bot will behave differently depending on whether it's posted a comment or not
    has_not_commented = len(not_my_comments) == len(all_comments)

    if has_not_commented:
        # FIXME (task 2)
        # if you have not made any comment in the thread, then post a top level comment
        #
        # HINT:
        # use the generate_comment() function to create the text,
        # and the .reply() function to post it to reddit;
        # a top level comment is created when you reply to a post instead of a message

        try:
            submission.reply(post)
            t=5
            while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                t-=1
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
                    if delay_int>300:
                        print('\nIn the meantime, let\'s tabulate the number of valid comments this bot has made and delete any invalid comments...')
                        start_time=time.time()
                        bot_counter.valid_comments()
                        end_time=time.time()
                        elapsed_time=int(end_time-start_time)
                        countdown=delay_int-elapsed_time
                        while countdown:
                            mins, secs = divmod(countdown, 60)
                            timer = '{:02d}:{:02d}'.format(mins, secs)
                            print(timer, end="\r")
                            time.sleep(1)
                            countdown-=1
                    while delay_int:
                        mins, secs = divmod(delay_int, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        delay_int-=1


    else:
        # FIXME (task 3): filter the not_my_comments list to also remove comments that
        # you've already replied to
        # HINT:
        # there are many ways to accomplish this, but my solution uses two nested for loops
        # the outer for loop loops over not_my_comments,
        # and the inner for loop loops over all the replies of the current comment from the outer loop,
        # and then an if statement checks whether the comment is authored by you or not
        comments_without_replies = []
        for comment in not_my_comments:
            reply_authors=[]
            for reply in comment.replies:
                reply_authors.append(reply.author)
            if bot_name not in reply_authors:
                comments_without_replies.append(comment)

        # This will allow the reddit bot to reply to the most upvoted comments:
        
        
        number_of_upvotes=0
        most_upvoted_comments_without_replies=[]
        for comment in comments_without_replies:
            if comment.score>number_of_upvotes:
                most_upvoted_comments_without_replies=[comment]
                number_of_upvotes=comment.score
            elif comment.score==number_of_upvotes:
                most_upvoted_comments_without_replies.append(comment)

        # HINT:
        # this is the most difficult of the tasks,
        # and so you will have to be careful to check that this code is in fact working correctly;
        # many students struggle with getting a large number of "valid comments"
        print('len(comments_without_replies)=',len(comments_without_replies))

        # FIXME (task 4): randomly select a comment from the comments_without_replies list,
        # and reply to that comment
        #
        # HINT:
        # use the generate_comment() function to create the text,
        # and the .reply() function to post it to reddit;
        # these will not be top-level comments;
        # so they will not be replies to a post but replies to a message
        try:
            random.choice(most_upvoted_comments_without_replies).reply(post)
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
                    if delay_int>300:
                        print('\nIn the meantime, let\'s tabulate the number of valid comments this bot has made and delete any invalid comments...')
                        start_time=time.time()
                        bot_counter.valid_comments()
                        end_time=time.time()
                        elapsed_time=int(end_time-start_time)
                        countdown=delay_int-elapsed_time
                        while countdown:
                            mins, secs = divmod(countdown, 60)
                            timer = '{:02d}:{:02d}'.format(mins, secs)
                            print(timer, end="\r")
                            time.sleep(1)
                            countdown-=1
                    while delay_int:
                        mins, secs = divmod(delay_int, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        delay_int-=1
        except IndexError:
            pass

    # FIXME (task 5): select a new submission for the next iteration;
    # your newly selected submission should be randomly selected from the 5 hottest submissions
    
    submission_list=list(reddit.subreddit('cs40_2022fall').hot(limit=5))
    submission=random.choice(submission_list)
    
    pass

    # We sleep just for 1 second at the end of the while loop.
    # This doesn't avoid rate limiting
    # (since we're not sleeping for a long period of time),
    # but it does make the program's output more readable.
    
    time.sleep(1)
