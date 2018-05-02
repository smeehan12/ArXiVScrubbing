#############################################
#
# Author : Sam Meehan - samuel.meehan@cern.ch
#
# This is a script which will sear for the occurrences of a certain term
# and makes the plot of occurrences over time
#
#############################################



import os
import numpy
import matplotlib
import matplotlib.pyplot as plt
import copy
import re


def main():



    myYears=list(numpy.arange(2000,2018,1))
    myLabels=[]
    for yr in myYears:
        myLabels.append(str(yr))
    
    globalDict={}
    listDict={}

    term = "dark matter"
    dictResult=FindTermSpan(term,myYears)
    globalDict[term]=copy.copy(dictResult)
    
    term = "axion"
    dictResult=FindTermSpan(term,myYears)
    globalDict[term]=copy.copy(dictResult)

    term = "wimp"
    dictResult=FindTermSpan(term,myYears)
    globalDict[term]=copy.copy(dictResult)
    
    #globalDict[term]={2000:100,2001:140,2002:170,2003:190,2004:160}
    
    #Plotting
    #sorting
    for term in globalDict.keys():
        listDict[term]=[]
        for year in sorted(globalDict[term].keys()):
            print year,globalDict[term][year]
            listDict[term].append(globalDict[term][year])
    
    # need to manually add an entry for each term
    plt.scatter(myYears, listDict["dark matter"], s=50, marker="o", color="r", label="dark matter")
    plt.scatter(myYears, listDict["axion"],       s=50, marker="o", color="b", label="axion")
    plt.scatter(myYears, listDict["wimp"],        s=50, marker="o", color="g", label="wimp")

    plt.title('Occurence of Term on ArXiV')
    plt.xlabel('Year')
    plt.ylabel('Number of Occurences')
    plt.legend(loc=2)
    plt.xticks(myYears, myLabels)
    plt.show()

def FindTermSpan(term,years,debug=False):

    print "Finding terms for : ",term
    print "Spanning years : ",years[0],years[-1]

    myDict={}

    for year in years:
    
        nfound = FindTerm(term,year,debug)

        print "NFound : ",year,nfound
        
        myDict[year]=nfound
        
    if debug:
        print "Summary : ",term
        for key in myDict.keys():
            print key,myDict[key]
        
    return myDict

def FindTerm(term,year,debug=False):

    searchTerm=""
    
    if len(term.split())==1:
        searchTerm=term
    else:
        for i in range(len(term.split())-1):
            searchTerm+=term.split()[i]
            searchTerm+="+"
        searchTerm+=term.split()[-1]
    
    
    searchYear=str(year)

    if debug:
        print "Searching for  : ",searchTerm
        print "Searching year : ",searchYear

    os.system('(wget "https://arxiv.org/search/advanced?advanced=1&terms-0-operator=AND&terms-0-term=%22'+searchTerm+'%22&terms-0-field=title&classification-physics=y&classification-physics_archives=all&date-filter_by=specific_year&date-year='+searchYear+'&date-from_date=&date-to_date=&size=50&order=" -q -O -) > myFile.txt')

    fin = open("myFile.txt","r+")
    
    results=[]

    for line in fin.readlines():
    
        if "Showing" in line.split() and "results" in line.split():
            results = line.split()
            break
            
    if debug:
        print results

    nreturn=-1
    
    if len(results)>0:
        if results[0]=="Showing":
        
            inString=results[3]
            
            inString = re.sub(',','',inString)
        
            nreturn=int(inString)
            
    return nreturn
    



if __name__ == "__main__":
    main()