# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:59:01 2021

@author: dmg530
"""
import csv

def csvToArray(file_path):
    results = []
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)
    return results