# Engineering Calculator

A menu-driven engineering reference and calculator built in Python, developed as part of the University of Cincinnati Experiential Education Program (EEP).

## Overview

This calculator covers 9 engineering and math categories with 30+ calculation functions, unit conversion support, and reference formula displays. It is designed to be useful as a quick reference and calculation tool for engineering students.

## Requirements

- Python 3.x
- No external libraries required (uses only built-in modules: `math`, `statistics`, `os`, `platform`, `subprocess`)

## How to Run

```bash
python Engineering_Calculator.py
```

Or on some systems:

```bash
python3 Engineering_Calculator.py
```

## Categories

| # | Category | Type |
|---|---|---|
| 1 | Basic Math | Calculator (quadratic formula, logarithms, percentages, factorial) |
| 2 | Geometry | Calculator (area, perimeter, volume, surface area — solve for any variable) |
| 3 | Statistics | Calculator (mean, median, std dev, variance — persistent dataset entry) |
| 4 | Calculus | Reference (derivatives, integrals, rules, integration techniques) |
| 5 | Differential Equations | Guided reference (classification, first/second order, Laplace table) |
| 6 | Statics | Calculator + reference (moments, resultant forces, beam reactions) |
| 7 | Physics | Calculator (mechanics, waves, optics, circuits, thermodynamics, electrostatics) |
| 8 | Materials Science | Calculator (stress, strain, elastic modulus, lever rule, heat capacity, calorimetry) |
| 9 | Unit Conversion | Converter (length, area, volume, temperature, energy, force, pressure, mass, time, speed, angle, acceleration) |

## Unit Handling

All physics and engineering calculations assume SI units. Use the Unit Conversion tool (option 9 from the main menu) to convert inputs before calculating if needed.

For geometry calculations, units are selected per calculation and conversion is offered after the result is displayed.

## Reference Files (Optional)

Some menu options can open external reference files (formula sheets, periodic table, etc.) if placed in a folder named `reference_files` in the same directory as the script. If the folder or files are not present, the calculator still works normally — only the file-opening options will be unavailable.

Supported file types depend on your operating system's default applications (PDF, PNG, JPG all work on most systems).

## Notes

- The statistics dataset persists for the duration of a session and clears when the program is closed
- Some complex equations (e.g. cylinder surface area solved for radius) display the formula for manual solving rather than computing it directly, due to the quadratic algebra involved
- The differential equations section uses a guided yes/no classification flow for first and second order ODEs

## Author

Ethan DeMoss  
University of Cincinnati — Mechanical Engineering  
[linkedin.com/in/Ethan-DeMoss](https://www.linkedin.com/in/Ethan-DeMoss)
