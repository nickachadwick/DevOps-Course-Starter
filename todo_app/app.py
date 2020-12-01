from flask import Flask, request, render_template, redirect
from todo_app.flask_config import Config
import requests
import json
from todo_app.list_class import get_starting_list_id, add_card_to_list
from todo_app.item_class import item, get_card_object, get_items_on_a_board,get_list_progress

app = Flask(__name__)
app.config.from_object(Config)
trello_authorisation = {'key': Config.API_KEY,'token': Config.TOKEN}
redirectURL = '/'


@app.route('/<todoJobs>,<progressingJobs>,<completedJobs>', methods=['GET', "POST"])
def index1(todoJobs,progressingJobs,completedJobs):
    cards_on_a_board = get_items_on_a_board()
    cards_on_a_board_json = cards_on_a_board.json()        
    my_card_instance = []

    for myitem in cards_on_a_board_json:
        item_progress = get_list_progress(myitem["idList"])
        if (todoJobs =="showToDoItemsTrue" and item_progress == "todo") or (progressingJobs == "showProgressingItemsTrue" and item_progress == "inprogress") or (completedJobs == "showCompletedJobsTrue" and item_progress == "done"):
            my_card_instance.append(item(myitem["idShort"],myitem["name"],myitem["id"],myitem["idList"], todoJobs, progressingJobs, completedJobs))
        

    return render_template('index.html', items=my_card_instance)

@app.route('/', methods=['GET'])
def index():
    todo_checkbox = 'showToDoItemsTrue'
    progressing_checkbox = 'showProgressingItemsTrue'
    done_checkbox = 'showCompletedJobsTrue'
    cards_on_a_board = get_items_on_a_board()
    cards_on_a_board_json = cards_on_a_board.json()        
    my_card_instance = []

    for myitem in cards_on_a_board_json:
        my_card_instance.append(item(myitem["idShort"],myitem["name"],myitem["id"],myitem["idList"],todo_checkbox, progressing_checkbox, done_checkbox ))
        
    return render_template('index.html', items=my_card_instance)

@app.route('/add_todo_item', methods=['POST']) 
def add_todo_item(): 
    new_todo_item = request.form.get('newitem', "")
    add_card_to_list(new_todo_item)
    todo_checkbox = request.values.get('todo_checkbox')
    progressing_checkbox = request.values.get('progressing_checkbox')
    done_checkbox = request.values.get('done_checkbox')
    redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox
    return redirect(redirectURL)

@app.route('/filterResults', methods=['POST']) 
def filterResults(): 
    todo_checkbox = request.form.get('todoJobs1', "showToDoItemsFalse")
    progressing_checkbox = request.form.get('progressingJobs', "showProgressingJobsFalse")
    done_checkbox = request.form.get('completedJobs', "showCompletedJobsFalse")
    redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox
    return redirect(redirectURL)

@app.route('/next_list', methods=['POST']) 
def completed(): 
    target_card_id = request.values.get('id')
    todo_checkbox = request.values.get('todo_checkbox')
    progressing_checkbox = request.values.get('progressing_checkbox')
    done_checkbox = request.values.get('done_checkbox')
    target_card = get_card_object(target_card_id) 

    my_item = item(target_card["idShort"],target_card["name"],target_card_id,target_card["idList"],todo_checkbox, progressing_checkbox, done_checkbox)
    my_item.update_card_list()
    redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox
    return redirect(redirectURL)

@app.route('/delete', methods=['POST']) 
def delete(): 
    target_card_id = request.values.get('id')
       
    todo_checkbox = request.values.get('todo_checkbox')
    progressing_checkbox = request.values.get('progressing_checkbox')
    done_checkbox = request.values.get('done_checkbox')
    target_card = get_card_object(target_card_id) 
    my_item = item(target_card["idShort"],target_card["name"],target_card_id,target_card["idList"],todo_checkbox, progressing_checkbox, done_checkbox)
    my_item.delete_card()
    redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox
    return redirect(redirectURL)


if __name__ == '__main__':
    app.run()
