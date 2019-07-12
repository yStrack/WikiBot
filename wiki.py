import requests
import re

class Wiki:
    # the term has to be in english. The wikipedia API service used searches and returns data in english only.
    def __init__(self,term):
        S = requests.Session()
        self.term = re.sub(' ','_',term) #raw term string
        self.searchUrl = 'https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search=';
        self.contentUrl = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=';
        sURL = self.searchUrl + term
        cURL = self.contentUrl + term
        try:
            sResponse = S.get(sURL)
            cResponse = S.get(cURL)
        except:
            return None
        self.searchData = sResponse.json()
        self.contentData = cResponse.json()
        return

    def __str__(self):
        # return the wiki page Title
        return self.searchData[0]

    def getTitle(self):
        #return the wiki page Title
        return self.__str__()

    def reSearch(self):
        #only called when term string is not enough
        S = requests.Session()
        Id = list(self.contentData['query']['pages'])[0]
        newTerm = re.search('\[\[.*\]\]',self.contentData['query']['pages'][Id]['revisions'][0]['*'])
        if newTerm == None:
            return False
        newTerm = self.contentData['query']['pages'][Id]['revisions'][0]['*'][newTerm.start()+2:newTerm.end()-2]
        newTerm = re.sub(' ', '_',newTerm) #sub white space to _
        sURL = self.searchUrl + newTerm
        try:
            sResponse = S.get(sURL)
        except:
            return False
        self.term = newTerm
        self.searchData = sResponse.json()
        return True


    def getSum(self):
        #return a summary of the searched term
        summary = self.searchData[2][0]
        if len(summary) == 0:
            if self.reSearch() == False:
                return 'No summary found, see more at ' + self.getLink()
            summary = self.searchData[2][0]
        summary = re.sub('\[.*\]','',summary) # remove anything between []
        summary = re.sub('\([^)]*\)','',summary) # remove anything between ()
        summary = re.sub('\{.*\}','',summary) # remove anything between {}
        if (len(summary) > 280):
            linkLen = len(self.getLink())
            aux =  len('See more at ')
            summary = summary[:-(linkLen+aux)]
            #find the last dot and remove anything after it.
            for i in range(len(summary)-1,0,-1):
                if summary[i] == '.':
                    summary = summary[:i+1]
                    break
            summary = summary + '\n\nSee more at ' + self.getLink()

        return summary

    def getLink(self):
        #return wikipedia link
        return self.searchData[3][0]
