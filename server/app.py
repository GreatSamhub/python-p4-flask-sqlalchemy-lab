#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if not animal:
        return make_response('', 404)
    response_data = f'''
        <ul> 
            <li>ID: {animal.id}</li>
            <li>Name: {animal.name}</li>   
            <li>Species: {animal.species}</li>
            <li>Zookeeper: {animal.zookeeper.name}</li>
            <li>Enclosure: {animal.enclosure.environment}</li>
        </ul>
    '''
    return response_data

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if not zookeeper:
        return make_response('', 404)
    response_data = f'''
        <ul>  
            <li>ID: {zookeeper.id}</li>
            <li>Name: {zookeeper.name}</li>  
            <li>Birthday: {zookeeper.birthday}</li>
            <li>Animals:
                <ul>
                    {"".join(f"<li>{animal.name} - {animal.species}</li>" for animal in zookeeper.animals)}
                </ul>
            </li>
        </ul>
    '''
    return response_data

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if not enclosure:
        return make_response('', 404)
    response_data = f'''
        <ul>    
            <li>ID: {enclosure.id}</li>
            <li>Environment: {enclosure.environment}</li>
            <li>Open to visitors: {enclosure.open_to_visitors}</li>
            <li>Animals:
                <ul>
                    {"".join(f"<li>{animal.name} - {animal.species}</li>" for animal in enclosure.animals)}
                </ul>
            </li>
        </ul>
    '''
    return response_data


if __name__ == '__main__':
    app.run(port=5555, debug=True)
