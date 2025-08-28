import random
import re
import SearchingItems
from math import floor, sqrt
from random import randint
from time import sleep

Dungeon = {
    "Entrance": {
        "Directions": ['North to Hallway'],
        "Monsters": '',
        "Items": ['Torch' + ' // ' + 'Knife'],
        "Description": 'Cold, dark chamber with a faint torch on the wall.'
    },

    "Hallway": {
        "Directions": ['South to Entrance' + ' // ' + 'North to PuzzleRoom' + ' // ' + 'East to Armory'],
        "Monsters": 'Goblin',
        "Items": ['Potion' + ' // ' + 'Apple'],
        "Description": 'Narrow corridor with cracked stone tiles.'
    },

    "Armory": {
        "Directions": ['West to Hallway'],
        "Monsters": 'Skeleton',
        "Items": ['Sword' + ' // ' + 'Shield'],
        "Description": 'Dusty weapons scattered around.'
    },

    "PuzzleRoom": {
        "Directions": ['South to Hallway' + ' // ' + 'North to TreasureChamber'],
        "Monsters": '',
        "Items": ['Passcode'],
        "Description": 'Glowing runes. A locked door lies ahead.'
    },

    "TreasureChamber": {
        "Directions": ['South to PuzzleRoom'],
        "Monsters": 'Spider',
        "Items": [],
        "Description": 'Glittering room with gold and a giant chest.'
    }
}

Monsters = {
    "Goblin": {
        "Name": 'Goblin',
        "HP": 20,
        "Attack": {
            "MaxDamage": 5,
            "MinDamage": 3,
        },
        'Loot': ['Axe', 'Apple']
    },

    "Skeleton": {
        "Name": 'Skeleton',
        "HP": 27,
        "Attack": {
            "MaxDamage": 8,
            "MinDamage": 5,
        },
        "Loot": ["Bone", 'Potion']
    },

    "Spider": {
        "Name": 'Spider',
        "HP": 60,
        "Attack": {
            "MaxDamage": 13,
            "MinDamage": 10,
        },
        "Loot": ['Spiderhead', 'Key']
    }
}

Player = {
    "Name": input("Type in your Name: ").title(),
    "HP": 50,
    "Attack": 7,
    "Inventory": [],
    "Current Room": "Entrance",
}

Weapons = {
    "Knife": {
        "MaxDamage": 7, # Maximum damage can be caused by this weapon
        "MinDamage": 3, # Maximum damage can be caused by this weapon
    },

    "Axe": {
        "MaxDamage": 13,
        "MinDamage": 1,
    },

    "Sword": {
        "MaxDamage": 20,
        "MinDamage": 14,
    },

    # "A": {
    #     "MaxDamage": 999999,
    #     "MinDamage": 999999,
    # },
}

Healers = {
    "Apple": 5,
    "Potion": 10,
}

print("""Type in '/help' to see the commands.\n""")
sleep(0.3)


pick_up_items = ''.join(Dungeon[Player["Current Room"]]["Items"]).split()
unvisited_rooms = ['Hallway', 'TreasureChamber']

rooms_list_for_monsters = ['Hallway', 'Armory', 'TreasureChamber']
monsters_list = ['Goblin', 'Skeleton', 'Spider']

healers_list = ['Apple', 'Potion']
weapons_list = ['Knife', 'Axe', 'Sword']
protection_items_list = ['Shield']
key_items_list = ['Key', 'Passcode', 'Torch']
flavor_items_list = ['Bone', 'Spiderhead']
items_list = ['Torch', 'Knife', 'Sword', 'Axe', 'Potion', 'Apple', 'Shield', 'Passcode', 'Key', 'Bone', 'Spiderhead']
items_list_definition = ['A light source used to navigate through the rooms.', 'A Weapon to attack monsters (Deals a minimum of 3 damage and a maximum of 7 damage).', 'A Weapon used to attack monsters (Deals a minimum of 14 damage and a maximum of 20).', 'A Weapon used to attack monsters (Deals a minimum of 1 damage and a maximum of 13 damage).', 'A healer used to regain 10 HP.', 'A Healer used to regain 5 HP', "Used a protection from the monsters' attack (reduces 20% of the damage dealt from the monster)", 'A paper with hints that helps you to solve the puzzles in order to find the code.', 'Used to open the grand door at the end of the game after defeating the dragon.', 'An item that has no real use in the game (flavor/loot item).', "Well.... you'll eventually find out."]
fight_ornot = None
puzzle_solved = False
i_repeating_passcode_puzzle = 0


while Player["HP"] >= 0:

    direction_i = 0
    pick_up_items_i = 0

    direction = ''.join(Dungeon[Player["Current Room"]]["Directions"]).split()
    pick_up_items = ''.join(Dungeon[Player["Current Room"]]["Items"]).split()
    direcitons_compass_list = ['North', 'South', 'East', 'West']

    print(f"Player Stats:\nName: {Player["Name"]}.\nHP: {Player["HP"]}\nCurrent Room: {' '.join(re.findall('[A-Z][^A-Z]*', Player['Current Room']))}.\nItems: {' '.join(Dungeon[Player["Current Room"]]["Items"])}\nDirections: {re.sub(' +', ' ', ' '.join(re.findall('[A-Z][^A-Z]*', ''.join(Dungeon[Player["Current Room"]]["Directions"]))))}.")

    command = input('\n>> ').lower()

    def endings():
        inventory_sorting(Player['Inventory'])
        print(f"\nInventory: {', '.join(player_inventory_link)}.")

        ending_key = input("\nPick an item to place on the Pedestal, or use the key to unlock the Grand Door. (Type in the name of the item).\n>> ").lower()
        sleep(0.5)

        if not ending_key.title() in Player['Inventory']:
            print("\nUNKNOWN ITEM!")
            sleep(1)
            endings()

        elif ending_key == 'bone' or ending_key == 'key' or ending_key == 'spiderhead' and ending_key.title() in Player['Inventory']:
            sure_or_not = input(f"\nAre you sure you want to continue using the {ending_key}?\n>> ").lower()
            sleep(0.5)

            if sure_or_not == 'no':
                print("ok.\n")
                sleep(0.3)
                endings()

            elif sure_or_not == 'yes':
                if ending_key == 'bone':
                    print("\nYou have unlocked the Secret Ending.\nAfter placing the Bone on the Pedestal, the Treasure Chest at the very back of the Treasure Chamber opens, revealing the Golden coins. There are thousands of these inside the chest,"
                          "which are worth billions!")
                    sleep(0.3)

                elif ending_key == 'spiderhead':
                    print("\nYou have unlocked the most Repugnant Failure Known to Man.\nAfter placing the Spiderhead on the Pedestal. The entire floor causes a MASSIVE Earthquake, causing the entire floor to collapse sending you flying downwards"
                          "at the speed of approximately 193 km/h (since it is the terminal velocity of a human and gravity pulls any object downwards around 9.80665 m/s2. My bad, I forgot that it is not Physics class.) You land on a big pile of "
                          "old mattresses while also break a few bones on the impact. The next thing you hear is loud Spider noises...")
                    sleep(0.3)

                elif ending_key == 'key':
                    print("\nYou have unlocked the Happy Ending.\nYou unlocked the Grand Door using the key at the right side of the Treasure Chamber. The door leads to an exit.")
                    sleep(0.3)

            else:
                print("Type in either 'yes' or 'no'.")
                sleep(1)
                endings()


        else:
            print("This item is not possible to use.")
            sleep(1)
            endings()

        print("\n\nTHE END.")
        sleep(0.1)
        exit()

    def torch_lighting():
        global command

        if 'Torch' in Player['Inventory']:
            agree_to_use = input("Use Torch (type Yes or No)? ")

            if agree_to_use.lower() == 'yes':
                Player["Inventory"].remove('Torch')
                unvisited_rooms.remove('Hallway')
                return

            elif agree_to_use.lower() == 'no':
                print('ok.\n')
                sleep(0.3)

            else:
                print("Type either yes or no.")
                torch_lighting()

    def inventory_sorting(inventory_list):
        global player_inventory_link

        healers = []
        weapons = []
        key_items = []
        flavor_items = []
        protection_items= []

        for item in inventory_list:
            if item in healers_list:
                healers.append(item)

            elif item in weapons_list:
                weapons.append(item)

            elif item in key_items_list:
                key_items.append(item)

            elif item in flavor_items_list:
                flavor_items.append(item)

            elif item in protection_items_list:
                protection_items.append(item)

        player_inventory_link = weapons + key_items + healers + protection_items + flavor_items
        for item in player_inventory_link:
            i = 0
            for item2 in player_inventory_link:
                if item == item2:
                    i += 1

            if i > 1:
                for e in range(i):
                    player_inventory_link.remove(item)
                item = f"x{i} {item}"

                player_inventory_link.append(item)

    def puzzle_room_calc():
        global ran_element
        global ran_num
        global passcode
        global i_repeating_passcode_puzzle

        elements = [
            "Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen", "Fluorine", "Neon",
            "Sodium", "Magnesium", "Aluminum", "Silicon", "Phosphorus", "Sulfur", "Chlorine", "Argon", "Potassium", "Calcium",
            "Scandium", "Titanium", "Vanadium", "Chromium", "Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc",
            "Gallium", "Germanium", "Arsenic", "Selenium", "Bromine", "Krypton", "Rubidium", "Strontium", "Yttrium","Zirconium",
            "Niobium", "Molybdenum", "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver", "Cadmium", "Indium", "Tin",
            "Antimony", "Tellurium", "Iodine", "Xenon", "Cesium", "Barium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium",
            "Promethium", "Samarium", "Europium", "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium",
            "Lutetium", "Hafnium", "Tantalum", "Tungsten", "Rhenium", "Osmium", "Iridium", "Platinum", "Gold", "Mercury",
            "Thallium", "Lead", "Bismuth", "Polonium", "Astatine", "Radon", "Francium", "Radium", "Actinium", "Thorium",
            "Protactinium", "Uranium", "Neptunium", "Plutonium", "Americium", "Curium", "Berkelium", "Californium", "Einsteinium", "Fermium",
            "Mendelevium", "Nobelium", "Lawrencium", "Rutherfordium", "Dubnium", "Seaborgium", "Bohrium", "Hassium","Meitnerium", "Darmstadtium",
            "Roentgenium", "Copernicium", "Nihonium", "Flerovium", "Moscovium", "Livermorium", "Tennessine", "Oganesson"]

        atomic_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
            61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
            91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118]

        if i_repeating_passcode_puzzle < 1:
            for i in range(1):
                nums = 100

                sqrt_nums_list = []

                for num in range(101):
                    sqrt_num = sqrt(num)
                    if sqrt_num.is_integer():
                        sqrt_nums_list.append(num)
                    nums -= 1


                ran_element = random.choice(elements)
                ran_atomic_masses = atomic_numbers[elements.index(ran_element)]

                ran_num = random.choice(sqrt_nums_list)
                sqr_ran_num = int((sqrt(ran_num) / 2) + 0.5)


                # ran_category = random.choice(categories)
                # ran_category_counts = category_counts[categories.index(ran_category)]

                passcode = ran_atomic_masses + sqr_ran_num

                i_repeating_passcode_puzzle += 1

    puzzle_room_calc()

    def puzzle_room_passcode_inp():
        global puzzle_solved

        try:
            passcode_attempt = input("Type in the Passcode: ")
            sleep(0.3)

            if passcode_attempt.lower() == 'back':
                return

            elif int(passcode_attempt) == passcode:
                print('Passcode is Correct. Access has been Granted.')
                sleep(0.5)
                Player['Inventory'].remove('Passcode')
                puzzle_solved = True
                combat_fighting()

            else:
                print("Passcode is Incorrect. Access has been Denied.")
                sleep(0.5)

        except ValueError:
            print('Type in positive integers only.')
            sleep(1)

    def movements():
        global direction_i
        global valueerror_occured
        global final_boss_fight
        global puzzle_solved

        valueerror_occured = ""

        try:
            for room in command.split():
                direction_i = 0
                room.lower()

                if room == 'west':
                    direction_i = direction.index('West')
                    direction_i += 2
                    combat_fighting()
                    break


                elif room == 'east':
                    direction_i = direction.index('East')
                    direction_i += 2
                    combat_fighting()
                    break


                elif room == 'north':

                    if 'Hallway' in unvisited_rooms:
                        print("The rooms are pitch black, You will need a light source to see and pass through.\n")
                        sleep(0.3)
                        torch_lighting()

                    if 'Hallway' not in unvisited_rooms:
                        direction_i = direction.index('North')
                        direction_i += 2
                        combat_fighting()
                        break


                elif room == 'south':
                    direction_i = direction.index('South')
                    direction_i += 2
                    combat_fighting()
                    break


        except ValueError:
                valueerror_occured = "yes"
                print("\nINVALID  DIRECTION!\n")
                sleep(1)

    def items_index():
        global pick_up_items_i
        try:
            for item in command.split():
                pick_up_items_i = 0
                item.lower()
                if item == 'torch':
                    pick_up_items_i = pick_up_items.index('Torch')

                elif item == 'knife':
                    pick_up_items_i = pick_up_items.index('Knife')

                elif item == 'potion':
                    pick_up_items_i = pick_up_items.index('Potion')

                elif item == 'apple':
                    pick_up_items_i = pick_up_items.index('Apple')

                elif item == 'sword':
                    pick_up_items_i - pick_up_items.index('Sword')

                elif item == 'shield':
                    pick_up_items_i = pick_up_items.index('Shield')

                elif item == 'passcode':
                    pick_up_items_i = pick_up_items.index('Passcode')
                    print("Type in 'Read Passcode' to get the code.")
                    sleep(0.5)


                elif item == 'key':
                    pick_up_items_i = pick_up_items.index('Key')

        except ValueError:
            pass

    def combat_fighting():
        global current_room
        global direction_i


        if 'Knife' not in Player['Inventory']:
            print("\nYou are not ready to fight, a weapon is required to start.\n")
            sleep(0.3)
            direction[direction_i] = 'Entrance'


        # if rooms_list_for_monsters and rooms_list_for_monsters[0] == direction[direction_i]:
        if direction[direction_i] in rooms_list_for_monsters:
            def fighting_ans():
                global direction_i
                global fight_ornot


                if direction[direction_i] == 'TreasureChamber' and puzzle_solved == False:
                    if 'Passcode' in Player['Inventory']:
                        puzzle_room_passcode_inp()

                    elif not 'Passcode' in Player['Inventory'] and direction[direction_i] == 'TreasureChamber':
                        print('To be able to continue, you must have the passcode in your inventory.')
                        sleep(0.3)
                    return

                else:
                    owned_healing = []
                    owned_weapons = []
                    monster = monsters_list[rooms_list_for_monsters.index(direction[direction_i])]

                    fight_ornot = input(f"Would you like to start fighting the {monster}? ").lower()
                    sleep(0.3)


                    if fight_ornot == 'yes':
                        if direction[direction_i] == 'TreasureChamber':
                                final_boss_fight_inp = input("Are you sure you want to continue? You will not be able to go back after the fight (Type in 'yes' or 'no')'.\n>> ").lower()
                                sleep(0.3)

                                if final_boss_fight_inp == 'yes':
                                    print("+20 HP")
                                    Player['HP'] += 20

                                elif final_boss_fight_inp == 'no':
                                    print('ok.\n')
                                    sleep(0.3)
                                    return

                                else:
                                    print("Type in either 'yes' or 'no'.")
                                    fighting_ans()
                                    return

                            # else:
                            #     puzzle_room()
                            #     # Check whether you need to add a 'return' or not here!
                        else:
                            sleep(0.1)
                            print("\n" * 50 + "YOU ARE READY FOR COMBAT!")
                            sleep(0.3)



                        while Monsters[monster]['HP'] >= 1 and Player['HP'] >= 1:

                            def heal_or_attack_func():
                                global damage_dealt_player
                                global player_hp
                                player_hp = 0
                                heal_or_attack = input("""Heal or Attack (Type in either "heal" or "attack")? """).lower()
                                sleep(0.3)

                                if heal_or_attack == 'heal':
                                    if Player['HP'] < 50:
                                        owned_healing = []
                                        for item in Player['Inventory']:
                                            if item in healers_list:
                                                owned_healing.append(item)

                                        if owned_healing == []:
                                            print("\nYou do not have any healers in your inventory.\n")
                                            sleep(0.3)
                                            heal_or_attack_func()

                                        else:
                                            for healing in owned_healing:
                                                inventory_sorting(owned_healing)
                                                healer_picked = input(f"Pick the healer (Type in the healer only): {', '.join(player_inventory_link)}\n>>> ").title()
                                                sleep(0.3)

                                                if healer_picked == 'Back':
                                                    heal_or_attack_func()
                                                    return

                                                elif healer_picked in Player['Inventory']:
                                                    player_hp = Player['HP']
                                                    player_hp += Healers[healer_picked]


                                                    if player_hp > 50:
                                                        Player['Inventory'].remove(healer_picked)
                                                        owned_healing.remove(healer_picked)
                                                        player_hp = 50 - Player['HP']
                                                        Player['HP'] = 50
                                                        print(f"\n+{player_hp} HP after using the {healer_picked}")
                                                        break


                                                    else:
                                                        Player['Inventory'].remove(healer_picked)
                                                        owned_healing.remove(healer_picked)
                                                        Player['HP'] += Healers[healer_picked]
                                                        print(f"\n+{Healers[healer_picked]} HP after using the {healer_picked}")
                                                        break


                                                else:
                                                    print(
                                                        "\nINVALID HEALER. Type in one of the healers that exists in your inventory.\n")
                                                    sleep(1)

                                                    heal_or_attack_func()
                                                    return
                                    else:
                                        print("\nYour HP is already at the max.")
                                        heal_or_attack_func()

                                elif heal_or_attack == 'attack':
                                    owned_weapons = []
                                    try:
                                        for item in Player['Inventory']:
                                            if item in weapons_list:
                                                owned_weapons.append(item)
                                        inventory_sorting(owned_weapons)
                                        weapon_picked = input(f"Pick your weapon (Type in the weapon only): {', '.join(re.findall('[A-Z][^A-Z]*', ''.join(player_inventory_link)))}\n>>> ").title()
                                        sleep(0.3)

                                        if weapon_picked == 'Back':
                                            heal_or_attack_func()
                                            return

                                        elif weapon_picked in owned_weapons:
                                            damage_dealt_player = randint(Weapons[weapon_picked]["MinDamage"], Weapons[weapon_picked]["MaxDamage"]) #Use a nested dictionary to say the minimum damage dealt to monster
                                        else:
                                            print("\nINVALID WEAPON. Type in a weapon that exists in your Inventory.\n")
                                            sleep(0.3)

                                            heal_or_attack_func()
                                            return

                                        Monsters[monster]["HP"] -= damage_dealt_player
                                        print(f"The monster was attacked with the {weapon_picked} and lost {damage_dealt_player} HP.")
                                        sleep(1)


                                    except KeyError:
                                        print("\nINVALID WEAPON. Type in one of the weapons that exists in your inventory.\n")
                                        sleep(1)
                                        heal_or_attack_func()

                                else:
                                    print("""\nINVALID COMMAND. Type in either 'Heal' or 'Attack'.\n""")
                                    sleep(1)
                                    heal_or_attack_func()


                            attack_damage_monster = (Monsters[monster]['Attack']['MaxDamage'] + Monsters[monster]['Attack']['MinDamage']) / 2
                            attack_damage_monster = round(attack_damage_monster)
                            print(f"\n{Monsters[monster]["Name"]} Stats:\nHP: {Monsters[monster]['HP']}\nAttack Damage: ~{attack_damage_monster}")
                            sleep(1)
                            print(f"\n{Player['Name']}'s Turn.")
                            heal_or_attack_func()

                            if Monsters[monster]['HP'] < 1:
                                print(f"You just defeated the {monster}")
                                sleep(1)

                                for loot in Monsters[monster]['Loot']:
                                    Player['Inventory'].append(loot)
                                print("Monster's loot has been collected.\n\n")
                                sleep(1)

                                Player['Current Room'] = direction[direction_i]
                                if monster == 'Spider':
                                    endings()

                                rooms_list_for_monsters.remove(direction[direction_i])
                                monsters_list.remove(monster)
                                return

                            print(f"\n{Monsters[monster]['Name']}'s Turn")
                            sleep(0.3)

                            damage_dealt_monster = randint(Monsters[monster]['Attack']['MinDamage'], Monsters[monster]['Attack']['MaxDamage'])

                            if 'Shield' in Player['Inventory']:
                                damage_dealt_monster = floor(damage_dealt_monster * 0.8)
                                Player['HP'] -= damage_dealt_monster
                            else:
                                Player['HP'] -= damage_dealt_monster

                            print(f"The Player was attacked by the monster and lost {damage_dealt_monster} HP.\n")
                            sleep(0.3)

                            if Player['HP'] < 0:
                                Player['HP'] = 0

                            print(f"Player Stats in Combat:\nName: {Player["Name"]}.\nHP: {Player["HP"]}")
                            sleep(0.3)


                            if Player['HP'] < 1:
                                print("\n\nGame Over. You have met your demise.")
                                sleep(0.1)
                                exit()

                    elif fight_ornot == 'no':
                        print("ok.\n")
                        sleep(0.3)
                        return

                    else:
                        print("""Invalid Input. Type in either "yes" or "no".""")
                        sleep(1)
                        fighting_ans()

            fighting_ans()

        else:
            Player['Current Room'] = direction[direction_i]

    def check_cmd():
        global direction_i
        global fight_ornot

        try:

            if command.lower() == '/help':
                print(
                    """\nMove either north, south, east or west to change rooms [command e.g: Move North].\nPick up an item [command e.g: Pick up 'torch']\nCheck inventory [command: Inv]\nSearching for the Use of an Item: Type in 'Search' to start searching the use of an item.\nType in 'Back' to undo any action [i.e. If healing/attacking was mistakenly selected during your phase while fighting a monster, typing in 'Back' will go back to the selection menu, exiting the search menu, etc.].\nExtra Info: When equipping/picking up a shield, the damage dealt by the monster will be reduced by 20%.\n""")
                sleep(1)

            elif command.lower().split()[0] == 'move':
                movements()

            elif command.lower() == 'inv':
                inventory_sorting(Player['Inventory'])
                print(f"Inventory: {', '.join(player_inventory_link)}.")

            elif command.lower() == 'search':
                SearchingItems.searching_items(items_list, items_list_definition)

            elif command.lower() == 'read passcode' and 'Passcode' in Player['Inventory']:
                print(f"The code is: The atomic number of the element '{ran_element}' plus the division of the square root of the number '{ran_num}' by 2. (make sure it is rounded to the nearest whole number)")
                sleep(1)

            elif command.lower().split()[0] == 'pick' and command.lower().split()[1] == 'up':
                items_index()

                if command.title().split()[2] in items_list and command.title().split()[2] in pick_up_items:
                    Player['Inventory'].append(pick_up_items[pick_up_items_i])
                    pick_up_items.pop(pick_up_items_i)

                    for char in pick_up_items:
                        if not char.isalpha():
                            char_i = pick_up_items.index(char)
                            pick_up_items.pop(char_i)

                    Dungeon[Player["Current Room"]]["Items"] = pick_up_items

                elif command.title().split()[2] in Player['Inventory']:
                    print("\nItem already exists in your inventory!\n")
                    sleep(0.3)

                else:
                    print("\nINVALID ITEM!\n")
                    sleep(1)

        except IndexError:
            pass

    check_cmd()

# ADDING FEATURE3: Make spacing between each statement to make it look organised.
# Finalise the code.
# ADDING FEATURE4: Add a split second so that the player can be able to see what happens as the statements are displaying.
# As always, good luck.... ig...