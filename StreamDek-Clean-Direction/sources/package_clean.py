from pathlib import Path
import json,hashlib,zipfile,shutil
ROOT=Path(__file__).resolve().parents[1]
assert json.loads((ROOT/'qa/validation.json').read_text())['status']=='PASS'
assert json.loads((ROOT/'qa/browser.json').read_text())['status']=='PASS'
prior=ROOT.parent/'StreamDek-Sans-Rounded-v0.910/fonts/ttf/StreamDekSansRounded-Regular.ttf'
if prior.exists():shutil.copy2(prior,ROOT/'references/previous-rounded-comparison.ttf')
paths=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.zip' and p.name!='SHA256SUMS.txt']
(ROOT/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix() for p in sorted(paths))+'\n')
paths.append(ROOT/'SHA256SUMS.txt')
out=ROOT.parent/'StreamDek-Sans-Clean-v0.920.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(paths):z.write(p,'StreamDek-Sans-Clean-v0.920/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(json.dumps({'zip':str(out),'bytes':out.stat().st_size,'files':len(paths),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))
