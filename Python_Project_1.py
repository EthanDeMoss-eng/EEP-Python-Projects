# ============================================================
# Engineering Calculator
# ============================================================
# Author:       Ethan DeMoss
# Created:      6/10/2026
# Last Updated: 6/18/2026
#
# Description:
#   A multi-function engineering calculator that solves
#   common engineering and math problems. Supports unit
#   selection and conversion for most calculations.
#
# Functions included:
#   - Basic Math, Geometry, Statistics, Calculus, Differential Equations,
#     Statics, Physics, Materials Science, and Unit Conversions.
#
# Usage:
#   Run the script and follow the menu prompts.
# ============================================================

import math
import statistics

dataset = []

# ---- HELPER FUNCTIONS ----

def get_float(prompt):
    while True:
        value = input(prompt)
        if value.strip().lower() == "x":
            return "x"
        try:
            return float(value)
        except ValueError:
            print("  Invalid input. Please enter a number or x.")

def get_units(measurement_type):
    print(f"\n  Select units for {measurement_type}:")
    print("  [1] mm")
    print("  [2] cm")
    print("  [3] m")
    print("  [4] in")
    print("  [5] ft")
    print("  [6] Custom (disables unit conversion)")

    choice = input("\n  Choice: ")
    units = {"1": "mm", "2": "cm", "3": "m", "4": "in", "5": "ft"}

    if choice in units:
        return units[choice], True
    elif choice == "6":
        custom = input("  Enter your unit: ")
        return custom, False
    else:
        print("  Invalid choice, defaulting to no units.")
        return "", False

def unit_conversion(value, from_unit, power=1):
    factors = {"mm": 0.001, "cm": 0.01, "m": 1, "in": 0.0254, "ft": 0.3048}

    if from_unit not in factors:
        print("\n  Cannot convert a custom unit.")
        input("  Press Enter to continue.")
        return

    print("\n  Convert to:")
    print("  [1] mm")
    print("  [2] cm")
    print("  [3] m")
    print("  [4] in")
    print("  [5] ft")

    choice = input("\n  Choice: ")
    target_map = {"1": "mm", "2": "cm", "3": "m", "4": "in", "5": "ft"}

    if choice not in target_map:
        print("\n  Invalid choice.")
        input("  Press Enter to continue.")
        return

    to_unit = target_map[choice]

    value_in_base = value * (factors[from_unit] ** power)
    result = value_in_base / (factors[to_unit] ** power)

    if power == 1:
        from_label, to_label = from_unit, to_unit
    elif power == 2:
        from_label, to_label = from_unit + "²", to_unit + "²"
    elif power == 3:
        from_label, to_label = from_unit + "³", to_unit + "³"

    print(f"\n  {value} {from_label} = {result:.4f} {to_label}")
    input("\n  Press Enter to continue.")


def basic_math_menu():
    while True:
        print("\n============================================================")
        print("                       BASIC MATH")
        print("============================================================")
        print("  [1] Quadratic Formula")
        print("  [2] Logarithms")
        print("  [3] Percentage")
        print("  [4] Factorial")
        print("  [0] Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            quadratic_formula()
        elif choice == "2":
            logarithms()
        elif choice == "3":
            percentage()
        elif choice == "4":
            factorial()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def logarithms():
    while True:
        print("\n============================================================")
        print("                        LOGARITHMS")
        print("============================================================")
        print("  [1] Log base 10     log₁₀(x)")
        print("  [2] Natural log     ln(x)")
        print("  [3] Log any base    y = log_b(x)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            x = get_float("\n  Enter x: ")
            if x == "x" or x <= 0:
                print("\n  Error: x must be a positive number.")
            else:
                result = math.log10(x)
                print(f"\n  log₁₀({x}) = {result:.4f}")
        elif choice == "2":
            x = get_float("\n  Enter x: ")
            if x == "x" or x <= 0:
                print("\n  Error: x must be a positive number.")
            else:
                result = math.log(x)
                print(f"\n  ln({x}) = {result:.4f}")
        elif choice == "3":
            print("\n  log_b(x) = y")
            print("  Enter x for the unknown you want to solve for.")

            x = get_float("\n  Enter x: ")
            base = get_float("  Enter base (b): ")
            y = get_float("  Enter result (y): ")

            unknowns = [v for v in [x, base, y] if v == "x"]
            if len(unknowns) != 1:
                print("\n  Error: please enter exactly one x.")
            elif base != "x" and (base <= 0 or base == 1):
                print("\n  Error: base must be a positive number and cannot be 1.")
            elif x != "x" and x <= 0:
                print("\n  Error: x must be a positive number.")
            elif y == 0 and base == "x":
                print("\n  Error: y cannot be 0 when solving for base.")
            else:
                if y == "x":
                    result = math.log(x, base)
                    print(f"\n  y = log_{base}({x}) = {result:.4f}")
                elif x == "x":
                    result = base ** y
                    print(f"\n  x = {base}^{y} = {result:.4f}")
                else:
                    result = x ** (1 / y)
                    print(f"\n  b = {x}^(1/{y}) = {result:.4f}")
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")

        if choice in ["1", "2", "3"]:
            input("\n  Press Enter to continue.")


def percentage():
    while True:
        print("\n============================================================")
        print("                        PERCENTAGE")
        print("============================================================")
        print("  [1] Percentage of a value     (x% of y)")
        print("  [2] Percentage change         (old to new)")
        print("  [3] What percentage is x of y")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            percent = get_float("\n  Enter percentage: ")
            value = get_float("  Enter value: ")
            if percent == "x" or value == "x":
                print("\n  Error: please enter numbers only.")
            else:
                result = (percent / 100) * value
                print(f"\n  {percent}% of {value} = {result:.4f}")

        elif choice == "2":
            old = get_float("\n  Enter old value: ")
            new = get_float("  Enter new value: ")
            if old == "x" or new == "x":
                print("\n  Error: please enter numbers only.")
            elif old == 0:
                print("\n  Error: old value cannot be 0.")
            else:
                result = ((new - old) / old) * 100
                print(f"\n  Percentage change: {result:.4f}%")

        elif choice == "3":
            x = get_float("\n  Enter x: ")
            y = get_float("  Enter y: ")
            if x == "x" or y == "x":
                print("\n  Error: please enter numbers only.")
            elif y == 0:
                print("\n  Error: y cannot be 0.")
            else:
                result = (x / y) * 100
                print(f"\n  {x} is {result:.4f}% of {y}")

        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")

        if choice in ["1", "2", "3"]:
            input("\n  Press Enter to continue.")


def factorial():
    print("\n============================================================")
    print("                        FACTORIAL")
    print("                          n!")
    print("============================================================")

    while True:
        raw = input("\n  Enter n (non-negative integer): ")
        try:
            n = int(raw)
            if n < 0:
                print("  Error: n must be 0 or greater.")
            else:
                break
        except ValueError:
            print("  Invalid input. Please enter a whole number.")

    result = math.factorial(n)
    print(f"\n  {n}! = {result}")
    input("\n  Press Enter to return.")

def quadratic_formula():
    print("\n============================================================")
    print("                   QUADRATIC FORMULA")
    print("                 ax² + bx + c = 0")
    print("        x = (-b ± √(b² - 4ac)) / (2a)")
    print("============================================================")

    a = get_float("\n  Enter a: ")
    b = get_float("  Enter b: ")
    c = get_float("  Enter c: ")

    if a == "x" or b == "x" or c == "x":
        print("\n  Error: all three coefficients must be numbers, not x.")
        input("\n  Press Enter to return.")
        return

    if a == 0:
        print("\n  Error: a cannot be 0 (not a quadratic equation).")
        input("\n  Press Enter to return.")
        return

    discriminant = b**2 - 4*a*c

    if discriminant > 0:
        x1 = (-b + discriminant**0.5) / (2*a)
        x2 = (-b - discriminant**0.5) / (2*a)
        print(f"\n  Two real solutions:")
        print(f"  x1 = {x1:.4f}")
        print(f"  x2 = {x2:.4f}")
    elif discriminant == 0:
        x1 = -b / (2*a)
        print(f"\n  One real solution (repeated root):")
        print(f"  x = {x1:.4f}")
    else:
        print("\n  No real solutions (discriminant is negative).")

    input("\n  Press Enter to return.")


# ---- GEOMETRY FUNCTIONS ----

def pythagorean_theorem():
    print("\n============================================================")
    print("                  PYTHAGOREAN THEOREM")
    print("                    a² + b² = c²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    a = get_float("\n  Enter side a: ")
    b = get_float("  Enter side b: ")
    c = get_float("  Enter side c (hypotenuse): ")

    unknowns = [v for v in [a, b, c] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        return

    unit, convertible = get_units("length")

    if a == "x":
        result = (c**2 - b**2) ** 0.5
        label = "a"
    elif b == "x":
        result = (c**2 - a**2) ** 0.5
        label = "b"
    else:
        result = (a**2 + b**2) ** 0.5
        label = "c"

    print(f"\n  {label} = {result:.4f} {unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def area_menu():
    while True:
        print("\n============================================================")
        print("                          AREA")
        print("============================================================")
        print("  [1] Circle")
        print("  [2] Rectangle")
        print("  [3] Triangle")
        print("  [0] Back to Geometry Menu")
        print("============================================================")

        choice = input("\nSelect a shape: ")

        if choice == "1":
            circle_area()
        elif choice == "2":
            rectangle_area()
        elif choice == "3":
            triangle_area()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")
    
def circle_area():
    print("\n============================================================")
    print("                       CIRCLE AREA")
    print("                      A = π r²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    area = get_float("\n  Enter area: ")
    radius = get_float("  Enter radius: ")

    unknowns = [v for v in [area, radius] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = math.pi * radius**2
        label = "Area"
        result_unit = unit + "²"
    else:
        result = (area / math.pi) ** 0.5
        label = "Radius"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
    if convert.lower() == "y":
        if area == "x":
            unit_conversion(result, unit, power=2)
        else:
            unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")


def rectangle_area():
    print("\n============================================================")
    print("                       RECTANGLE AREA")
    print("                      A = l*w")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    area = get_float("\n  Enter area: ")
    length = get_float("  Enter length: ")
    width = get_float("  Enter width: ")
    
    unknowns = [v for v in [area, length, width] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return
    
    unit, convertible = get_units("length")
    
    if area == "x":
        result = length * width
        label = "Area"
        result_unit = unit + "²"
    elif length == "x":
        result = area / width
        label = "Length"
        result_unit = unit
    else:
        result = area / length
        label = "Width"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
    if convert.lower() == "y":
        if area == "x":
            unit_conversion(result, unit, power=2)
        else:
            unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def triangle_area():
    print("\n============================================================")
    print("                       TRIANGLE AREA")
    print("                      A = 0.5 b*h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    area = get_float("\n  Enter area: ")
    base = get_float("  Enter base: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [area, base, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = 0.5 * base * height
        label = "Area"
        result_unit = unit + "²"
    elif base == "x":
        result = (2 * area) / height
        label = "Base"
        result_unit = unit
    else:
        result = (2 * area) / base
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
             if area == "x":
                unit_conversion(result, unit, power=2)
             else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def perimeter_menu():
    while True:
        print("\n============================================================")
        print("                        PERIMETER")
        print("============================================================")
        print("  [1] Circle (Circumference)")
        print("  [2] Rectangle")
        print("  [3] Triangle")
        print("  [0] Back to Geometry Menu")
        print("============================================================")

        choice = input("\nSelect a shape: ")

        if choice == "1":
            circle_perimeter()
        elif choice == "2":
            rectangle_perimeter()
        elif choice == "3":
            triangle_perimeter()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")

def circle_perimeter():
    print("\n============================================================")
    print("                  CIRCLE CIRCUMFERENCE")
    print("                      C = 2 π r")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    circumference = get_float("\n  Enter circumference: ")
    radius = get_float("  Enter radius: ")

    unknowns = [v for v in [circumference, radius] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if circumference == "x":
        result = 2 * math.pi * radius
        label = "Circumference"
    else:
        result = circumference / (2 * math.pi)
        label = "Radius"

    print(f"\n  {label} = {result:.4f} {unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def rectangle_perimeter():
    print("\n============================================================")
    print("                  RECTANGLE PERIMETER")
    print("                      P = 2l + 2w")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    perimeter = get_float("\n  Enter perimeter: ")
    length = get_float("  Enter length: ")
    width = get_float("  Enter width: ")

    unknowns = [v for v in [perimeter, length, width] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if perimeter == "x":
        result = 2 * (length + width)
        label = "Perimeter"
    elif length == "x":
        result = (perimeter / 2) - width
        label = "Length"
    else:
        result = (perimeter / 2) - length
        label = "Width"

    print(f"\n  {label} = {result:.4f} {unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def triangle_perimeter():
    print("\n============================================================")
    print("                  TRIANGLE PERIMETER")
    print("                      P = a + b + c")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    perimeter = get_float("\n  Enter perimeter: ")
    side_a = get_float("  Enter side a: ")
    side_b = get_float("  Enter side b: ")
    side_c = get_float("  Enter side c: ")

    unknowns = [v for v in [perimeter, side_a, side_b, side_c] if v=="x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return
    
    unit, convertible = get_units("length")

    if perimeter == "x":
        result = side_a + side_b + side_c
        label = "Perimeter"
    elif side_a == "x":
        result = perimeter - (side_b + side_c)
        label = "Side a"
    elif side_b == "x":
        result = perimeter - (side_a + side_c)
        label = "Side b"
    else:
        result = perimeter - (side_a + side_b)
        label = "Side c"

    print(f"\n  {label} = {result:.4f} {unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def volume_menu():
    while True:
        print("\n============================================================")
        print("                         VOLUME")
        print("============================================================")
        print("  [1] Sphere")
        print("  [2] Cylinder")
        print("  [3] Rectangular Prism")
        print("  [4] Cone")
        print("  [5] Pyramid")
        print("  [6] Triangular Prism")
        print("  [0] Back to Geometry Menu")
        print("============================================================")

        choice = input("\nSelect a shape: ")

        if choice == "1":
            sphere_volume()
        elif choice == "2":
            cylinder_volume()
        elif choice == "3":
            rectangular_prism_volume()
        elif choice == "4":
            cone_volume()
        elif choice == "5":
            pyramid_volume()
        elif choice == "6":
            triangular_prism_volume()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")

def sphere_volume():
    print("\n============================================================")
    print("                       SPHERE VOLUME")
    print("                      V = (4/3) π r³")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    volume = get_float("\n  Enter volume: ")
    radius = get_float("  Enter radius: ")

    unknowns = [v for v in [volume, radius] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if volume == "x":
        result = (4/3) * math.pi * radius**3
        label = "Volume"
        result_unit = unit + "³"
    else:
        result = ((3 * volume) / (4 * math.pi)) ** (1/3)
        label = "Radius"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if volume == "x":
                unit_conversion(result, unit, power=3)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def cylinder_volume():
    print("\n============================================================")
    print("                       CYLINDER VOLUME")
    print("                      V = π r² h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    volume = get_float("\n  Enter volume: ")
    radius = get_float("  Enter radius: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [volume, radius, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if volume == "x":
        result = math.pi * radius**2 * height
        label = "Volume"
        result_unit = unit + "³"
    elif radius == "x":
        result = ((volume / (math.pi * height)) ** 0.5)
        label = "Radius"
        result_unit = unit
    else:
        result = volume / (math.pi * radius**2)
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if volume == "x":
                unit_conversion(result, unit, power=3)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def rectangular_prism_volume():
    print("\n============================================================")
    print("                  RECTANGULAR PRISM VOLUME")
    print("                      V = l*w*h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    volume = get_float("\n  Enter volume: ")
    length = get_float("  Enter length: ")
    width = get_float("  Enter width: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [volume, length, width, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if volume == "x":
        result = length * width * height
        label = "Volume"
        result_unit = unit + "³"
    elif length == "x":
        result = volume / (width * height)
        label = "Length"
        result_unit = unit
    elif width == "x":
        result = volume / (length * height)
        label = "Width"
        result_unit = unit
    else:
        result = volume / (length * width)
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if volume == "x":
                unit_conversion(result, unit, power=3)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def cone_volume():
    print("\n============================================================")
    print("                       CONE VOLUME")
    print("                      V = (1/3) π r² h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    volume = get_float("\n  Enter volume: ")
    radius = get_float("  Enter radius: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [volume, radius, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if volume == "x":
        result = (1/3) * math.pi * radius**2 * height
        label = "Volume"
        result_unit = unit + "³"
    elif radius == "x":
        result = ((3 * volume) / (math.pi * height)) ** 0.5
        label = "Radius"
        result_unit = unit
    else:
        result = (3 * volume) / (math.pi * radius**2)
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if volume == "x":
                unit_conversion(result, unit, power=3)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def pyramid_volume():
    print("\n============================================================")
    print("                       PYRAMID VOLUME")
    print("                      V = (1/3) A_base h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    volume = get_float("\n  Enter volume: ")
    base_area = get_float("  Enter base area: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [volume, base_area, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if volume == "x":
        result = (1/3) * base_area * height
        label = "Volume"
        result_unit = unit + "³"
    elif base_area == "x":
        result = (3 * volume) / height
        label = "Base Area"
        result_unit = unit + "²"
    else:
        result = (3 * volume) / base_area
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if volume == "x":
                unit_conversion(result, unit, power=3)
            elif base_area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def triangular_prism_volume():
    print("\n============================================================")
    print("                  TRIANGULAR PRISM VOLUME")
    print("                      V = A_base * h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    volume = get_float("\n  Enter volume: ")
    base_area = get_float("  Enter base area: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [volume, base_area, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if volume == "x":
        result = base_area * height
        label = "Volume"
        result_unit = unit + "³"
    elif base_area == "x":
        result = volume / height
        label = "Base Area"
        result_unit = unit + "²"
    else:
        result = volume / base_area
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if volume == "x":
                unit_conversion(result, unit, power=3)
            elif base_area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def surface_area_menu():
    while True:
        print("\n============================================================")
        print("                      SURFACE AREA")
        print("============================================================")
        print("  [1] Sphere")
        print("  [2] Cylinder")
        print("  [3] Rectangular Prism")
        print("  [4] Cone")
        print("  [5] Pyramid")
        print("  [6] Triangular Prism")
        print("  [0] Back to Geometry Menu")
        print("============================================================")

        choice = input("\nSelect a shape: ")

        if choice == "1":
            sphere_surface_area()
        elif choice == "2":
            cylinder_surface_area()
        elif choice == "3":
            rectangular_prism_surface_area()
        elif choice == "4":
            cone_surface_area()
        elif choice == "5":
            pyramid_surface_area()
        elif choice == "6":
            triangular_prism_surface_area()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")
def sphere_surface_area():
    print("\n============================================================")
    print("                    SPHERE SURFACE AREA")
    print("                      A = 4 π r²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    area = get_float("\n  Enter surface area: ")
    radius = get_float("  Enter radius: ")

    unknowns = [v for v in [area, radius] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = 4 * math.pi * radius**2
        label = "Surface Area"
        result_unit = unit + "²"
    else:
        result = (area / (4 * math.pi)) ** 0.5
        label = "Radius"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def cylinder_surface_area():   
    print("\n============================================================")
    print("                    CYLINDER SURFACE AREA")
    print("                      A = 2 π r² + 2 π r h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    area = get_float("\n  Enter surface area: ")
    radius = get_float("  Enter radius: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [area, radius, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = 2 * math.pi * radius * (radius + height)
        label = "Surface Area"
        result_unit = unit + "²"
    elif radius == "x":
        # This is a more complex equation to solve for radius, so we'll just display the formula instead of calculating it
        print("\n  Solving for radius in this equation is complex. Please use the formula:")
        print("  r = (-h ± √(h² + (2A/π))) / 2")
        input("\n  Press Enter to return.")
        return
    else:
        result = (area / (2 * math.pi * radius)) - radius
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def rectangular_prism_surface_area():
    print("\n============================================================")
    print("                RECTANGULAR PRISM SURFACE AREA")
    print("                      A = 2lw + 2lh + 2wh")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    area = get_float("\n  Enter surface area: ")
    length = get_float("  Enter length: ")
    width = get_float("  Enter width: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [area, length, width, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = 2 * (length * width + length * height + width * height)
        label = "Surface Area"
        result_unit = unit + "²"
    elif length == "x":
        result = (area / 2 - width * height) / (width + height)
        label = "Length"
        result_unit = unit
    elif width == "x":
        result = (area / 2 - length * height) / (length + height)
        label = "Width"
        result_unit = unit
    else:
        result = (area / 2 - length * width) / (length + width)
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def cone_surface_area():
    print("\n============================================================")
    print("                    CONE SURFACE AREA")
    print("                      A = π r² + π r l")
    print("  Enter x for the unknown you want to solve for, (l is slant height).")
    print("============================================================")

    area = get_float("\n  Enter surface area: ")
    radius = get_float("  Enter radius: ")
    slant_height = get_float("  Enter slant height: ")

    unknowns = [v for v in [area, radius, slant_height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = math.pi * radius * (radius + slant_height)
        label = "Surface Area"
        result_unit = unit + "²"
    elif radius == "x":
        # This is a more complex equation to solve for radius, so we'll just display the formula instead of calculating it
        print("\n  Solving for radius in this equation is complex. Please use the formula:")
        print("  r = (-l ± √(l² + 4A/π)) / 2")
        input("\n  Press Enter to return.")
        return
    else:
        result = (area / (math.pi * radius)) - radius
        label = "Slant Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def pyramid_surface_area():
    print("\n============================================================")
    print("                    PYRAMID SURFACE AREA")
    print("                      A = A_base + (1/2) P_base l")
    print("  Enter x for the unknown you want to solve for, (l is slant height).")
    print("============================================================")

    area = get_float("\n  Enter surface area: ")
    base_area = get_float("  Enter base area: ")
    base_perimeter = get_float("  Enter base perimeter: ")
    slant_height = get_float("  Enter slant height: ")

    unknowns = [v for v in [area, base_area, base_perimeter, slant_height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = base_area + (0.5 * base_perimeter * slant_height)
        label = "Surface Area"
        result_unit = unit + "²"
    elif base_area == "x":
        result = area - (0.5 * base_perimeter * slant_height)
        label = "Base Area"
        result_unit = unit + "²"
    elif base_perimeter == "x":
        result = (area - base_area) / (0.5 * slant_height)
        label = "Base Perimeter"
        result_unit = unit
    else:
        result = (area - base_area) / (0.5 * base_perimeter)
        label = "Slant Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if area == "x" or base_area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

def triangular_prism_surface_area():
    print("\n============================================================")
    print("                TRIANGULAR PRISM SURFACE AREA")
    print("                      A = 2A_base + P_base h")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    area = get_float("\n  Enter surface area: ")
    base_area = get_float("  Enter base area: ")
    base_perimeter = get_float("  Enter base perimeter: ")
    height = get_float("  Enter height: ")

    unknowns = [v for v in [area, base_area, base_perimeter, height] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit, convertible = get_units("length")

    if area == "x":
        result = (2 * base_area) + (base_perimeter * height)
        label = "Surface Area"
        result_unit = unit + "²"
    elif base_area == "x":
        result = (area - (base_perimeter * height)) / 2
        label = "Base Area"
        result_unit = unit + "²"
    elif base_perimeter == "x":
        result = (area - (2 * base_area)) / height
        label = "Base Perimeter"
        result_unit = unit
    else:
        result = (area - (2 * base_area)) / base_perimeter
        label = "Height"
        result_unit = unit

    print(f"\n  {label} = {result:.4f} {result_unit}")

    if convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            if area == "x" or base_area == "x":
                unit_conversion(result, unit, power=2)
            else:
                unit_conversion(result, unit, power=1)

    input("\n  Press Enter to return.")

# ---- GEOMETRY MENU ----

def geometry_menu():
    while True:
        print("\n============================================================")
        print("                        GEOMETRY")
        print("============================================================")
        print("  [1] Pythagorean Theorem")
        print("  [2] Area")
        print("  [3] Perimeter")
        print("  [4] Volume")
        print("  [5] Surface Area")
        print("  [0] Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            pythagorean_theorem()
        elif choice == "2":
            area_menu()
        elif choice == "3":
            perimeter_menu()
        elif choice == "4":
            volume_menu()
        elif choice == "5":
            surface_area_menu()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")

# ---- OTHER MENUS (placeholders) ----

def statistics_menu():
    while True:
        print("\n============================================================")
        print("                        STATISTICS")
        print(f"           Current dataset: {len(dataset)} values")
        print("============================================================")
        print("  [1] Enter data")
        print("  [2] View current data")
        print("  [3] Calculate statistics")
        print("  [4] Clear data")
        print("  [0] Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            enter_data()
        elif choice == "2":
            view_data()
        elif choice == "3":
            calculate_statistics()
        elif choice == "4":
            clear_data()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def enter_data():
    global dataset
    print("\n============================================================")
    print("                       ENTER DATA")
    print("  Enter values separated by commas, e.g: 1, 4, 7, 2, 9")
    print("  Your new values will be added to any existing data.")
    print("============================================================")

    raw = input("\n  Enter values: ")

    new_values = []
    for item in raw.split(","):
        item = item.strip()
        try:
            new_values.append(float(item))
        except ValueError:
            print(f"  Skipping '{item}' — not a valid number.")

    dataset.extend(new_values)
    print(f"\n  Added {len(new_values)} values. Dataset now has {len(dataset)} values.")
    input("\n  Press Enter to return.")


def view_data():
    if len(dataset) == 0:
        print("\n  No data entered yet.")
        input("\n  Press Enter to return.")
        return

    print("\n============================================================")
    print("                     CURRENT DATASET")
    print("============================================================")
    formatted = ", ".join(str(v) for v in dataset)
    print(f"\n  {formatted}")
    print(f"\n  Total values: {len(dataset)}")
    input("\n  Press Enter to return.")


def clear_data():
    global dataset
    confirm = input("\n  Are you sure you want to clear all data? (y/n): ")
    if confirm.lower() == "y":
        dataset = []
        print("\n  Dataset cleared.")
    else:
        print("\n  Cancelled.")
    input("\n  Press Enter to return.")


def calculate_statistics():
    if len(dataset) == 0:
        print("\n  No data entered yet. Please enter data first.")
        input("\n  Press Enter to return.")
        return

    if len(dataset) < 2:
        print("\n  Need at least 2 values to calculate statistics.")
        input("\n  Press Enter to return.")
        return

    mean = statistics.mean(dataset)
    median = statistics.median(dataset)
    stdev = statistics.stdev(dataset)
    variance = statistics.variance(dataset)
    minimum = min(dataset)
    maximum = max(dataset)
    data_range = maximum - minimum

    print("\n============================================================")
    print("                  STATISTICS RESULTS")
    print("============================================================")
    print(f"  Count:              {len(dataset)}")
    print(f"  Mean:               {mean:.4f}")
    print(f"  Median:             {median:.4f}")
    print(f"  Std Deviation:      {stdev:.4f}")
    print(f"  Variance:           {variance:.4f}")
    print(f"  Minimum:            {minimum:.4f}")
    print(f"  Maximum:            {maximum:.4f}")
    print(f"  Range:              {data_range:.4f}")
    print("============================================================")
    input("\n  Press Enter to return.")

def calculus_menu():
    print("\nCalculus menu coming soon.")
    input("Press Enter to return to main menu.")

def diff_eq_menu():
    print("\nDifferential Equations menu coming soon.")
    input("Press Enter to return to main menu.")

def statics_menu():
    print("\nStatics menu coming soon.")
    input("Press Enter to return to main menu.")

def physics_menu():
    print("\nPhysics menu coming soon.")
    input("Press Enter to return to main menu.")

def materials_menu():
    print("\nMaterials Science menu coming soon.")
    input("Press Enter to return to main menu.")

def unit_conversion_menu():
    print("\nUnit Conversion menu coming soon.")
    input("Press Enter to return to main menu.")

# ---- MAIN MENU ----

def main_menu():
    while True:
        print("\n============================================================")
        print("               ENGINEERING CALCULATOR")
        print("============================================================")
        print("  [1] Basic Math")
        print("  [2] Geometry")
        print("  [3] Statistics")
        print("  [4] Calculus")
        print("  [5] Statics")
        print("  [6] Physics")
        print("  [7] Materials Science")
        print("  [8] Unit Conversion")
        print("  [0] Exit")
        print("============================================================")

        choice = input("\nSelect a category: ")

        if choice == "1":
            basic_math_menu()
        elif choice == "2":
            geometry_menu()
        elif choice == "3":
            statistics_menu()
        elif choice == "4":
            calculus_menu()
        elif choice == "5":
            statics_menu()
        elif choice == "6":
            physics_menu()
        elif choice == "7":
            materials_menu()
        elif choice == "8":
            unit_conversion_menu()
        elif choice == "0":
            print("\nExiting calculator. Goodbye!")
            break
        else:
            print("\nInvalid selection. Please try again.")

main_menu()