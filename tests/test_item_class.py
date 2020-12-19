"""Unit tests for item_class.py"""

import pytest
from flask import Flask, request, render_template, redirect, flash
import requests
import json
from todo_app.item_class import item, get_card_object, get_items_on_a_board,get_list_progress,check_if_task_recently_completed, get_current_date

def test_always_passes():
    assert True

def test_get_current_date():
    current_date = get_current_date()
    assert len(current_date) > 9

"""Integration tests for item_class.py"""

def test_get_items_on_a_board():
    item_count = 0
    test_items_on_board = get_items_on_a_board()
    found_item = False
    for myitem in test_items_on_board:
        if myitem["id"] == '5fc6941c796b150565cb3836':
            found_item = True

    assert found_item == True


def test_get_card_object():
    
    test_items_on_board = get_card_object('DummyCard')

    assert test_items_on_board["id"] == "5f74ee5505790c8355378641"




