#all the non async helper functions are here

def lerp(a, b, t):
    return a * (1.0 - t) + (b * t)

def parse_input(user_input):
    parts = user_input.split()
    if len(parts) < 2:
        print("Error: Input must contain at least ID and one command.")
        return None, []

    try:
        id = int(parts[0])
    except ValueError:
        print("Error: ID should be an integer.")
        return None, []

    commands = []
    for part in parts[1:]:
        header = part[0]
        value = part[1:].strip() if len(part) > 1 else ''
        commands.append((header, value))
    
    return id, commands