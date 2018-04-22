import requests
from bs4 import BeautifulSoup


def get_thisWeek_newMovies():

    webSite = 'https://movies.yahoo.com.tw/movie_thisweek.html'

    print('本周新片：')
    while webSite:
        resp = requests.get(webSite)
        soup = BeautifulSoup(resp.text, 'html.parser')
        thisWeekMoviePage = soup.find_all('div','release_info_text')
        #print(thisWeekMoviePage)

        for a in thisWeekMoviePage:
            movieName = a.find_all('a','gabtn')
            movieReleaseTime = a.find('div','release_movie_time').text
            movieInfo = a.find('span','jq_text_overflow_180 jq_text_overflow_href_list').text.strip()
            print('片名： ' + movieName[0].text.strip() + ' - ' + movieName[1].text.strip() + ' || ' + movieReleaseTime + ' || 簡介：' + movieInfo)
            
        nextPage = soup.find('li','nexttxt')

        try:
            if nextPage.find('a')['href'] :
                webSite = nextPage.find('a')['href']
        except TypeError:
            break 
    
if __name__ == '__main__':
    get_thisWeek_newMovies() 