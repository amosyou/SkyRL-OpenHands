import glob
import os
from datasets import load_dataset, DatasetDict

multi_swe_bench = load_dataset("amosyou/Multi-SWE-bench")
# currently all data is under train
multi_swe_bench = multi_swe_bench["train"]

# # attempts to stratify by column
multi_swe_bench = multi_swe_bench.class_encode_column("language")
train_valtest = multi_swe_bench.train_test_split(test_size=0.2, stratify_by_column="language")
val_test = train_valtest["test"].train_test_split(test_size=0.5, stratify_by_column="language")
dataset = DatasetDict({
    "train": train_valtest["train"],
    "validation": val_test["train"],
    "test": val_test["test"]
})
dataset.push_to_hub('NovaSky-AI/Multi-SWE-bench')

