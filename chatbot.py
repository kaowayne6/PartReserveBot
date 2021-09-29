# CS 421: Natural Language Processing
# University of Illinois at Chicago
# Fall 2020
# Chatbot Project - Evaluation
#
# Do not rename/delete any functions or global variables provided in this template and write your solution
# in the specified sections. Use the main function to test your code when running it from a terminal.
# Avoid writing that code in the global scope; however, you should write additional functions/classes
# as needed in the global scope. These templates may also contain important information and/or examples
# in comments so please read them carefully.
# =========================================================================================================

# Import any necessary libraries here, but check with the course staff before requiring any external
# libraries.
import random
import re
from collections import defaultdict

dst = defaultdict(list)


# update_dst(input): Updates the dialogue state tracker
# Input: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is
#        most appropriate for the corresponding slot.  Defaults to an empty list.
# Returns: Nothing
def update_dst(input=[]):
    # If no input, nothing to update
    if not input:
        return
    # There is something to update
    else:
        # For each tuple in input, check for valid input for each key
        for key, val in input:

            # This updates user intent history
            if key == 'user_intent_history':
                # Valid inputs for intent history
                valid_intent = ['respond_part', 'respond_brand', 'respond_variation', 'respond_order_completion',
                                'respond_name', 'respond_time', 'respond_date']
                if str(val) in valid_intent:
                    dst[key].append(str(val))

            # This updates dialogue state history for dialogue policy
            elif key == 'dialogue_state_history':
                # Valid inputs
                valid_state = ['request_part', 'request_brand', 'request_variation', 'request_order_completion',
                               'request_name', 'request_time', 'request_date']
                if str(val) in valid_state:
                    dst[key].append(str(val))

            # This checks to see if the input user put in is a valid in stock item in store
            elif key == 'part':
                # All the valid responses for parts
                dst['parts_list'] = ['gpu', 'cpu', 'graphics card', 'ssd', 'ram', 'processor', 'hard drive',
                                     'motherboard', 'power supply']

                # If user typed an input that is in parts list, make sure aliases go together
                # This also adds a dictionary entry for the valid brands of the part they chose
                if val in dst['parts_list']:
                    # gpu = graphics card. Name under gpu
                    if val == 'gpu' or val == 'graphics card':
                        dst[key].append('gpu')
                        dst['gpu_brands'] = ['Nvidia']
                    # cpu = processor. Name under cpu
                    elif val == 'cpu' or val == 'processor':
                        dst[key].append('cpu')
                        dst['cpu_brands'] = ['Intel']

                    # For every other key, just append the part into key 'part'
                    # Also add the valid brands based on key
                    elif val == 'ssd':
                        dst[key].append(val)
                        dst['ssd_brands'] = ['Samsung', 'Sandisk', 'WD']
                    elif val == 'ram':
                        dst[key].append(val)
                        dst['ram_brands'] = ['Corsair', 'Kingston', 'HyperX']
                    elif val == 'hard drive':
                        dst[key].append(val)
                        dst['hard_drive_brands'] = ['Seagate', 'Toshiba']
                    elif val == 'motherboard':
                        dst[key].append(val)
                        dst['motherboard_brands'] = ['ASRock', 'Asus', 'EVGA', 'MSI', 'Gigabyte']
                    else:  # For power supply
                        dst[key].append(val)
                        dst['power_supply_brands'] = ['Cooler Master', 'Corsair', 'SeaSonic', 'EVGA', 'Thermaltake']

                    # when a valid response is given, update the user intent saying they responded
                    dst['user_intent_history'].append('respond_part')

            # If key is choosing brand, make sure it is a valid brand
            # Also make dictionary input for different variations in products within a brand
            elif key == 'brand':
                responded = False  # this checks to see if they gave a valid variation

                # Get the part the user entered earlier and figure out if it's a valid
                # brand from that part
                cur_part = dst['part'][-1]
                if cur_part == 'gpu':
                    if val in dst.get('gpu_brands'):
                        dst[key].append(val)
                        # Adds variation in products within a brand for next question
                        dst['gpu_variation'] = ['1070', '1080', '2070', '2080', '1660 Super']
                        responded = True
                elif cur_part == 'cpu':
                    if val in dst.get('cpu_brands'):
                        dst[key].append(val)
                        dst['cpu_variation'] = ['i7', 'i9']
                        responded = True
                elif cur_part == 'ssd':
                    if val in dst.get('ssd_brands'):
                        dst[key].append(val)
                        dst['ssd_variation'] = ['256GB', '500GB', '1TB']
                        responded = True
                elif cur_part == 'ram':
                    if val in dst.get('ram_brands'):
                        dst[key].append(val)
                        dst['ram_variation'] = ['8GB']
                        responded = True
                elif cur_part == 'hard drive':
                    if val in dst.get('hard_drive_brands'):
                        dst[key].append(val)
                        dst['hard_drive_variation'] = ['500GB', '1TB', '2TB']
                        responded = True
                elif cur_part == 'motherboard':
                    if val in dst.get('motherboard_brands'):
                        dst[key].append(val)
                        dst['motherboard_variation'] = ['Intel', 'AMD']
                        responded = True
                elif cur_part == 'power supply':  # Power supply
                    if val in dst.get('power_supply_brands'):
                        dst[key].append(val)
                        dst['power_supply_variation'] = ['600W', '700W', '12000W']
                        responded = True

                # If user entered a valid brand, then update user intent history
                if responded:
                    dst['user_intent_history'].append('respond_brand')

            # Check to see if variation input is correct. If so, add variations to dict and
            # Add part, brand, variation in a tuple to cart.
            # Also update intent history
            elif key == 'variations':
                addedVariation = False
                cur_part = dst.get('part')[-1]
                if cur_part == 'gpu':
                    if val in dst.get('gpu_variation'):
                        dst[key].append(val)
                        addedVariation = True
                elif cur_part == 'cpu':
                    if val in dst.get('cpu_variation'):
                        dst[key].append(val)
                        addedVariation = True
                elif cur_part == 'ssd':
                    if val in dst.get('ssd_variation'):
                        dst[key].append(val)
                        addedVariation = True
                elif cur_part == 'ram':
                    if val in dst.get('ram_variation'):
                        dst[key].append(val)
                        addedVariation = True
                elif cur_part == 'hard drive':
                    if val in dst.get('hard_drive_variation'):
                        dst[key].append(val)
                        addedVariation = True
                elif cur_part == 'motherboard':
                    if val in dst.get('motherboard_variation'):
                        dst[key].append(val)
                        addedVariation = True
                elif cur_part == 'power supply':  # Power supply
                    if val in dst.get('power_supply_variation'):
                        dst[key].append(val)
                        addedVariation = True
                # Updates intent history and adds the item they wanted to cart for retrieval later
                if addedVariation:
                    dst['cart'].append((dst.get('part')[-1], dst.get('brand')[-1], dst.get('variations')[-1]))
                    dst['user_intent_history'].append('respond_variation')

            # This is when user is done with order and is asked for a name
            # This just make sure the string entered is all alphabetical
            # This also updates the user intent history
            elif key == 'name':
                name_t = val.split()
                for word in name_t:
                    if not word.isalpha():
                        return
                dst[key] = val
                dst['user_intent_history'].append('respond_name')

            # When user is asked for time and enter a time
            # For now, the program just checks if the input is a number (assuming like a 9-5 store opening)
            # Updates user intent
            elif key == 'time':
                # If the input is like 9:35
                if ':' in val:
                    temp = str(val).split(':')
                    try:
                        i1 = int(temp[0])
                        i2 = int(temp[1])
                        if i1 <= 0 or i1 > 12 or i2 < 0 or i2 > 60:
                            return
                        dst[key] = [temp[0], temp[1]]
                        dst['user_intent_history'].append('respond_time')
                    except:
                        print('Not valid time')
                # If the input is just like 4
                else:
                    try:
                        num = int(val)
                        if num <= 0 or num > 12:
                            print('Not valid time')
                            return
                        dst['time'] = num
                        dst['user_intent_history'].append('respond_time')
                    except:
                        print('Not a number')

            # This stores the date the user wants to pick up
            # For now, the date is entered like 9/18 for month/date
            # The program only takes the first two numbers ie before and after slash
            # Updates user intent history
            elif key == 'date':
                if '/' in str(val):
                    temp = str(val).split('/')
                    try:
                        i1 = int(temp[0])
                        i2 = int(temp[1])
                        if i1 <= 0 or i1 > 12 or i2 <= 0 or i2 > 31:
                            print('Date not valid')
                            return
                        dst[key] = [temp[0], temp[1]]
                        dst['user_intent_history'].append('respond_date')
                    except:
                        print('Date not valid')

            else:
                print('Not valid key')
    return

# Flow of bot
# Bot greets user and request part (changes intent_history to request_part)
# User enters input --> parse for parts list, if no parts found, fill ['part'] in dict with 'unknown' (update_dst)
# Bot asks for brand and request_brand
# User enters input --> parse for brands list, if no parts found, fill ['brand'] in dict with 'unknown' (update_dst)
# Bot asks for variation and request_variation
# User enters input --> parse for variations, if no variations found, fill ['variation'] in dict with unknown(update)
# Bot asks if user wants to continue reserving request_order_completion
# User enters data --> if valid no, change dialogue state history to 'request_part',
#                  --> if invalid input, don't do anything.
#                  --> if valid yes, change dialogue state history to 'request_name' and change
#                           user_intent to 'respond_order_completion
# Bot asks for name request_name
# User enters input --> update(dst)
# Bot asks for date request_date
# User enters input --> update(dst)
# Bot gives summary of order

# nlu(input): Interprets a natural language input and identifies relevant slots and their values
# Input: A string of text.
# Returns: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is most
#          appropriate for the corresponding slot.  If no slot values are extracted, the function should
#          return an empty list.
def nlu(input=""):
    # [YOUR CODE HERE]

    # In this code, the dialogue_state_history gets changed but not the intent_history
    # Return user_intent and then the data they got you

    # Dummy code for sample output (delete or comment out when writing your code!):
    slots_and_values = []

    # To narrow the set of expected slots, you may (optionally) first want to determine the user's intent,
    # based on what the chatbot said most recently.
    user_intent = dst['dialogue_state_history'][-1]
    # Fill out user intent based on the last index of user intent
    # valid_intent = ['respond_part', 'respond_brand', 'respond_variation', 'respond_order_completion',
    #                                 'respond_name', 'respond_time', 'respond_date']
    # valid_state = ['request_part', 'request_brand', 'request_variation', 'request_order_completion',
    #               'request_name', 'request_time', 'request_date']

    # If dialogue intent history is request part, check for a valid part
    if user_intent == 'request_part':
        # Compile patterns for all parts
        pt_list = ['gpu', 'cpu', 'ssd', 'ram', 'hard drive', 'motherboard', 'power supply']
        temp = input.lower()
        pattern_array = []
        pattern = re.compile(r"\b(gpu)|(graphics card)\b")
        pattern2 = re.compile(r"\b(cpu)|(processor)\b")
        pattern3 = re.compile(r"\b(ssd)|(solid state drive)\b")
        pattern4 = re.compile(r"\b(ram)\b")
        pattern5 = re.compile(r"\b(hard drive)|(hdd)\b")
        pattern6 = re.compile(r"\b(motherboard)\b")
        pattern7 = re.compile(r"\b(power supply)|(psu)\b")
        pattern_array.append(pattern)
        pattern_array.append(pattern2)
        pattern_array.append(pattern3)
        pattern_array.append(pattern4)
        pattern_array.append(pattern5)
        pattern_array.append(pattern6)
        pattern_array.append(pattern7)
        count = 0

        # Try to match the string with a part
        for pat in pattern_array:
            match = re.search(pat, temp)
            if match:
                u_var = [('part', pt_list[count])]
                update_dst(u_var)
                return u_var
            count += 1

        # No valid part found so return unknown
        dst['part'] = ['unknown']
        u_var = [('part', 'unknown')]
        update_dst(u_var)
        return u_var

    # If dialogue is request brand, search for a valid brand
    elif user_intent == 'request_brand':
        # Compile brands based on what part
        ssd_brands = ['Samsung', 'Sandisk', 'WD']
        ram_brands = ['Corsair', 'Kingston', 'HyperX']
        hd_brands = ['Seagate', 'Toshiba']
        mb_brands = ['ASRock', 'Asus', 'EVGA', 'MSI', 'Gigabyte']
        psu_brands = ['Cooler Master', 'Corsair', 'SeaSonic', 'EVGA', 'Thermaltake']
        gpu_brands = ['Nvidia']
        cpu_brands = ['Intel']
        brands = [ssd_brands, ram_brands, hd_brands, mb_brands, psu_brands, gpu_brands, cpu_brands]
        temp = input.lower()
        pattern_array = []
        pattern = re.compile(r"\b(samsung)|(sandisk)|(wd)\b")
        pattern2 = re.compile(r"\b(corsair)|(kingston)|(hyperx)\b")
        pattern3 = re.compile(r"\b(seagate)|(toshiba)\b")
        pattern4 = re.compile(r"\b(asrock)|(asus)|(evga)|(msi)|(gigabyte)\b")
        pattern5 = re.compile(r"\b(cooler master)|(corsair)|(seasonic)|(evga)|(thermaltake)\b")
        pattern6 = re.compile(r"\b(nvidia)\b")
        pattern7 = re.compile(r"\b(intel)\b")
        pattern_array.append(pattern)
        pattern_array.append(pattern2)
        pattern_array.append(pattern3)
        pattern_array.append(pattern4)
        pattern_array.append(pattern5)
        pattern_array.append(pattern6)
        pattern_array.append(pattern7)

        # Searches which pattern matches
        for part_idx in range(len(brands)):
            match = re.search(pattern_array[part_idx], temp)
            if match:
                # Searches which brand in a certain pattern level (pattern, pattern2, etc..) if matches
                for bd in range(len(brands[part_idx])):
                    if brands[part_idx][bd].lower() in temp:
                        u_var = [('brand', brands[part_idx][bd])]
                        update_dst(u_var)
                        return u_var
        # No match so return unknown
        dst['brand'] = ['unknown']
        u_var = [('brand', 'unknown')]
        update_dst(u_var)
        return u_var

    # When dialogue is at request variation
    elif user_intent == 'request_variation':

        # Compile patterns for each part variation
        ssd_variation = ['256GB', '500GB', '1TB']
        ram_variation = ['8GB']
        hd_variation = ['500GB', '1TB', '2TB']
        mb_variation = ['Intel', 'AMD']
        psu_variation = ['600W', '700W', '12000W']
        gpu_variation = ['1070', '1080', '2070', '2080', '1660 Super']
        cpu_variation = ['i7', 'i9']

        brands = [ssd_variation, ram_variation, hd_variation, mb_variation, psu_variation, gpu_variation, cpu_variation]
        temp = input.lower()
        pattern_array = []
        pattern = re.compile(r"\b(256gb)|(500gb)|(1tb)\b")
        pattern2 = re.compile(r"\b(8gb)\b")
        pattern3 = re.compile(r"\b(500gb)|(1tb)|(2tb)\b")
        pattern4 = re.compile(r"\b(intel)|(amd)\b")
        pattern5 = re.compile(r"\b(600w)|(700w)|(12000w)\b")
        pattern6 = re.compile(r"\b(1070)|(1080)|(2070)|(2080)|(1660 super)\b")
        pattern7 = re.compile(r"\b(i7)|(i9)\b")
        pattern_array.append(pattern)
        pattern_array.append(pattern2)
        pattern_array.append(pattern3)
        pattern_array.append(pattern4)
        pattern_array.append(pattern5)
        pattern_array.append(pattern6)
        pattern_array.append(pattern7)

        # Searches which pattern matches
        count = 0
        for part_idx in range(len(brands)):
            match = re.search(pattern_array[part_idx], temp)
            # If match, search which variation in this certain pattern
            if match:
                for bd in range(len(brands[count])):
                    if brands[part_idx][bd].lower() in temp:
                        u_var = [('variations', brands[count][bd])]
                        update_dst(u_var)
                        return u_var
            count += 1

        # No matches so return unknown
        u_var = [('variations', 'unknown')]
        update_dst(u_var)
        return u_var

    # When bot asks user if they want to order more
    elif user_intent == 'request_order_completion':
        temp = input.lower()
        # Check if pattern matches 'yes'
        pattern = re.compile(r"\b(yes)\b")
        match = re.search(pattern, temp)
        if match:
            dst_u = [('dialogue_state_history', 'request_name'), ('user_intent_history', 'respond_order_completion')]
            update_dst(dst_u)
            return dst_u

        # Check if pattern matches 'no'
        pattern = re.compile(r"\b(no)\b")
        match = re.search(pattern, temp)
        if match:
            dst_u = [('dialogue_state_history', 'request_part')]
            update_dst(dst_u)
            return dst_u

        # If input doesn't match yes or no
        return []

    # When user is done ordering and bot requests name
    # Update_dst takes care of this so just call it
    elif user_intent == 'request_name':
        dst_u = [('name', input)]
        update_dst(dst_u)
        return dst_u

    # When user is done ordering and bot requests time
    # Update_dst takes care of this so just call it
    elif user_intent == 'request_time':
        dst_u = [('time', input)]
        update_dst(dst_u)
        return dst_u

    # When user is done ordering and bot requests date
    # Update_dst takes care of this so just call it
    elif user_intent == 'request_date':
        dst_u = [('date', input)]
        update_dst(dst_u)
        return dst_u

    # Based on user intent, try to parse different things in the string to match a certain value in a certain
    # state in which the user intent is in

    return slots_and_values

    # if "dialogue_state_history" in dst:
    #     if dst["dialogue_state_history"][0] == "request_size":
    #         # Check to see if the input contains a valid size.
    #         pattern = re.compile(r"\b([Ss]mall)|([Mm]edium)|([Ll]arge)\b")
    #         match = re.search(pattern, input)
    #         if match:
    #             user_intent = "respond_size"
    #             slots_and_values.append(("user_intent_history", "respond_size"))
    #         else:
    #             user_intent = "unknown"
    #             slots_and_values.append(("user_intent_history", "unknown"))
    # # If you're maintaining a dialogue state history but there's nothing there yet, this is probably the
    # # first input of the conversation!
    # else:
    #     user_intent = "greeting"
    #     slots_and_values.append(("user_intent_history", "greeting"))
    #
    # # Then, based on what type of user intent you think the user had, you can determine which slot values
    # # to try to extract.
    # if user_intent == "respond_size":
    #     # In our sample chatbot, there's only one slot value we'd want to extract if we thought the user
    #     # was responding with a pizza size.
    #     pattern = re.compile(r"\b[Ss]mall\b")
    #     contains_small = re.search(pattern, input)
    #
    #     pattern = re.compile(r"\b[Mm]edium\b")
    #     contains_medium = re.search(pattern, input)
    #
    #     pattern = re.compile(r"\b[Ll]arge\b")
    #     contains_large = re.search(pattern, input)
    #
    #     # Note that this if/else block wouldn't work perfectly if the input contained, e.g., both "small"
    #     # and "medium" ... ;)
    #     if contains_small:
    #         slots_and_values.append(("pizza_size", "small"))
    #     elif contains_medium:
    #         slots_and_values.append(("pizza_size", "medium"))
    #     elif contains_large:
    #         slots_and_values.append(("pizza_size", "large"))


# get_dst(slot): Retrieves the stored value for the specified slot, or the full dialogue state at the
#                current time if no argument is provided.
# Input: A string value corresponding to a slot name.
# Returns: A dictionary representation of the full dialogue state (if no slot name is provided), or the
#          value corresponding to the specified slot.
def get_dst(slot=""):
    # If slot is empty, return whole dst
    if slot == "":
        return dst
    # Return slot
    else:
        return dst.get(slot)


# dialogue_policy(dst): Selects the next dialogue state to be uttered by the chatbot.
# Input: A dictionary representation of a full dialogue state.
# Returns: A string value corresponding to a dialogue state, and a list of (slot, value) pairs necessary
#          for generating an utterance for that dialogue state (or an empty list of no (slot, value) pairs
#          are needed).
def dialogue_policy(dst=[]):
    next_state = ""
    slot_values = []
    l_dialogue = None
    l_intent = None
    if dst:
        l_dialogue = len(dst['dialogue_state_history']) - 1
        l_intent = len(dst['user_intent_history']) - 1

    if not dst:
        update_dst([('dialogue_state_history', 'request_part')])
        next_state = "greeting"

    # Ask user for next part if they said yes
    elif dst['dialogue_state_history'][l_dialogue] == 'request_part' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][-1] == 'respond_variation':
        update_dst([('dialogue_state_history', 'request_part')])
        next_state = "ask_part"
        slot_values = dst['parts_list']

    # # If user didn't enter a valid part, ask them again sending them the list of options
    elif (bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_part') \
            and (not dst['user_intent_history'] or dst['user_intent_history'][l_intent] == 'respond_variation'):
        next_state = 'ask_part'
        slot_values = dst['parts_list']

    # User picked valid part and now asking user which choice of brand did they want to buy from
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_part' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_part':
        update_dst([('dialogue_state_history', 'request_brand')])
        cur_part = dst['part'][-1]
        choiceList = None
        # Figuring out which brand is availible
        if cur_part == 'gpu':
            choiceList = dst['gpu_brands']
        elif cur_part == 'cpu':
            choiceList = dst['cpu_brands']
        elif cur_part == 'ssd':
            choiceList = dst['ssd_brands']
        elif cur_part == 'ram':
            choiceList = dst['ram_brands']
        elif cur_part == 'hard drive':
            choiceList = dst['hard_drive_brands']
        elif cur_part == 'motherboard':
            choiceList = dst['motherboard_brands']
        elif cur_part == 'power supply':
            choiceList = dst['power_supply_brands']

        slot_values = choiceList
        if len(choiceList) == 1:
            next_state = 'one_brand'
        else:
            next_state = 'multiple_brand'

    # If user didn't enter a valid brand, ask them again sending them the list of options
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_brand' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] != 'respond_brand':
        # Figuring out which brand is availible
        cur_part = dst['part'][-1]
        choiceList = None
        if cur_part == 'gpu':
            choiceList = dst['gpu_brands']
        elif cur_part == 'cpu':
            choiceList = dst['cpu_brands']
        elif cur_part == 'ssd':
            choiceList = dst['ssd_brands']
        elif cur_part == 'ram':
            choiceList = dst['ram_brands']
        elif cur_part == 'hard drive':
            choiceList = dst['hard_drive_brands']
        elif cur_part == 'motherboard':
            choiceList = dst['motherboard_brands']
        elif cur_part == 'power supply':
            choiceList = dst['power_supply_brands']
        next_state = 'ask_brand'
        slot_values = choiceList

    # User entered a valid brand and now asking which variation they want
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_brand' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_brand':
        update_dst([('dialogue_state_history', 'request_variation')])
        cur_part = dst['part'][-1]
        choiceList = None
        # Figuring out which brand is availible
        if cur_part == 'gpu':
            choiceList = dst['gpu_variation']
        elif cur_part == 'cpu':
            choiceList = dst['cpu_variation']
        elif cur_part == 'ssd':
            choiceList = dst['ssd_variation']
        elif cur_part == 'ram':
            choiceList = dst['ram_variation']
        elif cur_part == 'hard drive':
            choiceList = dst['hard_drive_variation']
        elif cur_part == 'motherboard':
            choiceList = dst['motherboard_variation']
        elif cur_part == 'power supply':
            choiceList = dst['power_supply_variation']

        slot_values = choiceList
        if len(choiceList) == 1:
            next_state = 'one_variation'
        else:
            next_state = 'multiple_variation'

    # If user didn't enter a valid variation, ask them again sending them the list of options
    elif (bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_variation') and \
            (bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_brand'):
        # Figuring out which brand is availible
        cur_part = dst['part'][-1]
        choiceList = None
        if cur_part == 'gpu':
            choiceList = dst['gpu_variation']
        elif cur_part == 'cpu':
            choiceList = dst['cpu_variation']
        elif cur_part == 'ssd':
            choiceList = dst['ssd_variation']
        elif cur_part == 'ram':
            choiceList = dst['ram_variation']
        elif cur_part == 'hard drive':
            choiceList = dst['hard_drive_variation']
        elif cur_part == 'motherboard':
            choiceList = dst['motherboard_variation']
        elif cur_part == 'power supply':
            choiceList = dst['power_supply_variation']
        next_state = 'ask_variation'
        slot_values = choiceList

    # User entered a valid variation
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_variation' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_variation':
        update_dst([('dialogue_state_history', 'request_order_completion')])
        next_state = 'ask_complete_order'

    # # User entered wrong input for bot asking if they want to reserve more items
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_order_completion' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_variation':
        next_state = 'ask_complete_order'

    # User completed order and now asking for name. If user wanted to keep reserving, a code would
    # update_dst so that it's part, variation, and brand values are reset and update to request_part
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_name' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_order_completion':
        update_dst([('dialogue_state_history', 'request_name')])
        next_state = 'name'

    # # User didn't enter a valid name, so ask again
    # elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_name' \
    #         and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] != 'respond_order_completion':
    #     next_state = 'ask_name_again'
    # # FIX HERE

    # User entered name and transition to time
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_name' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_name':
        update_dst([('dialogue_state_history', 'request_time')])
        next_state = 'time'

    # User entered wrong time so ask again
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_time' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_name':
        next_state = 'ask_time'

    # User entered time and now asking for a date
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_time' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_time':
        update_dst([('dialogue_state_history', 'request_date')])
        next_state = 'date'

    # User entered date but wrong date format
    elif bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_date' \
            and bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_time':
        next_state = 'ask_date'

    # User entered name and transition to time
    elif (bool(dst['dialogue_state_history']) and dst['dialogue_state_history'][l_dialogue] == 'request_date') \
            and (bool(dst['user_intent_history']) and dst['user_intent_history'][l_intent] == 'respond_date'):
        slot_values = dst['cart']
        next_state = 'end'

    return next_state, slot_values
    # Dummy code for sample output (delete or comment out when writing your code!):
    # next_state = "clarification"
    # slot_values = [("num_pizzas", 5)]
    # return next_state, slot_values


# This function makes all the templates for each possible state in dst
def init_template():
    dst['templates'] = {}

    dst['templates']['greeting'] = ['Hi, how can I assist you?', 'Hi, what can I reserve for you?']

    dst['templates']['parts_list'] = ['We have <parts> in the store currently. Which part would you like?',
                                      'Currently, the parts we can reserve for you are: <parts>']

    dst['templates']['one_brand'] = ['We have brand <brand> available in store. Choose what brand you would like.',
                                     'We currently have this brand <brand>. Please choose your brand.']
    dst['templates']['multiple_brand'] = ['We have the brands <brands> available in store. Which would you like?',
                                          'For this part, the brands in the store is <brands>. Which would you prefer?']
    dst['templates']['ask_brand'] = ['The brands we have are: <brands>. Please choose a brand from this list.',
                                     'We have the following brands: <brands>. Choose one from this list.']

    dst['templates']['one_variation'] = ['We have this variation: <variation> ,available in store. Choose the variation.',
                                         'For this brand, we have this variation in the store <variation>. Choose the variation.']
    dst['templates']['multiple_variation'] = [
        'We have the variations: <variations> ,available in store. Which would you like?',
        'For this part, the variations in the store is: <variations>. Which would you prefer?']
    dst['templates']['ask_variations'] = [
        'The variations we have are: <variations>. Please choose a brand from this list.',
        'We have the following variations: <variations>. Choose one from this list.']

    dst['templates']['ask_complete_order'] = ['Did you want to complete your reservation?',
                                              'Is that all that you want to reserve?']
    dst['templates']['name'] = ['What name did you want to reserve under?',
                                'Under what name is this order going to be reserved under?']
    dst['templates']['ask_name_again'] = ['Please enter a valid name. (alphabetical)',
                                          'The time you entered is not valid. Please use this format: (alphabetical)']
    dst['templates']['time'] = ['What time did you want to pick up?',
                                'When, at what time, are you picking up?']
    dst['templates']['ask_time'] = ['Please enter a valid time: 0-12 or #:##',
                                    'The time you entered is not valid. Please use this format: 0-12 or #:##']
    dst['templates']['date'] = ['What date would you like to pickup?', 'When, at what date, would you like to pickup?']
    dst['templates']['ask_date'] = ['Please enter a valid date: ##/##',
                                    'The time you entered is not valid. Please use this format: ##/##']
    dst['templates']['end'] = ['This is your reservation:\n<reservation>It will be ready at your designated time.',
                               'You reserved:\n<reservation>This will be ready for pickup at your specified time.']
    return


# nlg(state, slots=[]): Generates a surface realization for the specified dialogue act.
# Input: A string indicating a valid state, and optionally a list of (slot, value) tuples.
# Returns: A string representing a sentence generated for the specified state, optionally
#          including the specified slot values if they are needed by the template.
def nlg(state, slots=[]):
    # Initialize variables
    output = None
    rand = random.randint(0, 1)

    # This adds to dst a key 'template' that stores a a dictionary with a bunch of keys and its values
    init_template()

    # For parts list, replace parts with a list of all parts
    if state == 'ask_part':
        output = dst['templates']['parts_list'][rand]
        output = output.replace("<parts>", str(slots))

    # All having to do with replacing the brand, either multiple or one brand. It also covers
    # when user doesn't pick a valid brand and prints a list of the brands for a part
    elif state == 'one_brand':
        output = dst['templates']['one_brand'][rand]
        output = output.replace("<brand>", str(slots))
    elif state == 'multiple_brand':
        output = dst['templates']['multiple_brand'][rand]
        output = output.replace("<brands>", str(slots))
    elif state == 'ask_brand':
        output = dst['templates']['ask_brand'][rand]
        output = output.replace("<brands>", str(slots))

    # All having to do with replacing the variations, either multiple or one variation. It also covers
    # when user doesn't pick a valid variation and prints a list of the variations for a brand
    elif state == 'one_variation':
        output = dst['templates']['one_variation'][rand]
        output = output.replace("<variation>", str(slots))
    elif state == 'multiple_variation':
        output = dst['templates']['multiple_variation'][rand]
        output = output.replace("<variations>", str(slots))
    elif state == 'ask_variation':
        output = dst['templates']['ask_variation'][rand]
        output = output.replace("<variations>", str(slots))

    # This case covers when the user is at the end and we just print out what they reserved.
    elif state == 'end':
        str_reservation = ''

        for i in range(len(slots)):
            str_reservation += '|Part: ' + slots[i][0] + ' |Brand: ' + slots[i][1] + ' |Variation: ' + slots[i][
                2] + '\n'
        output = dst['templates']['end'][rand]
        output = output.replace("<reservation>", str_reservation)

    # All other cases, just grab a random template from dst. Slots are not needed for these templates
    else:
        output = dst['templates'][state][rand]

    return output


# Use this main function to test your code when running it from a terminal
# Sample code is provided to assist with the assignment, feel free to change/remove it if you want
# You can run the code from terminal as: python3 chatbot.py

def main():
    
    # You can choose whether your chatbot or the participant will make the first dialogue utterance.
    # In the sample here, the chatbot makes the first utterance.
    current_state_tracker = get_dst()
    next_state, slot_values = dialogue_policy(current_state_tracker)
    output = nlg(next_state, slot_values)
    print('Bot: ' + output)

    # With our first utterance complete, we'll enter a loop for the rest of the dialogue.  In some cases,
    # especially if the participant makes the first utterance, you can enter this loop directly without
    # needing the previous code block.
    while next_state != "end":
        # Accept the user's input.
        print('User: ', end='')
        user_input = input()

        # Perform natural language understanding on the user's input.
        slots_and_values = nlu(user_input)
        # print(slots_and_values)

        # UPDATE DST IS DONE IN FUNCTION. NO NEED TO DO IT HERE

        # Get the full contents of the dialogue state tracker at this time.
        current_state_tracker = get_dst()

        # Determine which state the chatbot should enter next.
        next_state, slot_values = dialogue_policy(current_state_tracker)

        # for dct in dst:
        #     print(repr(dct), ":", dst[dct])
        # print('State: ' + str(next_state))
        # print('Slot: ' + str(slot_values))

        # Generate a natural language realization for the specified state and slot values.
        output = nlg(next_state, slot_values)

        # Print the output to the terminal.
        print('Bot: ' + output)



################ Do not make any changes below this line ################
if __name__ == '__main__':
    main()
