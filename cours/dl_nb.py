from pathlib import Path
import subprocess
import json
import sys
import yaml

git = f"https://fortierq:{sys.argv[1]}@github.com/fortierq/cours-src.git"
dir_repo = Path("/tmp/cours-src")
subprocess.run(["git", "clone", git, dir_repo])

def get_dl(d):
    if isinstance(d, list):
        for v in d: 
            get_dl(v)
    elif isinstance(d, dict):
        for k in d.copy():
            if k in ["tp", "cor", "slides"]:
                p = Path("files") / "dl" / d[k]
                p.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["cp", (dir_repo / d[k]).absolute(), p])
                cmd = f"jupyter nbconvert {p} --to ipynb --output {p.name} --allow-errors --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_input_tags hide"
                if type != "cor": 
                    cmd += " --TagRemovePreprocessor.remove_cell_tags cor"
                subprocess.run(cmd, shell=True)
                if k == "slides":
                    nb = json.load(p.open())
                    if len(nb["cells"]) > 0 and nb["cells"][0]["cell_type"] == "markdown":
                        nb["cells"][0]["source"][0] += '\n'
                        nb["cells"][0]["source"].append(f'<iframe src=https://mozilla.github.io/pdf.js/web/viewer.html?file=https://raw.githubusercontent.com/fortierq/cours/main/{Path(d[k]).with_suffix(".pdf")}#zoom=page-fit&pagemode=none height=500 width=100% allowfullscreen></iframe>')
                        json.dump(nb, p.open("w"))
                d["file"] = str(p.relative_to("files"))
                subprocess.run(["git", "add", p])
                subprocess.run(["git", "commit", "-m", f"Add {p.name}"])
                subprocess.run(["git", "push"])
            if k in ["exercices", "cours"]:
                p = (Path(f"files/{k}") / d[k]).with_suffix(".md")
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(f"# {k.capitalize()}")
                d["file"] = str(p.relative_to("files"))
            if k in ["tp", "cor", "exercices", "cours", "slides"]: 
                del d[k]
            else:
                get_dl(d[k])

d = yaml.safe_load(Path("files/_toc.yml").read_text())
get_dl(d)
yaml.dump(d, Path("files/_toc.yml").open("w"))
