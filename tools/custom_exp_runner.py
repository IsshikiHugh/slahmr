import os
import json

from glob import glob
from pathlib import Path

EXEC_DIR = "/home/xiayan/workspace/slahmr/slahmr"
INPUTS_DIR = "/home/xiayan/workspace/slahmr/inputs/custom_video"

def get_exec_cmd(fn: str, root: str):
    ext = fn.split(".")[-1]
    suffix_len = len(ext) + 1
    seq = fn[:-suffix_len]
    cmd = f"python run_opt.py"
    opt = f"data=video data.seq=\"{seq}\" data.ext={ext} data.root=\"{root}\" run_opt=True run_vis=True"
    return f"{cmd} {opt}"

if __name__ == "__main__":
    os.chdir(EXEC_DIR)
    # prepare inputs
    videos_path = Path(INPUTS_DIR).absolute() / "videos"
    fns = sorted(glob(str(videos_path / "*")))
    videos_path.absolute()
    # run experiments
    cmds = ""
    for fn in fns:
        fn = Path(fn).name
        cmd = get_exec_cmd(fn, INPUTS_DIR)
        cmds += f"echo Running \"{cmd}\"; "
        cmds += f"{cmd}; "
        
    os.system(f"{cmds}")