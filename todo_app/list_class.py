from todo_app.flask_config import Config
import requests
import json

trello_authorisation = {'key': Config.API_KEY,'token': Config.TOKEN}


def return_lists_on_a_board():
    return requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/lists', params = trello_authorisation)


def add_card_to_list(card_name):
    new_card_parameters = {'key': Config.API_KEY,'token': Config.TOKEN, 'name': card_name, 'idList': get_starting_list_id(return_lists_on_a_board())}
    requests.post('https://api.trello.com/1/cards/', params = new_card_parameters)


def return_cards_in_list(list_id):
    cards_in_list = requests.get('https://api.trello.com/1/lists/'+ list_id +'/cards', params = trello_authorisation)
    return cards_in_list.json()


def return_list_name(list_id):
    target_list = requests.get('https://api.trello.com/1/lists/'+ list_id, params = trello_authorisation)
    target_list_json = target_list.json()
    return target_list_json['name']

def return_number_of_list_objects(list_items):
    return len(list_items)

def get_starting_list_id(get_board_lists):
    get_board_lists_json = get_board_lists.json()
    return  get_board_lists_json[0]["id"]

class list:
    def __init__(self, list_id):
        self.list_id = list_id
        self.listname =  return_list_name(list_id)
        self.number_of_items = return_number_of_list_objects(return_cards_in_list(list_id))
