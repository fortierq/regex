from pathlib import Path
import subprocess
import yaml

git = f"https://github.com/fortierq/cours-src.git"
dir_repo = Path("/tmp/cours-src")
subprocess.run(["git", "clone", git, dir_repo])

def get_dl(d):
    if isinstance(d, dict):
        for k in ["tp", "cor"]:
            if k in d:
                yield k, d[k]
                d["file"] = d[k]
                del d[k]
        if "cours" in d:
            p = (Path("files/cours") / d["cours"]).with_suffix(".md")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f"# Cours : {d['cours']}")
            d["file"] = str(p.relative_to("files"))
            del d["cours"]
        for k, v in d.items():
            yield from get_dl(v)
    elif isinstance(d, list):
        for v in d:
            yield from get_dl(v)

d = yaml.safe_load(Path("files/_toc.yml").read_text())
for type, file in get_dl(d):
    p = Path("files") / file
    p.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cp", (dir_repo / file).absolute(), p])
    cmd = f"jupyter nbconvert {p} --to ipynb --output {p.name} --allow-errors --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_input_tags hide"
    if type != "cor":
        cmd += " --TagRemovePreprocessor.remove_cell_tags cor"
    subprocess.run(cmd, shell=True)

yaml.dump(d, Path("files/_toc.yml").open("w"))
