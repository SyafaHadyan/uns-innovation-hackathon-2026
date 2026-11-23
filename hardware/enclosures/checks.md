# WATTLINK enclosure checks (rancangan, concept)

Results of the code checks in section 10 of the notebook. 29 of 29 checks pass.
These checks only test the geometry of a concept design. They do not show that the design is safe for mains use.

| Check | WattLink Hub | WattLink Plug | WattLink Clamp | WattLink Clamp Meter |
|---|---|---|---|---|
| Each placeholder fits its cavity, no two placeholders overlap | pass (largest overlap 0.0 mm3 between boxes, 0.0 mm3 between cavities) | pass (largest overlap 0.0 mm3 between boxes, 0.0 mm3 between cavities) | pass (largest overlap 0.0 mm3 between boxes, 0.0 mm3 between cavities) | pass (largest overlap 0.0 mm3 between boxes, 0.0 mm3 between cavities) |
| Wall thickness at least 2.5 mm everywhere, except the 1.5 mm partition | pass (thinnest 2.5 mm in the base, 2.5 mm in the lid) | pass (thinnest 2.5 mm in the base, 2.5 mm in the lid) | pass (thinnest 2.5 mm in the base, 2.5 mm in the lid) | pass (thinnest 2.5 mm in the base, 2.5 mm in the lid) |
| AC and LV compartments split by a closed wall, except one wire slot | not applicable, one compartment | pass (thickness 1.5 mm measured True, wire slot 6 x 2 mm = 12.0 mm2, stray openings 0, blind pilot holes enclosed True) | pass (thickness 1.5 mm measured True, wire slot 6 x 2 mm = 12.0 mm2, stray openings 0, blind pilot holes enclosed True) | pass (thickness 1.5 mm measured True, wire slot 6 x 2 mm = 12.0 mm2, stray openings 0, blind pilot holes enclosed True) |
| Vent slots and the USB opening are open through the wall | pass (6 probed, closed []) | pass (6 probed, closed []) | pass (6 probed, closed []) | pass (6 probed, closed []) |
| Bounding box against the size target (mm) | pass (body [85.0, 60.0, 35.0], limit [85.0, 60.0, 35.0]) | pass (body [112.0, 64.0, 46.0], limit [112.0, 64.0, 46.0], with pins [112.0, 64.0, 65.0]) | no limit given (body [107.0, 64.0, 53.75], with glands [130.15, 64.0, 53.75]) | no limit given (body [161.01, 64.0, 53.76], with glands [161.01, 64.0, 53.76]) |
| Lid screws, bosses and standoffs exist and do not cut through the outer walls | pass (4 bosses, standoffs, posts and ribs 2 of 2 found) | pass (6 bosses, standoffs, posts and ribs 8 of 8 found) | pass (6 bosses, standoffs, posts and ribs 8 of 8 found) | pass (6 bosses, standoffs, posts and ribs 8 of 8 found) |
| Every STL is watertight | pass (hub-base 38.95 cm3, hub-lid 13.55 cm3) | pass (plug-base 64.51 cm3, plug-lid 21.24 cm3) | pass (clamp-base 71.32 cm3, clamp-lid 19.01 cm3) | pass (meter-base 107.55 cm3, meter-lid 19.01 cm3) |
| Every STL fits a 220 x 220 x 250 mm build volume | pass | pass | pass | pass |

## Method

- Placeholders are boxes of the real module size. A placeholder passes when its box lies inside its cavity box. Overlaps come from exact intersection volumes. The detailed component models of the renders sit inside the same cavities, except the header pin tails of the dev boards, which hang a little below the board.
- Wall thickness casts 15000 rays inward from random points on each exported STL and takes the shortest distance, with 0.05 mm of tolerance for tessellation. A feature smaller than the sample spacing can be missed. Points on the 1.5 mm partition slab are left out and the partition is measured on its own.
- The partition is probed on a 0.5 mm grid across its whole plane. Every open point must lie inside the wire slot or inside a blind pilot hole that has solid plastic on both sides.
- Vent slots and the USB opening are probed at their centre and must be open.
- Watertightness is read back from the saved STL files.

## Open points

- The Plug body meets the 112 x 64 x 46 mm target only without the 19 mm pins.
- One 6 x 2 mm wire slot cannot carry every wire between the compartments.
- The two hanging bosses at the -x end of the Plug, the Clamp and the Clamp meter need print supports.
- The PZEM-004T board may measure 74 x 31 mm and not 73 x 30 mm, which would leave 0.25 mm per side in its cavity.
- The Wago connectors, the inline fuse holder and the Dupont wires of the PDF have no space in the AC compartment.
- The USB-C port of the SuperMini sits 8.6 mm behind the inside of the side wall.
- The hinge, latch and CT core of the Clamp meter jaw are not modeled.
