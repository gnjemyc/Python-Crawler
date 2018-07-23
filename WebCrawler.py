from flask import Flask,jsonify,request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
stores = [{
    'name': 'Elton\'s first store',
    'items': [{'name':'my item 1', 'price': 30 }],
    },
    {
    'name': 'Elton\'s second store',
    'items': [{'name':'my item 2', 'price': 15 }],
    },
]

#get 
@app.route('/movie')
def get_movie():
    webSite = 'https://movies.yahoo.com.tw/movie_thisweek.html'

    result = '本周新片：\n'

    while webSite:
        resp = requests.get(webSite)
        soup = BeautifulSoup(resp.text, 'html.parser')
        thisWeekMoviePage = soup.find_all('div','release_info')
        #print(thisWeekMoviePage)

        for a in thisWeekMoviePage:
            movieName = a.find_all('a','gabtn')
            movieReleaseTime = a.find('div','release_movie_time').text
            movieInfo = a.find('span','jq_text_overflow_180 jq_text_overflow_href_list').text.strip()
            if(a.find('a','btn_s_vedio').get('href')):
                moviePreview = a.find('a','btn_s_vedio').get('href')
            else :
                moviePreview = ''
            result +='******************\n'
            result += ('片名： ' + movieName[0].text.strip() + ' - ' + movieName[1].text.strip() + ' || ' + movieReleaseTime + ' || 預告片：' + moviePreview + ' || 簡介：' + movieInfo + '\n\n')

        nextPage = soup.find('li','nexttxt')

        try:
            if nextPage.find('a')['href'] :
                webSite = nextPage.find('a')['href']
        except TypeError:
            break 

    postdata = { "text":result }

    r = requests.post("https://hooks.slack.com/services/xxxxxxxxxxxxxxxx",headers = {"content-type": "application/json"},json=postdata)
    print(r)
    
    return jsonify ([{'success': 'true','result':'ok'}])
#get /store
@app.route('/store')
def get_stores():
    return jsonify(stores)
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
        return jsonify ({'message': 'store not found'})
#get /store/<name>/item data: {name :}
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify( {'items':store['items'] } )
    return jsonify ({'message':'store not found'})
#post /store data: {name :}
@app.route('/store' , methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)
#post /store/<name> data: {name :}
@app.route('/store/<string:name>/item' , methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
        store['items'].append(new_item)
        return jsonify(new_item)

app.run(port=5000, debug=True)