#!/usr/bin/python3

from pathlib import Path
import subprocess
from itertools import chain
import os

def rm_tree(path):
    path = Path(path)
    for child in path.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    path.rmdir()

P = Path("/workspace/src").resolve()
for f in P.rglob("**/*.tex"):
    # print(f)
    os.chdir(f.parent)
    with f.open("r") as file:
        if 'exam' in file.readline():
            for i in [0, 1]:
                input = "\input{" + f.name + "}"
                output = f.stem
                if i == 1:
                    input = "\PassOptionsToClass{cor}{exam}" + input
                    output += "_cor"
                if not Path(output + ".pdf").exists():
                    cmd = f"lualatex -interaction nonstopmode -halt-on-error -file-line-error -shell-escape --jobname={output} '{input}'"
                    print(cmd)
                    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
                    if not Path(output + ".pdf").exists():
                        print(">"*10 + f" ERROR: {output} not generated")
    os.chdir(str(P))

extensions = ["aux", "log", "out", "toc", "vrb", "nav", "snm", "out", "pyg"]
for ext in extensions:
    for f in P.rglob(f"**/*.{ext}"):
        f.unlink()

for d in P.iterdir():
    if "minted" in d.name:
        rm_tree(d)