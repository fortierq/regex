from pathlib import Path
import subprocess

def run(cmd):
    print(cmd)
    subprocess.run(cmd, shell=True)

def dir(s):
    match s:
        case "cours" | "code":
            return Path.home() / s
        case "dev":
            return ".devcontainer"
        case "latex" | "python":
            return dir("code") / (s + "-devcontainer")
        case "itc1":
            return dir("cours") / "itc1"

def gh(s):
    return "git@github.com:fortierq/" + s

def ssh():
    run("ssh-keygen -t ed25519 -C fortierq@gmail.com")
    run("ssh-agent -s")
    run(f"ssh-add {(Path.home() / '.ssh/id_ed25519').resolve()}")
    print("ssh key must now be added to github")

def ln(src, dst):
    run(f"ln -s {src.resolve()} {dst.resolve()}")

def ln_dev(src, dst):
    ln(src / dir("dev"), dst / dir("dev"))

def clone(url, path):
    run(f"git clone {url} {path.resolve()}")

def clone_dev(s):
    clone(f'{gh(s)}-devcontainer', dir(s))

def itc1():
    clone(gh("ipt1_1819"), dir("itc1") / "ipt1_1819")
    for s in ["latex", "python"]:
        path = dir("itc1") / f"itc1-{s}"
        if not Path.exists(path):
            clone_dev(s)
            clone(gh("itc1-src"), path)
            ln_dev(dir(s), path)

# ssh()
itc1()
