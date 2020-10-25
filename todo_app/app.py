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

def return_card_object(card_id):
    get_target_card = requests.get('https://api.trello.com/1/cards/' + card_id, params = trello_authorisation)
    get_target_card_json = get_target_card.json()
    return get_target_card_json


class item:
    def __init__(self,idShort, card_name, card_id, list_id ):
        self.idShort = idShort
        self.card_id = card_id
        self.card_name = card_name
        self.status = get_status_name(card_id)
        self.list_id = list_id
        self.NextidList = get_next_list(list_id)

    def delete_card(self):
        requests.delete('https://api.trello.com/1/cards/'+ self.card_id, params = trello_authorisation)
    
    def update_card_list(self):
        update_card_parameters = {'key': Config.API_KEY,'token': Config.TOKEN, 'idList': self.NextidList['id']}
        requests.put('https://api.trello.com/1/cards/'+ self.card_id, params = update_card_parameters)

@app.route('/')
def index():
    cards_on_a_board = requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/cards', params = trello_authorisation)
    cards_on_a_board_json = cards_on_a_board.json()        
    my_card_instance = []
    for myitem in cards_on_a_board_json:
        my_card_instance.append(item(myitem["idShort"],myitem["name"],myitem["id"],myitem["idList"] ))
  
    return render_template('index.html', items=my_card_instance)

@app.route('/add_todo_item', methods=['POST']) 
def add_todo_item(): 
    new_todo_item = request.form.get('newitem', "")
    add_card_to_list(new_todo_item)
    return redirect('/')
    

@app.route('/completed', methods=['POST']) 
def completed(): 
    target_card_id = request.values.get('id')
    target_card = return_card_object(target_card_id) 
    my_item = item(target_card["idShort"],target_card["name"],target_card_id,target_card["idList"])
    my_item.update_card_list()
    return redirect('/')

@app.route('/delete', methods=['POST']) 
def delete(): 
    target_card_id = request.values.get('id')
    target_card = return_card_object(target_card_id)    
    my_item = item(target_card["idShort"],target_card["name"],target_card_id,target_card["idList"])
    my_item.delete_card()
    return redirect('/')


if __name__ == '__main__':
    app.run()
