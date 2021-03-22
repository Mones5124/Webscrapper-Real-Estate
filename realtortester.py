import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser
import random, sys

#line 21-22 (town) and 67-68 (budget)
#https://pypi.org/project/fake-useragent/
#antiblocking measures
from fake_useragent import UserAgent
ua = UserAgent()
User_Agent = str(ua.random) #always gets a random UserAgent
#User_Agent = random.choice(['Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36', 
#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'])
#print(User_Agent)
#sys.exit()
print()
print()

townname_ = 'Paterson'
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

"""

my_session = requests.session()
my_session.headers.update({'Accept-Encoding': 'br, gzip, deflate','Accept-Language': 'en-gb',
'Upgrade-Insecure-Requests': '1', 'User-Agent': User_Agent, 'Referer': 'https://www.google.com/'})
#recent Chome things^^

#Getting things from zumper
zumper_url = 'https://www.zumper.com/rent-research/'+townname.lower()+'-nj'
#webbrowser.open(zumper_url)
"""
"""
zumper = requests.get(zumper_url)
#print(zumper.request.headers)
#print(zumper.cookies)
#how can it have no cookies?
zcontents = zumper.text
zsoup = BeautifulSoup(zcontents, 'html.parser')

rent1, bleh = zsoup.find(class_='About_infoText__2tZYa').text.split("Median") #median 1 bed rent, splits the word after the Number when it starts to say Median
print(townname_space+" has a median rent of "+ rent1 +".") 
#"""

""" #not working right now
zumper = requests.get(zumper_url+'2-beds')
soup = BeautifulSoup(zumper.text, 'html.parser')
rent2 = soup.find(class_='About_infoText__2tZYa')#.text.split("Median") #median 2 bed rent
print(rent2)
#print(townname+" has a median rent of "+ rent2 +".") 

try:
    rent_percent,bleh = soup.find(class_='RentRanges_infoText__-xmoo').text.split("Renter")
    print(townname + " has a renter occupancy rate of "+ rent_percent)
#only try it if the information is available on the website
except:
    pass
"""
print()
#sys.exit()
#budget = int(input("What is your budget in thousands of dollars?" + "\n"))
budget = 900
budget = "price-na-" + str(budget*1000)
type_ = 'type-multi-family-home/'
realtor_url = 'https://www.realtor.com/realestateandhomes-search/'+townname+'_NJ/'+str(type_)+str(budget)+'/sby-6'
#'/show-newest-listings'

#used when the bottom doessn't work
"""
rdriver = webdriver.Chrome() 
rdriver.get(realtor_url)
rdriver.implicitly_wait(5)
#finding all the properties
properties = rdriver.find_elements_by_class_name('component_property-card')#.findall('li')
#waiting
rdriver.implicitly_wait(15)
input('Press ENTER to close the automated browser') 
rdriver.quit()
"""
#webbrowser.open(realtor_url)
#used when the top doesn't work 
my_session = requests.session()
my_session.headers.update({'Accept-Encoding': 'gzip','Accept-Language': 'en-US,en;q=0.9,es;q=0.8','Upgrade-Insecure-Requests': '1', 
'User-Agent': User_Agent, 
'Referer': 'https://www.realtor.com/realestateandhomes-search/'})
realtor = my_session.get(realtor_url)
#must be a GET request
#webbrowser.open(realtor_url)
html_soup = BeautifulSoup(realtor.text, 'html.parser')
#prop = html_soup.find(class_="property-list")
properties = html_soup.findAll(class_='component_property-card')#.findall('li')
#print(properties)

try:
    t, tn = townname.split("-")
except:
    tn = townname

for prop in properties:
    if tn.capitalize() in prop.text:
        #splitting the intire string so that it can be split into variables
        before, after = prop.text.split("Multi-Family Home") #after is the important one
        #Nprint(after)
        before, after = after.split(", "+townname_space+", NJ")
        #before is the only important part now
        print()
        #print(before)
        try:
            if 'lot' in before:
                before, Address = before.split('lot')
            else:
                before, Address = before.split('bath')
                before = before + 'bath'
            #print(before)
            #https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-16.php
            price, after = before.split("bed")
            after = price[len(price)-1] + " bed and " + after #uses the last character from price
            #adding spaces and and
            price = price[:len(price)-1] #skips the last character in price
            #print(after)
            #print(len(after))
            if len(after) > 18:
                bath, sqft = after.split("bath")
                bed_bath = bath + " bath"
            else:
                bed_bath, after = after.split("bath")
                #adding a space
                bed_bath = bed_bath + " bath"
                sqft = "? sqft"

            print(price)
            print(bed_bath)
            print(sqft)
            print(Address)
            #splits by the placement of characters
        except:
            print("Something broke the code")
        #convert everything above into a pandas dataframe


        #print(prop.text)
    elif 'Advertisement' not in prop.text:
        #once it sees something not in Paterson and not an Advertisement, it stops
        #print("BROKE")
        #print(prop.text)
        break
print()
print()
print("No more properties on the market that fit those criteria available.")
print("I'm sorry for your inconvenience.")

#webbrowser.open(realtor_url)
#print(realtor.cookies)
"""
#print(realtor.cookies)
#now I thinks I'm on Chrome!!
#print(realtor.cookies)

all_properties = realtor_soup.findAll(class_="component_property-card")
print(all_properties)
for prop in all_properties:
    print(all_properties.text)
"""
