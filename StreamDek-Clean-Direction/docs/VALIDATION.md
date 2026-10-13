# Validation — clean edition 0.920

The supplied machine-readable evidence is in `qa/validation.json` and `qa/browser.json`.

Passed:

- FontTools parsed all 24 delivered font files; each retains 2,852 mapped characters and 2,937 glyphs. The six OTFs contain actual CFF outlines.
- Copyright and licence metadata match the Inter foundation.
- HarfBuzz shaped the mixed Latin/accent/combining-mark test string without missing glyphs in every TTF/OTF.
- FreeType through Pillow rasterised each TTF/OTF at 12, 16, 24 and 48 px.
- Nine intermediate variable instances (weights 350, 550 and 750 at optical sizes 14, 23 and 32) shaped and rasterised successfully.
- All non-whitespace characters in the current English, German, Spanish, French, Italian, Dutch, Polish and Portuguese Android string resources are mapped.
- Tabular figures produce equal advances; AVATAR responds to kerning. Regular's horizontal metrics match the original Inter text instance exactly.
- Edge loaded all 24 files through FontFace. Preview text, weight, size and light/dark controls worked. The page had no horizontal overflow at 390 px width.
- The main design, comparison and small-text rendered specimens were visually inspected.

Limits: these checks do not prove every glyph pairing or every intermediate variable coordinate is visually perfect. No physical Android/TV, macOS/iOS or printer test was performed. No app integration or release has occurred. The custom outline adjustments should receive normal design acceptance before deployment.
