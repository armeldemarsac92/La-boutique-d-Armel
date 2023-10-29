import requests
import json

# read credentials.json file
with open('../Assets/Data/credentials.json') as f:
    cred = json.load(f)
    client_id = cred['client_id']
    client_secret = cred['client_secret']
redirect_uri = "https://oauthdebugger.com/debug"

# Send the user to the authorization page to get an authorization code
authorization_url = f"https://raindrop.io/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
print(f"Go to the following URL and grant access to your Raindrop.io account: {authorization_url}")
authorization_code = input("Enter the authorization code from the redirect URL: ")

# Exchange the authorization code for an access token
token_url = "https://raindrop.io/oauth/access_token"
response = requests.post(token_url, data={
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri,
    "code": authorization_code,
})
print(response.json())
access_token = response.json()["access_token"]
# Save the access token to credentials.json
with open('../Assets/Data/credentials.json', 'w') as f:
    json.dump({"api_key": "Bearer " + access_token,
               "client_secret": client_secret,
               "client_id": client_id}, f)
print(f"Your Raindrop.io API key is: {access_token}, it has been saved to credentials.json")
