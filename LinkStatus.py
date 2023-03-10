import zipfile
import os
import re
import requests

# Defining different counters for link types
successLinks = 0
redirectionLinks = 0
clientErrorLinks = 0
serverErrorLinks = 0
totalLinks = 0
validLinks = 0

# Code to extract all files from a specified zip folder
with zipfile.ZipFile('test.zip', 'r') as ref:
    ref.extractall("test")


files = os.listdir("test/test/")
print(files)

os.chdir('test/test')

for file in files:
    if file.endswith('.txt') or file.endswith('.html') or file.endswith('.rtf'):
        with open(file, 'r') as f:
            contents = f.read()
            # print(contents)
            links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', contents)
            print(links)

            for link in links:
                try:
                    responses = requests.get(link)
                    if 200 <= responses.status_code < 300:
                        successLinks += 1
                        validLinks += 1
                    elif 300 <= responses.status_code < 400:
                        redirectionLinks += 1
                        validLinks += 1
                    elif 400 <= responses.status_code < 500:
                        clientErrorLinks += 1
                    elif 500 <= responses.status_code < 600:
                        serverErrorLinks += 1
                    totalLinks += 1
                except:
                    serverErrorLinks += 1

# Calculating the total link validity

print("Total link's STATUS\n============")
print(f"{successLinks} Success links")
print(f"{redirectionLinks} Redirection links")
print(f"{clientErrorLinks} Client error links")
print(f"{serverErrorLinks} Server error links")
# print(f"{validLinks} Valid links")
# print(f"{totalLinks} Total links")

linkValidity = (validLinks/totalLinks) * 100

# Printing the output as shown in the question

print(f"Total link's validity: {linkValidity:.2f}%")
