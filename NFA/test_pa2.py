# Name: test_pa2.py
# Author: Dr. Glick
# Date: September 18, 2023
# Description: Tests pa2 for comp 370, fall 2023

import dfa
import nfa

def read_results_file(filename):
    """
    Returns contents of file "filename" as a list
    """
    file = open(filename)
    return [True if result == "Accept" else False for result in file.read().split()]

def dfa_data_ok(equiv_dfa, nfa_filename):
    """
    Checks if the dfa equiv_dfa has correctly formatted data.
    num_states should be a positive integer
    The states should be numbered 1, ..., num_states
    The alphabet should be the same as for the nfa.
    Transitions should be defined for all combinations of states and alphaget symbols.
    start_state should be a valid state index
    accepting_states should be valid states indices.
    Returns True if all is ok, and False if not.

    """
    nfa_f = open(nfa_filename, "r")

    # Get num states in dfa
    states_list_dfa = list(range(1, equiv_dfa.num_states + 1))
    nfa_f.readline() # skip over num states in nfa

    # Check that dfa alphabet is correct
    nfa_alphabet = nfa_f.readline().rstrip('\n')
    if set(equiv_dfa.alphabet) != set(nfa_alphabet):
        print("  DFA alphabet does not match NFA")
        return False

    # Check the dfa transition function
    try:
        for state in states_list_dfa:
            for ch in equiv_dfa.alphabet:
                if equiv_dfa.transition(state, ch) not in states_list_dfa:
                    return False
    except Exception:
        print("  Invalid DFA file.  Invalid transition function")
        return False
    
    # Check start state
    if equiv_dfa.start_state not in states_list_dfa:
        print("DFA start state invalid")
        return False
    
    # Check accept states
    for state in equiv_dfa.accept_states:
        if state not in states_list_dfa:
            print("DFA accept states invalid")
            return False
    
    # Everything ok
    return True
    
    
if __name__ == "__main__":
    """
    Run all tests
    """
    num_test_files = 14 # One test file for each test NFA.
    num_correct = 0
    for i in range(1, num_test_files + 1):
        nfa_filename = f"nfa{i}.txt"
        dfa_filename = f"dfa{i}.txt"
        input_filename = f"str{i}.txt"
        correct_results_filename = f"correct{i}.txt"

        print(f"Testing NFA {nfa_filename} on strings from {input_filename}")
        try:
            # Create NFA
            this_nfa = nfa.NFA(nfa_filename)

            # Convert to DFA
            equiv_dfa = this_nfa.to_DFA()

            # Check the format of the DFA file
            if not dfa_data_ok(equiv_dfa, nfa_filename):
                print("  DFA file has incorrect format")
            else:
                # Open string file.
                string_file = open(input_filename)

                # Simulate DFA on test strings
                results = []
                for str in string_file:
                    results.append(equiv_dfa.simulate(str.strip()))

                # Get correct results
                correct_results = read_results_file(correct_results_filename)

                # Check if correct
                if results == correct_results:
                    print("  Correct results")
                    num_correct += 1
                else:
                    print("  Incorrect results")
                    print(f"  Your results = {results}")
                    print(f"  Correct results = {correct_results}")
                print()
        except OSError as err:
            print(f"Could not open file: {err}")
        except Exception as err:
          print(f"Error simulating dfa: {err}")

    if num_correct == num_test_files:
        print("All tests correct.  Nice job")
    else:
        print(f"Number NFAs tested = {num_test_files}")
        print(f"Number correct = {num_correct}")
        print(f"Keep working on it")