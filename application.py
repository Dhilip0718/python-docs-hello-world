# Gremlin imports
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from flask import Flask
import json
    
graph = Graph()
connection = DriverRemoteConnection('ws://10.1.0.4:8182/gremlin', 'g')
# The connection should be closed on shut down to close open connections with connection.close()
g = graph.traversal().withRemote(connection)
# Reuse 'g' across the application


app = Flask(__name__)

@app.route('/')
def get_productID():
    try:
        #fetch product vertex with Product Id and Product Name properties. limit rows to 5
        productId = g.V().hasLabel('Product').limit(5).valueMap('productID','productName').toList()
        response = json.dumps(productId)
        return response
    except Exception as e:
        return e

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/product')
def get_product():
    #fetch product vertex with Product Id and Product Name properties. limit rows to 5
    products = g.V().hasLabel('Product').limit(5).valueMap('productID','productName').toList()
    return str(products)

@app.route('/prodCat')
def get_productCat():
    try:
        #fetch product vertex with Product Id and Product Name properties. limit rows to 5
        productCat = g.V().hasLabel('Product').limit(5).as_('p').out().hasLabel('Category').as_('c').select('p','c').by(valueMap('productID','productName')).by(valueMap('categoryID','categoryName'))
        response = json.dumps(productCat.toList())
        return response
    except Exception as e:
        return e

@app.route('/typeOf')
def get_type():
    try:
        #fetch product vertex with Product Id and Product Name properties. limit rows to 5
        prodType = g.V().hasLabel('Product').limit(5).valueMap('productID','productName').toList()
        response = type(prodType)
        print prodType
        return response
    except Exception as e:
        return e
