from flask import json, Response, render_template, Flask
from flask_restful import Api, Resource

import requests
import sqlite3 as sq

app = Flask(__name__)
api = Api()
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3fd71f50684a58f9c310b7a4e5df243f'


def get_list_db(data: list):
    new_list = []
    for i in data:
        for k in i:
            new_list.append(k)
    return new_list


with sq.connect('City.sqlite3') as con:
    cur = con.cursor()
    cur.execute('SELECT kz_name FROM City_name')
    kz_text = get_list_db(cur.fetchall())
    cur.execute('SELECT ru_name FROM City_name')
    ru_text = get_list_db(cur.fetchall())


class Main(Resource):
    def get(self, city):
        if city in kz_text:
            index = kz_text.index(city)
            city = ru_text[index]
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
            cur.execute(f'SELECT {lang}_name FROM City_name')
            data_list = get_list_db(cur.fetchall())
            json_string = json.dumps(data_list, ensure_ascii=False)
            response = Response(json_string, content_type="application/json; charset=utf-8")
        return response

    def post(self, text):
        name_city = text

        if name_city == 'x':  # Проверка равна ли строка 'x' если да, то просто возвращает все данные
            with sq.connect('City.sqlite3') as con:
                cur = con.cursor()
                cur.execute('SELECT Name FROM City_save')
                return cur.fetchall()

        with sq.connect('City.sqlite3') as con:
            cur = con.cursor()
            cur.execute('SELECT Name FROM City_save')
            data = get_list_db(cur.fetchall())

            if name_city in data:  # Проверяет, есть ли введённая строка уже в БД
                return data

            cur.execute('SELECT rowid FROM City_save')
            data_new = get_list_db(cur.fetchall())

            if len(data) <= 2:
                cur.execute(f"INSERT INTO City_save (Name) VALUES ('{name_city}')")
                con.commit()
            elif len(data) > 2:
                cur.execute(f"DELETE FROM City_save WHERE rowid = '{data_new[0]}'")
                con.commit()
                cur.execute(f"INSERT INTO City_save (Name) VALUES ('{name_city}')")
                con.commit()

            cur.execute(f"SELECT Name FROM City_save")
            data_list = get_list_db(cur.fetchall())
            return data_list

    def delete(self, text):
        city_name = text
        with sq.connect('City.sqlite3') as con:
            cur = con.cursor()
            if city_name in kz_text:
                index = kz_text.index(city_name)
                city_name = ru_text[index]
            cur.execute(f"DELETE FROM City_saveWHERE Name = '{city_name}'")
            con.commit()


class KzData(Resource):
    def post(self, text):
        name_city_kz = text

        if name_city_kz == 'x':  # Проверка равна ли строка 'x' если да, то просто возвращает все данные
            with sq.connect('City.sqlite3') as con:
                cur = con.cursor()
                cur.execute('SELECT Name FROM City_save')
                db_text = get_list_db(cur.fetchall())
                new_list = []
                for i in db_text:
                    index = ru_text.index(i)
                    new_text = kz_text[index]
                    new_list.append(new_text)
                return new_list
        with sq.connect('City.sqlite3') as con:
            cur = con.cursor()
            cur.execute('SELECT Name FROM City_save')
            db_text = get_list_db(cur.fetchall())
            cur.execute('SELECT rowid FROM City_save')
            rowid = get_list_db(cur.fetchall())

            index = kz_text.index(name_city_kz)
            name_city_ru = ru_text[index]

            if name_city_ru in db_text:  # Проверяет, есть ли введённая строка уже в БД
                return db_text

            if len(db_text) <= 2:
                cur.execute(f"""INSERT INTO City_save (Name) VALUES ('{name_city_ru}')""")
                con.commit()
            elif len(db_text) > 2:
                cur.execute(f"DELETE FROM City_save WHERE rowid = '{rowid[0]}';")
                con.commit()
                cur.execute(f"""INSERT INTO City_save (Name) VALUES ('{name_city_ru}')""")
                con.commit()

            cur.execute(f"""SELECT Name FROM City_save""")
            data_list = get_list_db(cur.fetchall())
            new_list = []
            for i in data_list:
                index = ru_text.index(i)
                name_city_kz = kz_text[index]
                new_list.append(name_city_kz)
            return new_list


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/indexkz.html')
def indexkz():
    return render_template('indexkz.html')

api.add_resource(Main, '/api/main/<string:city>')
api.add_resource(WorkDataBase, '/api/cities/<string:text>')
api.add_resource(KzData, '/api/cities/kz/<string:text>')
app.config['JSON_AS_UTF-8'] = False
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=3000)
