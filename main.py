# -*- coding: utf-8 -*-
from helperFunctions import csvToArray

day = '09-03-2021'
time = '14-46'
file = 'ne0'
path = day+'/'+time+'/'+file+'.csv'

print(csvToArray(path))

