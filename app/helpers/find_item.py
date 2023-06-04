def find_item(array, value):
    index = 0
    for item in array:
        if item == value:
            return index
        index = index + 1
    return -1
