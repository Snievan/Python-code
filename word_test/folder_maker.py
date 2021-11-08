import os
import traceback
from typing import List


def mkfolder(foldername: str, subfoldername: List = ['1-文档', '2-源代码']) -> None:
    """male folder for"""
    try:
        os.mkdir(foldername)
        for subfolder in subfoldername:
            subpath = os.path.join(foldername, subfolder)
            os.mkdir(subpath)
        print(f'Folder created at {foldername}')
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    foldername = './docs/ZB_M0028_关门输入信号异常诊断模型'
    subfolders = ['1-文档', '2-源代码']
    mkfolder(foldername=foldername, subfoldername=subfolders)
