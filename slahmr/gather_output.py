import os
import glob
import json
import subprocess
import pathlib
import numpy as np
from tqdm import tqdm

import torch
from torch.utils.data import DataLoader

from util.logger import Logger
from util.tensor import get_device, move_to, detach_all, to_torch

import hydra
from omegaconf import DictConfig, OmegaConf


def deal_seq(seq_root):
    # assert False, "test-Gym_010_cooking1  筛选多人"

    res_dir = pathlib.Path(seq_root) / "motion_chunks"
    res_list = sorted(glob.glob(str(res_dir) + "/*_world_results.npz"))
    if len(res_list) == 0:
        return None
    print(str(res_dir) + "/*_world_results.npz")
    res_path = res_list[-1]
    res = np.load(res_path, allow_pickle=True)
    # ['trans', 'latent_motion', 'joints_vel', 'floor_plane', 'root_orient',
    # 'latent_pose', 'floor_idcs', 'betas', 'trans_vel', 'world_scale', 'root_orient_vel',
    # 'pose_body', 'cam_R', 'cam_t', 'intrins', 'track_mask']

    sub_n = res["pose_body"].shape[0]
    smpl_params_subs = []
    masks_subs = []
    for sub in range(sub_n):
        body_pose21 = res["pose_body"][sub].reshape(-1, 21, 3)
        padd_zeros = np.zeros((body_pose21.shape[0], 2, 3))
        body_pose23 = np.concatenate([body_pose21, padd_zeros], axis=1)
        betas = res["betas"][[sub]]  # (1, 16)
        betas = np.tile(betas, (body_pose23.shape[0], 1))  # (L, 16)

        masks = res["track_mask"][sub]  # (L,)
        cam_R = res["cam_R"][sub]  # (L, 3, 3)
        cam_t = res["cam_t"][sub]  # (L, 3)
        smpl_params = {
            "betas": betas,  # (L, 16)
            "global_orient": res["root_orient"][sub].reshape(-1, 1, 3),  # (L, 1, 3)
            "body_pose": body_pose23,  # (L, 23, 3)
            "transl": res["trans"][sub].reshape(-1, 3),  # (L, 3)
        }
        smpl_params_subs.append(smpl_params)
        masks_subs.append(masks)

    return {
        "smpl_params": smpl_params_subs,
        "masks": masks_subs,
        "cam_R": cam_R,
        "cam_t": cam_t,
    }


@hydra.main(version_base=None, config_path="confs", config_name="config.yaml")
def main(cfg: DictConfig):
    OmegaConf.register_new_resolver("eval", eval)

    out_dir = "/home/xiayan/workspace/slahmr/outputs/rich"
    dump = {}

    seqs = sorted(glob.glob(f"{out_dir}/*"))
    for seq in tqdm(seqs):
        # Prepare meta info.
        seq_name_parts = seq.split("/")[-1].split("-")
        seq_name = "-".join(seq_name_parts[:3])
        sid, eid = int(seq_name_parts[-2]), int(seq_name_parts[-1])
        cur_seq = {"sid": sid, "eid": eid, "data": deal_seq(seq)}

        # Prepare the output list
        if seq_name not in dump.keys():
            dump[seq_name] = []
        dump[seq_name].append(cur_seq)

    np.save(f"/home/xiayan/workspace/HMR-4D/inputs/comp_exp/SLAHMR@RICH.npy", dump)


if __name__ == "__main__":
    main()
