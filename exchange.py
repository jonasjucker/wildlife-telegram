_bot_action = False

def set_bot_action(state):
    global _bot_action
    _bot_action = state

def is_bot_action():
    return _bot_action
