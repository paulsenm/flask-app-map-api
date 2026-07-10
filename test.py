from flask import Flask, request
import overpy

from poi_test import get_parks, get_intersections, add_resource_pins_db
from gps_from_pluscode import decode

app = Flask(__name__)

api = overpy.Overpass()

#http://127.0.0.1:5000/api/loc?lat=44.0521&lon=-123.0868
#http://127.0.0.1:5000/api/loc?lat=44.112861&lon=-123.135583
@app.route('/api/loc', methods=['GET'])
def get_parks_web():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    json_part = get_intersections(lat, lon)
    return json_part

#http://127.0.0.1:5000/api/pc?pc=84PR3VJP%2bJM
@app.route('/api/pc', methods=['GET'])
def gps_from_pc():
    pluscode = request.args.get('pc')
    coord_code_area = decode(pluscode)
    center_lat = coord_code_area.latitudeCenter
    center_lon = coord_code_area.longitudeCenter
    response = [center_lat, center_lon]
    
    return response

@app.route('/api/db/add-resources', methods=['GET'])
def add_resources_db():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    print('lat and lon were: ', lat, ', ', lon)
    add_resource_pins_db(lat, lon)
    return 'added'
    

@app.route('/api/dummy', methods=['GET'])
def dummy_api_call():
    return('dummy api call result')


if __name__ == '__main__':
    app.run(host='192.168.49.1')

