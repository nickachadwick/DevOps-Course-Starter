from flask import Flask, request, render_template, redirect
from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item, delete_item
from operator import itemgetter
import requests
import json

app = Flask(__name__)
app.config.from_object(Config)
trello_authorisation = {'key': Config.API_KEY,'token': Config.TOKEN}

def get_status_name(card_id):
    status_name = requests.get('https://api.trello.com/1/cards/' + card_id +'/list', params = trello_authorisation)
    status_name_json = status_name.json()
    return status_name_json["name"]

def get_next_list(list_id):
    next_list_response = requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/lists', params = trello_authorisation)
    next_list_response_json = next_list_response.json()
    use_next_list_entry = False
    next_list_name = "temp"
    for mylist in next_list_response_json:
        if use_next_list_entry == True:
            use_next_list_entry = False
            next_list_name = mylist["name"]
        
        if mylist["id"] == list_id:
            use_next_list_entry = True
    
    ##the card is already on the final list e.g completed
    if use_next_list_entry == True:
        next_list_name = "Completed"
 
    return next_list_name

def starting_list():
    get_board_lists = requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/lists', params = trello_authorisation)
    get_board_lists_json = get_board_lists.json()
    return  get_board_lists_json[0]["id"]


def add_card_to_list(card_name):
    card_starting_list = starting_list()
    new_card_parameters = {'key': Config.API_KEY,'token': Config.TOKEN, 'name': card_name, 'idList': card_starting_list}
    requests.post('https://api.trello.com/1/cards/', params = new_card_parameters)

@app.route('/')
def index():
    cards_on_a_board = requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/cards', params = trello_authorisation)
    cards_on_a_board_json = cards_on_a_board.json()
        
    for myitem in cards_on_a_board_json:
        card_status_name = get_status_name(myitem["id"]) 
        myitem["status"] = card_status_name
        next_status_name = get_next_list(myitem["idList"]) 
        myitem["nextstatus"] = next_status_name
        
    return render_template('index.html', items=cards_on_a_board_json)

@app.route('/add_todo_item', methods=['POST']) 
def add_todo_item(): 
    new_todo_item = request.form.get('newitem', "")
    add_card_to_list(new_todo_item)
    return redirect('/')
    

@app.route('/completed', methods=['POST']) 
def completed(): 
    ##retrieve the id of the completed task
    completed_item = request.values.get('id')
    ##retrieve the item of the completed task
    item = get_item(completed_item)
    ##create a new dictionary item that will be used to overwrite the existing value 
    updated_item = { 'id': item['id'],  'status': 'Completed', 'title': item['title']}
    
    ##overwrite the dictionary item with the new value containing a status of completed
    save_item(updated_item)
    ##retrieve the items
    items = get_items()
    
    ##renders the template with the items sorted by status
    return render_template('index.html',items=sorted(items,key=itemgetter('status'),reverse=True))


@app.route('/delete', methods=['POST']) 
def delete(): 
    ##retrieve the id of the item to delete
    target_item_id = request.values.get('id')
    ##retrieve the item of the completed task
    item = get_item(target_item_id)   
    ##overwrite the dictionary item with the new value containing a status of completed
    delete_item(item)
    ##retrieve the items
    items = get_items()
    
    ##renders the template with the items sorted by status
    return render_template('index.html',items=sorted(items,key=itemgetter('status'),reverse=True))


if __name__ == '__main__':
    app.run()
