from flask import Flask, request, Response
from bartender import Bartender
from drinks import drink_list, drink_options
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate


bartender = Bartender()
bartender.buildMenu(drink_list, drink_options)


app = Flask(__name__)

bartender.menuContext.select()
#bartender.menuContext.select()
#bartender.menuContext.select()

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.data)

    return Response(status=200)

