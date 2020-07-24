from flask import Flask, request, Response
from bartender import Bartender, screenItem
from drinks import drink_list, drink_options
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate


#bartender = Bartender()
#Bartender().buildMenu(drink_list, drink_options)
print(screenItem.name)
print(screenItem.type)

app = Flask(__name__)

#print(bartender.menuItemClicked.menuItem.name)

#bartender.menuContext.select()
#bartender.menuContext.select()
#bartender.menuContext.select()

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.data)

    return Response(status=200)

