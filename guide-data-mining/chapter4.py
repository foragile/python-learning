#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17/10/3 下午9:55
# @Author  : foragile
# @Site    : 
# @File    : chapter4.py
# @Software: pptb

users = {}


def manhattan(vector1, vector2):
    """Computes the Manhattan distance."""
    distance = 0
    total = 0
    n = len(vector1)
    for i in range(n):
        distance += abs(vector1[i] - vector2[i])
    return distance


def computeNearestNeighbor(itemName, itemVector, items):
    """creates a sorted list of items based on their distance to item"""
    distances = []
    for otherItem in items:
        if otherItem != itemName:
            distance = manhattan(itemVector - items[otherItem])
            distances.append((distance, otherItem))
    distances.sort()
    return distances


def classify(user, itemName, itemVector, items):
    """Classify the itemName based on user ratings
    Should really have items and users as parameters"""
    # first find nearest neighbor
    nearest = computeNearestNeighbor(itemName, itemVector, items)[0][1]
    rating = users[user][nearest]
    return rating


class Classifier:
    def __init__(self, filename):
        self.mediaAndDeviation = []

        # reading the data in from the file
        f = open(filename)
        lines = f.readlines()
        f.close()
        self.format = lines[0].strip().split('\t')
        self.data = []
        for line in lines[1:]:
            fields = line.strip().split('\t')
            ignore = []
            vector = []
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    vector.append(int(fields[i]))
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    classification = fields[i]
            self.data.append((classification, vector, ignore))
        # get length of instance vector
        self.vlen = len(self.data[0][1])
        # now normalize the data
        for i in range(self.vlen):
            self.normalizeColumn(i)

    def normalize(self, columnNumber):
        """given a column number,normalize that column in self.data"""
        # first extract values to list
        col = [v[1][columnNumber] for v in self.data]
        median = self.getMedian(col)
        asd = self.getAbsoluteStandardDeviation(col, median)
        # print("Median:%f ASD=%f" % (median,asd))
        self.mediaAndDeviation.append((median, asd))
        for v in self.data:
            v[1][columnNumber] = (v[1][columnNumber] - median) / asd

    def normalizeVector(self, v):
        """We have stored the median and asd for each column
        We now use them to normalize vector v"""
        vector = list(v)
        for i in range(len(vector)):
            (median, asd) = self.mediaAndDeviation[i]
            vector[i] = (vector[i] - median) / asd
        return vector

    def classify(self, itemVector):
        """Return class we can think item Vector is in"""
        return (self.nearestNeighbor(self.normalizeVector(itemVector)))[1][0]

    def manhattan(self, vector1, vector2):
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))

    def nearestNeighbor(self,itemVector):
        return min([(self.manhattan(itemVector,item[1]),item) for item in self.data])

    def getMedian(self, alist):
        """return median of alist"""
        if alist == []:
            return []
        blist = sorted(alist)
        length = len(blist)
        if length % 2 == 1:

            # length of list is odd so return middle element
            return blist[int((length + 1) / 2) - 1]
        else:
            # length of list is even so compute midpoint
            v1 = blist[int(length / 2)]
            v2 = blist[(int(length / 2) - 1)]
            return (v1 + v2) / 2.0

    def getAbsoluteStandardDeviation(self, alist, median):
        """given alist and median  return absolute standard deviation"""
        sum = 0
        for item in alist:
            sum += abs(item - median)
        return sum / len(alist)
