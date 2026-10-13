# StreamDek Sans Rounded — Version 02

Review build 0.910. A separate, softer alternative to StreamDek Sans v0.900.
The first version is preserved unchanged.

Open `index.html` for the interactive specimen, weight and size controls,
light/dark preview and comparison with the original. The most direct comparison
sheet is `specimens/08-original-vs-rounded.png`.

## What changed

- Acute apexes and zigzag turns in A, V, W, M, N and Z now use circular fillets.
- Stroke endings are almost semicircular instead of flat with a slight bevel.
- Merged crossbar construction rounds the inside joins of E, F, H, I, A and T.
- K/k arm joins are adjusted to avoid a spur at the stem.
- The 4 has a single rounded apex and an open triangular counter.
- The rounding system also applies to lowercase letters, numerals, accents and
  punctuation. Existing curved bowls remain recognisable.

The family is named **StreamDek Sans Rounded**, with unique PostScript names,
so original and rounded editions can be compared without font-name collisions.

## Deliverables

Six static weights: Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700
and ExtraBold 800, in TTF, genuine CFF OTF and WOFF2. Variable TTF and WOFF2
cover wght 300–800. Coverage remains 577 Unicode mappings / 589 glyphs.

`sources/` includes the generator, masters, designspace, OpenType feature code
and validation/proof scripts. `docs/` records the design, coverage, technical
validation and future Android/Web usage. `qa/` contains machine-readable results
and browser screenshots. `references/` holds unchanged comparison fonts only;
they are not used as build inputs.

This is a design-review release. Device/TV-distance acceptance and final design
sign-off remain pending. Nothing has been integrated into any StreamDek app.

## Rebuild

Install `sources/requirements.txt` in a Python environment, then run:

```sh
python sources/build.py
python sources/validate.py
python sources/proof.py
node sources/browser-qa.cjs
python sources/package.py
```

Browser QA requires Playwright and Microsoft Edge. Font compilation needs no
reference font or StreamDek app checkout. The specimen renderer reuses the
bundled logo if the original checkout is unavailable; locale validation skips
missing source files on another machine.

Choose static TTF, static OTF or variable TTF when installing this edition in a
desktop font manager; avoid installing multiple formats of the same edition.
