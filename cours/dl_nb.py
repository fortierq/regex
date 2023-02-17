from pathlib import Path
import subprocess
import json
import sys
import yaml

git = f"https://fortierq:{sys.argv[1]}@github.com/fortierq/cours-src.git"
dir_repo = Path("/tmp/cours-src")
subprocess.run(["git", "config", "--global", "user.email", "qpfortier@gmail.com"])
subprocess.run(["git", "config", "--global", "user.name", "Quentin Fortier"])
subprocess.run(["git", "clone", git, dir_repo])

def iframe(p):
    return f'<iframe src=https://mozilla.github.io/pdf.js/web/viewer.html?file=https://raw.githubusercontent.com/fortierq/cours/main/{p}#zoom=page-fit&pagemode=none height=500 width=100% allowfullscreen></iframe>'

menu = 0

def get_dl(d):
    global menu
    if isinstance(d, list):
        for v in d: 
            get_dl(v)
    elif isinstance(d, dict):
        for k in d.copy():
            if k in ["tp", "cor", "slides_ipynb"]:
                p = Path("files") / "dl" / d[k]
                p.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["cp", (dir_repo / d[k]).absolute(), p])
                cmd = f"jupyter nbconvert {p} --to ipynb --output {p.name} --allow-errors --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_input_tags hide"
                if type != "cor": 
                    cmd += " --TagRemovePreprocessor.remove_cell_tags cor"
                subprocess.run(cmd, shell=True)
                if k == "slides_ipynb":
                    nb = json.load(p.open())
                    if len(nb["cells"]) > 0 and nb["cells"][0]["cell_type"] == "markdown":
                        nb["cells"][0]["source"][0] += f'\n{iframe(Path(d[k]).with_suffix(".pdf"))}'
                        json.dump(nb, p.open("w"))
                d["file"] = str(p.relative_to("files"))
                subprocess.run(["git", "add", p])
                subprocess.run(["git", "commit", "-m", f"Add {p.name}"])
                subprocess.run(["git", "push"])
            if k in ["menu", "slides"]:
                p = (Path(f"files/menu/{menu}")).with_suffix(".md")
                menu += 1
                p.parent.mkdir(parents=True, exist_ok=True)
                s = f"# {d[k]}"
                if k == "slides":
                    s += f'\n{iframe(Path(d["file"]))}'
                p.write_text(s)
                d["file"] = str(p.relative_to("files"))
            if k in ["tp", "cor", "exercices", "cours", "slides", "slides_ipynb"]: 
                del d[k]
            else:
                get_dl(d[k])

d = yaml.safe_load(Path("files/_toc.yml").read_text())
get_dl(d)
yaml.dump(d, Path("files/_toc.yml").open("w"))
