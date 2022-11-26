# project_04

This is a GutHub repository for my submission of project_04. The `bot.py` file contains a program for a series of Reddit bots that post comments (generated using either a madlib technique or a Markovify text generation algorithm) in support of politician Andrew Yang. This bot works for the usernames botbombdotcom0, botbombdotcom1, botbombdotcom2, botbombdotcom3, and botbombdotcom4.

You can find a particularly funny thread involving my bots at the link [here](https://old.reddit.com/r/cs40_2022fall/comments/yz66wg/what_would_the_republicans_done_differently_in/iwy9lqn/). I think this thread is funny because it involves 4 of my bots ganging up on kpbot24. Here is a picture of the thread:

![Picture of thread involving my bots](redditthread.png)

Every time that any of my bots ran into a ratelimit longer than 5 minutes, I would make the `bot.py` file call a function in the `bot_counter` file that tabulated the number of valid posts that that bot has made and delete any invalid posts.

My score on project_04 should be 40/30. I completed all of the tasks in `bot.py`, which is worth 12 points. I completed this GitHub repo according to the specifications, which is worth 3 points. botbombdotcom0 posted 1000 valid comments (see output below), which is worth 10 points. I made botbomdotcom1 post 200 submissions with my `bot-submissions.py` file, which is worth 2 points. I made an army of 5 bots that all posted 500 valid comments, which is worth 2 points. I altered my `bot.py` file to make my bots reply to the most highly upvoted comment in a thread that they haven't already replied to using the code below, which is worth 2 points. I made botbombdotcom2 use the TextBlob analysis library to loop through 100+ submissions (and their respctive comments) and upvote/downvote the submissions that talk about Andrew Yang positively/negatively with my `bot_vote.py` file, which is worth 4 points. I made botbombdotcom3 and botbombdotcom4 use the Markovify text generation algorithm to generate more sophisticated comments based on thee comment to which they are responding and a Wikipedia article about Andrew Yang, which is worth 5 points (the Markovify text generation algorith can be called using the command line tag `--markovify`). This is equal to 40 points total.

Output of `bot_counter.py` file for botbombdotcom0:
```
len(comments)= 1000
len(top_level_comments)= 126
len(replies)= 874
len(valid_top_level_comments)= 126
len(not_self_replies)= 874
len(valid_replies)= 874
========================================
valid_comments= 1000
========================================
```

Code I used to make my bots respond to the most upvoted comments:
```
number_of_upvotes=0
    most_upvoted_comments_without_replies=[]
    for comment in comments_without_replies:
        if comment.score>number_of_upvotes:
            most_upvoted_comments_without_replies=[comment]
            number_of_upvotes=comment.score
        elif comment.score==number_of_upvotes:
            most_upvoted_comments_without_replies.append(comment)
```
