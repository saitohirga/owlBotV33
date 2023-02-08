from datetime import datetime
# some sick colors 
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m',
WHITE = '\x1B[37m'

# text color map
intent_map = {
    'white': WHITE,
    'header': HEADER,
    'okblue': OKBLUE,
    'okgreen': OKGREEN,
    'warning': WARNING,
    'fail': FAIL,
    'endc': ENDC,
    'bold': BOLD,
    'underline': UNDERLINE,
    None: ''
}

# intent corresponds 1:1 with globals above
def autoLog(message, intent=None):
    if isinstance(message, str) and ( isinstance(intent, str) or intent == None) :
        print(f'{intent_map["white"]}[{datetime.now().strftime("%y-%m-%d@%H:%M:%S")}]{intent_map[intent]}[{message}]') 