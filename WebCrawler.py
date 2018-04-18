import requests
from bs4 import BeautifulSoup


def main():
    resp = requests.get('https://movies.yahoo.com.tw/movie_thisweek.html')
    soup = BeautifulSoup(resp.text, 'html.parser')
    thisWeekNewMovie = soup.find_all('a',{'data-ga' : "['本週新片','本週新片_本週新片第1頁','圍雞總動員']"})
    #print(thisWeekNewMovie)
    for a in thisWeekNewMovie:
        if a.text and not a.text.isspace() :
            print(a.text.strip(),end=",")

if __name__ == '__main__':
    main()