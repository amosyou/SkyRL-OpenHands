import argparse
import glob
import os
import json

input_file = 'XXX.jsonl'
output_file = 'YYY.jsonl'

def change_data(input_file):

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
            new_item["problem_statement"] = item["resolved_issues"][0].get("title", "") + "\n" + item["resolved_issues"][0].get("body", "")
            new_item["FAIL_TO_PASS"] = []
            new_item["PASS_TO_PASS"] = []
            new_item["base_commit"] = item['base'].get("sha","")
            new_item["version"] = "0.1" # depends

            new_lines.append(json.dumps(new_item, ensure_ascii=False) + "\n")
    
    with open(input_file, 'w', encoding='utf-8') as fout:
        fout.writelines(new_lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir')

    args = parser.parse_args()
    input_dir = args.input_dir
    print(input_dir)

    for file in glob.glob(os.path.join(input_dir, "**/*.jsonl")):
        change_data(file)
