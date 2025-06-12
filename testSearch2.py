import re
mainkeyword=['MICROSCOPIC REACTION RATES', 'T-REG.    1  === REACTION RATE === ']
subkeyword=['NU*FISSION    FISSION ', 'TOTAL']
ifname1=input("Case ID? A:")
ifname2='VP'
ofname1=ifname1
filenum=input("How many files to process? A:")
#filename structure is "caseID"+"VP"+"2-digit number" for MVP pds files
for count in range(1, int(filenum)+1):
    if count<10:
        ifname3='0'+str(count)
    elif count>=10:
        ifname3=str(count)
    else:
        print("User input error. Please enter an integer.")
        break
    ifname=str(ifname1)+ifname2+ifname3 #input filename
    ofname2='_RR_step'
    ofname3=ifname3
    ofname=str(ofname1)+ofname2+ofname3 #output filename
    big_file=open(ifname, 'r')
    small_file=open(ofname, 'w')

    print_total=False
    subcount=0 #counter for printing lines with subkeyword
    #for loop below extracts the reaction rate information from pds files
    for line in big_file:
        for main in mainkeyword:
            mainmatch=re.findall(main, line)
        if mainmatch:
            small_file.write(line)
            print_total=True #activate subkeyword printing when mainkeyword is found
        if print_total: #subkeyword printing
            for sub in subkeyword:
                submatch=re.findall(sub, line)
            if submatch:
                small_file.write(line)
                subcount+=1
            if subcount==2:
                print_total=False
                subcount=0
    
    print(ofname)
    big_file.close()
    small_file.close()