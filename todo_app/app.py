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
    for mylist in next_list_response_json:
        if use_next_list_entry == True:
            use_next_list_entry = False
            next_list_name = mylist["name"]
            next_list_id = mylist["id"]
        
        if mylist["id"] == list_id:
            use_next_list_entry = True
    
    ##the card is already on the final list e.g completed
    if use_next_list_entry == True:
        next_list_name = "Completed"
        next_list_id = list_id
    
    next_list_dict = {'name':next_list_name, 'id': next_list_id}
 
    return next_list_dict

def starting_list():
    get_board_lists = requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/lists', params = trello_authorisation)
    get_board_lists_json = get_board_lists.json()
    return  get_board_lists_json[0]["id"]


def add_card_to_list(card_name):
    card_starting_list = starting_list()
    new_card_parameters = {'key': Config.API_KEY,'token': Config.TOKEN, 'name': card_name, 'idList': card_starting_list}
    requests.post('https://api.trello.com/1/cards/', params = new_card_parameters)

def update_card_list(card_id, new_idList):
    update_card_parameters = {'key': Config.API_KEY,'token': Config.TOKEN, 'idList': new_idList}
    requests.put('https://api.trello.com/1/cards/'+ card_id, params = update_card_parameters)

def delete_card(card_id):
    requests.delete('https://api.trello.com/1/cards/'+ card_id, params = trello_authorisation)

@app.route('/')
def index():
    cards_on_a_board = requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/cards', params = trello_authorisation)
    cards_on_a_board_json = cards_on_a_board.json()
        
    for myitem in cards_on_a_board_json:
        card_status_name = get_status_name(myitem["id"]) 
        myitem["status"] = card_status_name
        next_status_name = get_next_list(myitem["idList"]) 
        myitem["nextstatus_name"] = next_status_name["name"]
        myitem["nextstatus_id"] = next_status_name["id"]
        
    return render_template('index.html', items=cards_on_a_board_json)

@app.route('/add_todo_item', methods=['POST']) 
def add_todo_item(): 
    new_todo_item = request.form.get('newitem', "")
    add_card_to_list(new_todo_item)
    return redirect('/')
    

@app.route('/completed', methods=['POST']) 
def completed(): 
    completed_card_id = request.values.get('id')
    next_idList = request.values.get('next_idList')
    update_card_list(completed_card_id,next_idList )
    return redirect('/')

@app.route('/delete', methods=['POST']) 
def delete(): 
    target_card_id = request.values.get('id')
    delete_card(target_card_id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
