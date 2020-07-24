from flask import Flask, request, Response
from bartender import Bartender, screenItem
from drinks import drink_list, drink_options
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate

bartender = Bartender()
bartender.buildMenu(drink_list, drink_options)

app = Flask(__name__)

@app.route('/webhook/', methods=['POST'])
def respond():
    requestData = str(request.data)[1:].replace("'", "")
    print(requestData)
    print(screenItem.name)
    if (requestData == screenItem.name):
        bartender.menuContext.select()
    return Response(status=200)

