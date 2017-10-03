#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/10/1 下午9:41
# @Author  : foragile
# @Site    :
# @File    : recommender3.py
# @Software: pptb
from math import sqrt

users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5, "Lorde": 4, "Fall Out Boy": 1},

          "Matt": {"Imagine Dragons": 3, "Daft Punk": 4, "Lorde": 4, "Fall Out Boy": 1},

          "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3, "Lorde": 3, "Fall Out Boy": 1},

          "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4, "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},

          "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4, "Daft Punk": 5, "Fall Out Boy": 3}
          }


def computeSimilarity(band1, band2, userRatings):
    averages = {}
    for (key, ratings) in userRatings.items():
        averages[key] = (float(sum(ratings.values()))) / len(ratings.values())
    num = 0  # numerator
    dem1 = 0  # first half of denomintor
    dem2 = 0
    for (user, ratings) in userRatings.items():
        if band1 in ratings and band2 in ratings:
            avg = averages[user]
            num += (ratings[band1] - avg) * (ratings[band2] - avg)
            dem1 += (ratings[band1] - avg) ** 2
            dem2 += (ratings[band2] - avg) ** 2
    return num / (sqrt(dem1) * sqrt(dem2))


# print computeSimilarity("Imagine Dragons", "Lorde", users3)

users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}


class recommender:
    def __init__(self, data, k=1, metric='pearson', n=5):
        #
        # The following two variables are used for Slope One
        #
        self.data = data
        self.frequencies = {}
        self.deviations = {}

    def computeDeviations(self):
        # for each person in the data:
        #    get their ratings
        for ratings in self.data.values():
            # for each item & rating in that set of ratings:
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})
                # for each item2 & ratings2 in that set of ratings
                for (item2, ratings2) in ratings.items():
                    if item != item2:
                        # add the difference between the ratings
                        # to our computation
                        self.frequencies[item].setdefault(item2, 0)
                        self.deviations[item].setdefault(item2, 0)
                        self.frequencies[item][item2] += 1
                        self.deviations[item][item2] += rating - ratings2

        for (item, ratings) in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]

    def convertProductId2name(self, id):
        """Given product id number return product name"""
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    def slopeOneRecommendations(self, userRatings):
        recommendations = {}
        frequencies = {}
        # for every item and rating in the user's recommendations
        for (userItem, userRating) in userRatings.items:
            # for every item in our dataset that the user didn't rate
            for (diffItem, diffRatings) in self.deviations.items():
                if diffItem not in userRatings and \
                                userItem in self.deviations[diffItem]:
                    freq = self.frequencies[diffItem][userItem]
                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)
                    # add to the running sum representing the numerator
                    # of the formula
                    recommendations[diffItem] += (diffRatings[userItem] + userItem) * freq

                    # keep a running sum of the frequency of diffitem
                    frequencies[diffItem] += freq

        recommendations = [(self.convertProductId2name(k), v / frequencies[k]) for (k, v) in recommendations.items()]

        # finally sort and return
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return recommendations

    def loadMovieLensTrain(fileName='u1.base'):

        prefer = {}
        for line in open('ml-100k/u1.base', 'r'):  # 打开指定文件
            (userid, movieid, rating, ts) = line.split('\t')
            prefer.setdefault(userid, {})
            prefer[userid][movieid] = float(rating)

        return prefer


# r = recommender(users2)
# r.computeDeviations()
# print r.deviations
r=recommender(0)

