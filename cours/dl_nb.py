from pathlib import Path
import subprocess
import yaml

git = f"https://github.com/fortierq/cours.git"
dir_repo = Path("/tmp/cours-src")
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
    d = yaml.load(f, Loader=yaml.FullLoader)
    for dl in get_dl(d):
        p = Path("files") / dl
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", (dir_repo / dl).absolute(), p])
yaml.dump(d, Path("files/_toc.yml").open("w"))
