"""
================================================================================
CS4306: Algorithm Analysis - Assignment 1
Team Members: A.J. Robinson, Amir Aissat, Geza Martiny, Noor Muhammad
--------------------------------------------------------------------------------
(c) Pseudo-code of the Modified Gale-Shapley Algorithm:

Initialize all residents as unassigned/free
Initialize all hospital open slots to their maximum capacity
Initialize each hospital's current matchings as an empty list

While there is an unassigned resident who still has hospitals left to propose to:
    Let r be that resident
    Let h be the top preferred hospital on r's list that r has not proposed to yet
    
    r proposes to h
    If h has open slots available:
        Assign r to h
    Else (h is full):
        Let worst_resident be the resident currently assigned to h whom h prefers least
        If h prefers r to worst_resident:
            Unassign worst_resident (make them free/unassigned again)
            Assign r to h
        Else:
            r remains unassigned (h rejects r)
================================================================================
"""

def parse_input_file(file_path):
    """
    Step 1: Parse the input file format (Hospitals, Slots, Preferences)
    separated by a blank line from Residents and their Preferences.
    """
    hospitals = {}
    residents = {}
    parsing_residents = False

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                # A blank line indicates switching from parsing hospitals to residents
                parsing_residents = True
                continue

            parts = [p.strip() for p in line.split(',')]
            
            if not parsing_residents:
                # Parsing Hospital: NAME, SLOTS, RESIDENT_1, RESIDENT_2, ...
                name = parts[0]
                slots = int(parts[1])
                pref_list = parts[2:]
                
                # Inverse lookup dictionary for O(1) preference comparison
                pref_lookup = {res_name: idx for idx, res_name in enumerate(pref_list)}
                
                hospitals[name] = {
                    "slots": slots,
                    "preferences": pref_list,
                    "lookup": pref_lookup,
                    "current_matches": []
                }
            else:
                # Parsing Resident: NAME, HOSPITAL_1, HOSPITAL_2, ...
                name = parts[0]
                pref_list = parts[1:]
                residents[name] = {
                    "preferences": pref_list,
                    "current_hospital": None,
                    "next_proposal_idx": 0
                }
                
    return hospitals, residents


def run_modified_gale_shapley(hospitals, residents):
    """
    Step 3: Implement the Modified Gale-Shapley Core Logic
    Handles multiple slots per hospital and a surplus of medical students.
    """
    free_residents = list(residents.keys())

    while free_residents:
        r_name = free_residents.pop(0)
        r_data = residents[r_name]

        # If the resident has exhausted their preference list, they remain unassigned
        if r_data["next_proposal_idx"] >= len(r_data["preferences"]):
            continue

        # Get top preferred hospital that r has not proposed to yet
        h_name = r_data["preferences"][r_data["next_proposal_idx"]]
        r_data["next_proposal_idx"] += 1 

        if h_name not in hospitals:
            free_residents.append(r_name)
            continue

        h_data = hospitals[h_name]

        # Case A: Hospital has open slots available
        if len(h_data["current_matches"]) < h_data["slots"]:
            h_data["current_matches"].append(r_name)
            r_data["current_hospital"] = h_name

        # Case B: Hospital is completely full
        else:
            worst_resident = max(
                h_data["current_matches"], 
                key=lambda x: h_data["lookup"].get(x, float('inf'))
            )

            r_rank = h_data["lookup"].get(r_name, float('inf'))
            worst_rank = h_data["lookup"].get(worst_resident, float('inf'))

            if r_rank < worst_rank:
                h_data["current_matches"].remove(worst_resident)
                residents[worst_resident]["current_hospital"] = None
                free_residents.append(worst_resident)

                h_data["current_matches"].append(r_name)
                r_data["current_hospital"] = h_name
            else:
                free_residents.append(r_name)

    return hospitals, residents


def verify_stability(hospitals, residents):
    """
    Step 4: Build the Stability Checker Function per instruction (b).
    Checks for both Type 1 and Type 2 instabilities.
    """
    # Check Type 1 Instability: h prefers an unassigned resident s' to an assigned resident s
    for r_name, r_data in residents.items():
        if r_data["current_hospital"] is None:  # s' is unassigned
            for h_name, h_data in hospitals.items():
                # If hospital has matches, find their least preferred assigned resident s
                if h_data["current_matches"]:
                    worst_assigned = max(h_data["current_matches"], key=lambda x: h_data["lookup"].get(x, float('inf')))
                    
                    # Does hospital h prefer unassigned s' over their worst assigned s?
                    rank_s_prime = h_data["lookup"].get(r_name, float('inf'))
                    rank_s = h_data["lookup"].get(worst_assigned, float('inf'))
                    
                    if rank_s_prime < rank_s:
                        print(f"Type 1 Instability Found: {h_name} prefers unassigned {r_name} over assigned {worst_assigned}")
                        return False

    # Check Type 2 Instability: s is at h, s' is at h', but h prefers s' to s AND s' prefers h to h'
    for r_name, r_data in residents.items():
        h_name = r_data["current_hospital"]
        if h_name is None:
            continue
            
        for r_prime_name, r_prime_data in residents.items():
            h_prime_name = r_prime_data["current_hospital"]
            if h_prime_name is None or r_name == r_prime_name or h_name == h_prime_name:
                continue
                
            h_data = hospitals[h_name]
            
            # Condition 1: Does h prefer s' to s?
            rank_s = h_data["lookup"].get(r_name, float('inf'))
            rank_s_prime = h_data["lookup"].get(r_prime_name, float('inf'))
            
            # Condition 2: Does s' prefer h to h'?
            if h_name in r_prime_data["preferences"] and h_prime_name in r_prime_data["preferences"]:
                pref_h = r_prime_data["preferences"].index(h_name)
                pref_h_prime = r_prime_data["preferences"].index(h_prime_name)
                
                if rank_s_prime < rank_s and pref_h < pref_h_prime:
                    print(f"Type 2 Instability Found Between residents ({r_name}, {r_prime_name}) and hospitals ({h_name}, {h_prime_name})")
                    return False
                    
    return True


def print_output(hospitals):
    """
    Step 5: Format and display the required output structure.
    """
    for h_name, h_data in hospitals.items():
        matches = ", ".join(h_data["current_matches"])
        if matches:
            print(f"{h_name}, {matches}")
        else:
            print(f"{h_name}, NO_RESIDENTS")


# --- Execution Example ---
if __name__ == "__main__":
    # To run this, place a valid text file path here (e.g., 'sample_input_1.txt')
    # file_path = "sample_input_1.txt"
    # h_dict, r_dict = parse_input_file(file_path)
    # h_matched, r_matched = run_modified_gale_shapley(h_dict, r_dict)
    
    # if verify_stability(h_matched, r_matched):
    #     print_output(h_matched)
    pass