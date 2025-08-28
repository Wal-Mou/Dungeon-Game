from time import sleep

def searching_items(items, definitions):
    dictionary = {}

    for item in items:
        dictionary[item] = definitions[items.index(item)]

    item_search = input("\nSearch an item: ").title()
    sleep(0.3)

    if item_search.capitalize() in items:
        for k in dictionary: # k means 'key'
            if item_search == k:
                v = dictionary[k] # v means 'value'
                print('\n' + k + ': ' + v + '\n')
                break

    elif item_search.capitalize() == 'Back':
        print('Okay.')
        return
    else:
        print("Type in an existing item. (Tip: Type in 'Back' to undo this action)")
        searching_items(items, definitions)
    sleep(0.5)


# Read this before you're done: Make sure the user can go back in case they accidentally search.