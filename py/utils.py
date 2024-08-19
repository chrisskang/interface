#all the non async helper functions are here
import json

def lerp(a, b, t):
    return a * (1.0 - t) + (b * t)

def parse_input(user_input):

    cmdList = []

    for index, parts in enumerate(user_input.split()):
        parts = parts.split(':')
        id = parts[0]
        cmds = parts[1]
        
        cmdList.append({})
        cmdList[index]['id'] = id
        cmdList[index]['commands'] = []
    
        for part in cmds.split(','):
            header = part[0]
            value = part[1:].strip() if len(part) > 1 else ''
            cmdList[index]['commands'].append((header, value))
            
    return cmdList
