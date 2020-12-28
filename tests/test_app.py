"""Integration tests for app.py"""
import os
import pytest
import requests
import mock
import json
from flask import Flask, request, render_template, redirect, flash
from todo_app.flask_config import Config
from todo_app.app import create_app, app
import pytest
from dotenv import find_dotenv, load_dotenv
from todo_app.list_class import get_starting_list_id, add_card_to_list
from todo_app.item_class import item, get_card_object, get_items_on_a_board,get_list_progress,check_if_task_recently_completed


def test_always_passes():
    assert True


@pytest.fixture 
def client():     
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)     
    # Create the new app. 
    test_app = create_app() 
    test_app.config['TESTING'] = True
    # Use the app to create a test_client that can be used in our tests. 
    with test_app.test_client() as client:   
        yield client 


def test_index_page(client): 
    #assert str(response_json) == "None"
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True) 
    myConfig = Config()
    
      
    response = client.get('/', content_type='html/text')
    assert response.status_code == 302
    assert b"DOCTYPE HTML PUBLIC" in response.data


    response = client.get('/showToDoItemsTrue,showProgressingItemsTrue,showCompletedJobsTrue,all')
    assert response.status_code == 200

    #assert myConfig.API_KEY == os.environ.get('API_KEY') 
    assert os.environ.get('FLASK_ENV') == 'test'
    #cards_on_a_board = get_items_on_a_board()

