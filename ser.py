
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route, run
from nlp import nlp
import json
@route('/')
def hello_world():
    return 'Hello from Bott!'

@route('/ahmed3lanamedaddo')
def hello():
    return json.dumps({"data": [
        {"action": "JasperSitting", "actor": "Jasper", "obj": "chair"},
        {"action": "JasperWalking", "actor": "Jasper", "obj": ""},
        {"action": "PearlWalking", "actor": "Pearl", "obj": ""},
        {"action": "JasperJump", "actor": "Jasper", "obj": ""},
        # {"action": "PearlWalking", "actor": "Pearl", "obj": ""},
        # {"action": "PearlWalking", "actor": "Pearl", "obj": ""},
        # {"action": "PearlWalking", "actor": "Pearl", "obj": ""},
        # {"action": "PearlIdle", "actor": "Pearl", "obj": ""},
        # {"action": "PearlStandToSit", "actor": "Pearl", "obj": ""},
        # {"action": "JasperJump", "actor": "Jasper", "obj": ""},
        # {"action": "Jasper1StandToSit", "actor": "Jasper1", "obj": ""},
        # {"action": "PearlIdle", "actor": "Pearl", "obj": ""},
        # {"action": "JasperIdle", "actor": "Jasper", "obj": ""},
        # {"action": "Jasper1Idle", "actor": "Jasper1", "obj": ""},

    ]})


@route('/init')
def hi():
    # return json.dumps({"objects": ["Jasper"], "scene": ["street"]})
    return json.dumps({"characters": ["Jasper",  "Pearl"], "objects": ["chair"], "scene": ["street"]})

@route('/magdi')
def ser():
    return "hi magdi"


application = default_app()
