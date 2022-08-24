"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User ,People ,FavPeople,FavPlanetas,Planetas
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

    """ Ruta personajes , con serializados que encuentra a todos los personajes """
@app.route('/people',methods=['GET'])
def getPeople():
    all_people = People.query.all()
    serializados = list(map(lambda people: people.serialize(), all_people))
    return jsonify({
        "mensaje" :"Hola personaje !",
        "people" :serializados
    })
    """ Ruta Personaje por ID ! los encuentra por su ID usando una condicion si no hay un id registrado regresa un error"""
@app.route('/people/<int:people_id>',methods=['GET'])
def getPeopleid(people_id):
    one = People.query.filter_by(uid=people_id).first()
    if(one):
        return jsonify({
            "id ": people_id,
            "mensaje" : "la persona es",
            "people" : one.serialize()
        }),200
    else:
        return jsonify({
            "id ": people_id,
            "mensaje" : "not found"
            
        }),404   
    """Ruta favoritos personajes , con esta ruta agregamos favoritos a nuestra tabla FavPeople con el id del people creado"""    
@app.route('/favorite/people/<int:people_id>',methods=['POST'])
def peopleFv(people_id):
    body = request.get_json()
    Favorite= FavPeople(user=body["email"],people=people_id)
    db.session.add(Favorite)
    db.session.commit()
    return "Nuevo Favorito Agregado"






    """Ruta planeta , mostramos todos los planetas"""
@app.route('/planets',methods=['GET'])
def getPlanet():
    all_planetas = Planetas.query.all()
    serializados = list(map(lambda planetas: planetas.serialize(), all_planetas))
    return jsonify({
        "mensaje" :"Hola planeta !",
        "planeta":serializados
        
    }),200

@app.route('/planets/<int:planet_id>',methods=['GET'])
def getPlanetid(planet_id):
    planeta = Planetas.query.filter_by(uid=planet_id).first()
    if(planeta):
        return jsonify({
            "id ": planet_id,
            "mensaje" : "El planeta es",
            "planeta":planeta.serialize()
        }),200
    else:
        return jsonify({
            "id ": planet_id,
            "mensaje" : "not found"
            
        }),404   
    
""" ruta favorite de los planeta agregamos planetas a la tabla favplanetas con el id planeta"""   
@app.route('/favorite/planets/<int:planet_id>',methods=['POST'])
def planetsFv(planet_id):
    body = request.get_json()
    one=Planetas.query.get(planet_id)
    oneSerializado =one.serialize()
    planetaFv= FavPlanetas(user=body["email"],planetas=oneSerializado['name'])
    db.session.add(planetaFv)
    db.session.commit()
    return "Nuevo Planeta Favorito Agregado"











@app.route('/favorite/planet/<int:planet_id>',methods=['DELETE'])
def deletPlanet(planet_id):
    return jsonify({
        id : planet_id,
        "mensaje" : "planeta eliminado",
        "delete" : []
    })
@app.route('/favorite/people/<int:people_id>',methods=['DELETE'])
def deletPeople(people_id):
    return jsonify({
        id : people_id,
        "mensaje" : "people eliminado",
        "delete" : []
    })

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
