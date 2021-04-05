import requests
from bs4 import BeautifulSoup
#from selenium import webdriver
import webbrowser
import random, sys
from time import sleep as wait
import pandas as pd
import re           #is this even used?
import atexit

"""
#https://www.geeksforgeeks.org/how-to-exit-a-python-script/
def exit_handler():
    print('My application is ending!')
atexit.register(exit_handler)
print('GFG!')
sys.exit()
"""
#https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
#try to do this so that the code can constantly keep working instead of breaking every 10

#if the code keeps running, it will get copies of its self but will get a few morer from the web

#https://pypi.org/project/fake-useragent/
#antiblocking measures
from fake_useragent import UserAgent
ua = UserAgent()
User_Agent = str(ua.random) #always gets a random UserAgent
#User_Agent = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
#print(User_Agent)
#User_Agent = "*"
townname_ = "Bayonne"
#townname_ = 'Guttenberg'
#townname_ = 'North Bergen'
#townname_ = 'Union City'
#townname_ = 'Jersey City'
#townname_ = "Newark"
#.capitalize() capitalizes the word
#townname_ = str(input("Name of Town: ")).lower()
#townname_ = "East Rutherford"


try:
    townname = townname_.split(" ")
    townname_space = townname[0].capitalize()+" "+townname[1].capitalize()
    townname = townname[0].capitalize()+"-"+townname[1].capitalize() #townname used for zumper
    #rtownname = townname[0]+#townname used for realtor.com
except:
    townname = townname_.capitalize()
    townname_space = townname
    pass


try:
    # finds dataframe  
    folders = "/Users/juanm./Documents/Coding/Data Science?/github/Webscrapper-Real-Estate/Not Working/"
    og_filename = townname+'.csv'
    og_df = pd.read_csv(folders+og_filename)  
    # reads the already there file
    i = og_df.i.to_list()   #creates i into its own list
    #start = og_df["i"].tail(1)
    #start = len(og_df) #finds the length of the dataframe
    """
    if i[-1]<max(i): #if the last one is less than the max, it means it is not on page 1 anymore
        start = find_page(i)
    else:
        start = i[-1]+1
    #sys.exit()
    """
    start = i[-1]+1
except:
    start = 0
#sys.exit()
#print(start)
#global price
price = address = beds = baths = prop_taxes = ""

#Issue on line 80 where sometimes it still doesn't find the families of the house

"""Functions"""
#check the size
#go to line 118
def check_house_size(url):
    #User_Agent = str(ua.random) 
    #my_session.headers.update({'User-Agent': User_Agent, "referer": realtor_url})
    prop_session = my_session.get(url)
    prop_soup = BeautifulSoup(prop_session.text, 'html.parser')
    #print(prop_soup.text)
    #sys.exit()
    #finds important house stats
    price, beds, baths, address, prop_taxes = find_house_stats(prop_soup)
    #finds the description of the house
    
    prop_details = prop_soup.find(class_="content", attrs={"id": "content-property_details"})
    #just checks the entire description all at once
    #print(prop_details.text)
    try:
        for i in range (2, 4+1): #checks 2, 3 and 4 family houses
            family = str(i) + " family"
            if family in prop_details.text.lower():
                return (family.capitalize(), price, beds, baths, address, prop_taxes)
    except:
        pass
    try:
        #print("Here")
        before, after = prop_details.text.split("Number of Units: ")
        #print(before)
        #print(after)
        #print(after[0])
        family = str(after[0]) + " family"
        return (family.capitalize(), price, beds, baths, address, prop_taxes)
    except:
        pass
    #if nothing is found or if it crashes, still returns something
    return ("", price, beds, baths, address, prop_taxes)

#find house stats
def find_house_stats(soup):
    #finds the description of the house
    #print()
    #prop_taxes = ""
    prop_taxes = find_property_taxes(soup)
    #finds the price
    try:
        t_price = soup.find(class_="price")    #as long as it contains this, the code works
        #print(t_price.text) 

        #finds the address
        t_address = soup.find(class_="address")
        print(t_address.text)
    except:
        #print(soup.text)
        print("You have been blocked, try again in a couple of minutes")
        print("Inside of find_house_stats")


    #finds the beds
    t_beds = soup.find(attrs={"data-label": "pc-meta-beds"})
    #finds the baths
    t_baths = soup.find(attrs={"data-label": "pc-meta-baths"})

    return(t_price.text, t_beds.text, t_baths.text, t_address.text, prop_taxes)
    #I guess I could also just do everything in returns but this is probably better

def find_property_taxes(soup):
    taxes = "N/A"
    try:
        all_findings = soup.findAll(class_="features")
        for findings in all_findings:
            #global prop_taxes   #use the global variable
            before, splitt = (findings.text).split("Annual Tax Amount: ") #before is trash
            taxes, splitt = str(splitt[:12]).split("So")   #only uses the first 10 characters for tax ammount, then only keeps the integers
            return taxes
    except:
        return taxes

#make a dataframe
def make_houses_dataframe(t_dict):
    global og_df
    #global price, address, beds, baths, prop_link
    try:
        try:
            og_df = og_df.append(t_dict, ignore_index = True)
        except:     #in case it hasn't been created yet
            #print("yes")
            og_df = pd.DataFrame(t_dict, index = [0])
            #since I'm not giving it a list when there hasn't been a csv file, I need to pass an index value
    except:
        print("No homes at all?")
    #print(temp_add_list)
    #print(og_df)

    #print(realtor_houses)
    #folders = "/Users/juanm./Documents/Coding/Data Science?/github/Webscrapper-Real-Estate/"
    #filename = 'Houses_last.csv'
    #og_df.to_csv(folders+townname+".csv", encoding='utf-8', index=False)

def zumper_url():
    #Getting things from zumper
    zumper_url = 'https://www.zumper.com/rent-research/'+townname.lower()+'-nj'
    #webbrowser.open(zumper_url)

    #not working
    zumper = requests.get(zumper_url)
    zcontents = zumper.text
    zsoup = BeautifulSoup(zcontents, 'html.parser')

    rent1, bleh = zsoup.find(class_='About_infoText__2tZYa').text.split("Median") #median 1 bed rent, splits the word after the Number when it starts to say Median
    print(townname_space+" has a median rent of "+ rent1 +".") 
    return (rent1)

def end_code():
    print("END!!!")
    global og_df
    og_df.to_csv(folders+townname+".csv", encoding='utf-8', index=False)

temp_add_list = 0
og_df = pd.DataFrame({}, index = [0])
atexit.register(end_code)
#sys.exit()
#rent = zumper_url()
#rent = re.findall(r'\d+', rent)
#rent = int(rent[0])*1000 + int(rent[1])
rent = 0
#sys.exit()
#right now, the code gets blocked after 10 items

"""Creating a url"""
#sys.exit()
#budget = int(input("What is your budget in thousands of dollars?" + "\n"))
budget = 700
budget = "price-na-" + str(budget*1000)
type_ = 'type-multi-family-home/'
#extra = ""
extra = "beds-3/baths-3/"   #2 2-1 and one 1-1
#making it more likely to be a triplex

realtor_url = 'https://www.realtor.com/realestateandhomes-search/'+townname+'_NJ/'+extra+str(type_)+str(budget)#+'/sby-6'
#'/show-newest-listings'
#print(realtor_url)
#User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

#print(townname)

my_session = requests.session()

my_session.headers.update({'Accept-Encoding': 'gzip, deflate, br','Accept-language': 'en-US,en;q=0.9','Upgrade-Insecure-Requests': '1', 
'User-agent': User_Agent, 'Referer': 'https://www.realtor.com/'
})

"""
header = {'Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'en-US,en;q=0.9','Upgrade-Insecure-Requests': '1', 
'User-Agent': User_Agent}
# 'Referer': 'https://www.google.com/', 'PreviousUrl': 'https://www.google.com/'}
"""

#+townname+'_NJ/beds-3/type-multi-family-home'

"""Actual Code"""
realtor = my_session.get(realtor_url)#, headers = header)
#print(realtor.cookies)
print(realtor.request.headers)
#sys.exit()


html_soup = BeautifulSoup(realtor.text, 'html.parser')
#print(html_soup.text)
#check for blocking
#webbrowser.open(realtor_url)
blocktitle = html_soup.find("title")

if "Pardon Our Interruption" in blocktitle:
    #print(html_soup.text)
    #webbrowser.open(realtor_url)
    print("You have been blocked, try again in a couple of minutes")
    print("From the Start of the Code")
    sys.exit()

try:
    t, tn = townname.split("-")
except:
    tn = townname

#prop = html_soup.find(class_="property-list")
properties = html_soup.findAll(class_='component_property-card')#.findall('li')
#print(properties)

#start = 0
i = 0
print("Starting")
wait(random.randint(0, 100)/100)
for prop in properties:
    i+=1 
    if i < start:
        pass
        #print("skip")
    elif tn.capitalize() in prop.text:
        """Getting links to create a new session at the reference website"""

        href = prop.find("a")
        href = href.get('href') #gets what is inside of the href tag
        #new website uses the base of 'https://www.realtor.com'
        prop_link = 'https://www.realtor.com' + str(href)
        wait(random.randint(2,10))
        size, price, beds, baths, address, prop_taxes = (check_house_size(prop_link))  #gives the house size as a string
        #print(size)
        #sys.exit()
        total_rent = (int(size[0]) * rent)
        temp_add_list = {"i": i, "Size": size, "Price": price, "Gross Rent": total_rent, "Beds": beds, "Baths": baths, "Address": address, "Taxes": prop_taxes, "Urls": prop_link}

        make_houses_dataframe(temp_add_list)
        wait(random.randint(0, 100)/100)  #gets a random amount of milliseconds and waits a really tiny amount of time
        #maximum amount of wait time is around 1 second
        #wait one second to see if that allows it to work better

    elif 'Advertisement' not in prop.text:
        #once it sees something not in Paterson and not an Advertisement, it stops
        #print("BROKE")
        #print(prop.text)
        break

#make_houses_dataframe()
#find_page(i)
print()
print("No more properties on the market that fit those criteria available.")
print("I'm sorry for your inconvenience.")
#print("Something broken, either use next_page or find_page")
#next_page()
#sys.exit()
#try making a code so it can add "/pg-2" or "/pg-3" at the end once it can't find anymore properties

"""
options = webdriver.ChromeOptions();
options.add_argument('headless');
options.add_argument('window-size=1200x600'); // optional
driver = webdriver.Chrome(options=op)
"""