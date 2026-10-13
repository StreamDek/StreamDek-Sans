# StreamDek Sans

Original custom typeface • review build 0.900 • 11 October 2026

Open `index.html` for the interactive specimen. Change the sample text, weight,
size, background and zero style. Everything runs locally, without a network.

## Package

- `fonts/ttf`: Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700, ExtraBold 800.
- `fonts/otf`: the same six styles as genuine CFF OpenType fonts.
- `fonts/woff2`: the six static webfonts.
- `fonts/variable`: TrueType and WOFF2 variable fonts, `wght` 300–800.
- `specimens`: family, alphabet, brand composition, native-pixel small text,
  1920×1080 TV composition, reference comparison and complete glyph galleries.
- `sources`: authored outline generator, six compatible masters, designspace,
  feature source, specimen renderer and validation scripts.
- `docs`: design findings, exact coverage, validation and future integration.
- `qa`: machine-readable coverage, validation, hashes and browser evidence.
- `references`: Google Sans Regular and its OFL license, separate from the deliverable family.

The deliverable fonts are original generated outlines, not renamed or modified
Google/Apple fonts. The family uses 577 Unicode mappings and 589 glyphs.

This is a technically usable **design review build**, not a claim that physical
TV-distance testing, Android-device acceptance or every OS renderer has passed.
See `docs/VALIDATION.md` for the exact boundary before a production release.

No StreamDek application files are part of this package or modified by it.

## Rebuild

Use Python 3.12+ and install `sources/requirements.txt` into a virtual environment.
Run, in order:

```sh
python sources/build.py
python sources/validate.py
python sources/proof.py
```

`proof.py` copies the existing logo from the inspected Mobile checkout; for a
portable rebuild, keep `specimens/streamdek-logo.png` and use the source's existing
copy if the checkout isn't available. `validate.py` checks the eight locale files
when that checkout is available. Font generation itself needs no repository,
reference font or network. Specimen comparison needs the bundled Google reference.

For browser QA, install Playwright and Microsoft Edge, then run
`node sources/browser-qa.cjs`. The original run used the bundled Windows runtime.

Do not install static and variable editions simultaneously under the same family
in a desktop font manager; select one edition to avoid duplicate font selection.
