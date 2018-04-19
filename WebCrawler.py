import requests
from bs4 import BeautifulSoup


def get_thisWeek_newMovies():

    webSite = 'https://movies.yahoo.com.tw/movie_thisweek.html'

    while webSite:
        resp = requests.get(webSite)
        soup = BeautifulSoup(resp.text, 'html.parser')
        thisWeekMoviePage = soup.find_all('div','release_movie_name')
        #print(thisWeekMoviePage)
        

        for a in thisWeekMoviePage:
            movieName = a.find('a')['data-ga']
            index = movieName.rfind(',')
            print('本周新片:' + movieName[index+1:-1])

        nextPage = soup.find('li','nexttxt')

        try:
            if nextPage.find('a')['href'] :
                webSite = nextPage.find('a')['href']
        except TypeError:
            break 
    
if __name__ == '__main__':
    get_thisWeek_newMovies()