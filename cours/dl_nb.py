from pathlib import Path
import subprocess
import sys
import yaml
import os

dir_repo = Path("/tmp/cours-src")
subprocess.run(["git", "config", "--global", "user.email", "qpfortier@gmail.com"])
subprocess.run(["git", "config", "--global", "user.name", "Quentin Fortier"])

git = f"https://github.com/fortierq/cours.git"
subprocess.run(["git", "clone", "--dep", "1", git, dir_repo])

def get_dl(d):
    if isinstance(d, dict):
        if "dl" in d:
            yield d["dl"]
            d["file"] = d["dl"]
            del d["dl"]
        for k, v in d.items():
            yield from get_dl(v)
    elif isinstance(d, list):
        for v in d:
            yield from get_dl(v)

with Path("files/_toc.yml").open() as f:
    d = yaml.safe_load(f)
    for dl in get_dl(d):
        p = Path("files") / dl
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", (dir_repo / dl).absolute(), p])
yaml.dump(d, Path("files/_toc.yml").open("w"))

# for p in Path(dir).rglob("*.pdf"):
#     if p.name not in private_files and "rc" not in p.parts:
#         print(p)
#         p_rel = p.relative_to(dir)
#         p_rel.parent.mkdir(parents=True, exist_ok=True)
#         subprocess.run(["cp", p.absolute(), p_rel])

# subprocess.run(["git", "checkout", "--orphan", "new"])
# subprocess.run(["git", "add", "--all"])
# subprocess.run(["git", "commit", "-m", "Update", "-q"])
# subprocess.run(["git", "branch", "-D", "main"])
# subprocess.run(["git", "branch", "-m", "main"])
# subprocess.run(["git", "push", "-f", git, "--set-upstream", "main"])
