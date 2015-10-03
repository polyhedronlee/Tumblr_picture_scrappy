#This software is for downlaoding pictures from multiple trumblr blogs. 
#This software heavily takes reference of tumblr api instruction from http://blog.exz.me/2014/write-a-python-script-to-export-1280-size-picture-urls-of-tumblrs/

####Update Memo####
#v3 update, timeout setting
#v4 update 1.skip when there are duplicators 2.cross file document checking.


####Preparation work######
#Step 1. Afterdowing this code, under the same file of the script, create a new txt document to store the blognames.
#        If the blog is 'http://abc123.tumblr.com', then the blog name is 'abc123' (without the quotation marks). Each line stores only one blogname
#Step 2. In the con1 in the following Configuation Section, insert the address where do you store the pictures. using double slash\\ instead of single slash\, the defaut setting is i:\Tumblr.
#Step 3. In the con2, insert the name of the txt document that you store the blognames.
#Step 4. Go Check the rest configuration part, change the setting if necessary
#Step 5. Run the code (F5), the 


####Configuration Section####

#con1 the file that stores the pic
filemain="i:\\Tumblr\\"

#con2 the name of text document that stores the blogname
blogname = 'blogname.txt'

#con3 (if newdoc=True)save a duplicator in the _New document
#you need to creat a new file called "_New" under the address that you store the code.
newdoc = True

#con4 (if dupche=True) skip the document when the software encounter 25 duplicated picture in a row.
#the documents check duplicated picture based on the file name.
dupche=False
dupnum=0
duplim=25 # the limitation of duplicated pictures
dupbre=False

#con5 (if duecro = True) examing the duplicators in different files.
duecro=False
dueblonam =['',''] #the file names that you want to go through, please don't leave it empty if the duecro is True


####the actual code starts here####
import urllib.request
import re
import os, sys, urllib
import socket

def downpic (picurl,filename,filemain,blogname):
    #address =os.path.join(filemain,blogname,filename)
    #print(address)
    #urllib.request.urlretrieve(picurl,address)
    path =os.path.join(filemain,blogname)
    url = picurl
    name =os.path.join(path,filename)
    try:
        conn = urllib.request.urlopen(url,timeout=5)  
        f = open(name,'wb')  
        f.write(conn.read())  
        f.close()  
        print('Pic Saved!')   
    except socket.timeout:
        print('timeout')
    except urllib.error.URLError:
        print('URLError',url,filename)

def checkdup(picurl,blogname,duecro,dueblonam): #check duplicators, if retruns true means there is duplicators.
    if os.path.isfile (os.path.join(blogname.strip(),os.path.basename(picurl))): #check if there is same document under the same blog
        return True
    if duecro: #cross document check duplication
        for i in dueblonam:
            if os.path.isfile(os.path.join(i,os.path.basename(picurl))) :
                print('found in other blogs')
                return True

    


extractpicre = re.compile(r'(?<=<photo-url max-width="1280">).+?(?=</photo-url>)',flags=re.S)
#search for url of maxium size of a picture, which starts with '<photo-url max-width="1280">' and ends with '</photo-url>'
inputfile = open(blogname,'r')    #input file for reading blog names (subdomains). one per line
proxy= {'http':'http://127.0.0.1:8087'} #proxy setting for some reason
for blogname in inputfile:  #actions for every blog

    baseurl = 'http://'+blogname.strip()+'.tumblr.com/api/read?type=photo&num=100&start='    #url to start with
    start = 0   #start from num zero
    count=0
    dupnum=0
    dupbre=False
    
    while True: #loop for fetching pages
        url = baseurl + str(start)  #url to fetch
        print(url)   #show fetching info
        pagecontent = urllib.request.urlopen(url).read()    #fetched content
        pagecontent = str(pagecontent)
        pics = extractpicre.findall(pagecontent)    #find all picture urls fit the regex

        if not (os.path.exists(filemain+blogname.strip())): #see if the file exists
            print('File non-exist')
            os.mkdir(filemain+blogname.strip())
        name_of_blog=blogname.strip()
        
        for picurl in pics: #loop for writing url
            
            if checkdup(picurl,blogname,duecro,dueblonam): #check duplicator
                print(os.path.basename(picurl)+" existed")
                dupnum += 1              
            else:
                count +=1
                dupnum=0
                downpic(picurl,os.path.basename(picurl),filemain,blogname.strip())
                print('download',blogname,'no.',count,' picture')
                if newdoc:
                    downpic(picurl,os.path.basename(picurl),filemain,'_New')
                    
            if dupche: #see if the check too many duplicator fuction is activated.
                if dupnum > duplim:
                    dupbre = True
                    print ('more than', duplim, 'pictures found alreadly had been downloaded in a row. Hence skip')
                    break
        if dupbre:
            break
        if (len(pics) < 100):    #figure our if this is the last page. if less than 50 result were found 
            print('This is the end')
            break   #end the loop of fetching pages
        else:   #find 200 result
            start += 100 #heading to next page

    print(url)   #show fetching info
