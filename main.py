import bartender
from flask import Flask, request, Response
#from bartender import Bartender, screenItem
from drinks import drink_list, drink_options
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate

pete = bartender.Bartender()
pete.buildMenu(drink_list, drink_options)
#print("FIRST" + bartender.screenItem.name)
#pete.menuContext.advance()
#print("SECOND" + bartender.screenItem.name)

app = Flask(__name__)

@app.route('/webhook/', methods=['POST'])
def respond():
    requestData = str(request.data)[4:].replace("'", "")
    menuItem = str(bartender.screenItem.name)
    print('request: ' + requestData + ":")
    print(menuItem)

    while(requestData != bartender.screenItem.name):
        pete.menuContext.advance()
        print("REQUEST: " + requestData)
        print("MENU: " + bartender.screenItem.name)

    if(requestData == bartender.screenItem.name):
        pete.menuContext.select()

    return Response(status=200)

