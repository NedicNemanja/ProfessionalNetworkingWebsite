from .models import User, Advertisment
from django.utils import timezone

def CCFilterAds(user):
    #get user's skills
    usersSkills = user.get_skills()
    #print (usersSkills)
    #get all the available ads
    ads = Advertisment.objects.all()
    #print (ads)
    #create a dict with the score of each ad based on how similar skills has to the user
    adsScore = scoreAds(ads, usersSkills)
    #create a dict with every user and their similarity score based on how many same ads they have applied
    usersScore = scoreUsers(user)
    #create combined score dict ad:score of the content based and the collaborative filtering
    combinedScore = combineScores(adsScore, usersScore)
    #adding a penalty depending on how old is each add
    finalScore = timePenalty(combinedScore)
    #print (combinedScore)
    return sorted(finalScore, key=finalScore.get, reverse=True)

def scoreAds(ads, usersSkills):
    adsScore = {}
    for ad in ads:
        distanceScore = querySetsJaccardSimilarity(usersSkills, ad.skills.all())
        # add their similarity to a base score
        adsScore[ad] = 0.01 + distanceScore
    return adsScore

# calculate the Jaccard's similarity between to skills querysets
def querySetsJaccardSimilarity(set1, set2):
    un = querySetsUnion(set1, set2)
    inter = querySetsIntersection(set1, set2)
    unionLen = len(un)
    interLen = len(inter)
    if unionLen == 0:
        return 1
    else:
        return interLen/unionLen

def querySetsUnion(set1, set2):
    return set1.union(set2)

def querySetsIntersection(set1, set2):
    return set1.intersection(set2)

#return a dict of the user's friends and the how similar are they to the user based on their job applications
def scoreUsers(user):
    friends = user.get_users_friends()
    friendsComApps = {}
    for friend in friends:
        usersApplicationsSimilarity = querySetsJaccardSimilarity(user.get_applications(), friend.get_applications())
        friendsComApps[friend] = usersApplicationsSimilarity
    return friendsComApps

#add to each ad the value of the user's friend suggesting it divided by the number of user's friend suggesting to normalize it
def combineScores(adsScore, usersScore):
    for user in usersScore:
        usersApps = user.get_applications()
        for app in usersApps:
            adsScore[app] = adsScore.get(app, 0) + usersScore[user]/len(usersScore)
    return adsScore

# decrease the score of each ad depending on how many days old is it
def timePenalty(score):
    for ad in Advertisment.objects.all():
        timediff = timezone.now()-ad.creation_date
        #if is is 75 days old or less
        if timediff.days <= 75:
            #for each day old deduct 0.5% from the score of that ad
            score[ad] = score.get(ad, 0) - score.get(ad, 0)*timediff.days/200
        else:
            #other wise deduct the 75% of the score of that ad
            score[ad] = score.get(ad, 0) - score.get(ad, 0)*75/100
    return score