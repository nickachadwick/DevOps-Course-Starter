"""Unit tests for item_class.py"""

import pytest
from flask import Flask, request, render_template, redirect, flash
from todo_app.list_class import get_starting_list_id, add_card_to_list
from todo_app.item_class import item, get_current_date

def test_always_passes():
    assert True

def test_get_current_date():
    cards_on_a_board = get_items_on_a_board()
    cards_on_a_board_json = cards_on_a_board.json()        
    my_card_instance = []
    number_of_filtered_items = 0











