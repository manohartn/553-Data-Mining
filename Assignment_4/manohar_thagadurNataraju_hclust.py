import heapq
import sys
import math
import copy
import itertools

def readFile_to_InputList(inputList, inputFile):
    inputFileObj = open(inputFile)

    total_clusters = 0

    for line in inputFileObj:
        line = line.rstrip('\n')
        entry = line.split(',')

        inputList.append(entry)

        total_clusters = total_clusters + 1

    return total_clusters

def getEUDistance(point1, point2, nDimensionLength):

    sum = 0;
    for i in xrange(nDimensionLength):
        sum += pow((point1[i] - point2[i]), 2)
    euDist = pow(sum, 0.5)

    return euDist

def computeCentroid(cluster, pointsList, nDimensionLength):
    centroid = []
    for i in range(nDimensionLength):
        centroid.append(0.0)
    for i in range(nDimensionLength):
        for j in range(len(cluster)):
            centroid[i] += pointsList[cluster[j]][i]
        centroid[i] = centroid[i]/len(cluster)

    return centroid

def computeEuDistance_AddHeap(IndexA, IndexB, pointsList, pointsHeap, nonVisitedList, nDimensionLength):
    clusterA = nonVisitedList[IndexA]
    #print "cA ", clusterA

    for j in range(IndexB, len(nonVisitedList)):
        if len(clusterA) == 1:
            centroid_A = pointsList[clusterA[0]]
        else:
            #print "iA", IndexA
            centroid_A = computeCentroid(clusterA, pointsList, nDimensionLength)
        clusterB = nonVisitedList[j]
        #print "cB ", clusterB
        if len(clusterB) == 1:
            centroid_B = pointsList[clusterB[0]]
        else:
            #print "ib", IndexB
            centroid_B = computeCentroid(clusterB, pointsList, nDimensionLength) 

        #print "cp ", centroid_point
        #print "ci ", centroid_item

        eu_dist = getEUDistance(centroid_A, centroid_B, nDimensionLength)
        heapItem = []
        heapItem.append(eu_dist)

        pointTuple = []
        pointTuple.append(nonVisitedList[IndexA])
        pointTuple.append(nonVisitedList[j])

        heapItem.append(pointTuple)

        heapq.heappush(pointsHeap, heapItem)

def buildHeap(pointsHeap, pointsList, nonVisitedList, nDimensionLength):
    nonVisitedListLength = len(nonVisitedList)

    for i in xrange(nonVisitedListLength-2):
        remainingList = nonVisitedList[i+1:]
        computeEuDistance_AddHeap(i, i+1, pointsList, pointsHeap, nonVisitedList, nDimensionLength)

def testHeap(pointsHeap):
    while pointsHeap:
        item = heapq.heappop(pointsHeap)
        print item

def initializeNonVisitedList(nonVisitedList, total_clusters):
    for i in xrange(total_clusters):
        li = []
        li.append(i)
        nonVisitedList.append(li)

def areClustersValid(clusterA, clusterB, nonVisitedList):
    if clusterA in nonVisitedList and clusterB in nonVisitedList:
        return True
    else:
        return False

def getGoldStandard(inputList):
    goldStandardDict = {}
    index = 0
    for item in inputList:
        label = item[-1]
        goldStandardDict.setdefault(label, [])
        goldStandardDict[label].append(index)
        index = index + 1

    return goldStandardDict

def getAllPairs(clusterList):
    allPairs = []
    for item in clusterList:
        combList = list(itertools.combinations(sorted(item), 2))
        allPairs = allPairs + combList

    return allPairs

def getIntersectionSet(listA, listB):
    return set(listA).intersection(listB)

def getRecall(goldPairs, hclustPairs, intersectionSet):
    intersectionSize = float(len(intersectionSet))
    recall = intersectionSize / float(len(goldPairs))

    return recall

def getPrecision(goldPairs, hclustPairs, intersectionSet):
    
    intersectionSize = float(len(intersectionSet))
    precision = intersectionSize / float(len(hclustPairs))
    return precision

def getPrecisionAndRecall(actualClusterDict, goldStandardDict, clustersDesired): 
    actualClusterList = sorted(actualClusterDict[clustersDesired])
    goldStandardList = goldStandardDict.values()

    goldPairs = getAllPairs(goldStandardList)
    hclustPairs = getAllPairs(actualClusterList)

    #print "goldpairs", goldPairs, "\n\n"
    #print "algo pairs", hclustPairs

    intersectionSet = set(hclustPairs).intersection(goldPairs)
    #print "iSet ", intersectionSet

    #print "iSize", len(intersectionSet), "gp", len(goldPairs), "hP", len(hclustPairs)

    precision = getPrecision(goldPairs, hclustPairs, intersectionSet)
    recall = getRecall(goldPairs, hclustPairs, intersectionSet)

    return (precision, recall)

def main():
    args_len = len(sys.argv)
    if args_len != 3:
        print "Usage: python <source_file> <input_file> <no_of_desired_clusters>"
        sys.exit()

    inputFile = sys.argv[1]
    clustersDesired = sys.argv[2]

    clustersDesired = int(clustersDesired)

    inputList = []
    goldStandardDict = {}
    total_clusters = readFile_to_InputList(inputList, inputFile)
    goldStandardDict = getGoldStandard(inputList)

    nonVisitedList = []
    initializeNonVisitedList(nonVisitedList, total_clusters)
    
    #print nonVisitedList
    #print inputList

    pointsList = []
    nDimensionLength = len(inputList[0]) - 1
    for item in inputList:
        nDimensionPoint = item[0:nDimensionLength]
        nDimensionPoint = [float(i) for i in nDimensionPoint]
        pointsList.append(nDimensionPoint)

    #print pointsList
    
    pointsHeap = []
    buildHeap(pointsHeap, pointsList, nonVisitedList, nDimensionLength)

    #testHeap(pointsHeap)
    #print pointsHeap
    actualClusterDict = {}
    k = total_clusters
    while len(nonVisitedList) > 1:

        minItem = heapq.heappop(pointsHeap)
        #print "LEN ", len(nonVisitedList), len(minItem)
	eu_dist = minItem[0]

        clusters = minItem[1]

	clusterA = clusters[0]
	clusterB = clusters[1]

	validClusters = areClustersValid(clusterA, clusterB, nonVisitedList)

	if validClusters:
	    #add NVL to actual dict
	    #actualClusterDict.update({k : copy.copy(nonVisitedList)})
            actualClusterList = []
            actualClusterList = copy.copy(nonVisitedList)
	    actualClusterDict[k] = actualClusterList
            #print actualClusterList
            k = k-1

	    nonVisitedList.remove(clusterA)
	    nonVisitedList.remove(clusterB)

	    mergedCluster = clusterA + clusterB
            #print mergedCluster
	    nonVisitedList.insert(0, mergedCluster)

            computeEuDistance_AddHeap(0, 1, pointsList, pointsHeap, nonVisitedList, nDimensionLength)

    #Verify dictionary
    '''
    for key, values in actualClusterDict.iteritems():
        print key, values
    '''

    actualClusterDict[k] = sorted(nonVisitedList)
    precision, recall = getPrecisionAndRecall(actualClusterDict, goldStandardDict, clustersDesired)

    print precision
    print recall

    actualPrintList = sorted(actualClusterDict[clustersDesired])
    for item in actualPrintList:
        print sorted(item)

if __name__ == "__main__":
    main()
