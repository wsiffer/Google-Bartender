import bartender
import atexit
from flask import Flask, request, Response
from drinks import drink_list, drink_options
#import atexit
from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate

atexit.register(bartender.Bartender.atExit)
pete = bartender.Bartender()
pete.buildMenu(drink_list, drink_options)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    requestData = str(request.data)[4:].replace("'", "")

    if(requestData == "clean"):
        while(bartender.screenItem.name != "Configure"):
            pete.menuContext.advance()
        pete.menuContext.select()
        while(bartender.screenItem.name != "Clean"):
            pete.menuContext.advance()
        pete.menuContext.select()

        for i in range(0,1):
            while(bartender.screenItem.name != "Back"):
                pete.menuContext.advance()
            pete.menuContext.select()

        return Response(status=200)

    i = 0
    while(requestData != bartender.screenItem.name):
        if(i == 2):
            break

        pete.menuContext.advance()

        if(bartender.screenItem.name == "Configure"):
            i += 1

    if(requestData == bartender.screenItem.name):
        pete.menuContext.select()

    return Response(status=200)

if __name__=='__main__':
    #atexit.register(bartender.Bartender.atExit)
    app.run(host='0.0.0.0')

