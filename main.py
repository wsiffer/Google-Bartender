from flask import Flask, request, Response
from bartender import Bartender, screenItem
from drinks import drink_list, drink_options
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate

bartender = Bartender()
bartender.buildMenu(drink_list, drink_options)
bartender.menuContext.advance()


app = Flask(__name__)

@app.route('/webhook/', methods=['POST'])
def respond():
    requestData = str(request.data)[4:].replace("'", "")
    menuItem = str(screenItem.name)
    print('request: ' + requestData + ":")
    print(menuItem)

#    while(requestData != menuItem):
#        bartender.menuContext.advance()
#        print("REQUEST: " + requestData)
#        print("MENU: " + screenItem.name)

    return Response(status=200)

