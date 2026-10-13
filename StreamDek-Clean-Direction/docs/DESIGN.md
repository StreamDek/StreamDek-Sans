# Design and provenance

The visual target is quiet, familiar UI typography: balanced proportions, comfortable lowercase, consistent rhythm and strong small-text construction. The initial rounded geometric proposal was rejected in favour of this professional open-source foundation. This clean edition deliberately retains normal corners; it does not round every Z, W, V, A or E as the earlier proposal did.

Foundation: [Inter 4.1](https://rsms.me/inter/), by Rasmus Andersson and the Inter Project Authors. The official release was downloaded from https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip. Exact source SHA-256 and point-level edits are recorded in `qa/provenance.json`.

## Custom details

All adjustments are small relative to a 2,048-unit em:

- R: two diagonal-foot points move forward 18 units.
- e: four lower-aperture points move down 8–16 units.
- t and its t.1 alternate: six terminal points move forward 5–20 units and upward 2–8 units.

The same offsets apply across the inherited variable design. Composite accents inherit the changes to their underlying letters. Advance widths and original kerning are preserved. These details provide a slight difference from Inter; they do not turn the family into an entirely original typeface.

The weight range is restricted to 300–800. The original optical-size axis remains 14–32, allowing text and display construction to vary with size. Main static fonts use text optics at 14; supplementary display files use 32. CFF OTF outlines are converted from the quadratic outlines with a maximum conversion error setting of 0.5 font units.

## Licence and attribution

Copyright (c) 2016 The Inter Project Authors. The included original copyright and SIL Open Font License 1.1 notices are retained in the font metadata and `OFL.txt`. The derivative font software is distributed under that same OFL. Consult the included complete licence for its terms.

The design references the general cleanliness of iOS typography. No Apple font files or outlines are incorporated. No endorsement by Apple or the Inter authors is implied. StreamDek's supplied logo appears only in the specimens and is not part of the font licence.

The old rounded comparison font is an earlier project artifact included only to reproduce the before/after specimen; it is not part of the new family.
