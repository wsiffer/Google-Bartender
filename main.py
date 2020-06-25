from flask import Flask, request, Response
from bartender import Bartender
from drinks import drink_list, drink_options

#bartender = Bartender()
bartender.buildMenu(drink_list, drink_options)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.data)
    print(menuItem.name)
    return Response(status=200)

