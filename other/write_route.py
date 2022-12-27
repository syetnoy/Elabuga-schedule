from sqlite3 import connect
from json import load


connection = connect('../data/DB.sqlite')
cursor = connection.cursor()

with open('../data/buses.json', mode='r', encoding='utf-8') as file:
    file = load(file)

for station in file['1']['stations']:
    print(cursor.execute(f"""SELECT `Title` FROM `BusStations` WHERE `ID` = {station}""").fetchall()[0][0])
