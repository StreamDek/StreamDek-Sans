# Rounded design specification — 0.910

The user's second direction asks for points and angles to become curved for a
more flowing appearance. This edition evolves the original StreamDek Sans
construction, maintaining the same proportions, advance widths, line metrics,
six weights and character mapping. No application implementation is included.

## Geometry

The original small corner trim is replaced by a tangent circular fillet. For
each contour corner the cut distance depends on the angle, so acute A/V/W/Z
points lose their spikes rather than receiving a barely visible bevel. The
nominal fillet radius is 0.52 of the main stroke width, limited to 49% of the
available neighbouring edges to preserve counters and short details.

Rational quadratic arcs are sampled at eight intervals per corner. Terminals
extend half a stroke and are rounded almost to a semicircle. Existing cubic
bowls are retained through the same sampled-outline pipeline. Curved glyphs
have a softer terminal treatment without being replaced by circles.

For the angular capitals A/E/F/H/I/K/L/M/N/T/V/W/X/Y/Z and digits 1/4/7, the
construction is merged before rounding. This also rounds the interior crossbar
joins. A's crossbar ends compensate with weight to remain inside the legs.
K/k arm endpoints move inside the stem to avoid an external spur; K's cleaned
contour uses 384 perimeter-corresponding points for variable compatibility.
The 4's old short plateau becomes one rounded apex. The rounding radius is
reduced by local available space where necessary rather than closing counters.

## Family continuity

UPM: 1000. Nominal cap height: 700. X-height: 520. Ascender/descender line
metrics: 1100 / −300. Main strokes: 48, 66, 82, 98, 114 and 130 font units.
Tabular numeral advances remain 600. Spacing and 21 kerning classes are retained.
Rounded apexes have optical contour differences from the first edition; the
same advance width does not imply identical ink bounds.

I/l/1 and O/0 remain distinct; dotted zero is the default and slashed zero is
available via `zero`. Features `kern`, `mark`, `mkmk`, `pnum`, and `tnum` remain.
There is no italic or optical-size axis. Modern antialiasing is used; there is
no hand-tuned TrueType bytecode hinting.

All six independently generated masters feed the variable font. Static font
overlaps are removed. Variable-compatible contours and their overlap flags
are preserved in the variable format. This is outline design, not synthetic
bolding, a CSS stroke effect or a renamed third-party font.

## Review

Compare `specimens/08-original-vs-rounded.png` at the same Medium weight.
Review the live variable sample, all six weights, the complete glyph sheets,
12–32 px light/dark proofs and the 1080p TV composition. The comparison fonts
in `references/` are unchanged copies of the user's first edition, used only
for proofs. Google Sans remains a separate licensed reference; no Apple font
is included. See LICENSE.txt for provenance and docs/VALIDATION.md for limits.

The design is intended to look noticeably softer and more continuous. A final
native-device and physical TV-distance review remains necessary before adopting
either edition in production.
