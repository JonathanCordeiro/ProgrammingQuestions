# Created by Jonathan Cordeiro

import zipfile
import os
import re
import requests

# Specify directory to look in
directory = 'test.zip'

# Defining different counters for link types
successLinks = 0
redirectionLinks = 0
clientErrorLinks = 0
serverErrorLinks = 0
totalLinks = 0
validLinks = 0
validLinksList = []
invalidURLs = []

# Code to extract all files from a specified zip folder if the directory is zip
if directory.endswith('.zip'):
    with zipfile.ZipFile(directory, 'r') as ref:
        newDirectory = directory.split('.zip')[0]
        ref.extractall(newDirectory)
        files = os.listdir(f"{newDirectory}/{newDirectory}/")
        os.chdir(f'{newDirectory}/{newDirectory}')
else:
    files = os.listdir(f"{directory}")
    os.chdir(f"{directory}")

# print(files)


for file in files:
    if file.endswith('.txt') or file.endswith('.html') or file.endswith('.rtf'):
        with open(file, 'r') as f:
            contents = f.read()
            # print(contents)

            # regex pattern to find url in the file
            originalLinks = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                       contents)
            links = []
            # method to catch duplicates as some file types produce duplicates
            for link in originalLinks:
                # cutting off the string from the '\' character since I could not catch this in pattern matching
                result = link.split("\\")[0]
                if result not in links:
                    links.append(result)
            # print(links)

            for link in links:
                try:
                    responses = requests.get(link)
                    if 200 <= responses.status_code < 300:
                        successLinks += 1
                        validLinks += 1
                        validLinksList.append(link)
                    elif 300 <= responses.status_code < 400:
                        redirectionLinks += 1
                        validLinks += 1
                        validLinksList.append(link)
                    elif 400 <= responses.status_code < 500:
                        clientErrorLinks += 1
                        invalidURLs.append(link)
                    elif 500 <= responses.status_code < 600:
                        serverErrorLinks += 1
                        invalidURLs.append(link)
                    totalLinks += 1
                except:
                    serverErrorLinks += 1

# Printing the output as shown in the question
print("Total link's STATUS\n============")
print(f"{successLinks} Success links")
print(f"{redirectionLinks} Redirection links")
print(f"{clientErrorLinks} Client error links")
print(f"{serverErrorLinks} Server error links")
# print(f"{validLinks} Valid links")
# print(f"{totalLinks} Total links")

# Calculating the total link validity
linkValidity = (validLinks / totalLinks) * 100
print(f"Total link's validity: {linkValidity:.2f}%")

# Printing the valid links and invalid links
print(f"Valid links: {validLinksList}")
print(f"Invalid links: {invalidURLs}")
