from flask import Flask, request
from pytz import datetime
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError

import pytz
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://alickcam:alickcam@cluster0.cqwbq.mongodb.net/AlickCam?retryWrites=true&w=majority"
mongo = PyMongo(app)

class TankValidation(Schema):
    water_level = fields.Integer(required = True)
    tank_id = fields.String(required = True)



@app.route("/tank", methods = ["POST"])
def data_post():
    req = request.json
    water_level = req["water_level"]
    
    percentage = (water_level * -0.53) + 105.3
    tVar = datetime.datetime.now(tz=pytz.timezone('America/Jamaica'))
    tVartoString = tVar.isoformat()
    try:
        print(req)
        tankTemp = TankValidation().load(request.json)
        mongo.db.tanks.insert_one(tankTemp)
        print("Something")
        return {"success": "true","msg": "data saved in database successfully", "date": tVartoString} #no need to jsonify since its a single object. Only jsonify when a list of objects are returned

    except ValidationError as ve:
        return ve.messages, 400

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0")
