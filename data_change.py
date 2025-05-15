# adapted from https://github.com/All-Hands-AI/OpenHands/blob/main/evaluation/benchmarks/multi_swe_bench/scripts/data/data_change.py
import argparse
import glob
import os
import json


def change_data(input_file, language):

    new_lines = []

    with open(input_file, 'r', encoding='utf-8') as fin:
        print(input_file)
        for line in fin:
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)
            item = data

            # 提取原始数据
            org = item.get("org", "")
            repo = item.get("repo", "")
            number = str(item.get("number", ""))

            new_item = {}
            new_item["repo"] = f"{org}/{repo}"
            new_item["instance_id"] = f"{org}__{repo}-{number}"
            new_item["language"] = language
            new_item["fix_patch"] = item["fix_patch"]
            new_item["test_patch"] = item["test_patch"]
            new_item["problem_statement"] = item["resolved_issues"][0].get("title", "") + "\n" + item["resolved_issues"][0].get("body", "")
            new_item["FAIL_TO_PASS"] = list(item["fixed_tests"].keys()) if item["fixed_tests"] else []
            new_item["PASS_TO_PASS"] = list(item["p2p_tests"].keys()) if item["p2p_tests"] else []
            # TODO: potentially optional columns
            # new_item["f2p_tests"] = item["p2p_tests"]
            # new_item["s2p_tests"] = item["s2p_tests"]
            # new_item["n2p_tests"] = item["n2p_tests"]
            # new_item["run_result"] = item["run_result"]
            # new_item["test_patch_result"] = item["test_patch_result"]
            # new_item["fix_patch_result"] = item["fix_patch_result"]
            new_item["base_commit"] = item['base'].get("sha","")
            new_item["version"] = "0.1" # depends

            new_lines.append(json.dumps(new_item, ensure_ascii=False) + "\n")
    
    with open(input_file, 'w', encoding='utf-8') as fout:
        fout.writelines(new_lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', help='path to Multi-SWE-bench from ByteDance-Seed')

    args = parser.parse_args()
    input_dir = args.input_dir

    # Multi-SWE-bench/<language>/<repo>.jsonl
    for directory in glob.glob(os.path.join(input_dir, "*")):
        if os.path.isdir(directory):
            for file in glob.glob(os.path.join(directory, "*")):
                data_file = os.path.basename(file)
                language = os.path.basename(directory)
                change_data(file, language)
