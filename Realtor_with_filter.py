import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser
import random, sys
from time import sleep as wait
import pandas as pd

#if the code keeps running, it will get copies of its self but will get a few morer from the web

#line 21-22 (town) and 67-68 (budget)
#https://pypi.org/project/fake-useragent/
#antiblocking measures
from fake_useragent import UserAgent
ua = UserAgent()
User_Agent = str(ua.random) #always gets a random UserAgent

#whenever it says pending sale, the code can't find what type of house it is.
#try to fix that^^ and also try to make it skip properties it already checked before

#townname_ = 'North Bergen'
#townname_ = 'Union City'
#townname_ = 'Jersey City'
townname_ = "Paterson"
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

print()

try:
    # finds dataframe  
    folders = "/Users/juanm./Documents/Coding/Data Science?/github/Webscrapper-Real-Estate/"
    og_filename = townname+'.csv'

    og_df = pd.read_csv(folders+og_filename)  
    # reads the already there file
    i = og_df.i.to_list()   #creates i into its own list
    #start = og_df["i"].tail(1)
    #start = len(og_df) #finds the length of the dataframe
    start = i[-1]+1
    #sys.exit()
except:
    start = 0

#global price
price = address = beds = baths = prop_taxes = ""

#Issue on line 80 where sometimes it still doesn't find the families of the house

"""Functions"""
#check the size
#go to line 118
def check_house_size(url):
    User_Agent = str(ua.random) 
    my_session.headers.update({'User-Agent': User_Agent, "previousUrl": realtor_url})
    prop_session = my_session.get(url)
    prop_soup = BeautifulSoup(prop_session.text, 'html.parser')

    #finds important house stats
    find_house_stats(prop_soup)

    #finds the description of the house
    prop_details = prop_soup.find(class_="content", attrs={"id": "content-property_details"})
    print(prop_details.text)
    try:
        for i in range (2, 4+1): #checks 2, 3 and 4 family houses
            family = str(i) + " family"
            #print(prop_details.text.lower())
            #print(prop_features[-2].text.lower())
            if family in prop_details or family in prop_features[-2].text.lower():
                #uses the lower so that it can always find it accurately
                #print(family + " house found")
                #print(prop_link)
                #print("Worked")
                return (family.capitalize())
    except:
        pass

    """
    #finds the description of the house
    prop_details = prop_soup.find(class_="desc")    #, id='component-property_details')  
    #print(prop_details)
    #sometimes, there is no description
    #print(prop_details)
    if prop_details == None:
        prop_details = "<div>N/A</div>"
    else:
        prop_details = prop_details.text.lower()


    #finds the features
    prop_features = prop_soup.findAll("div", class_="jsx-2414508836 feature-item")

    try:
        for i in range (2, 4+1): #checks 2, 3 and 4 family houses
            family = str(i) + " family"
            #print(prop_details.text.lower())
            #print(prop_features[-2].text.lower())
            if family in prop_details or family in prop_features[-2].text.lower():
                #uses the lower so that it can always find it accurately
                #print(family + " house found")
                #print(prop_link)
                #print("Worked")
                return (family.capitalize())
            #print(prop_features[-2].text)   #always the second to last
        #webbrowser.open(prop_link)
        #print(prop_soup)
        print("Webscraper got blocked")
        #copy dataframe into csv
        
        #sys.exit()
    except:
        #make_houses_dataframe()
        print(prop_features[-2].text.lower())
        print("Something broke")
    return("")
    """


#find house stats
def find_house_stats(soup):
    #finds the description of the house
    print()
    print()
    
    find_property_taxes(soup)

    #finds the price
    try:
        t_price = soup.find(class_="price")    #as long as it contains this, the code works
        #print(t_price.text) 

        #finds the address
        t_address = soup.find(class_="address")
        print(t_address.text)
    except:
        print("You have been blocked, try again in a couple of minutes")

    #finds the beds
    t_beds = soup.find(attrs={"data-label": "pc-meta-beds"})
    #finds the baths
    t_baths = soup.find(attrs={"data-label": "pc-meta-baths"})
    #print(t_beds.text, t_baths.text)

    global price, address, beds, baths
    price = address = beds = baths = ""
    #resets all of the variables
    #call the global variables because python was being stupid
    price = t_price.text
    address = t_address.text
    beds = t_beds.text
    baths = t_baths.text
    
    #print("Got the Stats")
    #I guess I could also just do everything in returns but this is probably better

def find_property_taxes(soup):
    try:
        all_findings = soup.findAll(class_="features")
        for findings in all_findings:
            try:
                global prop_taxes   #use the global variable
                prop_taxes = "N/A"
                before, splitt = (findings.text).split("Annual Tax Amount: ") #before is trash
                prop_taxes, splitt = str(splitt[:12]).split("So")   #only uses the first 10 characters for tax ammount, then only keeps the integers
                #print(prop_taxes)
                #prop_taxes = [int(i) for i in splitt.split() if i.isdigit()]     #uses list comprehension to only keep digits
                #print(prop_taxes)
            except:
                pass
            try:
                before, splitt = (findings.text).split("Net: ") #before is trash
                #print(before)
                print(splitt)
            except: 
                pass
            try:
                before, splitt = (findings.text).split("Gross: ") #before is trash
                #print(before)
                print(splitt)
            except:
                pass
    except:
        pass


#make a dataframe
def make_houses_dataframe():
    global og_df
    #global price, address, beds, baths, prop_link
    try:
        print(prop_taxes)
        temp_add_list = {"i": i, "Size": size, "Price": price, "Beds": beds, "Baths": baths, "Address": address, "Taxes": prop_taxes, "Urls": prop_link}
        try:
            og_df = og_df.append(temp_add_list, ignore_index = True)
        except:     #in case it hasn't been created yet
            #print("yes")
            og_df = pd.DataFrame(temp_add_list, index = [0])
            #since I'm not giving it a list when there hasn't been a csv file, I need to pass an index value
    except:
        print("No homes at all?")
    
    #print(temp_add_list)
    #print(og_df)

    #print(realtor_houses)
    folders = "/Users/juanm./Documents/Coding/Data Science?/github/Webscrapper-Real-Estate/"
    #filename = 'Houses_last.csv'
    og_df.to_csv(folders+townname+".csv", encoding='utf-8', index=False)

def zumper_url():
    print("Code not done")
    my_session = requests.session()
    my_session.headers.update({'Accept-Encoding': 'br, gzip, deflate','Accept-Language': 'en-gb',
    'Upgrade-Insecure-Requests': '1', 'User-Agent': User_Agent, 'Referer': 'https://www.google.com/'})
    #recent Chome things^^

    #Getting things from zumper
    zumper_url = 'https://www.zumper.com/rent-research/'+townname.lower()+'-nj'
    #webbrowser.open(zumper_url)

    #not working
    zumper = requests.get(zumper_url)
    #print(zumper.request.headers)
    #print(zumper.cookies)
    #how can it have no cookies?
    zcontents = zumper.text
    zsoup = BeautifulSoup(zcontents, 'html.parser')

    rent1, bleh = zsoup.find(class_='About_infoText__2tZYa').text.split("Median") #median 1 bed rent, splits the word after the Number when it starts to say Median
    print(townname_space+" has a median rent of "+ rent1 +".") 


#right now, the code gets blocked after 10 items

"""Actual Code"""
#sys.exit()
#budget = int(input("What is your budget in thousands of dollars?" + "\n"))
budget = 600
budget = "price-na-" + str(budget*1000)
type_ = 'type-multi-family-home/'
#extra = ""
extra = "beds-3/baths-3/"   #2 2-1 and one 1-1
#making it more likely to be a triplex

realtor_url = 'https://www.realtor.com/realestateandhomes-search/'+townname+'_NJ/'+extra+str(type_)+str(budget)+'/sby-6'
#'/show-newest-listings'
#print(realtor_url)

#webbrowser.open(realtor_url)
my_session = requests.session()
my_session.headers.update({'Accept-Encoding': 'gzip','Accept-Language': 'en-US,en;q=0.9,es;q=0.8','Upgrade-Insecure-Requests': '1', 
'User-Agent': User_Agent, 
'previousUrl': 'https://www.realtor.com/realestateandhomes-search/'})
realtor = my_session.get(realtor_url)
#must be a GET request

html_soup = BeautifulSoup(realtor.text, 'html.parser')
#prop = html_soup.find(class_="property-list")
properties = html_soup.findAll(class_='component_property-card')#.findall('li')
#print(properties)

#print(html_soup)
#check for blocking
#webbrowser.open(realtor_url)
blocktitle = html_soup.find("title")
if "Pardon Our Interruption" in blocktitle:
    print("You have been blocked, try again in a couple of minutes")
    sys.exit()

try:
    t, tn = townname.split("-")
except:
    tn = townname

#start = 0
i = 0
#print(start)
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
        

        size = (check_house_size(prop_link))  #gives the house size as a string
        #print(prop_soup)

        make_houses_dataframe()
        #wait(random.randint(0, 2))
        #wait one second to see if that allows it to work better

    elif 'Advertisement' not in prop.text:
        #once it sees something not in Paterson and not an Advertisement, it stops
        #print("BROKE")
        #print(prop.text)
        break

#make_houses_dataframe()
print()
print()
print("No more properties on the market that fit those criteria available.")
print("I'm sorry for your inconvenience.")

#try making a code so it can add "/pg-2" or "/pg-3" at the end once it can't find anymore properties
