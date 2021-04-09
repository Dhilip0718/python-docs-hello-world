# Gremlin imports
# from gremlin_python import statics
# from gremlin_python.structure.graph import Graph
# from gremlin_python.process.graph_traversal import __
# from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import Cardinality
from gremlin_python.process.traversal import Column
from gremlin_python.process.traversal import Direction
from gremlin_python.process.traversal import Operator
from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import Pop
from gremlin_python.process.traversal import Scope
from gremlin_python.process.traversal import Barrier
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import WithOptions
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
        print('******************************')
        print(productId)
        
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
        productCat = g.V().hasLabel('Product').limit(5).as_('p').in_().hasLabel('Supplier').as_('s').where(select('p','s').by('productID','productName')).toList()
        response = json.dumps(productCat)
        print(response)
        return response
    except Exception as e:
        return e

@app.route('/typeOf')
def get_type():
    try:
        #fetch product vertex with Product Id and Product Name properties. limit rows to 5
        prodType = g.V().hasLabel('Product').limit(5).valueMap('productID','productName').toList()
        response = type(prodType)
        print(prodType)
        return response
    except Exception as e:
        return e
