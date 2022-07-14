from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
import pandas as pd
import datetime
import holidays
import country_converter as coco

app = Flask(__name__)
api = Api(app)

# body parser
input_args = reqparse.RequestParser()
input_args.add_argument("country", type=str, required=True, help="field is compulsory")
input_args.add_argument("state", type=str)
input_args.add_argument("start_date", type=str, required=True, help="field is compulsory")
input_args.add_argument("end_date", type=str, required=True, help="field is compulsory")


# body parser
class Inputs(Resource):
    def post(self):
        args = input_args.parse_args()
        country = args['country']
        state = args['state']
        start_date = args['start_date']
        end_date = args['end_date']

        start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y')
        yrs = [start_date.year, end_date.year]

        iso2_name = coco.convert(names=country, to='ISO2')

        if state is not None:
            state = state.upper()

        country_obj = holidays.country_holidays(iso2_name, subdiv=state, years=yrs)

        range_of_dates = pd.date_range(start=start_date, end=end_date).to_pydatetime()
        data = [{i.strftime("%d-%m-%Y"): country_obj.get(i).lower()} for i in range_of_dates if (country_obj.get(i))]

        return jsonify(data)


api.add_resource(Inputs, '/inputs')


@app.route('/')
def index():
    msg = {
        "message": "Server Works!"
    }
    return msg


# query parameters
@app.route('/inp', methods=['POST', 'GET'])
def tell_holidays():
    country = request.args.get('country', None)
    state = request.args.get('state', None)
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y')
    yrs = [start_date.year, end_date.year]

    iso2_name = coco.convert(names=country, to='ISO2')

    if state is not None:
        state = state.upper()

    country_obj = holidays.country_holidays(iso2_name, subdiv=state, years=yrs)

    range_of_dates = pd.date_range(start=start_date, end=end_date).to_pydatetime()
    data = [{i.strftime("%d-%m-%Y"): country_obj.get(i).lower()} for i in range_of_dates if (country_obj.get(i))]

    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
