import json


# dictionaries = {'a': {'beer': 'sober', 'portrait': 'quality'},
#                     'b': {'sea': 'fisher'},
#                     'c': {'hello': 'how are you?'}}
#
# for _, value in dictionaries.items():
#     with open('json.json', 'w') as file:
#         json.dump(value, file)
#
#     with open('json.json') as file:
#         print(json.dumps(json.load(file)))


def a(file_):
    print(json.dumps(json.load(file_)))


def b():
    file_ = open('json.json', 'w')
    json.dump({"hello": "world"}, file_)
    file_.close()
    file_ = open('json.json')
    a(file_)
    file_.close()


b()
