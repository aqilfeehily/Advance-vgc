#!/usr/bin/env python3
"""safuan-skill: python3 .claude/skills/safuan-skill/setup_project.py <name>  -> work/<name>/ (scripts, hf/, analysis/, qc/, renders/)
Also copies the BroSafuan circle logo to hf/assets/img/logo_icon.png."""
import os, shutil, sys
if len(sys.argv) != 2: sys.exit(__doc__)
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
T = os.path.join(R, ".claude", "skills", "safuan-skill", "template")
D = os.path.join(R, "work", sys.argv[1])
if os.path.exists(D): sys.exit(f"{D} exists")
os.makedirs(os.path.join(D, "hf", "assets", "video")); os.makedirs(os.path.join(D, "hf", "assets", "img")); os.makedirs(os.path.join(D, "hf", "assets", "audio"))
for d in ("analysis", "qc", "renders"): os.makedirs(os.path.join(D, d))
shutil.copytree(os.path.join(T, "scripts"), os.path.join(D, "scripts"))
for f in ("hyperframes.json", "package.json"): shutil.copy(os.path.join(T, f), os.path.join(D, "hf", f))
shutil.copy(os.path.join(R, ".claude", "skills", "content-safuan", "assets", "brosafuan_logo_circle.png"), os.path.join(D, "hf", "assets", "img", "logo_icon.png"))
print("project ready:", D)
