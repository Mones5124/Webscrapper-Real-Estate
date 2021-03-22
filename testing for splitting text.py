
#before = "$230,0009bed3bath2,614sqft"
#before = "$250,0003bed1.5bath"
#before = "$299,0005bed3bath2,178sqft"
before = "$295,0004bed2bath"
price, after = before.split("bed")
after = price[len(price)-1] + " bed and " + after #uses the last character from price
#adding spaces and and
print(after)
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

#price = before[:8] #0-8 characters
#print(price)
#beds = before[8:12] #+ " " + before[12:17]
#print(beds)
