from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




foursquare_client_id = 'DVWXKF41ZL5PL3UI4J5HAG5STZWVKVQDNH15BXGCAQWWANFG'

foursquare_client_secret = 'U02DQOWFB4SZOJXC5A2Q1OYWSZ01LX1NBHG3NXVOWUS4V3KH'

google_api_key = 'AIzaSyDYshpZj4t1jgQaTQWCdiB_0RAdG1B85tc'

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  if request.method == "GET":
    restaurants = session.query(Restaurant).all()
    print("Restaurants: ", restaurants)
    return jsonify([resto.serialize for resto in restaurants])
  elif request.method == "POST":
    print("it's a post!")
    name = str(request.args.get('name'))
    restaurant = Restaurant(restaurant_name = str(request.args['name']))
    session.add(restaurant)
    session.commit()
    return redirect('/restaurants')
    

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  restaurant = session.query(Restaurant).filter_by(id=id).one()
  if request.method == "GET":
    return jsonify(restaurant.serialize)
  elif request.method == "DELETE":
    session.delete(restaurant)
    session.commit()
    return redirect('/restaurants')
  elif request.method == "PUT":
      pass 


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  