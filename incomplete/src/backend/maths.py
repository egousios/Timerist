'''
The Resource package is a utility comprised of modules, classes, & functions 
that can help us easily break down implementations for GUI.

Module: maths.py
Purpose: Perform diffrent arithmetic operations on numerical data sets.
'''
import re
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)

def add(elems=[]):
    first_num = elems[0]
    temp = first_num
    for x in range(len(elems)):
        first_num += elems[x]
    result = first_num - temp ## Apply the Inverse Operation to Get The Correct Result!
    return result

def subtract(elems=[]):
    first_num = elems[0]
    temp = first_num
    for x in range(len(elems)):
        first_num -= elems[x]
    result = first_num + temp ## Apply the Inverse Operation to Get The Correct Result!
    return result

def multiply(elems=[]):
    first_num = elems[0]
    temp = first_num
    for x in range(len(elems)):
        first_num *= elems[x]
    result = first_num / temp ## Apply the Inverse Operation to Get The Correct Result!
    return result

def divide(elems=[]):
    first_num = elems[0]
    temp = first_num
    for x in range(len(elems)):
        first_num /= elems[x]
    result = first_num * temp ## Apply the Inverse Operation to Get The Correct Result!
    return result

def power(base, exp):
    return pow(base, exp)












