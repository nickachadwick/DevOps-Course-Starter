"""Unit tests for list_class.py"""

import pytest
import requests
import json
from flask import Flask, request, render_template, redirect, flash
from todo_app.list_class import list, return_number_of_list_objects



def test_always_passes():
    assert True

def test_return_number_of_list_objects():
    test_list = ['item1', 'item2', 'item3', 'item4']
    assert  return_number_of_list_objects(test_list) == 4

    test_list.append('item5')
    assert return_number_of_list_objects(test_list) == 5