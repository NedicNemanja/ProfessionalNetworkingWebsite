from .models import User,Post,Interest,Comment
from django.utils import timezone
import math

def CCFilterPosts(user):
    #get posts user interacted with
    interacted_posts = user.get_interacted_posts()
    #score friend's similarity based on how often they appear in posts in total
    similarity_scores_dict = ScoreUsers(interacted_posts)
    if user in similarity_scores_dict:
        del similarity_scores_dict[user]    #don't need score for himself
    #calculate jackard distance between user and his cluster
    user_jackard_distances = JackardDistance(user,similarity_scores_dict)
    #score all available posts
    post_scores_dict = PostScores(user.get_posts(),user_jackard_distances)
    #maybe boost fresh posts?
    #penalize posts that the user already has seen
    InteractedPenalty(post_scores_dict,interacted_posts)
    #penalize users own posts
    CreatedPenalty(user,post_scores_dict)
    #penalize older posts scores logarithmically
    DateTimePenalty(post_scores_dict)
    #order posts by score
    print(post_scores_dict)
    return sorted(post_scores_dict, key=post_scores_dict.get, reverse=True)
    #return this to see how it would look just with time ordered posts: return user.get_posts()

def ScoreUsers(posts):
    score_dict = {}
    #+1point for every time a user appeared in a common post
    for post in posts:
        for interest in post.get_interests():
            score_dict[interest.creator] = score_dict.get(interest.creator, 0) + 1
        for comment in post.get_comments():
            score_dict[comment.creator] = score_dict.get(comment.creator, 0) + 1
    return score_dict

def JackardDistance(target_user,score_dict):
    user_shill_score = target_user.shill_score()
    for user in score_dict:
        score_dict[user] = (score_dict[user]/(user_shill_score+user.shill_score()-score_dict[user]))
    return score_dict

def PostScores(posts,user_jackard_distances):
    post_scores = {}
    for post in posts:
        post_scores[post] = 1   #base score
        #every time a user appears in a post add his JackardDistance to post score
        for interest in post.get_interests():
            if interest.creator in user_jackard_distances:
                post_scores[post] += user_jackard_distances[interest.creator]
        for comment in post.get_comments():
            if comment.creator in user_jackard_distances:
                post_scores[post] += user_jackard_distances[comment.creator]
    print(post_scores)
    return post_scores

def InteractedPenalty(post_scores,interacted_posts):
    for post in post_scores:
        if post in interacted_posts:
            post_scores[post] *= 0.75

def CreatedPenalty(user,post_scores):
    for post in post_scores:
        if user == post.creator:
            post_scores[post] *= 0.5

def DateTimePenalty(post_scores):
    for post in post_scores:
        timediff = timezone.now()-post.creation_date
        if timediff.days >= 3:
            post_scores[post] /= math.log(timediff.days)
