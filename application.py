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
from gremlin_python.structure.io import graphsonV3d0
from flask import Flask

import json
    
graph = Graph()
connection = DriverRemoteConnection('ws://10.1.0.4:8182/gremlin', 'g')
# The connection should be closed on shut down to close open connections with connection.close()
g = graph.traversal().withRemote(connection)
# Reuse 'g' across the application
writer = graphsonV3d0.GraphSONWriter()


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
    try:
        #fetch product vertex with Product Id and Product Name properties. limit rows to 5
        products = g.V().hasLabel('Product').limit(5).valueMap('productID','productName').toList()
        return json.dumps(products)
    except Exception as e:
        return str(e)

@app.route('/prodSup')
def get_productSup():
    try:
        #fetch  Product Id, Product Name and related supplier id and supplier Name properties. limit rows to 5
        productSup = writer.writeObject(g.V().hasLabel('Product').limit(5).as_('p').in_().hasLabel('Supplier').as_('s').select('p','s').by('productID','productName').by('supplierID','companyName'))
        return productSup
    except Exception as e:
        return str(e)

@app.route('/prodCat')
def get_productCat():
    try:
        #fetch  Product Id, Product Name and related supplier id and supplier Name properties. limit rows to 5
        productCat = writer.writeObject(g.V().hasLabel('Product').limit(5).as_('p').out().hasLabel('Category').as_('c').select('p','c').by('productID','productName').by('categoryID','categoryName'))
        return productCat
    except Exception as e:
        return str(e)
