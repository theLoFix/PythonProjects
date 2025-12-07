import os
from collections import defaultdict
from pprint import pprint
from datetime import datetime
import time
import json

CODE_PATH = "Video_and_AddOns\\random-stuff-master"
INTERVAL = 60  # seconds

LANG_PYTHON = "Python"
LANG_JAVASCRIPT = "JavaScript"
LANG_C_CPP = "C/C++"

KNOWN_EXTENSIONS = {
    ".py": LANG_PYTHON,
    ".pyw": LANG_PYTHON,   
    ".js": LANG_JAVASCRIPT,
    ".bat": "Batch",
    ".cmd": "Batch",
    ".hpp": LANG_C_CPP,
    ".pl": "Perl",
    ".JS": LANG_JAVASCRIPT,
    "ino":LANG_C_CPP,
    ".kt": "Kotlin",
    ".java": "Java",
    ".cpp": LANG_C_CPP,
    ".c": LANG_C_CPP, 
    ".rb": "Ruby",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    "php3": "PHP",
    "php4": "PHP",
    "php5": "PHP",
    ".html": "HTML",
    ".css": "CSS",
    ".ts": "TypeScript",
    ".sh": "Shell",
    ".h": LANG_C_CPP,
    "yml": "YAML",
    "yaml": "YAML",
    ".ps1": "PowerShell",
    ".swift": "Swift",
    ".s": "Assembly",
    ".asm": "Assembly",
    ".as": "Assembly",
    "mk": "Makefile",
}

def detect_language(fpath):
    _, ext = os.path.splitext(fpath)
    ext = ext.lower()
    lang = KNOWN_EXTENSIONS.get(ext)
    if lang is not None:
        return lang
    
    fname = os.path.basename(fpath).lower()

    if fname == "makefile" or fname.startswith("makefile."):
        return "Makefile"

    return None


def count_lines_of_code(fpath, lang):
    with open(fpath, "r", encoding="ibm437") as f:
        file_content = f.read()
    
    # lines = [
    #  line for line in file_content.splitlines() if line.strip() != ""
    # ]
    loc = 0

    for line in file_content.splitlines():
        if line.strip() == "":
            continue
        
        if lang == LANG_PYTHON:
            if line.startswith("#"):
                continue
        
        elif lang == LANG_C_CPP or lang == LANG_JAVASCRIPT:
            if line.startswith("//"):
                continue
    
        loc += 1


    # return len(lines)
    return loc

def count_loc_in_path(code_path):
   
    statistics = defaultdict(int)
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    total_loc = 0

    for path, dirs, files in os.walk(code_path):
        # print(path)
        for file in files:
            fpath = f"{path}\\{file}"
            language = detect_language(fpath)

            if language is None:
                continue

            loc = count_lines_of_code(fpath, language)

            statistics[language] += loc
            # Alternative way without defaultdict:

            # if language  in statistics:
            #     statistics[language] += loc
            # else:
            #     statistics[language] = loc  
            
            total_loc += loc


#print(f"({date}: lines of Code statistics for path: {CODE_PATH} )")
# print("_" * 70)
# pprint(dict(statistics))
# print(f"Total LOC:", total_loc)

    return {
        "date": date,
        "total_loc": total_loc,
        "statistics": dict(statistics)
    }

stat_fpath = "{SCRIPT_DIR}\loc_statistics.json"

try:
    with open("loc_statistics.json", "r") as f:
        stats = json.load(f)
except FileNotFoundError:
    stats = []

while True:
    print("Counting...")
    loc = count_loc_in_path(CODE_PATH)
    pprint(loc)
    stats.append(loc)

    with open("loc_statistics.json", "w") as f:
        json.dump(stats, f, indent=4)

    print("Sleeping...")
    time.sleep(INTERVAL)