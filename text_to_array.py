import sys
import os

def textfile_to_farray(path):
    data: str = None
    array = []
    try:
        with open(path, 'r') as file:
            data = file.read()

        number = ''
        for item in data:
            if item.isdigit():
                number += item
            elif (number and item == '.') and (number[-1] != '-' and number[-1] != '.'):
                number += item
            elif not number and item == '-':
                number += item
            elif number and number != '-':
                array.append(float(number))
                number = ''

        if number and number != '-':
            array.append(float(number))

    except Exception as err:
        print(err)

    return array


def sanitize_input(text: str):
    result = ''

    number = ''
    for char in text:
        if char.isdigit():
            number += char
        elif (number and char == '.') and (number[-1] != '-' and number[-1] != '.'):
            number += char
        elif not number and char == '-':
            number += char
        elif number and number != '-':
            result += f'{number}, '
            number = ''

    if number and number != '-':
        result += f'{number}'

    return result


def valid_input(text: str):
    text = text.strip(' ').rstrip(',')
    array = text.split(',')

    for item in array:
        tmp = item.strip()
        if tmp and tmp[0] == '-':
            tmp = tmp[1:]

        if not tmp.isdigit():
            return False

    return True


def text_to_float_array(text: str):
    try:
        array = text.strip(',').rstrip(', \n')
        array = array.split(',')
        return [float(x.strip()) for x in array]
    except Exception:
        return None


def resource_path(*args):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    # try:
    #     base_path = sys._MEIPASS
    # except Exception:
    #     base_path = os.path.abspath('.')
    return os.path.join(base_path, *args)