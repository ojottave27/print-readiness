# 3D Print Readiness Report

Automated mesh verification for print shops, STL sellers and anyone printing third-party files.

**Live page:** https://ojottave27.github.io/print-readiness/

---

## Figure 040 (Non-Verbal Venn) - reconstructed from computed geometry

A figure rebuilt from a description of its *meaning*, not from coordinates: four shapes (circle, two rectangles, triangle), nineteen numbers, every one placed by code and validated in the correct region with at least 6 px clearance to every boundary.

- **SVG:** [figure-040.svg](figure-040.svg)
- **Generator:** [venn040.py](venn040.py)

The check that makes this worth something: `venn040.py` computes each number's actual region from the geometry and fails if a number lands in the wrong one, or gets closer than the threshold to any edge, or sits too near another number. Moving a number a few pixels makes it fail, so it is not a rubber stamp.

---

## What the mesh tool does

Takes a folder of STL files and returns, file by file, a verdict with the measured value and the exact fix. Eight independent checks:

| Check | Question it answers |
|---|---|
| manifold | Is the surface closed, with no edge shared by more than two faces? |
| watertight | Does it enclose a volume? |
| winding | Do the normals point outward? |
| components | Are there loose fragments or debris? |
| self_intersections | Does the surface cross itself? |
| thin_walls | Is any wall below the minimum thickness? |
| center_of_mass | Does the centroid fall outside the base footprint? |
| scale | Does the height match what was expected? |

Every failure comes with its meaning and the action to fix it. Two outputs are produced: JSON for a pipeline and Markdown for the client, plus exit codes (0 pass, 1 fail, 2 usage) for CI.

## The rule that matters

A check that cannot run is reported as `did not run` and is **never assumed to pass**. A file with missing checks never shows up as ready. A report that hides a skipped check is worse than no report.

## Verified, not claimed

- Fixtures: each bad mesh fails on the right check (hole -> manifold, inverted normals -> winding, stray shell -> components, thin wall -> thin_walls).
- The good mesh passes clean once the expected height is supplied, and the wrong-scale mesh moves from caveat to failure depending on whether that value exists - proof the check distinguishes cases rather than always returning the same answer.
- Real meshes: 667k, 747k and 1,409,534 faces, all checks passing, including wall thickness by voxelisation with the fill ratio verified between 80 and 120%.
- Measured cost: 294 s for those three files.

## What it does not do

It diagnoses; it does not repair. No automatic mesh repair, no hollowing, no support generation, no print quoting.

## Stack

Python, trimesh, scipy, numpy. CLI with batch input, per-file isolation (an unreadable file does not abort the batch), JSON and Markdown reports.
