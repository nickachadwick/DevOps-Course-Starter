from flask import Flask, request, render_template, redirect, flash
from todo_app.flask_config import Config
import os
import requests
import json
import pytest
from dotenv import find_dotenv, load_dotenv
from todo_app.list_class import get_starting_list_id, add_card_to_list
from todo_app.item_class import item, get_card_object, get_items_on_a_board,get_list_progress,check_if_task_recently_completed


redirectURL = '/'
trello_authorisation = {'key': os.environ.get('API_KEY'),'token': os.environ.get('TOKEN')}


def create_app():

    app = Flask(__name__)

    myConfig = Config() 
    app.config.from_object(myConfig) 
    

    @app.route('/<todoJobs>,<progressingJobs>,<completedJobs>,<doneoptions>', methods=['GET'])
    def index1(todoJobs,progressingJobs,completedJobs,doneoptions):
        cards_on_a_board_json = get_items_on_a_board()
        #cards_on_a_board_json = cards_on_a_board.json()        
        my_card_instance = []
        number_of_filtered_items = 0

        for myitem in cards_on_a_board_json:
            item_progress = get_list_progress(myitem["idList"])
            if (todoJobs =="showToDoItemsTrue" and item_progress == "todo") or (progressingJobs == "showProgressingItemsTrue" and item_progress == "inprogress"):
                my_card_instance.append(item(myitem["idShort"],myitem["name"],myitem["id"],myitem["idList"], todoJobs, progressingJobs, completedJobs, doneoptions))
                number_of_filtered_items = number_of_filtered_items + 1
            elif (completedJobs == "showCompletedJobsTrue") and (item_progress == "done"):
                if (doneoptions == "all") or (doneoptions == "xALL"):
                    my_card_instance.append(item(myitem["idShort"],myitem["name"],myitem["id"],myitem["idList"], todoJobs, progressingJobs, completedJobs, doneoptions))
                    number_of_filtered_items = number_of_filtered_items + 1
                else:
                    done_card_object =  get_card_object(myitem["id"])

                    check_card = check_if_task_recently_completed(done_card_object)

                    if (doneoptions == check_card):
                        my_card_instance.append(item(myitem["idShort"],myitem["name"],myitem["id"],myitem["idList"], todoJobs, progressingJobs, completedJobs, doneoptions))
                        number_of_filtered_items = number_of_filtered_items + 1

        if number_of_filtered_items == 0:
            return redirect('/showToDoItemsTrue,showProgressingItemsTrue,showCompletedJobsTrue,xALL')
        else:             
            return render_template('index.html', items=my_card_instance)
    

    @app.route('/', methods=['GET'])
    def index():
        return redirect('/showToDoItemsTrue,showProgressingItemsTrue,showCompletedJobsTrue,all')

    @app.route('/add_todo_item', methods=['POST']) 
    def add_todo_item(): 
        new_todo_item = request.form.get('newitem', "")
        add_card_to_list(new_todo_item)
        todo_checkbox = request.values.get('todo_checkbox')
        progressing_checkbox = request.values.get('progressing_checkbox')
        done_checkbox = request.values.get('done_checkbox')
        done_options = request.values.get('doneitems')
        redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox + ',' + done_options
        return redirect(redirectURL)

    @app.route('/filterResults', methods=['POST']) 
    def filterResults(): 
        todo_checkbox = request.form.get('todoJobs1', "showToDoItemsFalse")
        progressing_checkbox = request.form.get('progressingJobs', "showProgressingJobsFalse")
        done_checkbox = request.form.get('completedJobs', "showCompletedJobsFalse")
        done_options = request.values.get('doneitems',"all")
        redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox + ',' + done_options
        return redirect(redirectURL)
    

    @app.route('/next_list', methods=['POST']) 
    def completed(): 
        target_card_id = request.values.get('id')
        todo_checkbox = request.values.get('todo_checkbox')
        progressing_checkbox = request.values.get('progressing_checkbox')
        done_checkbox = request.values.get('done_checkbox')
        done_options = request.values.get('doneitems')
        target_card = get_card_object(target_card_id) 

        my_item = item(target_card["idShort"],target_card["name"],target_card_id,target_card["idList"],todo_checkbox, progressing_checkbox, done_checkbox,done_options)
        my_item.update_card_list()
        
        redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox + ',' + done_options
        return redirect(redirectURL)

    @app.route('/delete', methods=['POST']) 
    def delete(): 
        target_card_id = request.values.get('id')
        
        todo_checkbox = request.values.get('todo_checkbox')
        progressing_checkbox = request.values.get('progressing_checkbox')
        done_checkbox = request.values.get('done_checkbox')
        done_options = request.values.get('doneitems')
        target_card = get_card_object(target_card_id) 
        my_item = item(target_card["idShort"],target_card["name"],target_card_id,target_card["idList"],todo_checkbox, progressing_checkbox, done_checkbox, done_options)
        my_item.delete_card()
        
        redirectURL = '/'+ todo_checkbox + ',' + progressing_checkbox + ',' + done_checkbox + ',' + done_options
        return redirect(redirectURL)

    

    if __name__ == '__main__':
        app.run()
    
    return app

app = create_app()
