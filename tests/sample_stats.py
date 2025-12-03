import os
import json
import statistics
from os.path import join, basename

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)

# Get the directory containing the script
script_directory = os.path.dirname(script_path)

print(f"The directory of the current script is: {script_directory}")

base_path = join(script_directory, "../data/jsons")

lengths = {}          # folder -> number of elements in questions.json
task_counts = {}      # task_type -> total count across all questions.json
unique_task_counts = {}  # folder -> number of unique task types in that file

# Iterate through subdirectories
for subdir in os.listdir(base_path):
    full_path = os.path.join(base_path, subdir)
    if not os.path.isdir(full_path):
        continue

    questions_path = os.path.join(full_path, "questions.json")
    if not os.path.isfile(questions_path):
        continue

    try:
        with open(questions_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {questions_path}: {e}")
        continue

    # 1) total number of elements in this questions.json
    lengths[subdir] = len(data)

    # 2) collect task counts and unique task types per file
    tasks_in_this_file = set()
    for item in data:
        task = item.get("task")
        if task is None:
            continue
        # global task count
        task_counts[task] = task_counts.get(task, 0) + 1
        # track unique tasks for this file
        tasks_in_this_file.add(task)

    # number of unique task types in this file
    unique_task_counts[subdir] = len(tasks_in_this_file)

# --- Stats for length of lists per file (same as before) ---
length_values = list(lengths.values())

length_stats = {}
if length_values:
    length_stats = {
        "count_files": len(length_values),
        "min": min(length_values),
        "max": max(length_values),
        "mean": sum(length_values) / len(length_values),
        "median": statistics.median(length_values),
    }

# --- Stats for unique task types per file ---
unique_values = list(unique_task_counts.values())

unique_stats = {}
if unique_values:
    unique_stats = {
        "count_files": len(unique_values),
        "min": min(unique_values),
        "max": max(unique_values),
        "mean": sum(unique_values) / len(unique_values),
        "median": statistics.median(unique_values),
    }

# --- Outputs ---

print("Folder → Number of questions in questions.json:")
for k in sorted(lengths, key=lambda x: int(x) if x.isdigit() else x):
    print(f"{k}: {lengths[k]}")

print("\nGlobal task counts (task → total occurrences across all files):")
for task, count in sorted(task_counts.items(), key=lambda x: x[0]):
    print(f"{task}: {count}")

print("\nStats for list lengths per questions.json file:")
print(length_stats)

print("\nStats for number of unique task types per questions.json file:")
print(unique_stats)

