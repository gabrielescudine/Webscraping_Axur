# Axur AI Intern - Gabriel Escudine
This repository contains the solution to a technical challenge for the AI Intern position at Axur.

## Installation
1. Clone this repository to your local machine:
```bash
git clone https://github.com/gabrielescudine/Webscraping_Axur
cd Webscraping_Axur
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate # On Linux, use source venv/bin/activate
```
3. Install the required dependencies using the requirements.txt:
```bash
pip install -r requirements.txt
```
4. Create a .env file to insert your Token Key. Don't forget this step, otherwise the script won't run. In the .env file, follow the syntax below:
```bash
TOKEN_KEY = {"Your Token Key Here"}
```

## How to use
To run the ```script.py```, certify that you have installed all the necessary dependencies and execute the following command:
```bash
python script.py
```
After completing all the necessary setup, the script should be ready to run. First, it scrapes the target webpage and retrieves the desired image. Then, the image is encoded in base64 and sent to the model API using a specific prompt to generate a detailed caption.

The model returns a JSON response containing the image description. Finally, this response is submitted — without any modifications — to the evaluation API provided as part of the challenge.