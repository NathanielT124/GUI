# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 17:55:37 2022

@author: natha
"""
from flask import Flask
from hbbdata import elastic
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db  = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"
"""

@app.route('/home')
def home():
    return "Hello, this is the main page <h1>HELLO<h1>"

@app.route('/')
def index():
    return 'Hello!'

"""
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink. description}
        output.append(drink_data)
    return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}

@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink():
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message:": "That drink was yote"}
"""
@app.route('/youngs/')
def young():
    return {"name": "Cranberry Applesauce", "description": "It's a snack."}

@app.route('/elastic/youngs/<material>/<temperature>')
def youngs(material, temperature):
    # return {"name": "Cranberry Applesauce", "description": "It's more like a snack than a drink."}
    res = elastic.youngs(material, temperature);
    return {"value": float(res)}

if __name__ == "__main__":
    app.run()
