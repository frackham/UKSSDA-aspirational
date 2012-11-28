# Filename: codeanalysis.py
# TODO: [d] see page 8 of python data vis.
# TODO: [e] Write file size metrics.
# TODO: [e] Write file created metrics.
# TODO: [e] Write file updated metrics.
# TODO: [d] Write class count metrics.
# TODO: [d] Write function count metrics.
# TODO: [d] Write class list of file.
# TODO: [d] Write function list of file.
# TODO: [e] match unit test files to class files, and count tests. also get functions/properties without tests.
# TODO: [i] Get functions/classes that do not have docstrings.
# TODO: [e] output to do list to pdf. [i] ideally colour code to make easier ([i]idealistic = grey, [c]critical = amber (bugs are red!), [e]essential = green, [d]desirable = black) 
# TODO: [i] Assume idealistic if no tag.
# TODO: [e] objects...is it easiest to import each file, then use dir() on the module? see p. 99)
# TODO: [d] Check for 'conflicted copy' in title of file, and write as a system level bug with list of conflicted versions. [i] Get a diff of changes.
# TODO: [i] Decide how to handle multitagged TODOs (currently counts against all?).
# TODO: [d] Include results of unit tests (perhaps last unit test run outputs a text file and this reads that, rather than run unit test suite?).
# TODO: [i] Use http://docs.python.org/library/timeit.html#module-timeit to time how long unit tests take/how long it takes to import modules.
import os, sys
import socket
import datetime
import csv, json
import difflib

#BUG: Does not pick up 'TODO' items where square brackets immediately follow colon (e.g. TODO:[e] Blah... ). 
TODOITEMSCLOSED = 0
DATESTAMP = datetime.datetime.now() # Output: 2010-10-27 19:29:48.401560
COMPUTERSTAMP = socket.gethostname() #os.environ['COMPUTERNAME'] #TODO: [e]Check against http://stackoverflow.com/questions/799767/getting-name-of-windows-computer-running-python-script if doesn't work across systems.
LOCATIONSTAMP = "" #TODO: [i] Add location stamp (using what library?).
PROJECTROOTPATH = ""

def ca_analysepython(rootpath, currentfile, resultsList):
    #HACK: [i] Note the open() calls. This is probably quite inefficient, but shouldn't be an issue until/unless the project gets very big.
    #return list of analysed data.
    #print(currentfile) #Debug
    currentFileDataList = []
    PROJECTROOTPATH = rootpath #HACK: lazy.
    sFilePath = os.path.join(rootpath, currentfile)
    
    #(1) filename and path.
    currentFileDataList.append(sFilePath) 
    #(2) Line count.
    currentFileDataList.append(len(open(sFilePath, 'rU').readlines())) 
    #(3) Word count.
    wCount = 0
    wTodoCount = 0
    lTodoLines = []
    wBugCount = 0
    lBugLines = []
    wHackCount = 0
    lHackLines = []
    nLoCWhitespace = 0
    nLoCComment = 0
    nLoCCode = 0 #HACK: Will include docstrings in lines of code.
    nLoCOther = 0
    nLineCounter = 0
    tCriticalCount = 0
    tCriticalLines = []
    tEssentialCount = 0
    tEssentialLines = []
    tDesirableCount = 0
    tDesirableLines = []
    tIdealisticCount = 0
    tIdealisticLines = []
    tNoTagCount = 0
    tOtherTagCount = 0
    tOtherTagLines = []
    tOtherTags = []
    
    for line in open(sFilePath):
        nLineCounter += 1
        #LoC count. If whitespace only, whitespace. If first left character is comment, comment. If no comment, code. If comment, but not leftmost, code AND comment.
        sLine = line.strip()
        if sLine == "": #Whitespace
            nLoCWhitespace += 1
        elif sLine[0:1] == "#": #Comment, as no code characters before the # symbol.
            nLoCComment += 1
        elif sLine[0:1] != "#" and ("#" in sLine) == True: #Comment AND Code, as there are code characters before the # symbol.
            nLoCComment += 1
            nLoCCode += 1
        elif sLine[0:1] != "#": #Code, as no # symbol.
            nLoCCode += 1
        else:
            nLoCOther += 1 #shouldn't happen - a line cannot be NOT(whitespace, code, comment, code+comment).
            #TODO: [i] Add exception here for sLine that doesn't meet LoC matching pattern. What about docstrings, as currently flagged as code?
            
        bNoTag = True
        for word in line.split():
            wCount += 1  
            if word == "TODO:" or word == "#TODO:" or word == "TODO":
                wTodoCount += 1
                lTodoLines.append(str(nLineCounter) + " - " + line.strip())
            elif word == "BUG:" or word == "#BUG:" or word == "BUG":
                wBugCount += 1
                lBugLines.append(line.strip())
            elif word == "HACK:" or word == "#HACK:" or word == "HACK":
                wHackCount += 1
                lHackLines.append(line.strip())

            tagCheck = word[0:3]
            if tagCheck == "[c]" : 
                tCriticalCount += 1
                tCriticalLines.append(line.strip())
                bNoTag = False
            elif tagCheck == "[e]" :
                tEssentialCount += 1
                tEssentialLines.append(line.strip())
                bNoTag = False
            elif tagCheck == "[d]" :
                tDesirableCount += 1
                tDesirableLines.append(line.strip())
                bNoTag = False
            elif tagCheck == "[i]" :
                tIdealisticCount += 1
                tIdealisticLines.append(line.strip())
                bNoTag = False
            elif tagCheck[0:1] == "[" : #HACK: [i]May not work with strings such as '[tagname]textimmediatelyfollowing'.
                tOtherTagCount += 1
                tOtherTagLines.append(line.strip())
                tOtherTags.append(word)
                bNoTag = False
        if bNoTag == True:
            tNoTagCount += 1
        #TODO: [e] IMPORT here.
        #doOnce(eval("import " + sFilePath), "A"))
        #doOnce(exec("import " + sFilePath), "B"))
        #all the checks for classes and parts of code go here (and most likely, unit tests).

            
        
    currentFileDataList.append(wCount)
    #(4) -TODO- Count.
    currentFileDataList.append(wTodoCount) 
    #(5) -TODO- List.
    currentFileDataList.append(lTodoLines) 
    #(6) -BUG- Count.
    currentFileDataList.append(wBugCount) 
    #(7) -BUG- List.
    currentFileDataList.append(lBugLines)
    #(8) -HACK- Count.
    currentFileDataList.append(wHackCount) 
    #(9) -HACK- List.
    currentFileDataList.append(lHackLines)

    #(10) LoC: Code
    currentFileDataList.append(nLoCCode)
    #(11) LoC: Comment
    currentFileDataList.append(nLoCComment)
    #(12) LoC: Whitespace
    currentFileDataList.append(nLoCWhitespace)
    #(13) LoC: Other
    currentFileDataList.append(nLoCOther)
    
    #(14) Critical: [c] Count
    currentFileDataList.append(tCriticalCount)
    #(15) Critical: [c] List
    currentFileDataList.append(tCriticalLines)
    #(16) Essential: [e]
    currentFileDataList.append(tEssentialCount)
    #(17) Essential: [e] List
    currentFileDataList.append(tEssentialLines)
    #(18) Desirable: [d]
    currentFileDataList.append(tDesirableCount)
    #(19) Desirable: [d] List
    currentFileDataList.append(tDesirableLines)
    
    #(20) Idealistic: [i]
    currentFileDataList.append(tIdealisticCount)
    #(21) Idealistic: [i] List
    currentFileDataList.append(tIdealisticLines)
    #(22) No importance level: [blank] #TODO:[d]In list, this goes above idealistic. May need regex for [<any characters>] pattern.
    #currentFileDataList.append(nLoCOther)
    #(24) Other tagging: [other] #TODO: [d] append tag to list of additional tags. Means can get a list of specific todo related to [unittests], for example.
    #currentFileDataList.append(nLoCOther)

    #(20) Module import (class count), class list?, .... dir()
    #currentFileDataList.append(nLoCOther)
    

    
    

    
    #append these items and return.
    resultsList.append(currentFileDataList)
    #print("TODO List for " + currentfile)
    #for line in lTodoLines:
    #    print(line),


def handleResults(bDoAggregate, resultsList):
    #['..\\Functionality and Requirements\\Classes\\cSystem.py', 52, 209, 0, [], 0, [], 0, []]
    lineCount = 0
    wordCount = 0
    todoCount = 0
    bugCount = 0
    hackCount = 0
    LoCCode=0
    LoCComment=0
    LoCWhitespace=0
    LoCOther=0
    tagCritical=0
    tagEssential=0
    tagDesirable=0
    tagIdealistic=0
    tagBlank=0
    tagOther=0
    
    todoList = []
    bugList = []
    hackList = []

    criticalList = []
    essentialList = []
    desirableList = []
    idealisticList = []

    print("RESULTS: " +str(len(resultsList)))
    raw_input()
    for item in resultsList: #Remember that these are -1 from position in list above.
        lineCount += item[1]
        wordCount += item[2]
        todoCount += item[3]
        
        if len(item[4]) > 0: #TO-DO items exist.
            todoList.append("  " + os.path.basename(item[0])) #HACK: [i] Not a good way to get the class filename from the stored path.
            for todo in item[4]:
                todoList.append("   --" + todo)
        bugCount += item[5]
        hackCount += item[7]
        LoCCode += item[9]
        LoCComment += item[10]
        LoCWhitespace += item[11]
        LoCOther += item[12]
        tagCritical+= item[13]
        if len(item[14]) > 0:
            criticalList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for crititem in item[14]:
                criticalList.append("   --" + crititem)
        tagEssential+= item[15]
        if len(item[16]) > 0:
            essentialList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for essitem in item[16]:
                essentialList.append("   --" + essitem)
        tagDesirable+= item[17]
        if len(item[18]) > 0:
            desirableList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for desirableitem in item[18]:
                desirableList.append("   --" + desirableitem)
        tagIdealistic+= item[19]
        if len(item[20]) > 0:
            idealisticList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for idealisticitem in item[20]:
                idealisticList.append("   --" + idealisticitem)

    if bDoAggregate:
        #HACK: [i]Quick and dirty. If bDoAggregate, then print out the details, else you're writing a record to the log. This whole module should be refactored as a class, but pretty low priority.
        print ("CODE ANALYSIS:")
        print (" Total files:          " + str(len(resultsList)))
        print (" Total lines:          " + str(lineCount))
        print (" Total words:          " + str(wordCount))
        print ("\n")
        print (" Total lines:          " + str(lineCount))
        print ("  Lines of Code:       " + str(LoCCode))
        print ("  Lines of Comments:   " + str(LoCComment))
        print ("  Lines of Whitespace: " + str(LoCWhitespace))
        print ("  Unidentified Lines:  " + str(LoCOther))
        print ("\n")
        print (" TODO Items:           " + str(todoCount)) 
        print (" ...[c] Critical:       " + str(tagCritical))
        print (" ...[e] Essential:      " + str(tagEssential))
        print (" ...[d] Desirable:      " + str(tagDesirable))
        print (" ...[i] Idealistic:     " + str(tagIdealistic))
        print (" ...[<other>]:          " + str(0))
        #TODO: [i] For each 'other' tag item, print count?
        #TODO: [d] Display other tag list.
        print (" ...[<blank>]:          " + str(0))
        print (" BUG Items:            " + str(bugCount))
        print (" HACK Items:           " + str(hackCount))
        print ("\n")
        print (" TODO ITEMS as of " + str(DATESTAMP))
        for line in todoList:
            #if line.strip()[0:2] == "..": #TODO: [d] change to option of true/false of showing only file and not path breaks this.
            if line.strip()[-3:] == ".py":
                print ("\n"), #For readability, insert newline before each new file is named.
            print (line), #TODO: [i] Replace these with stdout calls. print(string), <-- with trailing comma just smells bad to me. Makes it look unfinished.
        
        print ("\n")
        print (" CRITICAL ITEMS")
        for lineB in criticalList:
            if lineB.strip()[-3:] == ".py":
                print ("\n"), #For readability, insert newline before each new file is named.
            print (lineB), #TODO: [i] Replace these with stdout calls. print(string), <-- with trailing comma just smells bad to me. Makes it look unfinished.
        print ("\n")
        print (" ESSENTIAL ITEMS")
        for lineB in essentialList:
            if lineB.strip()[-3:] == ".py":
                print ("\n"), #For readability, insert newline before each new file is named.
            print (lineB), #TODO: [i] Replace these with stdout calls. print(string), <-- with trailing comma just smells bad to me. Makes it look unfinished.
        print ("\n")
        print (" DESIRABLE ITEMS")
        for lineB in desirableList:
            if lineB.strip()[-3:] == ".py":
                print ("\n"), #For readability, insert newline before each new file is named.
            print (lineB), #TODO: [i] Replace these with stdout calls. print(string), <-- with trailing comma just smells bad to me. Makes it look unfinished.
        print ("\n")
        print (" IDEALISTIC ITEMS")
        for lineB in idealisticList:
            if lineB.strip()[-3:] == ".py":
                print ("\n"), #For readability, insert newline before each new file is named.
            print (lineB), #TODO: [i] Replace these with stdout calls. print(string), <-- with trailing comma just smells bad to me. Makes it look unfinished.

    else:

        print("x!")
        raw_input()
        entry = [DATESTAMP, COMPUTERSTAMP, LOCATIONSTAMP, lineCount, wordCount,
                 todoCount, bugCount, hackCount, LoCCode, LoCComment, LoCWhitespace, LoCOther,
                 tagCritical, tagEssential, tagDesirable, tagIdealistic,
                 TODOITEMSCLOSED]
        #HACK: [i]'entry' values mapping to columns is not consecutive. e.g. hackCount = no, LocCode != no + 1.
        #TODO: [d]Check against http://stackoverflow.com/questions/2666863/list-to-csv-in-python
        #BUG: [c]Currently appending CSV row record to existing entry. Does it need a manual newline character adding?
        #Possible fix, now using http://bugs.python.org/issue7198 .

        """
        f = open('file.txt', 'r+')
        f.seek(-2, 2) # last character in file
        if f.read(2) == '\n\n':
           f.seek(-1, 1) # wow, we really did find a newline! rewind again!
        f.write('orange')
        f.close()
        """
        fileObject = csv.writer(open('code_record.csv','ab'),delimiter=',')
        fileObject.writerow(entry)
        
    
def aggregateResults(resultsList):
    handleResults(True, resultsList)    

def writeResultsRecord(resultsList):
    """
    Handles all writing of records (so anything that should happen every time (e.g. collating todo lists, running unit test suite(?)) should go here).
    Note that the order is important here - need to store the todo before comparing it to 'currentTODO', which is the PREVIOUS todo list.
    """
    sThisTODO = handleResults_Additional(resultsList, "TODO List")
    compareTODOLists(sThisTODO) 
    storeCurrentTODOList(sThisTODO) #This also updates the number of items closed since last time.   
    handleResults(False, resultsList)

    #Render to HTML.
    #TODO: [i] Fix HMTL render.
    #jsondata = csvtojson(open( 'code_record.csv', 'r' ))
    #renderHTMLanalysis(jsondata)
    pass
    
def compareTODOLists(sThisTODO):
    """
    Compares sThisTODO to currentTODO.txt.
    Expects a list (not pythonic!)
    """
    #SOURCE: From http://blog.doughellmann.com/2007/10/pymotw-difflib.html
    """
    d = difflib.Differ()
    t = open("currentTODO.txt").readlines()
    diff = d.compare(t, sThisTODO.split("\n"))
    s = '\n'.join(list(diff))

    d = difflib.Differ()
    t = ["a","b"]
    x = "a\nb\nc"
    diff = d.compare(t, x)
    s = '\n'.join(list(diff))
    """
    d = difflib.Differ()
    #a = str(open("a.txt").read())
    #b = "a" + "\n" + "b" + "\n" + "c" + "\n" + "\n" + "d" + "\n" + "e" + "\n" + "f" + "\n" + "g"
    a = open("currentTODO.txt").readlines()
    b = sThisTODO
    a = [w.replace('\n', '') for w in a] #Clear newline characters from text file.

    #Ignore first 10 characters, else it's pulling line numbers in.
    a = [w.replace(w[0:9], '') for w in a] 
    b = [w.replace(w[0:9], '') for w in b] 
    #HACK: This works, but it means that we can't see where the TODO came from.

    diff = d.compare(a, b)
    s=diff
    s2 = list()
    itemsclosed=0
    for line in s:
        if line[0:1] == "+" or line[0:1] == "-":
            s2.append(line)
            if line[0:1] == "-":
                itemsclosed +=1
    TODOITEMSCLOSED = itemsclosed
    #TODO: [d] Remove all these debug strings.
    print("A:")
    print(str(type(a)))
    #print(a)
    print("\n")
    print("B:")
    print(str(type(b)))
    #print(b)
    print("DIFF:")

    #print(s2)
    print("\n")
    
    
    #DEBUG:
    print("\n\n")
    print("DIFFS IN TODO")
    #print(s2)
    print("\n")
    updateTODOChangelog(s2) 
    return s2
    

def storeCurrentTODOList(sList):
    """Stores todo list as text file called currentTODO.txt"""
    open('currentTODO.txt', 'w').close() #Clears the file.
    f = open("currentTODO.txt", 'r+')
    """print("\n")
    print("SLIST")
    print(type(sList))
    print(sList)
    print("\n")"""
    f.seek(0)
    for line in sList:
        f.write(line)
        f.write("\n")
    f.close()
    #TODO: [i] Add call to PDF write here. Would like colour coding for categories (e.g replace [c] with RED [c]).

def updateTODOChangelog(sList):
    """
    Appends todo list changes to text file called TODOChangeLog.txt
    """
    #appends using open() in 'a' mode. e.g. open(file, mode='a')
    f = open("TODOChangeLog.txt", mode='a')
    f.write("\n")
    f.write(str(DATESTAMP) + "\n")
    for line in sList:
        f.write(line)
        f.write("\n")
    f.write("\n")
    f.close()


def handleResults_Additional(resultsList, sReturnType = "TODO List"):
    """
    Returns a list.
    """
    #TODO: [i] I only needed to duplicate handleResults because it wasn't broken down enough. Refactor these.
    lineCount = 0
    wordCount = 0
    todoCount = 0
    bugCount = 0
    hackCount = 0
    LoCCode=0
    LoCComment=0
    LoCWhitespace=0
    LoCOther=0
    tagCritical=0
    tagEssential=0
    tagDesirable=0
    tagIdealistic=0
    tagBlank=0
    tagOther=0
    
    
    todoList = []
    bugList = []
    hackList = []

    criticalList = []
    essentialList = []
    desirableList = []
    idealisticList = []

    for item in resultsList: #Remember that these are -1 from position in list above.
        lineCount += item[1]
        wordCount += item[2]
        todoCount += item[3]
        
        if len(item[4]) > 0: #TO-DO items exist.
            todoList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for todo in item[4]:
                todoList.append("   --" + todo)
        bugCount += item[5]
        hackCount += item[7]
        LoCCode += item[9]
        LoCComment += item[10]
        LoCWhitespace += item[11]
        LoCOther += item[12]
        tagCritical+= item[13]
        if len(item[14]) > 0:
            criticalList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for crititem in item[14]:
                criticalList.append("   --" + crititem)
        tagEssential+= item[15]
        if len(item[16]) > 0:
            essentialList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for essitem in item[16]:
                essentialList.append("   --" + essitem)
        tagDesirable+= item[17]
        if len(item[18]) > 0:
            desirableList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for desirableitem in item[18]:
                desirableList.append("   --" + desirableitem)
        tagIdealistic+= item[19]
        if len(item[20]) > 0:
            idealisticList.append("  " + os.path.basename(item[0])) #HACK: [i]Not a good way to get the class filename from the stored path.
            for idealisticitem in item[20]:
                idealisticList.append("   --" + idealisticitem)

    sReturn = ""
    if sReturnType == "TODO List":
        sReturn = todoList
    elif sReturnType == "Critical List":
        sReturn = criticalList
    elif sReturnType == "Essential List":
        sReturn = essentialList
    elif sReturnType == "Desirable List":
        sReturn = desirableList
    elif sReturnType == "Idealistic List":
        sReturn = idealisticList
    else:
        return "Failed handleResults_Additional, unrecognised sReturnType"
        exit
    return sReturn

def csvtojson(csvfile):
    reader = csv.DictReader(csvfile)
    out = json.dumps( [ row for row in reader ] )
    return out

def renderHTMLToDoLists(results):
    essentials = handleResults_Additional(results, "Essential List")
    print(PROJECTROOTPATH)
    htmlpath = os.path.join(PROJECTROOTPATH, "codeanalysisrender", "codeanalysis.html")
    f = open(htmlpath, 'w') #Overwrite existing codeanalysis.              
    f.write("<!DOCTYPE html>\n")         
    f.write("<html>\n")         
    f.write("<head>\n")
    f.write(" <link rel=\"stylesheet\" type=\"text/css\" href=\"codeanalysis.css\" />\n")
    f.write("</head>\n")        
    f.write("<body>\n")
    #input()
    #do x6 (bug, critical, essential, desirable, hack, idealistic).
    
    f.write("<div id=\"essentials\">\n")
    count=0
    for line in essentials:
        sLine = "" + line #HACK: [c] Seems to be writing back the stripping to the list.
        sLine.lstrip(" ") 
        if sLine[0:2] == "--":
            f.write("<p class=\"essential\">" + sLine + "</p>\n")
        else:
            f.write("<p class=\"essential source\">" + sLine + "</p>\n")
    f.write("</div>\n")

    f.write("</body>\n")
    f.write("</html>")
    f.close()
    print("Done")
    

def renderHTMLanalysis(jsondataset):
    """renders time series comparison of code analysis"""
    #TODO: [e] Use jflot (or current js render library) to plot line comparison of LoC and TODO items.
    print(PROJECTROOTPATH)
    htmlpath = os.path.join(PROJECTROOTPATH, "codeanalysisrender", "codeanalysis.html")
    f = open(htmlpath, 'w') #Overwrite existing codeanalysis.              

    count = 0
    codeAnalysisDataList = []
    print("LEN:" + str(len(jsondataset)))
    for line in jsondataset:
        if count > 0:
            lList = []
            lData = line.split(',')
            if len(lData)>0:
                lList = [lData[5], lData[6]] #Should be timestamp and LOC.
                codeAnalysisDataList.append(lList)
                count+=1

    print("codeAnalysisDataList:: \n " + str(codeAnalysisDataList) )
    sHTML = """<!DOCTYPE html>
<html>
<head>
<title>Code Analysis</title>
<script type="text/javascript" src="js/jquery.min.js"></script>
<!-- jqplot includes -->
<!--[if lt IE 9]><script language="javascript" type="text/javascript" src="js/excanvas.js"></script><![endif]-->
<script language="javascript" type="text/javascript" src="js/jquery.jqplot.min.js"></script>
<link rel="stylesheet" type="text/css" href="js/jquery.jqplot.css" />
<script type="text/javascript" src="js/jqplot.dateAxisRenderer.min.js"></script>
<!--  -->
<script type="text/javascript">
$(document).ready(function(){
 $("div").click(function(event){
   alert('clicked');
   event.preventDefault();
   $(this).hide("slow");
 });


  $.jqplot('chartdiv2',  [[[1, 2],[3,5.12],[5,13.1],[7,33.6],[9,85.9],[11,219.9]]]);
    
  var line1=""" + str(codeAnalysisDataList) + """var plot2 = $.jqplot('chartdiv', [line1], {
      title:'Customized Date Axis',
      axes:{
        xaxis:{
          renderer:$.jqplot.DateAxisRenderer,
          tickOptions:{formatString:'%b %#d, %#I %p'},
          min:'June 16, 2008 8:00AM',
          tickInterval:'2 weeks'
        }
      },
      series:[{lineWidth:4, markerOptions:{style:'square'}}]
  });
});
</script>


</head>
<body>
<p>Currently: jQuery is working (as per event working). jqPlot is not.</p>
<div id="chartdiv" style="height:600px;width:800px;background-color:red; "></div>
<div id="chartdiv2" style="height:600px;width:800px;background-color:green; "></div>
<p>Test render</p>
<!-- <p>""" +  jsondataset  + """ -->
</p>
</body>
</html>
    """
    f.write(sHTML)
    f.close()

#global variables here. include path to dropbox text file where log is appended.
# should build this function into a unit test suite. every time we di a full check, we also log code review.
# entry should be time stamp, location if available, computer, DATA. Header should indicate data headers. if new metrics  added, update previous rows?
if __name__ == "__main__":
    """Does not run if imported - use to allow importing without running test code."""

    
    RESETPATH = sys.path #store system path for import of modules to be reset at end, after hackish adding to system path.
    RESETCWD = os.getcwd()
    #TODO: Change the path addition to only append if not already in path?

    print(str(os.getcwd())) # show current working directory. will need changing to import from libraries.
    os.chdir("..")
    print(str(os.getcwd()))
    #os.chdir("Libraries")
    #print(str(os.getcwd()))
    for root, dirs, files in os.walk("."): #Note that is not walking os.path.join("..", "Libraries") , as the cwd has been changed.
        for thisdir in dirs:
            #print("Appending " + thisdir + " to sys.path")
            sPath = os.path.abspath(os.path.join(root, thisdir))
            print(sPath)
            sys.path.append(sPath)

    print(sys.path)

    results=[]
    folderIgnoreList = [os.path.join("..", "codeanalysis"),
                        os.path.join("..", "js", "vendor"),
                        os.path.join("..", "_bak"),
                        os.path.join("..", "backup"),
                        os.path.join("..", "img")]
    fileIgnoreList = [""] #TODO: ignore codeanalysis.py &    imported non-project files (Add at later date. This file should be done fairly early in project (before lit review finished)).
    for root, dirs, files in os.walk(".."):
        #print (root, dirs, files) #debug. uncomment to show paths in interactive mode.
        #print("DIR:" + str(dir(dirs)))
        #for sDir in dirs:
        #    print(sDir)
         #   thisDir = os.path.join(root, sDir)
            for file in files:
                bfolderIgnore = False
                thisfile = os.path.join(root, file)
                thisdir = os.path.dirname(thisfile)
                #print(thisdir)
                if (thisfile.endswith(".py")) or (thisfile.endswith(".html")) or (thisfile.endswith(".css")):
                    for folder in folderIgnoreList:
                        if folder in thisdir:
                            #print("'" + thisdir + "' is in '" + folder +"'") 
                            bfolderIgnore = True
                    if thisfile in fileIgnoreList:
                        #print("FILE IGNORE LIST: FILE IGNORED: " + thisfile)
                        #print("\n\n")
                        pass
                    elif bfolderIgnore:
                        #print("FOLDER IGNORE LIST: FILE IGNORED: " + thisfile)
                        #print("\n\n")
                        pass
                    else:
                        #print("DIR of '" + file + "' is '" + thisdir)
                        ca_analysepython(root, file, results)

    ##from pyPdf import PdfFileWriter, PdfFileReader
    #BUG: [c]Resolve pypdf import issues. 




    #print (results)
    sys.path = RESETPATH
    os.chdir(RESETCWD)
    #print("11!")
    raw_input()
    aggregateResults(results)
    #print("12!")
    raw_input()
    writeResultsRecord(results)
    #print("13!")
    raw_input()
    renderHTMLToDoLists(results)
    #print("14!")
    #TODO: [e]Write to PDF.
    raw_input()

    #Cleanup
    sys.path = RESETPATH
    os.chdir(RESETCWD)
    #raw_input() #HACK: [e]Added so that results can be read when run from console. Not needed in interactive mode (or if we've run this solely to update the code analysis record).
