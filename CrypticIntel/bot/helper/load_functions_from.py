import os

def load_functions_from(path):
    functions = []
    for file in os.listdir(path):
        if (file.endswith('.py')):
            functions.append(file[:-3])

    try:
        functions.remove('__init__')
    except:
        pass
    # print(functions)
    return functions
