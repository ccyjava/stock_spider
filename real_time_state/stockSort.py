__author__ = 'ccyjava'
class stocksort(object):
    def __init__(self,stockDict):
        self.stockDict=stockDict

    def getSort(self):
        sortList={}

        for key in self.stockDict:
            if len(self.stockDict[key])!=0:
                sortList[key]=self.stockDict[key][-1]

        return sorted(sortList.items(), lambda x, y: cmp(x[1], y[1]),reverse=True)