from flask import json, Response, render_template, Flask
from flask_restful import Api, Resource

import requests
import sqlite3 as sq

app = Flask(__name__)
api = Api()
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3fd71f50684a58f9c310b7a4e5df243f'

class Main(Resource):
    def get(self, city):
        res = requests.get(url.format(city)).json()
        try:
            city_info = {
                'city': res['name'],                       # Название города 
                'temp': res['main']['temp'],               # Температура в городе
                'temp_feels': res['main']['feels_like'],   # Температура по ощущениям
                'icon': res['weather'][0]['icon'],        # Скорость ветра (вроде м/c)
            }
        except KeyError:
            return 'Incorect name'    #Если неверное имя города, то возвращает эту строку 
        return city_info

class City(Resource):
    def get(self, lang):
        with sq.connect('City.sqlite3') as con:
            cur = con.cursor()
            cur.execute(f'''SELECT {lang}_name
                        FROM City_name
                                    ''')
            data_list = get_list_db(cur.fetchall())
            json_string = json.dumps(data_list,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
        return response



def get_list_db(data: list):
    new_list = []
    for i in data:
        for k in i:
            new_list.append(k)
    return new_list 


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(Main, '/api/main/<string:city>')
api.add_resource(City, '/api/cities/<string:lang>')
app.config['JSON_AS_UTF-8'] = False
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=3000)