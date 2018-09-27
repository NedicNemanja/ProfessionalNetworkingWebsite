from .models import User, Advertisment
from django.utils import timezone
#import math

def CCFilterAds(user):
    #get user's skills
    usersSkills = user.get_skills()
    #print (usersSkills)
    #get all the available ads
    ads = Advertisment.objects.all()
    #print (ads)
    #create a dict with the score of each ad based on how similar skills has to the user
    ads_score = ScoreAds(ads, usersSkills)
    #print (ads_score)
    return sorted(ads_score, key=ads_score.get, reverse=True)
    

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
    return sorted(post_scores_dict, key=post_scores_dict.get, reverse=True)
    #return this to see how it would look just with time ordered posts: return user.get_posts()

def ScoreAds(ads, usersSkills):
    ads_score = {}
    for ad in ads:
        # if not usersSkills or not ad.skills.all():
        #     ads_score[ad] = 0.25
        # else:
        #     distanceScore = SkillsJaccardSimilarity(usersSkills, ad.skills.all())
        #     ads_score[ad] = 0.25 + distanceScore
        # calculate the Jaccard's similarity between user's skills and each ad's skills
        distanceScore = SkillsJaccardSimilarity(usersSkills, ad.skills.all())
        # add their similarity to a base score
        ads_score[ad] = 0.25 + distanceScore
        # print (usersSkills)
        # print (ad.skills.all())

        # for skill in usersSkills:
        #     if skill in ad.skills.all():
        #         ads_score[ad] = ads_score.get(ad, 0) + 1
    return ads_score

# calculate the Jaccard's similarity between to skills querysets
def SkillsJaccardSimilarity(usersSkills, adsSkills):
    un = SkillsUnion(usersSkills, adsSkills)
    inter = SkillsIntersection(usersSkills, adsSkills)
    unionLen = len(un)
    interLen = len(inter)
    return interLen/unionLen

def SkillsUnion(usersSkills, adsSkills):
    return usersSkills.union(adsSkills)

def SkillsIntersection(usersSkills, adsSkills):
    return usersSkills.intersection(adsSkills)

