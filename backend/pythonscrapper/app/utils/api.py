import requests as request
import json


class Api:

    def __init__(self, site, proxy):
        self.site = site
        self.proxy = {
            "https": proxy
        }

        try:
            # Pass self.proxy as the proxies argument, not proxy directly
            response = request.get(site, proxies=self.proxy, verify=False)
            # Convert cookies to a dictionary
            self.cookies = request.utils.dict_from_cookiejar(response.cookies)
            print('api initiated')

        except Exception as e:
            print(f"error connecting to the website: {e}")




    def call(self, api_endpoint):
        print('calling...')
        url = self.site + api_endpoint
        # Use the cookies dictionary, not the JSON string
        response = request.get(url, proxies=self.proxy, verify=False, cookies=self.cookies)
        response_json = response.json()
        return response_json
