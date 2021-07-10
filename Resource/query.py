'''
The Resource package is a utility comprised of modules, classes, & functions 
that can help us easily break down implementations for GUI.

Module: query.py
Purpose: Read, Save, Edit, and Delete items from a given queryset of data from a text file.
'''

class Tree():
    def __init__(self, branches={"hello":1, "bye":2, "hi":3}):
        self.branches = branches

    def show(self, option, id=0):
        item_values = []
        for keys, values in option.items():
            item_values.append(values)
        if id == "all":
            for value in item_values:
                print(value)
        else:
            if id < len(item_values):
                print(item_values[id])
            else:
                print("index of item does not exist.")

    def save(self, option, id="all", path=""):
        item_values = []
        for keys, values in option.items():
            item_values.append(values)
        if id == "all":
            for value in item_values:
                file = open(f"{path}", "a", encoding='utf-8')
                file.write(f"{value}\n")
                file.close()

def slice_per(source, y):
    return [source[x:x+y] for x in range(0, len(source), y)]

def delete_item_from_query(item_to_delete, path):
    file = open(f"{path}", "r", encoding='utf-8')
    data = file.readlines()
    file.close()
    data = [line.replace('\n', '') for line in data]
    desired_lines = data[0::1]
    fov = slice_per(desired_lines, 3)
    if item_to_delete in fov:
        fov.remove(item_to_delete)
        file = open(path, 'w', encoding='utf-8').close()
        file = open(path, 'a', encoding='utf-8')
        for item in fov:
            for elem in item:
                file.write(f"{elem}\n")
        file.close()

def change_item_from_query(prev_item, new_item, path):
    file = open(f"{path}", "r", encoding='utf-8')
    data = file.readlines()
    file.close()
    data = [line.replace('\n', '') for line in data]
    desired_lines = data[0::1]
    fov = slice_per(desired_lines, 3)
    if prev_item in fov:
        idx = fov.index(prev_item)
        fov[idx] = new_item
        file = open(path, 'w', encoding='utf-8').close()
        file = open(path, 'a', encoding='utf-8')
        for item in fov:
            for elem in item:
                file.write(f"{elem}\n")
        file.close()

def read_contents_from_query(path):
    file = open(f"{path}", "r", encoding='utf-8')
    data = file.readlines()
    file.close()
    data = [line.replace('\n', '') for line in data]
    desired_lines = data[0::1]
    fov = slice_per(desired_lines, 3)
    for item in fov:
        print(item)

def return_contents_from_query(path):
    file = open(f"{path}", "r", encoding='utf-8')
    data = file.readlines()
    file.close()
    data = [line.replace('\n', '') for line in data]
    desired_lines = data[0::1]
    fov = slice_per(desired_lines, 3)
    return fov

def edit_item_from_query(item_to_edit, new_data, path):
    file = open(f"{path}", "r", encoding='utf-8')
    data = file.readlines()
    file.close()
    data = [line.replace('\n', '') for line in data]
    desired_lines = data[0::1]
    fov = slice_per(desired_lines, 3)
    if item_to_edit in fov:
        idx = fov.index(item_to_edit)
        fov[idx][1] = new_data
        file = open(path, 'w', encoding='utf-8').close()
        file = open(path, 'a', encoding='utf-8')
        for item in fov:
            for elem in item:
                file.write(f"{elem}\n")
        file.close()

def edit_item(item_to_edit, date, todo, status, path):
    file = open(f"{path}", "r", encoding='utf-8')
    data = file.readlines()
    file.close()
    data = [line.replace('\n', '') for line in data]
    desired_lines = data[0::1]
    fov = slice_per(desired_lines, 3)
    if item_to_edit in fov:
        idx = fov.index(item_to_edit)
        fov[idx][0] = date
        fov[idx][1] = todo
        fov[idx][2] = status
        file = open(path, 'w', encoding='utf-8').close()
        file = open(path, 'a', encoding='utf-8')
        for item in fov:
            for elem in item:
                file.write(f"{elem}\n")
        file.close()



def fetch_sorted_todos(path, fetchType):

    CompletedTodosStdFetchId = "completed"
    IncompleteTodosStdFetchId = "incomplete"

    todo_item_status_completed_id = 'Completed ✅'
    todo_item_status_incomplete_id = 'Incomplete ❌'

    contents = return_contents_from_query(path)

    todo_item_status = [
        todo_item_status_completed_id,
        todo_item_status_incomplete_id
    ]

    completed_todos = []
    incomplete_todos = []

    if fetchType == CompletedTodosStdFetchId:
        for todo_item_collection in contents:
            if todo_item_collection[2] == 'Completed ✅':
                print(todo_item_collection)  

    elif fetchType == IncompleteTodosStdFetchId:
        for todo_item_collection in contents:
            if todo_item_collection[2] == 'Incomplete ❌':
                print(todo_item_collection)
    else:
        print("Invalid fetch type.")    