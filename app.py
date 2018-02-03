from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.
#Assuming walNee.db is in your app root folder
e = create_engine ('sqlite:///walNee.db')

app = Flask(__name__)
api = Api(app)

# API
class Stores(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select * from TB_STORE")
		return {'stores': [i[1] for i in query.cursor.fetchall()]}

class CatLanes(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select * from TB_LANE")
		return {'catLanes': [i[2] for i in query.cursor.fetchall()]}

class CatProducts(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select * from TB_PRODUCT")
		# return {'catProducts': [i[2] for i in query.cursor.fetchall()]}
		return {'catProducts': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Categories(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select * from TB_CATEGORY")
		return {'categories': [i[2] for i in query.cursor.fetchall()]}

class Products(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()

		strQry = """SELECT
						distinct PROD.PRO_NAME,
						PROD.PRO_DESCRIPTION,
						STORE.STO_NAME,
						CATEGORY.CAT_NAME,
						LANE.LAN_NAME,
						LANE.LAN_NUM_NAME
						from
							TB_STORE AS STORE,
							TB_PRODUCT AS PROD,
							TB_LANE AS LANE,
							TB_CATEGORY AS CATEGORY
						WHERE
							PROD.PK_TB_PRODUCT = CATEGORY.FK_TB_PRODUCT
							AND LANE.PK_TB_LANE = PROD.FK_TB_LANE"""

		#Perform query and return JSON data
		query = conn.execute(strQry)
		result = {'products': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return result

api.add_resource(Stores, '/stores')
api.add_resource(CatLanes, '/catLanes')
api.add_resource(Categories, '/categories')
api.add_resource(Products, '/products')
api.add_resource(CatProducts, '/catProducts')

if __name__ == '__main__':
    app.run(debug=True)
