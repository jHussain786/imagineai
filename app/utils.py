import requests
import threading
import os
import time
import json

from openai import OpenAI


class NextLegAPI:
    def __init__(self, auth_token):
        self.imagine_url = "https://api.thenextleg.io/v2/imagine"
        self.get_message_url = "https://api.thenextleg.io/v2/message/"
        self.button_press_url = "https://api.thenextleg.io/v2/button/"

        self.headers = {
            'Authorization': 'Bearer 47d532f2-5962-4318-bd35-983dcc455e06' ,
            'Content-Type': 'application/json'
        }

    def get_images(self, datas):
        response_datas = []
        threads = []

        for prompt in datas['prompts']:
            thread = threading.Thread(target=self.request_midjourney, args=(prompt, datas["imageSize"], response_datas))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        urls = [image_urls['response']['imageUrls'] for image_urls in response_datas]
        response_datas = [url for sublist in urls for url in sublist]

        return response_datas

    def request_midjourney(self, prompt, image_size, response_datas):
        payload = json.dumps({
            "msg": prompt + " --ar " + image_size,
            "ref": "",
            "webhookOverride": "",
            "ignorePrefilter": "false"
        })

        response = requests.request("POST", self.imagine_url, headers=self.headers, data=payload)
        returned_response = self.get_message(response.json()['messageId'])
        response_datas.append(returned_response)

    def get_message(self, message_id):
        message_url = self.get_message_url + message_id + '?expireMins=2'
        response = requests.request("GET", message_url, headers=self.headers)
        while int(response.json()['progress']) < 100:
            time.sleep(10)
            response = requests.request("GET", message_url, headers=self.headers)
        return response.json()
    
class OpenAIapi:
    def __init__(self):
        self.client = OpenAI(api_key="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")

    def get_images(self, input):
        urls = []
        threads = []

        for _ in range(input['num_images']):
            thread = threading.Thread(target=self.request_dall_e, args=(input['prompt'], urls))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return urls
    
    def request_dall_e(self, prompt, urls):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            quality="standard"
        )
        url = response.data[0].url
        urls.append(url)
    

        