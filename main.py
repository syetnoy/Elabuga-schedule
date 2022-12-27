from flask import Flask, render_template
from sqlite3 import connect
from datetime import datetime
from static.classes import *


app = Flask(__name__)

data_bus_stations: list[BusStation] = list()
data_intervals: list[Interval] = list()
data_buses: list[Bus] = list()
data_routes: list[Route] = list()


def load_bus_stations():
    global data_bus_stations
    connection = connect('data/DB.sqlite')
    cursor = connection.cursor()

    for station in cursor.execute("""SELECT * FROM `BusStations`""").fetchall():
        obj = BusStation(*station)
        data_bus_stations.append(obj)
    connection.close()
    print(f'load bus stations - {len(data_bus_stations)}')


def load_buses():
    global data_buses
    connection = connect('data/DB.sqlite')
    cursor = connection.cursor()

    for bus in cursor.execute("""SELECT * FROM `Buses`""").fetchall():
        obj = Bus(*bus)
        data_buses.append(obj)
    connection.close()
    print(f'load buses - {len(data_buses)}')


def load_intervals():
    global data_intervals
    connection = connect('data/DB.sqlite')
    cursor = connection.cursor()

    for interval in cursor.execute("""SELECT * FROM `Intervals`""").fetchall():
        obj = Interval(*interval)
        data_intervals.append(obj)
    connection.close()
    print(f'load intervals - {len(data_intervals)}')


def load_routes():
    from json import load
    global data_routes

    with open('data/buses.json', mode='r', encoding='utf-8') as file:
        temp = load(file)
    for route in temp:
        obj = Route(route, temp[route]['stations'], temp[route]['full_round'])
        data_routes.append(obj)
    print(f'load routes - {len(data_routes)}')


@app.route('/')
def path():
    return render_template('index.html')


@app.route('/bus_stations')
def path_buses():
    return render_template('bus_stations.html', stations=data_bus_stations)


@app.route('/bus_station/<string:params>')
def path_the_bus_station(params: str):
    params = create_response(params)
    params['ID'] = int(params['ID'])

    return render_template('bus_station.html',
                           station=data_bus_stations[params['ID'] - 1],
                           buses=get_routes_of_station(params['ID']),
                           closely_routes=get_closely_routes(params['ID']))


@app.route('/<path:other>')
def path_other(other: str):
    return render_template('index.html')


def get_routes_of_station(station: int) -> list[str]:
    routes: list[str] = list()
    for route in data_routes:
        if station in route.stations:
            routes.append(route.number)
    return routes


# def get_closely_routes(station: int, count_routes: int = 10) -> list:
#     buses: list[Bus] = list()
#     now = get_time()
#     for bus in data_buses:
#         temp = bus.start
#         while temp + 40 < now:
#             temp += 80
#         buses.append(bus)
#     buses.sort(key=lambda x: x.start)
#     for i in buses:
#         print(i.__dict__)
#     return buses[:count_routes]


def get_closely_routes(station: int, count_routes: int = 10) -> list:
    def get_time_route_to_station(route_: int, station_: int) -> int:
        from itertools import cycle
        count = 0
        stations = cycle(find_obj_route(route_).stations)
        for station_in_route in stations:
            station_in_route1 = station_in_route
            station_in_route2 = next(stations)
            if station_in_route == station_:
                break
            count += find_obj_interval(st1=station_in_route1, st2=station_in_route2)
        return count

    closely_routes: list[CloselyRoute] = list()

    for bus in data_buses:
        obj = CloselyRoute(bus.route_number, get_time_route_to_station(bus.route_number, station))
        closely_routes.append(obj)

    closely_routes.sort(key=lambda x: x.minute)
    for i in closely_routes: print(i.__dict__)
    return closely_routes[:count_routes]


def create_response(params: str):
    result = dict()
    params = params.split('&')
    for param in params:
        item = param.split('=')
        result[item[0]] = item[1]
    return result


def get_time() -> int:
    d = datetime.now()
    return d.hour * 60 + d.minute


def find_obj_interval(inter=0, st1=0, st2=0) -> Interval:
    for obj in data_intervals:
        if st1 and st2:
            if obj.station1 == st1 and obj.station2 == st2:
                return obj.interval
        if st1 and inter:
            if obj.station1 == st1 and obj.interval == inter:
                return obj


def find_obj_route(number: str) -> Route:
    for obj in data_routes:
        if obj.number == number:
            return obj


if __name__ == '__main__':
    load_bus_stations()
    load_buses()
    load_intervals()
    load_routes()

    app.run(host='127.0.0.1', port=5000)
