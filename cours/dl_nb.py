from pathlib import Path
import subprocess
import yaml

git = f"https://github.com/fortierq/cours.git"
dir_repo = Path("/tmp/cours-src")
subprocess.run(["git", "clone", "--dep", "1", git, dir_repo])

def get_dl(d):
    if isinstance(d, dict):
        for k in ["tp", "cor"]:
            if k in d:
                yield d[k]
                d["file"] = d[k]
                del d[k]
        for k, v in d.items():
            yield from get_dl(v)
    elif isinstance(d, list):
        for v in d:
            yield from get_dl(v)

with Path("files/_toc.yml").open() as f:
    d = yaml.load(f, Loader=yaml.FullLoader)
    for type, file in get_dl(d):
        p = Path("files") / file
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", (dir_repo / file).absolute(), p])
        cmd = f"jupyter nbconvert {p} --to ipynb --output {p.name} --allow-errors --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_input_tags hide"
        if type != "cor":
            cmd += " --TagRemovePreprocessor.remove_cell_tags cor"
        subprocess.run(cmd, shell=True)

yaml.dump(d, Path("files/_toc.yml").open("w"))
