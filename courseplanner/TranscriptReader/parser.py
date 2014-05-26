import sys
import cStringIO
import re
import json

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams

CMD_LINE = False

# prints standard debug info to stdout when set to true
PRINT_LOG = True

# Set to true only if manually resolving transcript ambiguities
MANUAL_RESOLVE = False



def main(argv):
    import getopt
        
    CMD_LINE = True
    
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:R:t:c:s:')
    except getopt.GetoptError:
        return usage()

    outfp = cStringIO.StringIO()
    resultFp = open("out.csv", "w")
    
    for fname in args:
        fp = file(fname, 'rb')
        getTransContent(fp, resultFp)

def helloWorld(resultFp):
	resultFp.write("hello, world")

def getTransContent(fp, resultfp):
    outfp = cStringIO.StringIO()

	# This secontion contains pdf parsing boilerplate
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outtype = None
    imagewriter = None
    rotation = 0
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    rsrcmgr = PDFResourceManager(caching=caching)
    device = TagExtractor(rsrcmgr, outfp, codec=codec)
    # end boilerplate for pdf parsing
    

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                					maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    fp.close()
    
    parseTrans(outfp.getvalue(), resultfp)
    device.close()


def parseTrans(transContent, outfp):
    ARStr = "--------- Beginning of Academic Record --------- "
    
    # patterns used to match parts of a single class in transcript
    courseIdStr = "([A-Z]|&amp;)+  ? ?[0-9]{1,3}[GEFDNSPAXCBLW]?(?![0-9])"
    courseTitleStr = "([A-Z+_:-]+ ? ? ?|&amp; )+"
    unitStr = "[0-9]\.[0-9][0-9]"
    gradeStr = "([A-Z][A-Z]?[-+]?)? ?  "
    profStr = "([A-Z][a-z]+( [A-Z][A-Z]?[a-z]*)?,[A-Z][a-z]*(-[A-Z][a-z]+)?( [A-Z][a-z]*)?;? ?)+"
    
    yearStr = "2[0-9]{3}-2[0-9]{3}"
    
    # first check for academic record string; if not present, the file
    # is likely not a Stanford transcript and should be handled as such
    try:
        startIndex = transContent.index(ARStr) + len(ARStr)
        transContent = transContent[startIndex:]
    except Exception, e:
        error("Could not find start of academic record")
    
    # Compile regexes for matching
    courseIdPattern = re.compile(courseIdStr)
    courseTitlePattern = re.compile(courseTitleStr)
    unitPattern = re.compile(unitStr)
    gradePattern = re.compile(gradeStr)
    profPattern = re.compile(profStr)
    
    yearPattern = re.compile(yearStr)
    
    # Keep track of the current quarter and year as we parse
    quarter = AcademicQuarter()

    while True:
        quarterIndex = findCurQuarter(transContent, quarter, yearPattern)
        if quarterIndex == -1: # this is returned when we reach end of transcript
            break
        log ("Now in quarter: " + quarter.toString() + " at index " + `quarterIndex`)
        transContent = transContent[quarterIndex:]
        
        while True:
            m1 = yearPattern.search(transContent)
            m2 = courseIdPattern.search(transContent)
            
            # check if no more classes found, or if we have reached next quarter
            if m2 == None or (m1 != None and m1.start() < m2.start()):
                break
            
            currentCourse = CourseInformation(quarter)
            
            # parse remaining fields for course:
            
            currentCourse.id = m2.group()
            charsToAdvance = resolveCourseIDAmbiguity(currentCourse, transContent, m2)

            transContent = transContent[m2.start() + charsToAdvance:]
            
            m = courseTitlePattern.search(transContent)
            currentCourse.title = m.group()
            transContent = transContent[m.start() + len(currentCourse.title):]
            
            m = unitPattern.search(transContent)
            currentCourse.units = m.group()
            transContent = transContent[m.start() + len(currentCourse.units):]
            
            m = unitPattern.search(transContent)
            currentCourse.unitsReceived = m.group()
            transContent = transContent[m.start() + len(currentCourse.unitsReceived):]
            
            m = gradePattern.search(transContent)
            if (m == None or m.group().strip() == ""):
                currentCourse.grade = ""
            else:
                currentCourse.grade = m.group()
                transContent = transContent[m.start() + len(currentCourse.grade):]
                
            currentCourse.grade = currentCourse.grade.strip()
            
            m = profPattern.search(transContent)
            if m == None:
                courseProf = "UNK"
            else:
                courseProf = m.group()
            transContent = transContent[m.start() + len(courseProf):]
            
            
            outfp.write(currentCourse.id + "," + currentCourse.title +  "," + quarter.year + "," + quarter.quarter + "," + currentCourse.units + "," + currentCourse.unitsReceived + "," + currentCourse.grade + "," + courseProf + "\n")
    #print transContent
    
    
# Finds the current academic quarter given the current state of parsing
# in the transcript. Returns the index of the end of the academic quarter
# string, or -1 if none is found
def findCurQuarter(transContent, curAQ, yearPattern):    
    qtrStr = "(Autumn|Winter|Spring|Summer)"

    qtrPattern = re.compile(qtrStr)
        
    m = yearPattern.search(transContent)
    if m == None and curAQ.year == "No Year":
        error("No year string found")
    elif m == None:
        return -1
    curYear = m.group()
    deletedChars = m.end()
    
    transContent = transContent[m.end():]
        
    m = qtrPattern.search(transContent)
    if m == None and urAQ.quarter == "No Quarter":
        error("No quarter string found")
    curQuarter = m.group()
    
    curAQ.year = curYear
    curAQ.quarter = curQuarter
    
    return m.end() + deletedChars


# Resolves course ambiguities caused by the limitations of the pdf parser
def resolveCourseIDAmbiguity(course, transContent, match):
	if MANUAL_RESOLVE:
		return manualResolveAmbiguity(course, transContent, match)
	else:
		charsToAdvance = autoResolveAmbiguity(course, transContent, match)
		if charsToAdvance == -1:
			return len(course.id)
		return charsToAdvance
			
		
		
# prompts the user to manually resolve ambiguities from their course list
def manualResolveAmbiguity(course, transContent, match):
	if CMD_LINE:
		courseId = course.id
		startLen = len(courseId)
		lastChar = courseId[len(courseId) - 1:]
	
		# this portion allows user to answer ambiguities by selecting how
		# many alphabetic chars to accept at the end of the course ID
		if (lastChar.isalpha()):
			curChars = 1
			while True:
				courseId = transContent[match.start():match.start() + startLen - 1 + curChars]
				lastChar = courseId[len(courseId) - curChars:]
				log( "Course ID is currently " + courseId + ", ending portion is " + lastChar)
				log( "press enter to accept, m to add more chars, l to add less chars to ending portion")
				input = raw_input("--> ")
				if input == "":
					break
				elif input == "l":
					if curChars != 0:
						curChars -= 1
				elif input == "m":
					curChars += 1
				else:
					break          
		course.id = courseId
		return len(course.id)

# Uses JSON course data to attempt to automatically resolve ambiguities
# in course titles.
def autoResolveAmbiguity(course, transContent, match):
	baseCourseId = getBaseCourseId(course.id)
	shortenedBaseCourseId = ' '.join(baseCourseId.split())
	numDeletedChars = len(baseCourseId) - len(shortenedBaseCourseId)
	
	baseCourseId = shortenedBaseCourseId
	
	courseList = getCourseList(baseCourseId)
	
	for numAlphaChars in range(0,4):
		courseIdCand = transContent[match.start():match.start() + len(baseCourseId) + numDeletedChars + numAlphaChars]
		courseIdCand = ' '.join(courseIdCand.split())
		for courseObj in courseList:
			#pprint(courseObj)
			curCourseId = courseObj['course_num']
			#TODO: check for correct course title for year
			# currently just uses title from most recent offering
			offerings = courseObj['offering']
			courseTitle = offerings[-1]['course_title']
			if curCourseId == courseIdCand and transcriptMatches(baseCourseId, numAlphaChars, courseTitle, transContent, match, numDeletedChars):
				course.id = courseIdCand
				log ("Selected course: " + curCourseId + " : " + courseTitle, True)
				return len(curCourseId) + numDeletedChars
	warn ("unable to resolve ambiguity for " + baseCourseId)
	return -1
    
# determines whether both the course ID terms match, and whether the start of the
# ensuing transcript content matches the course title
def transcriptMatches(courseId, numAlphaChars, courseTitle, transContent, match, numDeletedChars):
	log ("Checking if course " + courseTitle + " matches transcript")
	for ind in range(3,1,-1):
		titleSnippet = courseTitle[:ind].lower()
		endCourseIdIndex = match.start() + len(courseId) + numAlphaChars + numDeletedChars
		transcriptSnippet = transContent[endCourseIdIndex : endCourseIdIndex + ind].lower()
		log ("Examining candidate: " + transcriptSnippet + " for: " + titleSnippet)
		log ("Course ID: " + courseId + " numAlpha: " + `numAlphaChars`)
		if titleSnippet == transcriptSnippet:
			if ind != 3:
				warn ("Selected course with less than 3 matching chars: " + courseId + "" + titleSnippet)
			return True
	return False
    
# Returns the base course ID (the course ID minus any extra letters at the end)
# i.e CS 106A  --> CS 106
def getBaseCourseId(courseId):
    index = len(courseId) - 1
    while(courseId[index:].isalpha()):
    	index = index - 1
    	if index == -1:
    		error("Course ID only contains alphabetic characters; this violates an assumption of this loop")
    return courseId[:(index+1)]
    
# Gets the list of possible matching courses for a given base course ID (ie. CS 106)
def getCourseList(courseId):
	courseList = []
	json_data=open('../Data/courses_json')
	allCourses = json.load(json_data)
	for courseCand in allCourses:
		courseInfo = allCourses[courseCand]
		#pprint(courseInfo)
		if courseId in courseInfo["course_num"]:
			log ("Adding to course list for " + courseId + ": " + courseInfo["course_num"])
			courseList.append(courseInfo)
	return courseList
	
	
    
# currently this just prints error message and exits. Should change
# to log the error on the server side
def error(errorString):
    print errorString
    sys.exit(-1)
    
# Less serious than an error, but more important than just debug information
def warn(errorString):
	print "WARNING: " + errorString

# Log information for debugging, does not indicate an actual error though
def log(logString, override = False):
    if (PRINT_LOG or override):
    	print logString

# Encapsulates all informaiton about a single academic quarter: year and the quarter name
class AcademicQuarter:
    def __init__(self):
        self.quarter = "No Quarter"
        self.year = "NoYear"

    def toString(self):
        return "Quarter: " + self.quarter + " | Year: " + self.year

# Encapsulates all information about a course
class CourseInformation:
    def __init__(self, curQuarter):
        self.quarter = curQuarter
    
if __name__ == '__main__': sys.exit(main(sys.argv))
