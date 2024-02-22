import os
from glob import glob

EXEC_DIR = "/home/xiayan/workspace/slahmr/slahmr"
EXP_DIR = "/home/xiayan/workspace/slahmr/inputs/custom_exp"


def get_exp_cmd(fn, root):
    ext = fn.split(".")[-1]
    seq = fn[: -len(ext) - 1]
    cmd = f"python run_opt.py"
    opt = f'data=video data.seq="{seq}" data.ext="{ext}" data.root="{root}" run_opt=True run_vis=True'
    log_ro = f"{root}/logs/{seq}"
    return f"{cmd} {opt} >> {log_ro}.log"


if __name__ == "__main__":
    os.chdir(EXEC_DIR)
    base = f"{EXP_DIR}/videos"
    fns = sorted(glob(f"{base}/*"))

    full_cmd = ""
    for fn in fns:
        exp_cmd = get_exp_cmd(fn=fn[len(base) + 1 :], root=EXP_DIR)
        prompt_cmd = f'echo "Running {exp_cmd}"'
        full_cmd += f"{prompt_cmd}; {exp_cmd}; "

    print(full_cmd)
    # os.system(full_cmd)
