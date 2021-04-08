"""
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "test"
"""

# Gremlin imports
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from flask import Flask
    
def invoke_gremlin_connection():
    graph = Graph()
    connection = DriverRemoteConnection('ws://10.1.0.4:8182/gremlin', 'g')
    # The connection should be closed on shut down to close open connections with connection.close()
    g = graph.traversal().withRemote(connection)
    # Reuse 'g' across the application
    gcnt1 = g.V().count()
    return str(gcnt1)

app = Flask(__name__)

@app.route("/")
def hello():
    return invoke_gremlin_connection()

