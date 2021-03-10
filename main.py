import requests
from bs4 import BeautifulSoup
import json
import re
import os

servers = []

with open('sites.json', 'r') as fp:
    sites = json.load(fp)
    if len(sites) >= 1:
        print(f'Total Sites: {len(sites)}')

    for site in sites:
        print(site['name'])
        session = requests.Session()
        url = site['directoryIndexUrl'].replace('BASE_URL', site['baseUrl'])
        if not os.path.exists(f"data/{site['name']}/raw/{site['name']}.html"):
            response = session.get(url)
            with open(f"data/{site['name']}/raw/{site['name']}.html", "w") as fx:
                fx.write(response.text)
        with open(f"data/{site['name']}/raw/{site['name']}.html", "r") as fx:
            html = fx.read()
            soup = BeautifulSoup(html, 'html.parser')
            numPagesText = soup.find(class_="listing-summary").get_text() # Showing 1 - 24 of 926745 servers
            print(numPagesText)
            matches = re.search(r"Showing\s+(\d+)\s+-\s+(\d+)\s+of\s+(\d+)\s+servers", numPagesText).groups(0)
            if len(matches) == 3:
                perPage = 24
                totalServers = int(matches[2])
                numPages = totalServers / perPage
                print(f"Total Pages: {round(numPages)}")

                rawServers = soup.find(class_="listing").find_all(class_="column")
                for server in rawServers:
                    reviewCountElem = server.find(class_="review-count")
                    reviewCount = ""
                    if reviewCountElem:
                        reviewCount = reviewCountElem.get_text()

                    iconUrl = server.find(class_="server-icon").img['src']

                    name = server.find(class_="server-name").get_text()

                    membersOnline = server.find(class_="server-online").get_text()

                    tags = []
                    rawTagsContainer = server.find(class_="server-tags")
                    if (rawTagsContainer):
                        rawTags = rawTagsContainer.find_all(class_="tag")
                        for tag in rawTags:
                            tags.append(tag['title'])

                    serverDescElem = server.find(class_="server-description")
                    serverDescription = ""
                    if serverDescElem:
                        serverDescription = serverDescElem.get_text()

                    serverId = server.div['class'][1].replace('server-', '')
                    
                    servers.append({
                        "id": serverId,
                        "name": name,
                        "reviewCount": reviewCount,
                        "iconUrl": iconUrl,
                        "membersOnline": membersOnline,
                        "tags": tags,
                        "description": serverDescription,
                    })

                with open(f"data/{site['name']}/json/{site['name']}-1.json", "w") as fx:
                    fx.write(json.dumps(servers))
                
                for page in range(2, round(numPages)):
                    pageServers = []
                    url = site['otherDirectoryPagesUrl'].replace('BASE_URL', site['baseUrl']) % page
                    if not os.path.exists(f"data/{site['name']}/raw/{site['name']}-{page}.html"):
                        response = session.get(url)
                        with open(f"data/{site['name']}/raw/{site['name']}-{page}.html", "w") as fx:
                            fx.write(response.text)
                    with open(f"data/{site['name']}/raw/{site['name']}-{page}.html", "r") as fx:
                        html = fx.read()
                        soup = BeautifulSoup(html, 'html.parser')
                        numPagesText = soup.find(class_="listing-summary").get_text() # Showing 1 - 24 of 926745 servers
                        print(numPagesText)
                        matches = re.search(r"Showing\s+(\d+)\s+-\s+(\d+)\s+of\s+(\d+)\s+servers", numPagesText).groups(0)
                        if len(matches) == 3:
                            totalServers = int(matches[2])
                            numPages = totalServers / perPage
                            print(f"Pages Remaining: {round(numPages) - page}")

                            rawServers = soup.find(class_="listing").find_all(class_="column")
                            for server in rawServers:
                                reviewCountElem = server.find(class_="review-count")
                                reviewCount = ""
                                if reviewCountElem:
                                    reviewCount = reviewCountElem.get_text()

                                iconUrl = server.find(class_="server-icon").img['src']

                                name = server.find(class_="server-name").get_text()

                                membersOnline = server.find(class_="server-online").get_text()

                                tags = []
                                rawTagsContainer = server.find(class_="server-tags")
                                if (rawTagsContainer):
                                    rawTags = rawTagsContainer.find_all(class_="tag")
                                    for tag in rawTags:
                                        tags.append(tag['title'])

                                serverDescElem = server.find(class_="server-description")
                                serverDescription = ""
                                if serverDescElem:
                                    serverDescription = serverDescElem.get_text()

                                serverId = server.div['class'][1].replace('server-', '')
                                
                                pageServers.append({
                                    "id": serverId,
                                    "name": name,
                                    "reviewCount": reviewCount,
                                    "iconUrl": iconUrl,
                                    "membersOnline": membersOnline,
                                    "tags": tags,
                                    "description": serverDescription,
                                })

                    with open(f"data/{site['name']}/json/{site['name']}-{page}.json", "w") as fx:
                        fx.write(json.dumps(pageServers))   
                        
                    




        