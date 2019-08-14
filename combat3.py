from operator import attrgetter
import os

longest_creature_name = 8
longest_status_name = 6

class Creature(object):
    name = ''
    initiative = 0
    status_effect = {}

    def __init__(self, new_name, new_initiative):
        self.name = new_name
        self.initiative = new_initiative
        global longest_creature_name
        if len(new_name) > longest_creature_name:
            longest_creature_name = len(new_name)

    def __repr__(self):
        return self.name

    def rename(self, new_name):
        self.name = new_name

class PC(Creature):
    def __init__(self, new_name, new_initiative):
        super(PC, self).__init__(new_name, new_initiative)

    def __repr__(self):
        return self.name

class NPC(Creature):
    #name = '' # Shouldn't be needed; defined in Creature()
    max_hit_points = 0
    temp_hit_points = 0
    current_hit_points = 0
    armor_class = 0
    #status_effect = {} # Samesies

    def __init__(self, new_name, new_hit_points, new_armor_class, new_initiative):
        super(NPC, self).__init__(new_name, new_initiative)
        self.max_hit_points = new_hit_points
        self.current_hit_points = new_hit_points
        self.armor_class = new_armor_class
        self.initiative = new_initiative
        #self.temp_hit_points = 0 #defined in NPC(), so why here also?
        #self.status = {} #same here...

    def __repr__(self):
        return self.name

    def add_temp_hit_points(self):
        temp_hit_points_amount = input('  Temporary hit_points: ')
        self.temp_hit_points += temp_hit_points_amount

    def heal(self):
        heal_amount = input('  Heal: ')
        self.current_hit_points += heal_amount
        if self.current_hit_points > self.max_hit_points:
            self.current_hit_points = self.max_hit_points

    def hit(self):
        damage_amount = input('  Damage: ')
        if self.temp_hit_points > damage_amount:
            self.temp_hit_points -= damage_amount
        elif self.temp_hit_points < damage_amount:
            damage_amount -= self.temp_hit_points
            self.temp_hit_points = 0
            self.current_hit_points -= damage_amount
            if self.current_hit_points < 0:
                self.current_hit_points = 0
            if self.current_hit_points <= 0:
                return True
        return False

    def add_status_effect(self):
        new_status_effect = input('  Status effect name: ')
        duration = input("  Duration in rounds ('-' for infinite) ")
        if duration != '-':
            try:
                duration = int(duration) # only here for error-checking, python3 _should_ convert to int automatically
            except:
                print('Invalid duration')
                return
        self.status_effect[new_status_effect] = duration
        global longest_status_name
        if len(new_status_effect) > longest_status_name:
            longest_status_name = len(new_status_effect)

def remove_status_effect(self):
    to_remove = input('  Status effect to remove: ')
    to_remove = to_remove.lower()
    while to_remove not in self.status_effect.lower():
        to_remove = input('  Invalid status effect, try again: ')
        if to_remove == 'cancel':
            return
    del self.status_effect[to_remove]

def get_initiative(Creature):
    return Creature.initiative

def is_creature(creatures, to_check):
    for creature in creatures:
        if (creature.name == to_check):
            return True
    return False

def get_creatures():
    creatures = []
    is_PC = ''
    while is_PC != 'done':
        is_PC = input('PC, NPC, or done? ')
        is_PC = is_PC.lower()
        if is_PC == 'pc' or is_PC == 'p':
            PC_name = input('  PC name: ')
            while is_creature(creatures, PC_name):
                PC_name = input('  Invalid name. Try again: ')
            PC_initiative = input('  PC initiative: ')
            creatures.append(PC(PC_name, PC_initiative))
        elif is_PC == 'npc' or is_PC == 'n':
            NPC_name = input('  NPC name: ')
            while is_creature(creatures, NPC_name):
                NPC_name = input('  Invalid name. Try again: ')
            hit_points = input('  NPC hit_points: ')
            armor_class = input('  NPC AC: ')
            initiative = input('  NPC initiative: ')
            creatures.append(NPC(NPC_name, hit_points, armor_class, initiative))
        elif is_PC != 'done' or is_PC != 'd':
            print('Invalid command. Try again')
    return creatures

def add_creatures(existing_creatures):
    new_creatures = get_creatures()
    for to_add in new_creatures:
        existing_creatures.append(to_add)
    existing_creatures.sort(key=get_initiative, reverse=True)

def update(creatures, current):
    current_creature = creatures[current]
    if isinstance(current_creature, NPC):
        to_delete = []
        for effect in current_creature.status:
            if current_creature.status[effect] != '-':
                current_creature.status[effect] -= 1
                if current_creature.status[effect] < 0:
                    to_delete.append(effect)
        for item in to_delete:
            del current_creature.status[item]

def print_table(creatures, current_creature_number, message):
    # lengths
    current_creature = creatures[current_creature_number]
    creature_line_length = max(10, longest_creature_name + 2)
    status_line_length = max(8, longest_status_name + 2)
    creature_header = ' Creature ' + (' ' * (creature_line_length - 10))
    status_header = ' Status ' + (' ' * (status_line_length - 8))
    header_length = 35 + creature_line_length + status_line_length
    # lines
    main_line = '=' * header_length + '\n'
    big_creature_line = '=' * creature_line_length
    little_creature_line = '-' * creature_line_length
    big_status_line = '=' * status_line_length
    little_status_line = '-' * status_line_length
    big_separator = big_creature_line + '|=====|====|=====|=====|' + big_status_line + '|==========\n'
    little_separator = little_creature_line + '|---|-----|-----|' + little_status_line + '|----------\n'
    # table creator
    if message != '':
        table = message + '\n'
    else:
        table = ''
    table += main_line + ' CURRENT: ' + current_creature.name + '\n' + main_line + creature_header + '| No. | AC | HP  | THP |' + status_header + '| Duration\n' + big_separator
    index = 0
    for creature in creatures:
        table += ' ' + creature.name + ' ' + (' ' * (longest_creature_name - len(creature.name))) + '| '
        table += str(index) + ' '
        if index < 100:
            table += ' '
        if index < 10:
            table += ' '
        table += '| '
        index += 1
    if isinstance(creature, PC):
        table += '-  | -   | -   | - ' + (' ' * (status_line_length - 3)) + '| -\n'
    else:
        armor_class_buffer = ' '
        if creature.armor_class / 10 == 0:
            armor_class_buffer += ' '
        table += str(creature.armor_class) + armor_class_buffer + '| '

        hit_points_buffer = ''
        if creature.current_hit_points / 100 == 0:
            hit_points_buffer += ' '
            if creature.current_hit_points / 10 == 0:
                hit_points_buffer += ' '
        table += str(creature.current_hit_points) + hit_points_buffer + ' | '

        temp_hit_points_buffer = ''
        if creature.temp_hit_points / 100 == 0:
            temp_hit_points_buffer += ' '
            if creature.temp_hit_points / 10 == 0:
                temp_hit_points_buffer += ' '
        table += str(creature.temp_hit_points) + temp_hit_points_buffer + ' |'

        if creature.status_effect == {}:
            table += ' -' + (' ' * (status_line_length - 2)) + '| -\n'
        else:
            is_first = True
            for effect in creature.status_effect:
                if is_first:
                    is_first = False
                    table += ' ' + effect + (' ' * (status_line_length - len(effect) -1)) + '| '
                else:
                    table += (' ' * creature_line_length) + '|    |     | ' + effect + (' ' * (status_line_length - len(effect) - 1)) + '| '
                if creature.status_effect[effect] == '-':
                    table += u'\u221e' + '\n'
                else:
                    table += str(creature.status_effect[effect]) + '\n'
    table += main_line[:-1]
    os.system('clear')
    print(table)

def find_creature(creatures, to_find):
    try:
        to_find = int(to_find)
        ret = creatures[to_find]
        to_find = str(to_find)
        for creature in creatures:
            if creature.name == to_find:
                print('Creature found with name ' + to_find + '. Note, index overrides name.')
        return ret
    except:
        for creature in creatures:
            if creature.name == to_find:
                return creature
    return None

def get_target(creatures):
    target_command = input('  Target: ')
    target_creature = find_creature(creatures, target_command)
    while target_creature == None:
        target_command = input('  Invalid target, try again: ')
        target_creature = find_creature(creatures, target_command)
    return target_creature

def run_combat(creatures):
    print('Starting combat...')
    action = ''
    current_creature = 0
    print_table(creatures, current_creature, '')
    to_kill = []
    while action != 'end' and action != 'done':
        message = ''
        action = input('Action: ')
        action = action.lower()
        if action == 'next turn' or action == next or action == 'n':
            for dead in to_kill:
                message += 'Killed ' + dead.name + '\n'
                creatures.remove(dead)
                to_kill = []
            if len(creatures) <= 0:
                print('All creatures have died!')
                break
            current_creature += 1
            if current_creature >= len(creatures):
                current_creature = 0
                update(creatures, current_creature)

        elif action == 'hit' or action == 'h' or action == 'damage':
            target_creature = get_target(creatures)
            #may remove this bit when PCs get HP tracking
            if isinstance(target_creature, PC):
                message = 'Cannot target a PC'
            else:
                message = 'Hit ' + target_creature.name
                is_dead = target_creature.hit()
                if is_dead:
                    to_kill.append(target_creature)

        elif action == 'kill' or action == 'k' or action == 'remove':
            target_creature = get_target(creatures)
            message = 'Marked ' + target_creature.name + ' for death'
            to_kill.append(target_creature)

        elif action == 'add status' or action == 'stat':
            target_creature = get_target(creatures)
            #remove when PCs get status tracking
            if isinstance(target_creature, PC):
                message = 'Cannot target a PC'
            else:
                message = 'Added status from ' + target_creature.name()
                target_creature.add_status_effect()

        elif action == 'remove status' or action == 'unstat':
            target_creature = get_target(creatures)
            #remove when PCs get status tracking
            if isinstance(target_creature, PC):
                message = 'Cannot target a PC'
            else:
                message = 'Removed status from ' + target_creature.name()
                target_creature.remove_status_effect()

        elif action == 'heal':
            target_creature = get_target(creatures)
            #to be removed when PCs get HP tracking
            if isinstance(target_creature, PC):
                message = 'Cannot target a PC'
            else:
                message = 'Added temporary HP to ' + target_creature.name
                target_creature.add_temp_hit_points()

        elif action == 'add creatures' or action == 'add':
            add_creatures(creatures)
            creatures.sort(key=get_initiative, reverse=True)

        elif action == 'rename':
            target_creature = get_target(creatures)
            new_name = input('New name: ')
            target_creature.rename(new_name)

        print_table(creatures, current_creature, message)

def main():
    creatures = get_creatures()
    creatures.sort(key=get_initiative, reverse=True)
    run_combat(creatures)

main()