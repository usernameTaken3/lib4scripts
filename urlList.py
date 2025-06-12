#ページのリンクを全部出力する
import requests
import re
import codecs
urlkeyword=["https://syllabus.s.isct.ac.jp/courses/2025/7/0-907-0-110100-0/"]
subjectword=["LAH."]
removeword=["<td>","<\\td>","<a href=","</a>"," tabindex=\"0\" style=\"\">"]
ifname="BunkeiSyllabus.html" #input filename
ofname1="BunkeiURL"
ofname2="subjectList"
#html_file=codecs.open(ifname, 'r', 'utf-8', 'ignore')
url_file=codecs.open(ofname1, 'w', 'utf-8', 'ignore')
subject_file=codecs.open(ofname2, 'w', 'utf-8', 'ignore')

#print_total=False
count=0 #counter for printing lines with subkeyword

# for line in big_file:
    # #print(line)
    # for main in mainkeyword:
        # mainmatch=re.findall(main, line)
    # if mainmatch:
        # for delword in removeword:
            # line=line.replace(delword,"")
        # small_file.write(line)
        # # print_total=True #activate subkeyword printing when mainkeyword is found
    # # elif print_total: #subkeyword printing
        # # small_file.write(line)
        # # print_total=False #activate subkeyword printing when mainkeyword is found
        # count+=1

def find_word(ifname, outfile, word, removeword):
    infile=codecs.open(ifname, 'r', 'utf-8', 'ignore')
    count=0
    for line in infile:
        #print(line)
        for lookfor in word:
            mainmatch=re.findall(lookfor, line)
        if mainmatch:
            for delword in removeword:
                line=line.replace(delword,"")
            outfile.write(line)
            # print_total=True #activate subkeyword printing when mainkeyword is found
        # elif print_total: #subkeyword printing
            # small_file.write(line)
            # print_total=False #activate subkeyword printing when mainkeyword is found
            count+=1
    outfile.write(str(count))
    infile.close()
    return

find_word(ifname, url_file, urlkeyword, removeword)
find_word(ifname, subject_file, subjectword, removeword)
print("URL list output to", ofname1)
print("Subject list output to", ofname2)

#html_file.close()
url_file.close()
subject_file.close()