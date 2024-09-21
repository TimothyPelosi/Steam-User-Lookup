import json as js
import requests as rq
from bs4 import BeautifulSoup
import re

# Get and return the API key from the user.
def setAPIKey():
    APIKey = input("Please enter your Steam API Key: ")
    print(f"Your API key is: " + APIKey)

    return APIKey

# Get and return steam community URL from user.
def getURL():
    communityURL = input("Please enter the steam community url: ")

    return communityURL

# Parse the given URL and return the 64-bit steamID.
def parseURL(communityURL):
    # Take in the given URL, scrape HTML and parse it, and find all instances of the word "script".
    userURL = rq.get(communityURL)
    soup = BeautifulSoup(userURL.content, 'html.parser')
    scripts = soup.find_all('script')
    steamID = []

    for script in scripts:
        # If the variable g_rgProfileData is in the script.
        if 'g_rgProfileData' in script.text:
            # Use re to find the steamid.
            steamID.extend(re.findall(r'\"steamid\":\"(\d+)\"', script.text))

    return steamID

# Call the steam api with the API key and the steamID64 appended to the url. 
# Return the information as list.
def getUserSummary(APIKey, steamID64):
    response = rq.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={APIKey}&steamids={steamID64}')
    data = js.loads(response.text)

    return data

def organizeUserData(userData):
    for key, value in userData.items():
        print(f"{key}: {value}")

#=========================================================================================================================================

APIKey = setAPIKey()
communityURL = getURL()

# Get and assign steamID64 to variable from first element in list. 
steamID64 = parseURL(communityURL)[0]

# Get userData and print it. 
response = getUserSummary(APIKey, steamID64)
userData = response['response']['players'][0]

print("------------------------------------------------------")
organizeUserData(userData)

print("------------------------------------------------------")
print(userData)