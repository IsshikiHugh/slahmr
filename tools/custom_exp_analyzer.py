import os
import json
from glob import glob
from pathlib import Path

EXEC_DIR = "/home/xiayan/workspace/slahmr/slahmr"
INPUT_DIRS = "/home/xiayan/workspace/slahmr/inputs/custom_exp"
OUTPUT_DIR = "/home/xiayan/workspace/slahmr/outputs/log/video-val/2024-01-31"

def print_items(exps: dict, order: list, item_name: str, item_func: function):
    print(f"==== {item_name} ====")
    for idx in order:
        print(item_func(exps[idx]))

if __name__ == "__main__":
    os.chdir(EXEC_DIR)
    imgs_dir = f"{INPUT_DIRS}/images" # use this to get frames count and exp names
    raw_fns = sorted(glob(f"{imgs_dir}/*"))
    exps = []
    
    # get frames count
    for fn in raw_fns:
        exp = {
            "name": fn[len(imgs_dir)+1:],
            "frames": len(glob(f"{fn}/*")),
        }
        exps.append(exp)

    # get output meta info
    for i, exp in enumerate(exps):
        # read output dir
        exp_name = exp["name"]
        out_path = Path(OUTPUT_DIR) / f"{exp_name}-all-shot-0-0-180"
        meta_path = out_path / "meta_info.json"
        # read meta info
        with open(meta_path, "r") as f:
            meta = json.load(f)
            exps[i].update(meta)
            
    # get the order of exps
    exp_order_map = [-1] * len(exps) 
    for iter_id, exp in enumerate(exps):
        print_order = int(exp["name"].split(".")[0])
        exp_order_map[print_order] = iter_order

    # print needed items exp by exp
    def print_exp_frames(exp):
        return exp["name"]
    