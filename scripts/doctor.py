from pathlib import Path
import sys

root=Path.cwd()
po=root/".planonce"
checks=[]
checks.append((".planonce exists", po.exists()))
checks.append(("PROJECT.md exists", (po/"PROJECT.md").exists()))
checks.append(("standards index exists", (po/"standards"/"index.yml").exists()))
checks.append(("POLICY.yml exists", (po/"POLICY.yml").exists()))
for label, ok in checks:
    print(("PASS" if ok else "WARN") + " - " + label)
if not po.exists():
    print("Run/use planonce-init first.")
