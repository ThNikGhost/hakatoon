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
        city_info = {
                'city': res['name'],
                'temp': res['main']['temp'],
                'temp_feels': res['main']['feels_like'],
                'icon': res['weather'][0]['icon'],
            }
        return city_info


class WorkDataBase(Resource):
    def get(self, text):
        lang = text
        with sq.connect('City.sqlite3') as con:
            cur = con.cursor()
            cur.execute(f'''SELECT {lang}_name
                        FROM City_name
                                    ''')
            data_list = get_list_db(cur.fetchall())
            json_string = json.dumps(data_list,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
        return response
    
    def post(self, text):
        name_city = text
        
        if text == '': # Проверка пустая ли строка, если да, то просто возвращает все данные
            with sq.connect('City.sqlite3') as con:
                cur = con.cursor()
                cur.execute('SELECT Name FROM City_save')
                return cur.fetchall()

        with sq.connect('City.sqlite3') as con:
            cur = con.cursor()
            cur.execute('SELECT Name FROM City_save')
            data = get_list_db(cur.fetchall())

            if name_city in data: # Проверяет, есть ли введённая строка уже в БД
                return data
            
            cur.execute('SELECT rowid FROM City_save')
            data_new = get_list_db(cur.fetchall())

            if len(data) <= 2:
                cur.execute(f"""INSERT INTO City_save (Name) VALUES ('{name_city}')""")
                con.commit()
            elif len(data) > 2:
                cur.execute(f"DELETE FROM City_save WHERE rowid = '{data_new[0]}';")
                con.commit()
                cur.execute(f"""INSERT INTO City_save (Name) VALUES ('{name_city}')""")
                con.commit()
            
            cur.execute(f"""SELECT Name FROM City_save""")
            data_list = get_list_db(cur.fetchall())
            return data_list



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
api.add_resource(WorkDataBase, '/api/cities/<string:text>')
app.config['JSON_AS_UTF-8'] = False
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=3000)