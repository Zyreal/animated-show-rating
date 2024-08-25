import requests, json
from bs4 import BeautifulSoup

# selenium stuff cause some searches do not dynamically load content
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# to activate venv use .venv\Scripts\activate
from flask import Flask

import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

@app.route('/search/<userSearch>', methods=['GET'])
def index(userSearch):
    search = userSearch
    searchCache = redis_client.hget("alias", userSearch)
    if searchCache:
        animeSearch = redis_client.hget("anime", searchCache)
        # if somehow the alias has a key but not the anime
        if animeSearch:
            return json.loads(animeSearch)
    
    searchPlus = search.replace(" ", "+")

    # MAL---------------------------------------------

    searchUrl = "https://myanimelist.net/anime.php?q=" + searchPlus + "&cat=anime"
    response = requests.get(searchUrl)
    soup = BeautifulSoup(response.content, 'html.parser')

    # get first result (first actual row is sorting)
    table = soup.find("div", {"class": "js-categories-seasonal js-block-list list"})
    firstResult = table.find_all('tr')[1]
    hoverLink = firstResult.find("a", {"class": "hoverinfo_trigger fw-b fl-l"})

    # store the actual name of the anime
    animeName = hoverLink.find('strong').get_text()
    redis_client.hset('alias', userSearch, animeName)
    animeCache = redis_client.hget('anime', animeName)
    if animeCache:
        return json.loads(animeCache)

    searchPlus = animeName.replace(" ", "+")
    searchPerc = animeName.replace(" ", "%20")

    url = hoverLink.get('href')

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    scoreMAL = soup.find("div", {"class": "score-label"}).get_text() + "/10"
    print(scoreMAL)


    # Anilist----------------------------------------------

    searchUrl = "https://anilist.co/search/anime?search=" + searchPerc
    print(searchUrl)

    options = webdriver.ChromeOptions()
    # this headless thing is broke for anilist ._. use default for now (check xvfb)
    # maybe something like --disable-extensions or running all at the same time for efficiency
    # stops the browser from appearing
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(searchUrl)

    time.sleep(2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

    link = soup.find("div", {"class" : "media-card"})
    scoreAnilist = "N/A"
    if link:
        link = link.find('a').get('href')
        link = "https://anilist.co" + link
        print(link)

        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find("div", {"class" : "cover-wrap"})
        animeImage = images.find("img")
        animeImageLink = animeImage['src']

        data = soup.find("div", {"class" : "el-tooltip data-set"})
        if data:
            scoreAnilist = data.find("div", {"class" : "value"}).get_text()
    print(scoreAnilist)

    # Livechart-------------------------------------------------------------
    
    searchUrl = "https://www.livechart.me/search?q=" + searchPlus 
    print(searchUrl)

    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    driver.get(searchUrl)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

    scoreLivechart = "N/A"
    table = soup.find("li", {"class": "grouped-list-item anime-item"})
    if table:
        rating = table.find("div", {"class" : "info"})
        if rating.find("span", {"class" : "fake-link"}):
            scoreLivechart = rating.find("span", {"class" : "fake-link"}).get_text().strip() + "/10"
    print(scoreLivechart)

    res = {"animeImage" : animeImageLink,
            "MAL" : scoreMAL, 
            "Anilist" : scoreAnilist, 
            "Livechart" : scoreLivechart,
            "name" : animeName
            }
    redis_client.hset('anime', animeName, json.dumps(res))
    return res

# if __name__ == "__main__":
#     app.run(debug=True)