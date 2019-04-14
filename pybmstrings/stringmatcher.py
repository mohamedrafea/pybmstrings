from pycommonutil import string_util
def updateMatchingIndices(matchingIndices):
    currentConsecutive = 0
    lastI = -10
    for i in matchingIndices:
        if i-lastI>2:
            if currentConsecutive==1:
                #print("lastI:",lastI)
                matchingIndices.remove(lastI)
                #print("matchingIndices", matchingIndices)
            currentConsecutive=1
        else:
            currentConsecutive+=1
        lastI = i
    """
    if len(matchingIndices)==1:
        matchingIndices.remove(matchingIndices[0])
    """

def calcMatchScore(word1, word2,debug=False):
    #print("entered calcMatchScore")
    if word1 == word2:
        return len(word1)
    m = map(str.__eq__, word1[:len(word2)], word2[:len(word1)])
    l = list(m)

    if debug:        
        print("l",l)
        print("sum(m)",sum(m))

    matchingIndices = listToMatchingIndices(l)
    #print("matchingIndices",matchingIndices)
    updateMatchingIndices(matchingIndices)
    return (len(matchingIndices),matchingIndices)

def getSingleWords(lineText):
    # print("lineText:",lineText)
    return lineText.split()

#e.g. strToMatch: unitedstatesofamerica
#potentialStrWord: each word of united states of america
def wordScore(strToMatch,potentialStrWord,debug=False):
    i = strToMatch.find(potentialStrWord)
    matchScore = 0
    matchedIndices = []
    s = set()
    if i>-1:
        matchScore = len(potentialStrWord)
        if matchScore==1:
            #matchScore = 0
            None
        else:
            matchedIndices = [x+i for x in range(len(potentialStrWord))]
    else:
        #search for 1st 2 characters
        i = strToMatch.find(potentialStrWord[:2])
        if i > -1:
            sub = strToMatch[i:]
            matchScore,matchedIndices = calcMatchScore(sub,potentialStrWord)
            matchedIndices = [x + i for x in matchedIndices]
        else:
            matchScore,matchedIndices = calcMatchScore(strToMatch, potentialStrWord)
    spaceSeparators = len(getSingleWords(strToMatch))-1
    penaltyScore = len(strToMatch) - spaceSeparators - matchScore
    if debug:
        print("match score of " + potentialStrWord + " with "+strToMatch+": ", matchScore)
        print("penalty score of "+potentialStrWord+ " with "+strToMatch+": ",penaltyScore)
    return matchScore, penaltyScore,matchedIndices

def score(strToMatch,potentialStr,debug=False):
    strToMatch = strToMatch.lower()
    potentialStr = potentialStr.lower()
    singleWords = getSingleWords(potentialStr)
    totalMatchScore = 0
    totalPenaltyScore = 0
    totalRedundancyScore = 0
    matchedIndices = set()
    for singleWord in singleWords:
        matchScore, penaltyScore,wordMatchedIndices = wordScore(strToMatch,singleWord)
        oldMatchedIndicesLength = len(matchedIndices)
        wordMatchedIndicesLength = len(wordMatchedIndices)
        matchedIndices.update(wordMatchedIndices)
        redundancyScore = wordMatchedIndicesLength - (len(matchedIndices)-oldMatchedIndicesLength)
        #totalRedundancyScore = totalRedundancyScore + redundancyScore
        totalMatchScore = totalMatchScore + matchScore - redundancyScore
        totalPenaltyScore = totalPenaltyScore + penaltyScore + redundancyScore
        if debug:
            print("singleWord:",singleWord)
            print("wordMatchedIndices:", wordMatchedIndices)
            print("RedundancyScore:", redundancyScore)
            print("totalMatchScore:", totalMatchScore)
            print("totalPenaltyScore:", totalPenaltyScore)

    if debug:
        #print(matchedIndices)
        print("totalMatchScore:",totalMatchScore)
        print("totalPenaltyScore:", totalPenaltyScore)

    #return (totalMatchScore - (totalPenaltyScore - ((len(singleWords) - 1) * totalMatchScore)))
    #return (totalMatchScore - (totalPenaltyScore - ((len(singleWords)-1)*totalMatchScore)))/len(singleWords)
    spaceSeparators = len(getSingleWords(strToMatch)) - 1
    maxMatchScore = len(strToMatch)-spaceSeparators
    minMatchScore = -maxMatchScore
    absScore =  totalMatchScore - (totalPenaltyScore - ((len(singleWords) - 1) * maxMatchScore))
    return (absScore - minMatchScore)/(maxMatchScore-minMatchScore)

def suggestions(wordList,word,debug=False):
    suggList = []
    maxScore = -10000
    for potWord in wordList:
        if debug:
            print('calling score with ',word+","+potWord)
        sc = score(word,potWord)
        if sc>maxScore:
            if debug:
                print("Score of ",potWord,"=",sc)
            score(word, potWord,debug)
            suggList = []
            suggList.append(potWord)
            maxScore = sc
        elif sc==maxScore:
            if debug:
                print("Score of ", potWord, "=", sc)
            score(word, potWord, debug)
            suggList.append(potWord)
    if len(suggList)>0:
        for w in suggList:
            if string_util.equalsIgnoreCase(w,word):
                return [w],maxScore
    if debug:
        print("suggestions:",suggList)
    return suggList,maxScore

def listToMatchingIndices(l,debug=False):
    mi = []
    #print("l",l)
    for idx, val in enumerate(l):
        if val:
            mi.append(idx)
    if debug:
        print("mi",mi)
    return mi
