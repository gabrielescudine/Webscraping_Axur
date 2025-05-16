# Technical Challenge for Axur AI Intern - Gabriel Escudine
# This script scrapes an image from a given URL, processes it, and sends it to a model for inference.
# I will upload this code on my GitHub repository, you can check it out at: https://github.com/gabrielescudine/Webscraping_Axur
# I'll try to explain the code as much as possible.

import os
import json
import base64
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Scraping and Model Configuration:

# URL of the website to scrape
scraping_url = "https://intern.aiaxuropenings.com/scrape/a178a7cd-3823-48e1-8045-de5dab02c1ce"

# API Inference
inference_api = "https://intern.aiaxuropenings.com/v1/chat/completions"

# API to submit the answer
submit_url = "https://intern.aiaxuropenings.com/api/submit-response"

# Token for authentication
TOKEN = os.getenv("TOKEN_KEY") # Don't forget to set your token in the .env file

if not TOKEN:
    print("Please set the TOKEN_KEY in your .env file.")
    exit()

# Model name for this task
model = "microsoft/Florence-2-large"

# Prompt for the model. This will describe a caption about the image.
PROMPT_TAG = "<DETAILED_CAPTION>"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Scrape the website to get the image URL

print(f"1. Starting to scrape the website")

html = requests.get(scraping_url)
soup = BeautifulSoup(html.content, "html.parser")

img_tag = soup.find("img")

if not img_tag or not img_tag.get("src"):
    print("Image not found in the HTML content.")
    exit()

image_url = img_tag["src"]

# 2. Decoding the image and downloading it

print(f"\n2. Processing the image")

if image_url.startswith("data:image"):
    header, encoded = image_url.split(",", 1)
    image_data = base64.b64decode(encoded)
    
    with open("scrape_image.jpg", "wb") as file:
        file.write(image_data)
    
    print(f"Image saved as 'scrape_image.jpg'")
else:
    img_response = requests.get(image_url)
    with open("scrape_image.jpg", "wb") as file:
        file.write(img_response.content)
        
    print("Image downloaded successfully.")

# 3. Sending the image to the model for inference

print(f"\n3. Sending the image to the model for inference")

with open("scrape_image.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

payload = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": PROMPT_TAG
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ]
}

response = requests.post(inference_api, headers=headers, json=payload)

if response.status_code != 200:
    print(f"Error in inference: {response.status_code} - {response.text}")
    exit()
    
result = response.json()

print("Inference completed successfully.\n")

print("Answer's model:")
print(json.dumps(result, indent=2))

# 4. Submitting caption to the response API

print(f"\n4. Submitting the caption to the response API")

submit_response = requests.post(submit_url, headers=headers, json=result)

if submit_response.status_code == 200:
    print("Response submitted successfully.")
    print("Response:", submit_response.json())
else:
    print(f"Error in submitting response: {submit_response.status_code} - {submit_response.text}")
    