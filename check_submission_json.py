import os
import glob
import json

required_general_keys = set(["course_id","question_id", "chat_id", "confidence", "interaction"])
required_interaction_keys = set(["role", "content"])
possible_roles = ["system", "user", "assistant"]

def parse_json_to_dict(filename):
    with open(filename, 'r') as read_file:
        data = json.load(read_file)
    return data

def test():
    print("#" * 50)
    print("Searching for json files...")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = glob.glob(os.path.join(dir_path, "**", "*.json"), recursive=True)

    all_data_filenames = [f"{i}.json" for i in range(65)]
    print([filename.split('/')[-1] for filename in files])

    filtered_files = [filename for filename in files if filename.split('\\')[-1] not in all_data_filenames]
    json_cnt = len(filtered_files)

    if json_cnt == 0:
        print("#" * 50)
        print("ERROR: No json files (excluding the given data package) were found.")
        exit(1)

    print(f"Found {json_cnt} json files (excluding the given data package).")

    for filepath in filtered_files:
        print("-" * 50)
        print("Verifying the format of: ", filepath)
        mydictlist = parse_json_to_dict(filepath)

        dict_cnt = 0
        for mydict in mydictlist:
            ####################################################################
            # Dict keys
            remaining_set = required_general_keys - set(mydict.keys())
            if len(remaining_set) > 0:
                remaining_set_str = ", ".join(remaining_set)
                print("#" * 50)
                print(f"ERROR: Missing the keys [{remaining_set_str}] in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)

            ####################################################################
            # Dict values
            # required_general_keys = set(["course_id","question_id", "chat_id", "confidence", "interaction"])
            if type(mydict["course_id"]) != int:
                print("#" * 50)
                print(f"ERROR: course_id value type is not an int in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)

            if type(mydict["question_id"]) != int:
                print("#" * 50)
                print(f"ERROR: question_id value type is not an int in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)

            if type(mydict["chat_id"]) != int:
                print(f"ERROR: chat_id value type is not an int in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)

            if type(mydict["confidence"]) != int: # or type(mydict["confidence"]) != float:
                print("#" * 50)
                print(f"ERROR: confidence value type is not an int in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)

            if type(mydict["interaction"]) != list: # or type(mydict["confidence"]) != float:
                print("#" * 50)
                print(f"ERROR: interaction value type is not a list in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)
            
            if len(mydict["interaction"]) == 0:
                print("#" * 50)
                print(f"ERROR: interaction list is empty in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)

            if type(mydict["interaction"][0]) != dict:
                print("#" * 50)
                print(f"ERROR: the first value of the interaction list is not a dict in dictionary #{dict_cnt} in the json file {filepath}.")
                exit(1)
            
            ####################################################################
            # Subdict keys
            subdict_cnt = 0
            for subdict in mydict["interaction"]:
                sub_remaining_set = required_interaction_keys - set(subdict.keys())
                if len(sub_remaining_set) > 0:
                    sub_remaining_set_str = ", ".join(sub_remaining_set)
                    print("#" * 50)
                    print(f"ERROR: Missing the interaction keys [{sub_remaining_set_str}] in dictionary #{dict_cnt} and interaction sub-dictionary #{subdict_cnt} in the json file {filepath}.")
                    exit(1)
                
                ####################################################################
                # Subdict values
                # required_interaction_keys = set(["role", "content"])
                role = subdict["role"]
                if role not in possible_roles:
                    possible_roles_str = ", ".join(possible_roles)
                    print("#" * 50)
                    print(f"ERROR: role `{role}` isn't any of the following allowed roles [{possible_roles_str}] in dictionary #{dict_cnt} and interaction sub-dictionary #{subdict_cnt} in the json file {filepath}.")
                    exit(1)

                if type(subdict["content"]) != str:
                    print("#" * 50)
                    print(f"ERROR: content value type is not a str in dictionary #{dict_cnt} and interaction sub-dictionary #{subdict_cnt} in the json file {filepath}.")
                    exit(1)
                
                subdict_cnt += 1

            dict_cnt += 1
        print(f"Found {dict_cnt} interaction entries in the json file {filepath}.")

    print("#" * 50)
    print("Successfully passed format verification for demonstration json files.")

if __name__ == '__main__':
    test()


