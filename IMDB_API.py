import imdb
import requests
from bs4 import BeautifulSoup
import re
#print(movie.keys())
#for i in movie.keys():

#print(movie['imdbID'])

def IMDB_API(name):
    moviesDB = imdb.IMDb()
    movies = moviesDB.search_movie(name)
    id = movies[0].getID()
    movie = moviesDB.get_movie(id)
    movie_id = movie['imdbID']
    url_movie = 'https://www.imdb.com/title/tt' + movie_id
    strhtml = getHtmlList(url_movie)
    current = strhtml.find_all('a', {'class': 'ipc-chip ipc-chip--on-base'})
    tmpt = ''
    for j,i in enumerate(current):
        pattern1 = r'\?keywords=(.*)&amp'
        i_1 = str(i)
        result = re.search(pattern1, i_1)
        txt = result.group(1)
        if j == 0:
            tmpt = txt
        else:
            tmpt = tmpt + ',' + txt
    return tmpt



def getHtmlList(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except:
        pass


#<a class="ipc-chip ipc-chip--on-base" href="/search/keyword/?keywords=crime-epic&amp;ref_=tt_stry_kw"><span class="ipc-chip__text" role="presentation">crime epic</span></a>
#document.querySelector("#__next > main > div > section.ipc-page-background.ipc-page-background--base.TitlePage__StyledPageBackground-wzlr49-0.dDUGgO > div > section > div > div.TitleMainBelowTheFoldGroup__TitleMainPrimaryGroup-sc-1vpywau-1.btXiqv.ipc-page-grid__item.ipc-page-grid__item--span-2 > section:nth-child(32) > div.Storyline__StorylineWrapper-sc-1b58ttw-0.iywpty > div.ipc-chip-list.Keywords__PlotKeywords-ke3vmf-0.bHzejW > a:nth-child(1)")
if __name__ == "__main__":
    tst_url = IMDB_API('The Godfather')
    print('result is',tst_url)

#strhtml = getHtmlList(tst_url)

#total = re.findall(pattern1,strhtml)

    #print(i.select)

