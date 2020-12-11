"""Unit tests for item_class.py"""

import pytest
from flask import Flask, request, render_template, redirect, flash
import requests
import json
from todo_app.list_class import get_starting_list_id, add_card_to_list
from todo_app.item_class import item, get_card_object, get_items_on_a_board,get_list_progress,check_if_task_recently_completed, get_current_date

def test_always_passes():
    assert True

def test_get_current_date():
    current_date = get_current_date()
    assert len(current_date) > 9












