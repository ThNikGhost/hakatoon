import sqlite3 as sq
from flask import Response, json

def get_list_db(data: list):
    new_list = []
    for i in data:
        for k in i:
            new_list.append(k)
    return new_list

def select(column, table, param=False):
    with sq.connect('City.sqlite3') as con:
        cur = con.cursor()
        cur.execute(f"SELECT {column} FROM {table}")
        if param == True:
            return get_list_db(cur.fetchall())
        else:
            return cur.fetchall()

def insert(value: str):
    with sq.connect('City.sqlite3') as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO City_save (Name) VALUES ('{value}')")
        con.commit()
    return None

def delete(text: str, where: str):
    with sq.connect('City.sqlite3') as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM City_save WHERE {where} = '{text}'")
        con.commit()
    return None

def trans_city(name: str, lang: str):
    if lang == 'ru':
        if name in KZ_NAME:
            index = KZ_NAME.index(name)
            name = RU_NAME[index]
    elif lang == 'kz':
        if name in RU_NAME:
            index = RU_NAME.index(name)
            name = KZ_NAME[index]
    return name

def utf8(text: str):
    json_string = json.dumps(text, ensure_ascii=False)
    response = Response(
        json_string, content_type="application/json; charset=utf-8")
    return response

KZ_NAME = select('kz_name', 'City_name', True)
RU_NAME = select('ru_name', 'City_name', True)
