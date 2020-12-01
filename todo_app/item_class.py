from todo_app.flask_config import Config
from todo_app.list_class import list
import requests
import json

trello_authorisation = {'key': Config.API_KEY,'token': Config.TOKEN}

def get_items_on_a_board():
    return requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/cards', params = trello_authorisation)

def get_card_object(card_id):
    get_target_card = requests.get('https://api.trello.com/1/cards/' + card_id, params = trello_authorisation)
    get_target_card_json = get_target_card.json()
    return get_target_card_json

def get_status_name(card_id):
    status_name = requests.get('https://api.trello.com/1/cards/' + card_id +'/list', params = trello_authorisation)
    status_name_json = status_name.json()
    return status_name_json["name"]

def get_progress_list(list_id):
    next_list_response = requests.get('https://api.trello.com/1/boards/' + Config.TRELLO_BOARD + '/lists', params = trello_authorisation)
    use_next_list_entry = False
    card_progress = "todo"
    list_loop_iterations = 0
    for mylist in next_list_response.json():
        if use_next_list_entry == True:
            use_next_list_entry = False
            next_list_name = mylist["name"]
            next_list_id = mylist["id"]
            break

        if mylist["id"] == list_id:
            use_next_list_entry = True
            

        list_loop_iterations = list_loop_iterations + 1
    
    
    if list_loop_iterations != 1:
        card_progress = "inprogress"

    ##the card is already on the final list e.g completed
    if use_next_list_entry == True:
        next_list_name = "xxLastListxx"
        card_progress = "done"
        next_list_id = list_id
    
    next_list_dict = {'name':next_list_name, 'id': next_list_id, 'progress':  card_progress}

    return next_list_dict

def get_list_progress(list_id):
    get_next_list_dict = get_progress_list(list_id)
    return get_next_list_dict["progress"]

class item:
    def __init__(self,idShort, card_name, card_id, list_id, showToDoItems, showProgressingItems, showCompletedJobs ):
        self.idShort = idShort
        self.card_id = card_id
        self.card_name = card_name
        self.status = get_status_name(card_id)
        self.list = list(list_id)
        self.progress = get_progress_list(list_id)
        self.showItemsToDo = showToDoItems
        self.showProgressing = showProgressingItems
        self.showCompleted = showCompletedJobs

    def delete_card(self):
        requests.delete('https://api.trello.com/1/cards/'+ self.card_id, params = trello_authorisation)
    
    def update_card_list(self):
        update_card_parameters = {'key': Config.API_KEY,'token': Config.TOKEN, 'idList': self.progress['id']}
        requests.put('https://api.trello.com/1/cards/'+ self.card_id, params = update_card_parameters)


