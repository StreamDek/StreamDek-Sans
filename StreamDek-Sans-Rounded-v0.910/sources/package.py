"""Write evidence-derived release documentation and a clean portable ZIP."""
from pathlib import Path
import json,hashlib,zipfile
from build import ROOT

def main():
    q=json.loads((ROOT/'qa/validation.json').read_text(encoding='utf-8'))
    b=json.loads((ROOT/'qa/browser-validation.json').read_text(encoding='utf-8'))
    assert q['status']=='PASS' and b['status']=='PASS'
    assert len(q['font_files'])==20
    coverage=json.loads((ROOT/'qa/coverage.json').read_text(encoding='utf-8'))
    cps={int(x['codepoint'][2:],16) for x in coverage}
    ranges=[]
    for cp in sorted(cps):
        if ranges and cp==ranges[-1][1]+1: ranges[-1][1]=cp
        else: ranges.append([cp,cp])
    rangestr=', '.join(f'U+{a:04X}'+(f'–U+{z:04X}' if z!=a else '') for a,z in ranges)
    cov=f'''# Character and language coverage

{len(cps)} mapped Unicode characters, 589 glyphs, identical across all weights and formats.

Complete printable ASCII U+0020–007E, Latin-1 Supplement U+00A0–00FF and Latin
Extended-A U+0100–017F are included. Also supplied: selected Latin Extended
Additional characters, 16 combining marks, smart quotes, dashes, ellipsis,
currency, arithmetic, arrows, common fractions, superscripts and control spaces.

Current app-string audit: all characters appearing in the eight inspected
Mobile `strings.xml` sets are mapped. This includes English, German, Spanish,
French, Italian, Dutch, Polish and Portuguese. It is a character audit, not a
linguistic or translation review. The exact resource inputs are identified in
`qa/validation.json` and DESIGN.md. Backend-supplied titles can contain other scripts.

Latin-1/Extended-A repertoire also provides the letters needed for several other
Western/Central European orthographies, but those languages have not received
native-reader review. Do not infer complete Vietnamese, IPA or pan-European
language support from selected additional glyphs. Greek, Cyrillic, Arabic,
Hebrew, Indic scripts, CJK and emoji require a platform fallback.

Combining marks: grave, acute, circumflex, tilde, macron, breve, dot above,
diaeresis, ring, double acute, caron, cedilla, ogonek, comma below, dot below,
hook above. Top/bottom attachment and stacking are supplied; NFC and NFD sample
equivalence is tested through HarfBuzz. Test unusual multi-mark combinations
before relying on them in production.

Exact mapped ranges:

{rangestr}

`qa/coverage.json` lists every code point, Unicode name and character. The seven
`specimens/glyphs-*.png` sheets show every mapping. Invisible spacing/control
characters naturally have no visible outline.
'''
    (ROOT/'docs/COVERAGE.md').write_text(cov,encoding='utf-8')
    rows='\n'.join(f"| {x['file']} | {x['bytes']:,} | {x['glyphs']} |" for x in q['font_files'])
    validation=f'''# Validation record

Build 0.910, 11 October 2026. Technical tests: **PASS**. Design status: **review
candidate**, with device and human-review gates still open.

## Completed checks

- All 20 deliverable files parsed, all tables decompiled and recompiled with
  fontTools. TTF has real TrueType outlines; OTF has real CFF charstrings;
  WOFF2 is compressed font data, not a renamed file.
- Every file has the same 577-character mapping and 589 glyphs. Printable ASCII,
  Latin-1 and Latin Extended-A are complete. No missing characters were found
  in the eight current Mobile locale resource files.
- Typographic family is StreamDek Sans Rounded. Style/weight values, embedding flags,
  fixed vertical metrics and PostScript names were checked. The package uses
  legacy RIBBI style groups for old Windows font menus.
- HarfBuzz checks passed for kerning (AVATAR), tabular digits, proportional
  digits, optional slashed zero, combining-mark attachment and NFC/NFD sample
  equivalence. All tested samples shaped without a .notdef glyph.
- Every glyph's bounds were checked against ascent 1100 / descent −300.
- All static TTF/OTF files were rasterized through Pillow/FreeType at 12, 16,
  24 and 48 px. The full specimen set includes native-pixel 12–32 px proofs,
  large display headings, light/dark backgrounds and a 1920×1080 TV composition.
- Variable axis is wght 300–800, default 400, with six named styles. Eleven
  weights at 50-unit intervals instantiated and rasterized. All glyph coordinates
  at each of the six master locations matched the authored masters within
  one font unit.
- All 20 files loaded through the browser FontFace API in Windows Microsoft
  Edge {b['browser']}. No browser font/JavaScript errors were reported.
  The interactive specimen's text, 725 weight, 36 px size, zero option and
  light/dark control were exercised. A 390 px viewport had no horizontal overflow.
- Main specimen layouts and glyph-sheet contact proofs were visually reviewed
  during development. This is not an exhaustive typographer's review of every
  glyph at every weight, size and language combination.

Raw results: `qa/validation.json` and `qa/browser-validation.json`. Browser
screenshots: `qa/edge-desktop.png` and `qa/edge-mobile.png`. File hashes appear
in the validation record and SHA256SUMS.txt.

## Open release gates

1. Review letterforms and spacing with the StreamDek owner; follow with a
   native-reader and professional type-design review for final optical polish.
2. Inspect the 1080p proof on target TV hardware at actual viewing distance.
   No physical TV-distance readability test has been performed.
3. Validate on target Android rasterizers, Firefox and Safari/CoreText, desktop
   font menus, accessibility text scaling and real fallback text. Chromium and
   FreeType acceptance do not establish identical cross-platform rendering.
4. Review 12–14 px text carefully. The family has no TrueType bytecode hinting;
   small Light text and very fine details are intentionally not approved for
   tiny labels. Modern antialiasing and gasp flags are the current approach.
5. Finalize the recipient's distribution notice and naming/trademark clearance.
   Original build provenance is documented; global legal uniqueness is not
   certified by outline generation or technical testing.

No Android/TV application installation, UI integration, font-manager
installation, publication or source-repository change was performed.

## Files

| File | Bytes | Glyphs |
|---|---:|---:|
{rows}
'''
    (ROOT/'docs/VALIDATION.md').write_text(validation,encoding='utf-8')
    files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.tmp' and p.name!='SHA256SUMS.txt' and 'trial' not in p.name]
    manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in sorted(files))
    (ROOT/'SHA256SUMS.txt').write_text(manifest,encoding='utf-8')
    files.append(ROOT/'SHA256SUMS.txt')
    dest=ROOT.parent/(ROOT.name+'.zip')
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files): z.write(p,Path(ROOT.name)/p.relative_to(ROOT))
    with zipfile.ZipFile(dest) as z: assert z.testzip() is None
    print(json.dumps({'zip':str(dest),'bytes':dest.stat().st_size,'files':len(files),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__': main()
