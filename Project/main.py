from flask import render_template, Flask, jsonify
from flask_restful import Api, Resource
import requests
from function import *

app = Flask(__name__)
api = Api()
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3fd71f50684a58f9c310b7a4e5df243f'

class WorkDataBase(Resource):
    def get(self, text):
        data_list = select(f'{text}_name', 'City_name')
        data_list = get_list_db(data_list)
        return utf8(data_list)
    
    def post(self, text):
        if len(text) == 1:
            data = select('Name', 'City_save', True)
            match text:
                case 'r':
                    return utf8(data)
                case 'k':
                    some_list = []
                    for i in data:
                        mew = trans_city(i, 'kz')
                        some_list.append(mew)
                    return utf8(some_list)     
                
        elif len(text) != 1:
            data = select('Name', 'City_save', True)
            text_ru = trans_city(text[:-1], 'ru')
            if text_ru in data:
                return utf8(data)
            rowid = select('rowid', 'City_save', True)
            if len(data) < 3:
                insert(text_ru)
            else:
                delete(rowid[0], 'rowid')
                insert(text_ru)
            match text[-1]:
                case 'r':
                    return utf8(select('Name', 'City_save', True))
                case 'k':
                    mew = select('Name', 'City_save', True)
                    new_list = []
                    for i in mew:
                        new_list.append(trans_city(i, 'kz'))
                    return utf8(new_list)
                
    def delete(self, text):
        text = trans_city(text[:-1], 'ru')
        delete(text, 'Name')
        return None

@app.route('/api/text/<string:lang>')
def get_text(lang):
    data = select(lang, 'lang_text', True)
    json_data = {
        "title": data[5],
        "city-has-already": data[6],
        "enter-city": data[0],
        "Kazakhstan": data[2],
        "feels": data[4],
        "locations": data[3],
        "documentation": data[1]
    }
    return jsonify(json_data)

@app.route('/api/weather/<string:city>')
def get_weather(city):
    city = trans_city(city, 'ru')
    res = requests.get(url.format(city)).json()
    city_info = {
        'city': res['name'],
        'temp': res['main']['temp'],
        'temp_feels': res['main']['feels_like'],
        'icon': res['weather'][0]['icon'],
    }
    return city_info


@app.route('/')
def index():
    return render_template('index.html')
# @app.route('/indexkz.html')
# def indexkz():
#     return render_template('indexkz.html')

api.add_resource(WorkDataBase, '/api/db/<string:text>')
app.config['JSON_AS_UTF-8'] = False
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=3000)
