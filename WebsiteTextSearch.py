import requests #require install
from lxml import html #require install
import re #require install
from bs4 import BeautifulSoup #require install
import codecs #require install

def get_content(url):
    """
    Fetches the HTML content of a web page or an entire website and searches for a specific word or phrase.

    Args:
        url (str): The URL of the web page or website.
        word (str): The word or phrase to search for.

    Returns:
        str: A markdown-formatted string indicating whether the word was found or not.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        soup = BeautifulSoup(response.content, "html.parser")
        textweblines = soup.find_all(['h3','p'])
        subjectName = soup.find_all("h1", "c-h1")
        return textweblines, str(subjectName)
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the content: {e}"

mainkeyword = ["成績評価の方法及び基準"] #what to search for
# Example usage
ifname="BunkeiURLonly.txt" #URL filename
ifname2="subjectList" #subject list filename
ofname="BunkeiKadaiList3.csv"
url_file=codecs.open(ifname, 'r', 'utf-8', 'ignore')
subject_file=codecs.open(ifname2, 'r', 'utf-8', 'ignore')
out_file=codecs.open(ofname, 'w', 'shift-jis', 'ignore')

urllist = []
subjectlist = []
subjectNamelist = []
# weblines = pagesoup.find_all(['h3','p'])
#print(weblines)
#extract each URL from url_file into urllist
removeword=[" ","\""]
for url in url_file:
    for delword in removeword:
        url=url.replace(delword,"")
    urllist.append(url.rstrip())
    
#extract each URL from url_file into urllist    
for subject in subject_file:
    subjectlist.append(subject.rstrip())
#print(subjectlist)
    # for delword in removeword:
        # url=url.replace(delword,"")
#print(urllist)

subcount=0 #counter for number of kougi subject accessed

for url in urllist:
    hyoukaExist=False
    enum=0
    weblines = []
    kadai_hyouka=[]
    getweblines, subjectName = get_content(url)
    removeword=[" ","[<h1class=\"c-h1\">","</h1>","]","\n"] #remove [<h1class="c-h1">
    for delword in removeword:
        subjectName="".join(subjectName.replace(delword,""))
    subjectNamelist.append(subjectName.rstrip())
    #print(getweblines)
    print(subjectName)
    
    for ii in getweblines:
        #print(ii)
        weblines.append(ii.contents)
    #print(weblines)
    for line in weblines:
        enum+=1
        for main in mainkeyword:
            mainmatch=re.findall(main, str(line))
        if mainmatch:
            hyoukaExist=True
            #print(line)
            #print(weblines[enum])
            #print(type(weblines[enum]))
            kadai_hyouka=str(" ".join(map(str,weblines[enum])))
            removeword=["<br/>",","]
            for delword in removeword:
                kadai_hyouka=kadai_hyouka.replace(delword,"")
        if hyoukaExist==False:
            kadai_hyouka="None"
    out_file.write(subjectNamelist[subcount]+","+kadai_hyouka.strip()+","+subjectlist[subcount]+","+str(subcount+1)+"\n")    
    print(subjectlist[subcount])
    subcount+=1
    #print(subcount)
    
#out_file.write(str(subcount))
url_file.close()
out_file.close()
