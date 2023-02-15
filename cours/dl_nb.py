from pathlib import Path
import subprocess
import yaml

git = f"https://github.com/fortierq/cours.git"
dir_repo = Path("/tmp/cours-src")
subprocess.run(["git", "clone", "--dep", "1", git, dir_repo])

def get_dl(d):
    if isinstance(d, dict):
        if "tp" in d:
            yield d["tp"]
            d["file"] = d["tp"]
            del d["tp"]
        for k, v in d.items():
            yield from get_dl(v)
    elif isinstance(d, list):
        for v in d:
            yield from get_dl(v)

with Path("files/_toc.yml").open() as f:
    d = yaml.load(f, Loader=yaml.FullLoader)
    for dl in get_dl(d):
        p = Path("files") / tp
        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", (dir_repo / dl).absolute(), p])
        subprocess.run(f"""jupyter nbconvert {p} --to ipynb --output {p} --allow-errors \
        --TagRemovePreprocessor.enabled=True \
        --TagRemovePreprocessor.remove_input_tags hide \
        --TagRemovePreprocessor.remove_cell_tags cor""")
yaml.dump(d, Path("files/_toc.yml").open("w"))
