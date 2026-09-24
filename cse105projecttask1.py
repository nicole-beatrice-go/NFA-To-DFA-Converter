
# CHATGPT: "how can i fix this code to make a powerset? how can i make it so there are no duplicates?"
# CHATGPT: "why are there commas after my single items in tuples?"
# CHATGPT: "what is the difference between split and replace?"
# CHATGPT: "what is wrong with my for loop and if statements for my transition function?"
# CHATGPT: "how can i remove duplicates from a list?"

def main():
    NFAtoDFA()

def NFAtoDFA():
    user_input_NFA = input("Please input a NFA by it's formal definition (Q, Σ, δ, q₀, F) and separating commas for each component. Please define the transition function as a Python list of transitions for each combination of state and input (δ(q, a) = P(Q)) \n Ex. ({q₀, q₁, q₂}, {a, b}, [δ(q₀, a) = {q₁, q₂}, δ(q₁, b) = {q₂}], q₀, {q₁, q₂}): \n")
    split_after_transition = user_input_NFA.split("}],")
    components_before_start = split_after_transition[0].split("}, ", 2)
    components_after_transition = split_after_transition[1].split(",", 1)

    states_NFA = list(components_before_start[0].split(","))
    states_NFA[0] = states_NFA[0].strip("({")
    for i in range(len(states_NFA)):
        states_NFA[i] = states_NFA[i].strip()

    # alphabet would be same because DFA consumes the same input
    alphabet = list(components_before_start[1].split(","))
    alphabet[0] = alphabet[0].strip("{")
    for i in range(len(alphabet)):
        alphabet[i] = alphabet[i].strip()

    # converts transition function into the form of a dictionary where a tuple of the state and the input is the key, the power set (as a list) of possible states to go to is the value
    
    transition_function_NFA = list(components_before_start[2].split("},"))
    transition_function_NFA[0] = transition_function_NFA[0].strip("[")
    transition_function_dict_NFA = {}
    for item in transition_function_NFA:
        item = item.strip()
        item = item.replace("δ", "")
        item = item.replace(")", "")
        item = item.replace("(", "")
        item = item.replace("}", "")
        item = item.replace("{", "")
        split_input_output = item.split(" = ")
        if len(split_input_output) == 2:
            input_state_input = split_input_output[0].split(", ")
            if len(split_input_output) == 2:
                tuple_state_and_input = tuple(input_state_input)
                list_output_powerset_states = split_input_output[1].split(", ")
                transition_function_dict_NFA[tuple_state_and_input] = list_output_powerset_states
            else:
                print("Invalid format")
        else:
            print("Invalid format")
   
    #start state would be the same in DFA assuming there are no spontaneous moves 
    #(because there would then be no other states accessible from the start state that don't require consuming an input)
    start_state = components_after_transition[0]
    start_state = start_state.strip()

    accept_states_NFA = components_after_transition[1]
    accept_states_NFA = accept_states_NFA.replace(")", "")
    accept_states_NFA = accept_states_NFA.replace("(", "")
    accept_states_NFA = accept_states_NFA.replace("}", "")
    accept_states_NFA = accept_states_NFA.replace("{", "")
    accept_states_NFA = accept_states_NFA.strip()
    accept_states_NFA_list = accept_states_NFA.split(", ")
    if len(accept_states_NFA_list) > 1:
        for i in range(len(accept_states_NFA_list)):
            accept_states_NFA[i] = accept_states_NFA[i].strip()
            accept_states_NFA[i] = accept_states_NFA[i].strip("}{)()")





    # in the form of a list creates powerset of states_NFA (so all subsets of the set of states in NFA)
    # where each element is a Python tuple representing the subset/state
    
    states_DFA = []
    states_DFA.append(tuple())
    for item in states_NFA:
        states_DFA.append(tuple(item))
    for i in range(1 << len(states_NFA)):
        subset = []
        for j in range(len(states_NFA)):
            if i & (1 << j):
                subset.append(states_NFA[j])
        states_DFA.append(tuple(subset))
    states_DFA = list(set(states_DFA))
    states_DFA.sort()
    
    # creates dictionary of transitions in DFA form Q x Σ -> Q where Q is a state of the DFA (where states are subsets) and every input has an arrow
    # the keys are the input (as tuples) and the values are the output (a single tuple element of states_DFA)
    # empty set state points to itself
    
    transition_function_dict_DFA = {}
    for symbol in alphabet:
        transition_function_dict_DFA[(states_DFA[0], symbol)] = states_DFA[0]
    for state in states_DFA:
        for symbol in alphabet:
            list_accepted_from_multiple_state = []
            for item in state:
                if (item, symbol) in transition_function_dict_NFA:
                    output_string = str(transition_function_dict_NFA[(item, symbol)])  
                    final_output_string = output_string.replace('[', "").replace("]", "").replace("'", "")
                    final_output_string = final_output_string.strip("'")
                    integers = [int(substring) for substring in final_output_string.split(',')]
                    list_accepted_from_multiple_state.extend(integers)
                    list_accepted_from_multiple_state = sorted(set(list_accepted_from_multiple_state))

            transition_function_dict_DFA[(state, symbol)] = tuple(list_accepted_from_multiple_state)

    # creates list of accept states for DFA by checking if a state's subset contains and accept state and appends that state if it does
    # in the form of a list of tuples where each tuple is a state
    accept_states_DFA = []
    for state in states_DFA:
        for accept_state in accept_states_NFA_list:
            if accept_state in state:
                accept_states_DFA.append(state)
    

    string_states_DFA = ", ".join(map(str, states_DFA))
    string_states_DFA = "{" + string_states_DFA
    string_states_DFA = string_states_DFA + "}"

    string_alphabet_DFA = ", ".join(alphabet)
    string_alphabet_DFA = "{" + string_alphabet_DFA
    string_alphabet_DFA = string_alphabet_DFA + "}"

    string_transition_DFA = "["
    for key in transition_function_dict_DFA:
        string_value = str(transition_function_dict_DFA[key])
        string_value = string_value.replace("(", "{")
        string_value = string_value.replace(")", "}")
        string_transition_DFA = string_transition_DFA + "δ" + str(key) + " = " + string_value + ", " + "\n"
    string_transition_DFA = string_transition_DFA[:-3]
    string_transition_DFA = string_transition_DFA + "]"

    string_start_DFA = str(start_state)

    string_accept_states_DFA = ", ".join(map(str, accept_states_DFA))
    string_accept_states_DFA = "{" + string_accept_states_DFA
    string_accept_states_DFA = string_accept_states_DFA + "}"

    print("States: " + string_states_DFA + "\n")
    print("Alphabet: " + string_alphabet_DFA + "\n")
    print("Transition Function: " + "\n" + string_transition_DFA + "\n")
    print("Start State: " + string_start_DFA + "\n")
    print("Accept States: " + string_accept_states_DFA)
        


main()