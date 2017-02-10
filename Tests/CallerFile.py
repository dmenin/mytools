from TasksFile import reverse
import os

#os.getcwd()



result = reverse.delay('foo')

result.get()



#from TasksFile import fetch_url
#
#tasks = []
##curl -s -O http://s3.amazonaws.com/alexa-static/top-1m.csv.zip ; unzip -q -o top-1m.csv.zip top-1m.csv ; head -1000 top-1m.csv | cut -d, -f2 | cut -d/ -f1 > topsites.txt
#for url in open('topsites10.txt'):
#    tasks.append(fetch_url.delay('http://' + url.strip()))
#    
    