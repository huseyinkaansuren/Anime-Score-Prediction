import pandas as pd
import numpy as np
import requests
import requests as rq
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def pull_data():
    BeautifulSoup.attrs = {"data-id": True}
    # Main Site Connection
    url = "https://myanimelist.net/topanime.php?limit="
    url_list = []

    url_page = 0
    for pnum in range(0, 20):# 20
        temp_url = url + str(url_page)
        url_list.append(temp_url)
        url_page = url_page + 50

    print(rq.get(url))
    animeList = []

    # MyAnimeList Connection
    for i in range(len(url_list)):  # len(url_list)
        req = rq.get(url_list[i])
        soup = BeautifulSoup(req.content, "html.parser")
        for j in range(0, 50):  # 0, 50
            anime = soup.find_all("tr", class_="ranking-list")[j]
            animeList.append(anime)

    print(len(animeList))

    df = pd.DataFrame(columns=["Name", "Studio", "Genre", "Score", "Ranked", "Popularity", "Members"])
    for i in range(len(animeList)):
        try:
            anime_url = animeList[i].find("h3").a["href"]  # anime link
            # print(anime_url)
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            # anime_req = rq.get(anime_url)
            session.mount("https://", adapter)
            anime_req = session.get(anime_url)
            animesoup = BeautifulSoup(anime_req.content, "html.parser")

            anime_name = animesoup.find("h1", class_="title-name").text
            print(anime_name)  # get anime name

            # Anime Information
            anime_info = animesoup.find_all("div", class_="spaceit_pad")

            # anime_epi = int(anime_info[3].find_all()[0].next_sibling[3:])#episode
            # print(anime_epi)

            studio_div = animesoup.find("span", text="Studios:").parent
            anime_stu = str(studio_div.find("a").text)  # Studio
            # print(anime_stu)

            anime_genre = animesoup.find("span", itemprop="genre").text

            # print(anime_genre)
            # Anime Statistics
            anime_score = float(animesoup.find("span", itemprop="ratingValue").text)
            # print(anime_score)

            anime_rank_temp = animesoup.find("div", attrs={"data-id": "info2"}).text[12:]
            anime_rank = anime_rank_temp[:-109]
            print(anime_rank)

            anime_pop = int(animesoup.find("span", text="Popularity:").next_sibling.text[4:])
            # print(anime_pop)

            anime_memb = int(animesoup.find("span", text="Members:").next_sibling.replace(",", ""))
            # print(anime_memb)

            anime_row = [anime_name, anime_stu, anime_genre, anime_score, anime_rank, anime_memb, anime_pop]
            df.loc[len(df)] = anime_row
        except AttributeError:
            pass

        df.to_csv("Data.csv", index=False)
