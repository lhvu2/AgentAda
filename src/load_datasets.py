import pandas as pd
import json
from src.utils import check_and_fix_dataset

import os
from os.path import join, basename

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)

# Get the directory containing the script
script_directory = os.path.dirname(script_path)

print(f"The directory of the current script is: {script_directory}")


def get_dataset(challenge="toy", debug: bool=False):
    """
    returns dataset as a list of dictionaries containing questions, metadata, goal, persona, insights, and table
    """
    base_path = join(script_directory, "../data/jsons")
    base_data_path = join(script_directory, "../data/csvs")

    # get the challenge
    print("challenge", challenge)
    if challenge == "toy":
        id_list = list(range(64,67))
    elif challenge == "pilot":
        # id_list = list(range(70,75))
        id_list= [346,447,482,551,700]
    elif challenge == "full":
        id_list = list(range(1, 26)) + list(range(27, 101))
    else:
        raise ValueError(f"Challenge {challenge} not found")

    print(id_list)
    data_list = []
    for _id in id_list:
        meta_dict = json.load(open(f"{base_path}/{_id}/meta.json", "r"))
        goal_dict = json.load(open(f"{base_path}/{_id}/goal.json", "r"))
        question_list = json.load(open(f"{base_path}/{_id}/questions.json", "r"))
        # insight_dict = json.load(open(f"{base_path}/{_id}/insights.json", "r"))

        if debug:
            import random
            random.seed(42)
            #random.shuffle(question_list)
            question_list = question_list[0:2]

        data_dict = {}
        data_dict["id"] = _id
        data_dict["questions"] = question_list
        data_dict["dataset_path"] = f"{base_data_path}/{_id}/data.csv"
        data_dict["meta"] = meta_dict
        data_dict["goal"] = goal_dict["goal"]
        data_dict["persona"] = goal_dict["persona"]
        # data_dict["insight"] = insight_dict["insight"]
        data_dict["table"] = check_and_fix_dataset(f"{base_data_path}/{_id}/data.csv")

        reference_files_path = []
        for help_data_file_name in meta_dict["help_data_file_names"]:
            reference_files_path.append(f"{base_data_path}/{_id}/{help_data_file_name}")

        data_dict["reference_files"] = reference_files_path

        data_list.append(data_dict)

    return data_list
