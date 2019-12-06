'''A simple  calculator module for learning tdd in python.'''

def add(x,y):
    '''Add function'''
    return x + y


def subtract(x,y):
    '''Subtraction function'''
    return x - y


def multiply(x,y):
    '''Multiply function'''
    return x * y


def devide(x,y):
    '''Division function'''
    if y == 0;
        raise ValueError('Can not devide by zero!')
    return x / y
