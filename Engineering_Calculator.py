# ============================================================
# Engineering Calculator
# ============================================================
# Author:       Ethan DeMoss
# Created:      6/10/2026
# Last Updated: 7/06/2026
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

from fileinput import filename
import math
import statistics
import os
import platform
import subprocess

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

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius * 9 / 5 + 32
    else:
        return celsius + 273.15
    
def convert_angle(value, from_unit, to_unit):
    if from_unit == "deg":
        radians = math.radians(value)
    else:
        radians = value

    if to_unit == "deg":
        return math.degrees(radians)
    else:
        return radians

UNIT_TYPES = {
    "length":   {"mm": 0.001, "cm": 0.01, "m": 1, "in": 0.0254, "ft": 0.3048},
    "energy":   {"J": 1, "kJ": 1000, "cal": 4.184, "kcal": 4184, "BTU": 1055.06},
    "force":    {"N": 1, "kN": 1000, "lbf": 4.44822, "kip": 4448.22},
    "pressure": {"Pa": 1, "kPa": 1000, "MPa": 1e6, "psi": 6894.76, "atm": 101325, "bar": 100000},
    "mass":     {"kg": 1, "g": 0.001, "lb": 0.453592, "slug": 14.5939, "oz": 0.0283495},
    "time":     {"s": 1, "min": 60, "hr": 3600},
    "speed":    {"m/s": 1, "km/h": 0.277778, "mph": 0.44704, "ft/s": 0.3048},
    "acceleration": {"m/s²": 1, "ft/s²": 0.3048, "g": 9.81},
}

def get_units(measurement_type, unit_type="length"):
    if unit_type == "temperature":
        print(f"\n  Select units for {measurement_type}:")
        print("  [1] Celsius (°C)")
        print("  [2] Fahrenheit (°F)")
        print("  [3] Kelvin (K)")
        choice = input("\n  Choice: ")
        temp_map = {"1": "C", "2": "F", "3": "K"}
        if choice in temp_map:
            return temp_map[choice], True
        print("  Invalid choice, defaulting to Celsius.")
        return "C", True
    if unit_type == "angle":
        print(f"\n  Select units for {measurement_type}:")
        print("  [1] Degrees")
        print("  [2] Radians")
        choice = input("\n  Choice: ")
        angle_map = {"1": "deg", "2": "rad"}
        if choice in angle_map:
            return angle_map[choice], True
        print("  Invalid choice, defaulting to degrees.")
        return "deg", True

    options = UNIT_TYPES[unit_type]
    keys = list(options.keys())

    print(f"\n  Select units for {measurement_type}:")
    for i, k in enumerate(keys, start=1):
        print(f"  [{i}] {k}")
    custom_choice = len(keys) + 1
    print(f"  [{custom_choice}] Custom (disables unit conversion)")

    choice = input("\n  Choice: ")
    if choice.isdigit() and 1 <= int(choice) <= len(keys):
        return keys[int(choice) - 1], True
    elif choice == str(custom_choice):
        custom = input("  Enter your unit: ")
        return custom, False
    else:
        print("  Invalid choice, defaulting to no units.")
        return "", False


def unit_conversion(value, from_unit, power=1, unit_type="length"):
    if unit_type == "temperature":
        print("\n  Convert to:")
        print("  [1] Celsius (°C)")
        print("  [2] Fahrenheit (°F)")
        print("  [3] Kelvin (K)")
        choice = input("\n  Choice: ")
        temp_map = {"1": "C", "2": "F", "3": "K"}
        if choice not in temp_map:
            print("\n  Invalid choice.")
            input("  Press Enter to continue.")
            return
        to_unit = temp_map[choice]
        result = convert_temperature(value, from_unit, to_unit)
        print(f"\n  {value}°{from_unit} = {result:.4f}°{to_unit}")
        input("\n  Press Enter to continue.")
        return
    if unit_type == "angle":
        print("\n  Convert to:")
        print("  [1] Degrees")
        print("  [2] Radians")
        choice = input("\n  Choice: ")
        angle_map = {"1": "deg", "2": "rad"}
        if choice not in angle_map:
            print("\n  Invalid choice.")
            input("  Press Enter to continue.")
            return
        to_unit = angle_map[choice]
        result = convert_angle(value, from_unit, to_unit)
        label = "degrees" if to_unit == "deg" else "radians"
        print(f"\n  {value} → {result:.6f} {label}")
        input("\n  Press Enter to continue.")
        return

    options = UNIT_TYPES[unit_type]
    if from_unit not in options:
        print("\n  Cannot convert a custom unit.")
        input("  Press Enter to continue.")
        return

    keys = list(options.keys())
    print("\n  Convert to:")
    for i, k in enumerate(keys, start=1):
        print(f"  [{i}] {k}")
    choice = input("\n  Choice: ")
    if not (choice.isdigit() and 1 <= int(choice) <= len(keys)):
        print("\n  Invalid choice.")
        input("  Press Enter to continue.")
        return
    to_unit = keys[int(choice) - 1]

    value_in_base = value * (options[from_unit] ** power)
    result = value_in_base / (options[to_unit] ** power)

    suffix = "" if power == 1 else ("²" if power == 2 else "³")
    print(f"\n  {value} {from_unit}{suffix} = {result:.4f} {to_unit}{suffix}")
    input("\n  Press Enter to continue.")

def open_reference_file(filename):
    folder = "reference_files"
    filepath = os.path.join(folder, filename)

    if not os.path.exists(filepath):
        print(f"\n  File not found: {filepath}")
        print(f"  Make sure '{filename}' is inside a folder named")
        print(f"  '{folder}', placed next to this script.")
        input("\n  Press Enter to return.")
        return

    print(f"\n  Opening {filename}...")

    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(filepath)
        elif system == "Darwin":
            subprocess.run(["open", filepath])
        else:
            subprocess.run(["xdg-open", filepath])
    except Exception as e:
        print(f"  Could not open file: {e}")

    input("\n  Press Enter to return.")


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
        # This is a more complex equation to solve for radius, so just display the formula instead of calculating it
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
    while True:
        print("\n============================================================")
        print("                        CALCULUS")
        print("============================================================")
        print("  [1] Derivatives — Polynomial & Exponential")
        print("  [2] Derivatives — Trigonometric")
        print("  [3] Derivatives — Inverse Trigonometric")
        print("  [4] Integrals — Polynomial & Exponential")
        print("  [5] Integrals — Trigonometric")
        print("  [6] Integrals — Inverse Trigonometric (results)")
        print("  [7] Derivative Rules")
        print("  [8] Integration Techniques")
        print("  [0] Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            derivatives_poly_exp()
        elif choice == "2":
            derivatives_trig()
        elif choice == "3":
            derivatives_inverse_trig()
        elif choice == "4":
            integrals_poly_exp()
        elif choice == "5":
            integrals_trig()
        elif choice == "6":
            integrals_inverse_trig()
        elif choice == "7":
            derivative_rules()
        elif choice == "8":
            integration_techniques()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def derivatives_poly_exp():
    print("\n============================================================")
    print("            DERIVATIVES — POLYNOMIAL & EXPONENTIAL")
    print("============================================================")
    print("  d/dx [x^n]   = n·x^(n-1)")
    print("  d/dx [c]     = 0          (c = constant)")
    print("  d/dx [e^x]   = e^x")
    print("  d/dx [a^x]   = a^x · ln(a)")
    print("  d/dx [ln(x)] = 1/x")
    print("  d/dx [log_a(x)] = 1 / (x·ln(a))")
    print("============================================================")
    input("\nPress Enter to return.")


def derivatives_trig():
    print("\n============================================================")
    print("              DERIVATIVES — TRIGONOMETRIC")
    print("============================================================")
    print("  d/dx [sin(x)] = cos(x)")
    print("  d/dx [cos(x)] = -sin(x)")
    print("  d/dx [tan(x)] = sec²(x)")
    print("  d/dx [cot(x)] = -csc²(x)")
    print("  d/dx [sec(x)] = sec(x)tan(x)")
    print("  d/dx [csc(x)] = -csc(x)cot(x)")
    print("============================================================")
    input("\nPress Enter to return.")


def derivatives_inverse_trig():
    print("\n============================================================")
    print("           DERIVATIVES — INVERSE TRIGONOMETRIC")
    print("============================================================")
    print("  d/dx [sin⁻¹(x)] =  1 / √(1 - x²)")
    print("  d/dx [cos⁻¹(x)] = -1 / √(1 - x²)")
    print("  d/dx [tan⁻¹(x)] =  1 / (1 + x²)")
    print("  d/dx [cot⁻¹(x)] = -1 / (1 + x²)")
    print("  d/dx [sec⁻¹(x)] =  1 / (|x|√(x² - 1))")
    print("  d/dx [csc⁻¹(x)] = -1 / (|x|√(x² - 1))")
    print("============================================================")
    input("\nPress Enter to return.")


def integrals_poly_exp():
    print("\n============================================================")
    print("             INTEGRALS — POLYNOMIAL & EXPONENTIAL")
    print("============================================================")
    print("  ∫ x^n dx     = x^(n+1)/(n+1) + C     (n ≠ -1)")
    print("  ∫ 1/x dx     = ln|x| + C")
    print("  ∫ e^x dx     = e^x + C")
    print("  ∫ a^x dx     = a^x / ln(a) + C")
    print("============================================================")
    input("\nPress Enter to return.")


def integrals_trig():
    print("\n============================================================")
    print("                INTEGRALS — TRIGONOMETRIC")
    print("============================================================")
    print("  ∫ sin(x) dx  = -cos(x) + C")
    print("  ∫ cos(x) dx  =  sin(x) + C")
    print("  ∫ sec²(x) dx =  tan(x) + C")
    print("  ∫ csc²(x) dx = -cot(x) + C")
    print("  ∫ sec(x)tan(x) dx =  sec(x) + C")
    print("  ∫ csc(x)cot(x) dx = -csc(x) + C")
    print("  ∫ tan(x) dx  =  ln|sec(x)| + C")
    print("  ∫ cot(x) dx  =  ln|sin(x)| + C")
    print("============================================================")
    input("\nPress Enter to return.")


def integrals_inverse_trig():
    print("\n============================================================")
    print("         INTEGRALS — INVERSE TRIGONOMETRIC (RESULTS)")
    print("============================================================")
    print("  ∫ 1/√(1-x²) dx     = sin⁻¹(x) + C")
    print("  ∫ -1/√(1-x²) dx    = cos⁻¹(x) + C")
    print("  ∫ 1/(1+x²) dx      = tan⁻¹(x) + C")
    print("  ∫ 1/(|x|√(x²-1)) dx = sec⁻¹(x) + C")
    print("============================================================")
    input("\nPress Enter to return.")


def derivative_rules():
    print("\n============================================================")
    print("                    DERIVATIVE RULES")
    print("============================================================")
    print("  Power Rule:     d/dx [x^n] = n·x^(n-1)")
    print("  Product Rule:   d/dx [f·g] = f'g + fg'")
    print("  Quotient Rule:  d/dx [f/g] = (f'g - fg') / g²")
    print("  Chain Rule:     d/dx [f(g(x))] = f'(g(x)) · g'(x)")
    print("============================================================")
    input("\nPress Enter to return.")


def integration_techniques():
    print("\n============================================================")
    print("                  INTEGRATION TECHNIQUES")
    print("============================================================")
    print("  U-Substitution:")
    print("      Let u = g(x), du = g'(x) dx")
    print("      ∫ f(g(x))g'(x) dx  =  ∫ f(u) du")
    print()
    print("  Integration by Parts:")
    print("      ∫ u dv = uv - ∫ v du")
    print("============================================================")
    input("\nPress Enter to return.")

def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("  Please enter y or n.")


def diff_eq_menu():
    while True:
        print("\n============================================================")
        print("                  DIFFERENTIAL EQUATIONS")
        print("============================================================")
        print("  [1] First-Order ODE (guided classification)")
        print("  [2] Second-Order ODE (guided classification)")
        print("  [3] Cauchy-Euler Equations")
        print("  [4] Method of Undetermined Coefficients")
        print("  [5] Variation of Parameters")
        print("  [6] Solution Theory (IVP, Wronskian, Abel's Theorem)")
        print("  [7] Power Series Solutions")
        print("  [8] Laplace Transform Table")
        print("  [9] Formula Sheets")
        print("  [0] Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            first_order_guided()
        elif choice == "2":
            second_order_guided()
        elif choice == "3":
            cauchy_euler()
        elif choice == "4":
            undetermined_coefficients()
        elif choice == "5":
            variation_of_parameters()
        elif choice == "6":
            solution_theory()
        elif choice == "7":
            power_series_solutions()
        elif choice == "8":
            laplace_table()
        elif choice == "9":
            diffeq_formula_sheets()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def first_order_guided():
    print("\n============================================================")
    print("                FIRST-ORDER ODE CLASSIFICATION")
    print("============================================================")

    if ask_yes_no("\n  Is the equation separable, i.e. g(y)dy = f(x)dx? (y/n): "):
        print("\n  SEPARABLE EQUATION")
        print("  Form:        dy/dx = f(x)g(y)")
        print("  Method:      ∫ dy/g(y) = ∫ f(x) dx, then solve for y")

    elif ask_yes_no("\n  Is it linear, i.e. y' + P(x)y = Q(x)? (y/n): "):
        print("\n  FIRST-ORDER LINEAR ODE")
        print("  Standard form:        y' + P(x)y = Q(x)")
        print("  Integrating factor:   μ(x) = e^(∫P(x) dx)")
        print("  General solution:     y = [ ∫ μ(x)Q(x) dx + C ] / μ(x)")

    elif ask_yes_no("\n  Is it homogeneous in form, i.e. dy/dx = F(y/x)? (y/n): "):
        print("\n  HOMOGENEOUS (SUBSTITUTION) EQUATION")
        print("  Form:        dy/dx = F(y/x)")
        print("  Substitute:  v = y/x,  so y = vx  and  dy/dx = v + x(dv/dx)")
        print("  This reduces the equation to a separable one in v and x.")

    elif ask_yes_no("\n  Is it exact, i.e. M(x,y)dx + N(x,y)dy = 0 with My = Nx? (y/n): "):
        print("\n  EXACT EQUATION")
        print("  Form:        M(x,y)dx + N(x,y)dy = 0")
        print("  Exactness check:   ∂M/∂y = ∂N/∂x")
        print("  Solution:    Find F(x,y) such that ∂F/∂x = M and ∂F/∂y = N")
        print("               General solution: F(x,y) = C")

    else:
        print("\n  This equation may require another technique (e.g. Bernoulli")
        print("  substitution, or an integrating factor for a non-exact equation).")

    input("\n  Press Enter to return.")


def second_order_guided():
    print("\n============================================================")
    print("               SECOND-ORDER ODE CLASSIFICATION")
    print("============================================================")

    if not ask_yes_no("\n  Is the equation linear? (y/n): "):
        print("\n  Nonlinear second-order ODEs generally require specialized")
        print("  or numerical techniques not covered in this reference.")
        input("\n  Press Enter to return.")
        return

    if ask_yes_no("\n  Is the right-hand side equal to 0 (homogeneous)? (y/n): "):
        if ask_yes_no("\n  Are the coefficients constant (not functions of x)? (y/n): "):
            print("\n  SECOND-ORDER LINEAR HOMOGENEOUS (constant coefficients)")
            print("  Form:                 ay'' + by' + cy = 0")
            print("  Characteristic eqn:    ar² + br + c = 0")
            print("  Real distinct roots:   y = C1·e^(r1x) + C2·e^(r2x)")
            print("  Real repeated root:    y = C1·e^(rx) + C2·x·e^(rx)")
            print("  Complex roots (α±βi): y = e^(αx)[C1·cos(βx) + C2·sin(βx)]")
        else:
            print("\n  Variable-coefficient homogeneous equations often require")
            print("  Cauchy-Euler methods (see option 3) or power series methods")
            print("  (see option 7), depending on the equation's structure.")
    else:
        print("\n  SECOND-ORDER LINEAR NONHOMOGENEOUS")
        print("  Form:    ay'' + by' + cy = g(x)")
        print("  General solution:    y = y_h + y_p")
        print("  Solve for y_p using either:")
        print("    - Method of Undetermined Coefficients (see option 4)")
        print("    - Variation of Parameters (see option 5)")

    input("\n  Press Enter to return.")


def cauchy_euler():
    print("\n============================================================")
    print("                  CAUCHY-EULER EQUATIONS")
    print("              ax²y'' + bxy' + cy = 0")
    print("============================================================")
    print("  Try a solution of the form: y = x^r")
    print()
    print("  Characteristic equation:")
    print("      ar(r-1) + br + c = 0")
    print()
    print("  Case 1 — Real, distinct roots:")
    print("      y = C1·x^r1 + C2·x^r2")
    print()
    print("  Case 2 — Real, repeated root:")
    print("      y = C1·x^r + C2·x^r·ln(x)")
    print()
    print("  Case 3 — Complex roots (r = α ± βi):")
    print("      y = x^α [C1·cos(β·ln x) + C2·sin(β·ln x)]")
    print("============================================================")
    input("\nPress Enter to return.")


def undetermined_coefficients():
    print("\n============================================================")
    print("        METHOD OF UNDETERMINED COEFFICIENTS")
    print("============================================================")
    print("  Used for: ay'' + by' + cy = g(x), constant coefficients")
    print()
    print("  Guess y_p based on the form of g(x):")
    print("      g(x) = polynomial   → guess a matching polynomial")
    print("      g(x) = e^(kx)       → guess A·e^(kx)")
    print("      g(x) = sin/cos(kx)  → guess A·sin(kx) + B·cos(kx)")
    print()
    print("  If the guess duplicates a term already in y_h,")
    print("  multiply the guess by x (or x² if needed) and try again.")
    print("============================================================")
    input("\nPress Enter to return.")


def variation_of_parameters():
    print("\n============================================================")
    print("              VARIATION OF PARAMETERS")
    print("============================================================")
    print("  Used for: y'' + P(x)y' + Q(x)y = g(x)")
    print("  Works even when g(x) doesn't fit Undetermined Coefficients.")
    print()
    print("  Given two independent homogeneous solutions y1, y2:")
    print("      y_p = -y1·∫(y2·g / W) dx + y2·∫(y1·g / W) dx")
    print()
    print("  Where W is the Wronskian of y1 and y2 (see Solution Theory).")
    print("============================================================")
    input("\nPress Enter to return.")


def solution_theory():
    print("\n============================================================")
    print("                    SOLUTION THEORY")
    print("============================================================")
    print("  Initial Value Problem (IVP):")
    print("      An ODE paired with initial condition(s), e.g. y(0) = y0,")
    print("      used to solve for the constants in the general solution.")
    print()
    print("  Wronskian (for y1, y2):")
    print("      W(y1, y2) = y1·y2' - y2·y1'")
    print("      If W ≠ 0 on an interval, y1 and y2 are linearly independent.")
    print()
    print("  Abel's Theorem:")
    print("      For y'' + P(x)y' + Q(x)y = 0:")
    print("      W(x) = C · e^(-∫P(x) dx)")
    print("      Shows the Wronskian is either always zero or never zero.")
    print("============================================================")
    input("\nPress Enter to return.")


def power_series_solutions():
    print("\n============================================================")
    print("                 POWER SERIES SOLUTIONS")
    print("============================================================")
    print("  Ordinary Point:")
    print("      x0 is an ordinary point if P(x), Q(x) are analytic at x0")
    print("      (for y'' + P(x)y' + Q(x)y = 0).")
    print("      → Solution can be written as a power series centered at x0.")
    print()
    print("  Singular Point:")
    print("      A point that is not ordinary.")
    print()
    print("  Regular Singular Point:")
    print("      x0 is a regular singular point if (x - x0)P(x) and")
    print("      (x - x0)²Q(x) are both analytic at x0.")
    print()
    print("  Radius of Convergence:")
    print("      For a power series solution, at minimum equal to the")
    print("      distance from the center to the nearest singular point.")
    print("============================================================")
    input("\nPress Enter to return.")


def laplace_table():
    print("\n============================================================")
    print("                 LAPLACE TRANSFORM TABLE")
    print("                      f(t)  →  F(s)")
    print("============================================================")
    print("  1                 →  1/s")
    print("  t                 →  1/s²")
    print("  t^n               →  n! / s^(n+1)")
    print("  e^(at)            →  1 / (s - a)")
    print("  sin(at)           →  a / (s² + a²)")
    print("  cos(at)           →  s / (s² + a²)")
    print("  f'(t)             →  sF(s) - f(0)")
    print("  f''(t)            →  s²F(s) - sf(0) - f'(0)")
    print("  δ(t)  (unit imp.) →  1")
    print("  u(t)  (unit step) →  1/s")
    print("============================================================")
    input("\nPress Enter to return.")

def diffeq_formula_sheets():
    while True:
        print("\n============================================================")
        print("              DIFF EQ FORMULA SHEET (PHOTOS)")
        print("============================================================")
        print("  [1] Sheet 1 Page 1")
        print("  [2] Sheet 1 Page 2")
        print("  [3] Sheet 2 Page 1")
        print("  [4] Sheet 2 Page 2")
        print("  [5] Sheet 3 Page 1")
        print("  [6] Sheet 3 Page 2")
        print("  [7] Laplace Transform Table")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect a page: ")

        if choice == "1":
            open_reference_file("Diffeq_Sheet1_Page1.jpg")
        elif choice == "2":
            open_reference_file("Diffeq_Sheet1_Page2.jpg")
        elif choice == "3":
            open_reference_file("Diffeq_Sheet2_Page1.jpg")
        elif choice == "4":
            open_reference_file("Diffeq_Sheet2_Page2.jpg")
        elif choice == "5":
            open_reference_file("Diffeq_Sheet3_Page1.jpg")
        elif choice == "6":
            open_reference_file("Diffeq_Sheet3_Page2.jpg")
        elif choice == "7":
            open_reference_file("Diffeq_Laplace_Table.jpg")
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")

def statics_menu():
    while True:
        print("\n============================================================")
        print("                         STATICS")
        print("============================================================")
        print("  [1] Moment / Torque")
        print("  [2] Equilibrium Conditions (Reference)")
        print("  [3] Resultant of 2D Concurrent Forces")
        print("  [4] Centroid of Composite Shapes (Reference)")
        print("  [5] Simple Beam Reactions")
        print("  [6] Distributed Load — Equivalent Point Load")
        print("  [0] Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            moment_calc()
        elif choice == "2":
            equilibrium_reference()
        elif choice == "3":
            resultant_forces()
        elif choice == "4":
            centroid_reference()
        elif choice == "5":
            beam_reactions()
        elif choice == "6":
            distributed_load()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def moment_calc():
    print("\n============================================================")
    print("                     MOMENT / TORQUE")
    print("                       M = F · d")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    moment = get_float("\n  Enter moment (M): ")
    force = get_float("  Enter force (F): ")
    distance = get_float("  Enter perpendicular distance (d): ")

    unknowns = [v for v in [moment, force, distance] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if moment == "x":
        result = force * distance
        label = "Moment (M)"
    elif force == "x":
        result = moment / distance
        label = "Force (F)"
    else:
        result = moment / force
        label = "Distance (d)"

    print(f"\n  {label} = {result:.4f}")
    print("  (Units depend on inputs, e.g. N·m, lb·ft)")
    input("\n  Press Enter to return.")


def equilibrium_reference():
    print("\n============================================================")
    print("               EQUILIBRIUM CONDITIONS (2D)")
    print("============================================================")
    print("  For a body in static equilibrium:")
    print()
    print("  ΣFx = 0   (sum of all x-direction forces = 0)")
    print("  ΣFy = 0   (sum of all y-direction forces = 0)")
    print("  ΣM  = 0   (sum of all moments about any point = 0)")
    print()
    print("  Steps:")
    print("  1. Draw a free body diagram (FBD)")
    print("  2. Identify all forces and their directions")
    print("  3. Choose a convenient moment point to eliminate unknowns")
    print("  4. Write equilibrium equations and solve")
    print()
    print("  Sign convention (typical):")
    print("      Right → positive Fx")
    print("      Up    → positive Fy")
    print("      CCW   → positive moment")
    print("============================================================")
    input("\nPress Enter to return.")


def resultant_forces():
    print("\n============================================================")
    print("           RESULTANT OF 2D CONCURRENT FORCES")
    print("============================================================")
    print("  Enter as many forces as you have.")
    print("  Each force needs a magnitude and angle from +x axis (degrees).")
    print("============================================================")

    forces = []
    while True:
        print(f"\n  Force {len(forces) + 1} (or press Enter to finish):")
        raw_mag = input("    Magnitude: ").strip()
        if raw_mag == "":
            if len(forces) < 2:
                print("  Please enter at least 2 forces.")
                continue
            break
        try:
            magnitude = float(raw_mag)
            angle = float(input("    Angle from +x axis (degrees): "))
            forces.append((magnitude, angle))
        except ValueError:
            print("  Invalid input, please enter numbers.")

    fx_total = sum(m * math.cos(math.radians(a)) for m, a in forces)
    fy_total = sum(m * math.sin(math.radians(a)) for m, a in forces)
    resultant = (fx_total**2 + fy_total**2) ** 0.5
    angle_result = math.degrees(math.atan2(fy_total, fx_total))

    print(f"\n  ΣFx = {fx_total:.4f}")
    print(f"  ΣFy = {fy_total:.4f}")
    print(f"\n  Resultant magnitude = {resultant:.4f}")
    print(f"  Resultant angle     = {angle_result:.4f}° from +x axis")
    input("\n  Press Enter to return.")


def centroid_reference():
    print("\n============================================================")
    print("             CENTROID OF COMPOSITE SHAPES")
    print("============================================================")
    print("  x̄ = ΣAᵢx̄ᵢ / ΣAᵢ")
    print("  ȳ = ΣAᵢȳᵢ / ΣAᵢ")
    print()
    print("  Steps:")
    print("  1. Divide the composite into simple shapes")
    print("  2. Find the area and centroid of each part")
    print("  3. For cutouts, treat the area as negative")
    print("  4. Multiply each area by its centroid location")
    print("  5. Sum all (A·x̄) and divide by total area")
    print()
    print("  Common centroids:")
    print("      Rectangle:  x̄ = b/2,   ȳ = h/2")
    print("      Triangle:   x̄ = b/3,   ȳ = h/3  (from base/left)")
    print("      Circle:     x̄ = r,     ȳ = r     (from center)")
    print("      Semicircle: ȳ = 4r/3π  (from flat edge)")
    print("============================================================")
    input("\nPress Enter to return.")


def beam_reactions():
    print("\n============================================================")
    print("        SIMPLE BEAM REACTIONS — POINT LOADS")
    print("  Simply supported beam, span L, with point loads")
    print("============================================================")

    l = get_float("\n  Enter beam span length (L): ")
    if l == "x" or l <= 0:
        print("\n  Error: beam length must be a positive number.")
        input("\n  Press Enter to return.")
        return

    loads = []
    while True:
        print(f"\n  Load {len(loads) + 1} (or press Enter to finish):")
        raw = input("    Force magnitude (positive = downward): ").strip()
        if raw == "":
            if len(loads) < 1:
                print("  Please enter at least 1 load.")
                continue
            break
        try:
            force = float(raw)
            position = float(input("    Distance from left support (a): "))
            if position < 0 or position > l:
                print(f"  Position must be between 0 and {l}.")
                continue
            loads.append((force, position))
        except ValueError:
            print("  Invalid input, please enter numbers.")

    ra = sum(f * (l - a) / l for f, a in loads)
    rb = sum(f * a / l for f, a in loads)

    print(f"\n  Left reaction  (Ra) = {ra:.4f}")
    print(f"  Right reaction (Rb) = {rb:.4f}")
    print(f"  Check — Ra + Rb = {ra + rb:.4f}  (should equal total load)")
    input("\n  Press Enter to return.")


def distributed_load():
    print("\n============================================================")
    print("          DISTRIBUTED LOAD — EQUIVALENT POINT LOAD")
    print("============================================================")
    print("  Uniform distributed load (UDL):")
    print("      F_eq = w · L")
    print("      Acts at midpoint of loaded length")
    print()
    print("  Triangular distributed load:")
    print("      F_eq = (1/2) · w_max · L")
    print("      Acts at L/3 from the larger end")
    print("============================================================")
    print()
    print("  --- Calculate equivalent point load ---")

    load_type = input("  [1] Uniform  [2] Triangular: ").strip()

    if load_type == "1":
        w = get_float("\n  Enter load intensity (w, force per length): ")
        length = get_float("  Enter loaded length (L): ")
        if w == "x" or length == "x":
            print("\n  Error: please enter numbers only.")
        else:
            f_eq = w * length
            location = length / 2
            print(f"\n  Equivalent force = {f_eq:.4f}")
            print(f"  Acts at          = {location:.4f} from left end")

    elif load_type == "2":
        w_max = get_float("\n  Enter maximum load intensity (w_max): ")
        length = get_float("  Enter loaded length (L): ")
        if w_max == "x" or length == "x":
            print("\n  Error: please enter numbers only.")
        else:
            f_eq = 0.5 * w_max * length
            location = length / 3
            print(f"\n  Equivalent force = {f_eq:.4f}")
            print(f"  Acts at          = {location:.4f} from larger end")
    else:
        print("\n  Invalid selection.")

    input("\n  Press Enter to return.")

def physics_menu():
    while True:
        print("\n============================================================")
        print("                         PHYSICS")
        print("============================================================")
        print("  [1] Mechanics")
        print("  [2] Waves, Optics & Electricity")
        print("  [0] Back to Main Menu")
        print("============================================================")
        print("  NOTE: All calculations assume SI units.")
        print("  Use the Unit Conversion tool (Main Menu [9]) to convert first.")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            physics_mechanics_menu()
        elif choice == "2":
            physics_waves_menu()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def physics_mechanics_menu():
    while True:
        print("\n============================================================")
        print("                        MECHANICS")
        print("============================================================")
        print("  [1] Kinematics")
        print("  [2] Newton's Laws")
        print("  [3] Work, Energy & Power")
        print("  [4] Momentum & Impulse")
        print("  [5] Springs")
        print("  [6] Rotational & Angular Motion")
        print("  [0] Back to Physics Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            kinematics_menu()
        elif choice == "2":
            newtons_laws_menu()
        elif choice == "3":
            work_energy_menu()
        elif choice == "4":
            momentum_menu()
        elif choice == "5":
            springs_menu()
        elif choice == "6":
            rotational_menu()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def kinematics_menu():
    while True:
        print("\n============================================================")
        print("                       KINEMATICS")
        print("  Select the equation that matches your known variables.")
        print("============================================================")
        print("  [1] v = v₀ + at")
        print("  [2] x = v₀t + ½at²")
        print("  [3] v² = v₀² + 2ax")
        print("  [4] x = ½(v + v₀)t")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            kinematics_vvat()
        elif choice == "2":
            kinematics_xvat()
        elif choice == "3":
            kinematics_vvax()
        elif choice == "4":
            kinematics_xvvt()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def kinematics_vvat():
    print("\n============================================================")
    print("                    v = v₀ + at")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    v = get_float("\n  Enter final velocity (v): ")
    v0 = get_float("  Enter initial velocity (v₀): ")
    a = get_float("  Enter acceleration (a): ")
    t = get_float("  Enter time (t): ")

    unknowns = [i for i in [v, v0, a, t] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if v == "x":
        result = v0 + a * t
        label = "v"
    elif v0 == "x":
        result = v - a * t
        label = "v₀"
    elif a == "x":
        result = (v - v0) / t
        label = "a"
    else:
        result = (v - v0) / a
        label = "t"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def kinematics_xvat():
    print("\n============================================================")
    print("                 x = v₀t + ½at²")
    print("  Enter x for the unknown (type 'x' for position,")
    print("  use variable names if needed).")
    print("  Note: solving for t or a requires quadratic methods.")
    print("  Solve for x, v₀ only here.")
    print("============================================================")
    pos = get_float("\n  Enter position (x): ")
    v0 = get_float("  Enter initial velocity (v₀): ")
    a = get_float("  Enter acceleration (a): ")
    t = get_float("  Enter time (t): ")

    unknowns = [i for i in [pos, v0, a, t] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if pos == "x":
        result = v0 * t + 0.5 * a * t**2
        label = "x (position)"
    elif v0 == "x":
        result = (pos - 0.5 * a * t**2) / t
        label = "v₀"
    elif a == "x":
        result = (pos - v0 * t) / (0.5 * t**2)
        label = "a"
    else:
        print("\n  Solving for t requires the quadratic formula.")
        print("  Rearranges to: ½at² + v₀t - x = 0")
        disc = v0**2 + 2 * a * pos
        if disc < 0:
            print("  No real solution (negative discriminant).")
        else:
            t1 = (-v0 + disc**0.5) / a
            t2 = (-v0 - disc**0.5) / a
            print(f"  t₁ = {t1:.4f}")
            print(f"  t₂ = {t2:.4f}")
            print("  (Take the positive, physically meaningful value)")
        input("\n  Press Enter to return.")
        return

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def kinematics_vvax():
    print("\n============================================================")
    print("                 v² = v₀² + 2ax")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    v = get_float("\n  Enter final velocity (v): ")
    v0 = get_float("  Enter initial velocity (v₀): ")
    a = get_float("  Enter acceleration (a): ")
    pos = get_float("  Enter position/displacement (x): ")

    unknowns = [i for i in [v, v0, a, pos] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if v == "x":
        val = v0**2 + 2 * a * pos
        if val < 0:
            print("\n  Error: v² is negative — check your inputs.")
        else:
            print(f"\n  v = {val**0.5:.4f}  (taking positive root)")
    elif v0 == "x":
        val = v**2 - 2 * a * pos
        if val < 0:
            print("\n  Error: v₀² is negative — check your inputs.")
        else:
            print(f"\n  v₀ = {val**0.5:.4f}  (taking positive root)")
    elif a == "x":
        result = (v**2 - v0**2) / (2 * pos)
        print(f"\n  a = {result:.4f}")
    else:
        result = (v**2 - v0**2) / (2 * a)
        print(f"\n  x = {result:.4f}")

    input("\n  Press Enter to return.")


def kinematics_xvvt():
    print("\n============================================================")
    print("                 x = ½(v + v₀)t")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    pos = get_float("\n  Enter position (x): ")
    v = get_float("  Enter final velocity (v): ")
    v0 = get_float("  Enter initial velocity (v₀): ")
    t = get_float("  Enter time (t): ")

    unknowns = [i for i in [pos, v, v0, t] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if pos == "x":
        result = 0.5 * (v + v0) * t
        label = "x"
    elif v == "x":
        result = (2 * pos / t) - v0
        label = "v"
    elif v0 == "x":
        result = (2 * pos / t) - v
        label = "v₀"
    else:
        result = (2 * pos) / (v + v0)
        label = "t"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def newtons_laws_menu():
    while True:
        print("\n============================================================")
        print("                     NEWTON'S LAWS")
        print("============================================================")
        print("  [1] Second Law  (F = ma)")
        print("  [2] Weight      (W = mg)")
        print("  [3] Friction    (f = μN)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            fma_calc()
        elif choice == "2":
            weight_calc()
        elif choice == "3":
            friction_calc()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def fma_calc():
    print("\n============================================================")
    print("                   NEWTON'S SECOND LAW")
    print("                       F = ma")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    force = get_float("\n  Enter force (F): ")
    mass = get_float("  Enter mass (m): ")
    accel = get_float("  Enter acceleration (a): ")

    unknowns = [i for i in [force, mass, accel] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if force == "x":
        result, label = mass * accel, "F"
    elif mass == "x":
        result, label = force / accel, "m"
    else:
        result, label = force / mass, "a"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def weight_calc():
    print("\n============================================================")
    print("                         WEIGHT")
    print("                       W = mg")
    print("  g = 9.81 m/s² (or 32.2 ft/s² for imperial)")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    weight = get_float("\n  Enter weight (W): ")
    mass = get_float("  Enter mass (m): ")

    unknowns = [i for i in [weight, mass] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit = input("\n  Use [1] metric (g=9.81) or [2] imperial (g=32.2)? ")
    g = 9.81 if unit == "1" else 32.2

    if weight == "x":
        result, label = mass * g, "W"
    else:
        result, label = weight / g, "m"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def friction_calc():
    print("\n============================================================")
    print("                        FRICTION")
    print("                       f = μN")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    f = get_float("\n  Enter friction force (f): ")
    mu = get_float("  Enter coefficient of friction (μ): ")
    n = get_float("  Enter normal force (N): ")

    unknowns = [i for i in [f, mu, n] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if f == "x":
        result, label = mu * n, "f"
    elif mu == "x":
        result, label = f / n, "μ"
    else:
        result, label = f / mu, "N"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def work_energy_menu():
    while True:
        print("\n============================================================")
        print("                  WORK, ENERGY & POWER")
        print("============================================================")
        print("  [1] Work        (W = Fd cosθ)")
        print("  [2] Kinetic Energy  (KE = ½mv²)")
        print("  [3] Potential Energy (PE = mgh)")
        print("  [4] Power       (P = W/t)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            work_calc()
        elif choice == "2":
            kinetic_energy_calc()
        elif choice == "3":
            potential_energy_calc()
        elif choice == "4":
            power_calc()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def work_calc():
    print("\n============================================================")
    print("                          WORK")
    print("                    W = F · d · cosθ")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    w = get_float("\n  Enter work (W): ")
    f = get_float("  Enter force (F): ")
    d = get_float("  Enter displacement (d): ")
    theta = get_float("  Enter angle between F and d (θ, degrees): ")

    unknowns = [i for i in [w, f, d, theta] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if w == "x":
        result = f * d * math.cos(math.radians(theta))
        label = "W"
    elif f == "x":
        result = w / (d * math.cos(math.radians(theta)))
        label = "F"
    elif d == "x":
        result = w / (f * math.cos(math.radians(theta)))
        label = "d"
    else:
        cos_theta = w / (f * d)
        if abs(cos_theta) > 1:
            print("\n  Error: no valid angle — check your inputs.")
            input("\n  Press Enter to return.")
            return
        result = math.degrees(math.acos(cos_theta))
        label = "θ"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def kinetic_energy_calc():
    print("\n============================================================")
    print("                     KINETIC ENERGY")
    print("                     KE = ½mv²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    ke = get_float("\n  Enter kinetic energy (KE): ")
    mass = get_float("  Enter mass (m): ")
    v = get_float("  Enter velocity (v): ")

    unknowns = [i for i in [ke, mass, v] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if ke == "x":
        result, label = 0.5 * mass * v**2, "KE"
    elif mass == "x":
        result, label = (2 * ke) / v**2, "m"
    else:
        val = (2 * ke) / mass
        if val < 0:
            print("\n  Error: negative value under square root.")
            input("\n  Press Enter to return.")
            return
        result, label = val**0.5, "v"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def potential_energy_calc():
    print("\n============================================================")
    print("                   GRAVITATIONAL POTENTIAL ENERGY")
    print("                       PE = mgh")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    pe = get_float("\n  Enter potential energy (PE): ")
    mass = get_float("  Enter mass (m): ")
    h = get_float("  Enter height (h): ")

    unknowns = [i for i in [pe, mass, h] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    unit = input("\n  Use [1] metric (g=9.81) or [2] imperial (g=32.2)? ")
    g = 9.81 if unit == "1" else 32.2

    if pe == "x":
        result, label = mass * g * h, "PE"
    elif mass == "x":
        result, label = pe / (g * h), "m"
    else:
        result, label = pe / (mass * g), "h"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def power_calc():
    print("\n============================================================")
    print("                          POWER")
    print("                        P = W/t")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    p = get_float("\n  Enter power (P): ")
    w = get_float("  Enter work (W): ")
    t = get_float("  Enter time (t): ")

    unknowns = [i for i in [p, w, t] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if p == "x":
        result, label = w / t, "P"
    elif w == "x":
        result, label = p * t, "W"
    else:
        result, label = w / p, "t"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def momentum_menu():
    while True:
        print("\n============================================================")
        print("                   MOMENTUM & IMPULSE")
        print("============================================================")
        print("  [1] Momentum    (p = mv)")
        print("  [2] Impulse     (J = FΔt)")
        print("  [3] Impulse-Momentum Theorem  (J = Δp)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            momentum_calc()
        elif choice == "2":
            impulse_calc()
        elif choice == "3":
            impulse_momentum_calc()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def momentum_calc():
    print("\n============================================================")
    print("                        MOMENTUM")
    print("                        p = mv")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    p = get_float("\n  Enter momentum (p): ")
    m = get_float("  Enter mass (m): ")
    v = get_float("  Enter velocity (v): ")

    unknowns = [i for i in [p, m, v] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if p == "x":
        result, label = m * v, "p"
    elif m == "x":
        result, label = p / v, "m"
    else:
        result, label = p / m, "v"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def impulse_calc():
    print("\n============================================================")
    print("                         IMPULSE")
    print("                        J = FΔt")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    j = get_float("\n  Enter impulse (J): ")
    f = get_float("  Enter force (F): ")
    dt = get_float("  Enter time interval (Δt): ")

    unknowns = [i for i in [j, f, dt] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if j == "x":
        result, label = f * dt, "J"
    elif f == "x":
        result, label = j / dt, "F"
    else:
        result, label = j / f, "Δt"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def impulse_momentum_calc():
    print("\n============================================================")
    print("             IMPULSE-MOMENTUM THEOREM")
    print("                 J = Δp = m(v - v₀)")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    j = get_float("\n  Enter impulse (J): ")
    m = get_float("  Enter mass (m): ")
    v = get_float("  Enter final velocity (v): ")
    v0 = get_float("  Enter initial velocity (v₀): ")

    unknowns = [i for i in [j, m, v, v0] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if j == "x":
        result, label = m * (v - v0), "J"
    elif m == "x":
        result, label = j / (v - v0), "m"
    elif v == "x":
        result, label = j / m + v0, "v"
    else:
        result, label = v - j / m, "v₀"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def springs_menu():
    while True:
        print("\n============================================================")
        print("                         SPRINGS")
        print("============================================================")
        print("  [1] Hooke's Law       (F = kx)")
        print("  [2] Elastic PE        (PE = ½kx²)")
        print("  [3] Period of oscillation (T = 2π√(m/k))")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            hookes_law()
        elif choice == "2":
            spring_pe()
        elif choice == "3":
            spring_period()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def hookes_law():
    print("\n============================================================")
    print("                      HOOKE'S LAW")
    print("                       F = kx")
    print("  Enter x for the unknown (type 'x' for any variable).")
    print("  Note: 'x' here means the unknown, displacement uses 'd'.")
    print("============================================================")
    f = get_float("\n  Enter spring force (F): ")
    k = get_float("  Enter spring constant (k): ")
    d = get_float("  Enter displacement (d): ")

    unknowns = [i for i in [f, k, d] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if f == "x":
        result, label = k * d, "F"
    elif k == "x":
        result, label = f / d, "k"
    else:
        result, label = f / k, "d"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def spring_pe():
    print("\n============================================================")
    print("                   SPRING POTENTIAL ENERGY")
    print("                      PE = ½kd²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    pe = get_float("\n  Enter potential energy (PE): ")
    k = get_float("  Enter spring constant (k): ")
    d = get_float("  Enter displacement (d): ")

    unknowns = [i for i in [pe, k, d] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if pe == "x":
        result, label = 0.5 * k * d**2, "PE"
    elif k == "x":
        result, label = (2 * pe) / d**2, "k"
    else:
        val = (2 * pe) / k
        if val < 0:
            print("\n  Error: negative value under square root.")
            input("\n  Press Enter to return.")
            return
        result, label = val**0.5, "d"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def spring_period():
    print("\n============================================================")
    print("                PERIOD OF SPRING OSCILLATION")
    print("                    T = 2π√(m/k)")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    t = get_float("\n  Enter period (T): ")
    m = get_float("  Enter mass (m): ")
    k = get_float("  Enter spring constant (k): ")

    unknowns = [i for i in [t, m, k] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if t == "x":
        result, label = 2 * math.pi * (m / k)**0.5, "T"
    elif m == "x":
        result, label = k * (t / (2 * math.pi))**2, "m"
    else:
        result, label = m / (t / (2 * math.pi))**2, "k"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def rotational_menu():
    while True:
        print("\n============================================================")
        print("                  ROTATIONAL & ANGULAR MOTION")
        print("============================================================")
        print("  [1] Angular velocity   (ω = θ/t)")
        print("  [2] Angular acceleration (α = Δω/t)")
        print("  [3] Linear ↔ Angular   (v = ωr, a = αr, s = θr)")
        print("  [4] Rotational KE      (KE = ½Iω²)")
        print("  [5] Torque             (τ = Iα)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            angular_velocity()
        elif choice == "2":
            angular_acceleration()
        elif choice == "3":
            linear_angular_conversion()
        elif choice == "4":
            rotational_ke()
        elif choice == "5":
            torque_inertia()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def angular_velocity():
    print("\n============================================================")
    print("                    ANGULAR VELOCITY")
    print("                      ω = θ / t")
    print("  Enter x for the unknown you want to solve for.")
    print("  θ in radians, ω in rad/s")
    print("============================================================")
    omega = get_float("\n  Enter angular velocity (ω, rad/s): ")
    theta = get_float("  Enter angle (θ, radians): ")
    t = get_float("  Enter time (t): ")

    unknowns = [i for i in [omega, theta, t] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if omega == "x":
        result, label = theta / t, "ω (rad/s)"
    elif theta == "x":
        result, label = omega * t, "θ (rad)"
    else:
        result, label = theta / omega, "t"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def angular_acceleration():
    print("\n============================================================")
    print("                  ANGULAR ACCELERATION")
    print("                    α = Δω / t")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    alpha = get_float("\n  Enter angular acceleration (α, rad/s²): ")
    delta_omega = get_float("  Enter change in angular velocity (Δω): ")
    t = get_float("  Enter time (t): ")

    unknowns = [i for i in [alpha, delta_omega, t] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if alpha == "x":
        result, label = delta_omega / t, "α (rad/s²)"
    elif delta_omega == "x":
        result, label = alpha * t, "Δω"
    else:
        result, label = delta_omega / alpha, "t"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def linear_angular_conversion():
    while True:
        print("\n============================================================")
        print("              LINEAR ↔ ANGULAR CONVERSIONS")
        print("============================================================")
        print("  [1] Arc length:   s = θr")
        print("  [2] Linear vel:   v = ωr")
        print("  [3] Linear accel: a = αr")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice in ["1", "2", "3"]:
            labels = {
                "1": ("s (arc length)", "θ (rad)", "r"),
                "2": ("v (linear vel)", "ω (rad/s)", "r"),
                "3": ("a (linear accel)", "α (rad/s²)", "r"),
            }
            l1, l2, l3 = labels[choice]
            a_val = get_float(f"\n  Enter {l1}: ")
            b_val = get_float(f"  Enter {l2}: ")
            r = get_float(f"  Enter {l3} (radius): ")

            unknowns = [i for i in [a_val, b_val, r] if i == "x"]
            if len(unknowns) != 1:
                print("\n  Error: please enter exactly one x.")
            elif a_val == "x":
                print(f"\n  {l1} = {b_val * r:.4f}")
            elif b_val == "x":
                print(f"\n  {l2} = {a_val / r:.4f}")
            else:
                print(f"\n  {l3} = {a_val / b_val:.4f}")

            input("\n  Press Enter to return.")

        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def rotational_ke():
    print("\n============================================================")
    print("                   ROTATIONAL KINETIC ENERGY")
    print("                      KE = ½Iω²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    ke = get_float("\n  Enter rotational KE: ")
    i_val = get_float("  Enter moment of inertia (I): ")
    omega = get_float("  Enter angular velocity (ω, rad/s): ")

    unknowns = [i for i in [ke, i_val, omega] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if ke == "x":
        result, label = 0.5 * i_val * omega**2, "KE"
    elif i_val == "x":
        result, label = (2 * ke) / omega**2, "I"
    else:
        val = (2 * ke) / i_val
        if val < 0:
            print("\n  Error: negative value under square root.")
            input("\n  Press Enter to return.")
            return
        result, label = val**0.5, "ω"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def torque_inertia():
    print("\n============================================================")
    print("                    TORQUE (ROTATIONAL)")
    print("                       τ = Iα")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    tau = get_float("\n  Enter torque (τ): ")
    i_val = get_float("  Enter moment of inertia (I): ")
    alpha = get_float("  Enter angular acceleration (α): ")

    unknowns = [i for i in [tau, i_val, alpha] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if tau == "x":
        result, label = i_val * alpha, "τ"
    elif i_val == "x":
        result, label = tau / alpha, "I"
    else:
        result, label = tau / i_val, "α"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")

def physics_waves_menu():
    while True:
        print("\n============================================================")
        print("           WAVES, OPTICS & ELECTRICITY")
        print("============================================================")
        print("  [1] Waves")
        print("  [2] Optics")
        print("  [3] Circuits")
        print("  [4] Electrostatics")
        print("  [5] Thermodynamics")
        print("  [6] Gravity")
        print("  [0] Back to Physics Menu")
        print("============================================================")
        print("  NOTE: All calculations assume SI units.")
        print("  Use Unit Conversion (Main Menu [9]) to convert first.")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            waves_menu()
        elif choice == "2":
            optics_menu()
        elif choice == "3":
            circuits_menu()
        elif choice == "4":
            electrostatics_menu()
        elif choice == "5":
            thermodynamics_menu()
        elif choice == "6":
            gravity_menu()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def waves_menu():
    while True:
        print("\n============================================================")
        print("                          WAVES")
        print("============================================================")
        print("  [1] Wave equation     (v = fλ)")
        print("  [2] Period & frequency (T = 1/f)")
        print("  [3] Wave speed on string (v = √(T/μ))")
        print("  [4] Sound intensity level (dB = 10·log(I/I₀))")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            wave_equation()
        elif choice == "2":
            period_frequency()
        elif choice == "3":
            wave_speed_string()
        elif choice == "4":
            sound_intensity()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def wave_equation():
    print("\n============================================================")
    print("                      WAVE EQUATION")
    print("                       v = f · λ")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    v = get_float("\n  Enter wave speed (v, m/s): ")
    f = get_float("  Enter frequency (f, Hz): ")
    lam = get_float("  Enter wavelength (λ, m): ")

    unknowns = [i for i in [v, f, lam] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if v == "x":
        result, label = f * lam, "v (m/s)"
    elif f == "x":
        result, label = v / lam, "f (Hz)"
    else:
        result, label = v / f, "λ (m)"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def period_frequency():
    print("\n============================================================")
    print("                  PERIOD & FREQUENCY")
    print("                      T = 1/f")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    t = get_float("\n  Enter period (T, s): ")
    f = get_float("  Enter frequency (f, Hz): ")

    unknowns = [i for i in [t, f] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if t == "x":
        result, label = 1 / f, "T (s)"
    else:
        result, label = 1 / t, "f (Hz)"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def wave_speed_string():
    print("\n============================================================")
    print("                 WAVE SPEED ON A STRING")
    print("                   v = √(T_tension / μ)")
    print("  T_tension = tension (N), μ = linear mass density (kg/m)")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    v = get_float("\n  Enter wave speed (v, m/s): ")
    tension = get_float("  Enter tension (T, N): ")
    mu = get_float("  Enter linear mass density (μ, kg/m): ")

    unknowns = [i for i in [v, tension, mu] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if v == "x":
        result, label = (tension / mu) ** 0.5, "v (m/s)"
    elif tension == "x":
        result, label = mu * v**2, "T (N)"
    else:
        result, label = tension / v**2, "μ (kg/m)"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def sound_intensity():
    print("\n============================================================")
    print("                  SOUND INTENSITY LEVEL")
    print("                 dB = 10 · log₁₀(I / I₀)")
    print("  I₀ = 1×10⁻¹² W/m²  (threshold of hearing)")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    I0 = 1e-12
    db = get_float("\n  Enter intensity level (dB): ")
    intensity = get_float("  Enter intensity (I, W/m²): ")

    unknowns = [i for i in [db, intensity] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if db == "x":
        result, label = 10 * math.log10(intensity / I0), "dB"
    else:
        result, label = I0 * 10**(db / 10), "I (W/m²)"

    print(f"\n  {label} = {result:.6f}")
    input("\n  Press Enter to return.")


def optics_menu():
    while True:
        print("\n============================================================")
        print("                         OPTICS")
        print("============================================================")
        print("  [1] Snell's Law         (n₁sinθ₁ = n₂sinθ₂)")
        print("  [2] Thin Lens / Mirror  (1/f = 1/do + 1/di)")
        print("  [3] Magnification       (m = -di/do)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            snells_law()
        elif choice == "2":
            thin_lens()
        elif choice == "3":
            magnification()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def snells_law():
    print("\n============================================================")
    print("                       SNELL'S LAW")
    print("                  n₁·sinθ₁ = n₂·sinθ₂")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    n1 = get_float("\n  Enter index of refraction 1 (n₁): ")
    theta1 = get_float("  Enter angle of incidence (θ₁, degrees): ")
    n2 = get_float("  Enter index of refraction 2 (n₂): ")
    theta2 = get_float("  Enter angle of refraction (θ₂, degrees): ")

    unknowns = [i for i in [n1, theta1, n2, theta2] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if n1 == "x":
        result, label = n2 * math.sin(math.radians(theta2)) / math.sin(math.radians(theta1)), "n₁"
    elif theta1 == "x":
        val = n2 * math.sin(math.radians(theta2)) / n1
        if abs(val) > 1:
            print("\n  Error: no valid angle — total internal reflection may apply.")
            input("\n  Press Enter to return.")
            return
        result, label = math.degrees(math.asin(val)), "θ₁ (degrees)"
    elif n2 == "x":
        result, label = n1 * math.sin(math.radians(theta1)) / math.sin(math.radians(theta2)), "n₂"
    else:
        val = n1 * math.sin(math.radians(theta1)) / n2
        if abs(val) > 1:
            print("\n  Error: no valid angle — total internal reflection may apply.")
            input("\n  Press Enter to return.")
            return
        result, label = math.degrees(math.asin(val)), "θ₂ (degrees)"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def thin_lens():
    print("\n============================================================")
    print("                  THIN LENS / MIRROR EQUATION")
    print("                   1/f = 1/do + 1/di")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    f = get_float("\n  Enter focal length (f): ")
    do = get_float("  Enter object distance (do): ")
    di = get_float("  Enter image distance (di): ")

    unknowns = [i for i in [f, do, di] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if f == "x":
        result, label = 1 / (1/do + 1/di), "f"
    elif do == "x":
        result, label = 1 / (1/f - 1/di), "do"
    else:
        result, label = 1 / (1/f - 1/do), "di"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def magnification():
    print("\n============================================================")
    print("                     MAGNIFICATION")
    print("                     m = -di / do")
    print("  Negative m = inverted image")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    m = get_float("\n  Enter magnification (m): ")
    di = get_float("  Enter image distance (di): ")
    do = get_float("  Enter object distance (do): ")

    unknowns = [i for i in [m, di, do] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if m == "x":
        result, label = -di / do, "m"
    elif di == "x":
        result, label = -m * do, "di"
    else:
        result, label = -di / m, "do"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def circuits_menu():
    while True:
        print("\n============================================================")
        print("                        CIRCUITS")
        print("============================================================")
        print("  [1] Ohm's Law           (V = IR)")
        print("  [2] Series resistance   (R = R₁ + R₂ + ...)")
        print("  [3] Parallel resistance (1/R = 1/R₁ + 1/R₂ + ...)")
        print("  [4] Electrical power    (P = IV = I²R = V²/R)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            ohms_law()
        elif choice == "2":
            series_resistance()
        elif choice == "3":
            parallel_resistance()
        elif choice == "4":
            electrical_power()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def ohms_law():
    print("\n============================================================")
    print("                       OHM'S LAW")
    print("                        V = IR")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    v = get_float("\n  Enter voltage (V, volts): ")
    i = get_float("  Enter current (I, amps): ")
    r = get_float("  Enter resistance (R, ohms): ")

    unknowns = [val for val in [v, i, r] if val == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if v == "x":
        result, label = i * r, "V (volts)"
    elif i == "x":
        result, label = v / r, "I (amps)"
    else:
        result, label = v / i, "R (ohms)"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def series_resistance():
    print("\n============================================================")
    print("                    SERIES RESISTANCE")
    print("               R_total = R₁ + R₂ + R₃ + ...")
    print("============================================================")
    resistances = []
    while True:
        raw = input(f"  Enter R{len(resistances)+1} (or press Enter to finish): ").strip()
        if raw == "":
            if len(resistances) < 2:
                print("  Please enter at least 2 resistors.")
                continue
            break
        try:
            resistances.append(float(raw))
        except ValueError:
            print("  Invalid input.")

    result = sum(resistances)
    print(f"\n  R_total = {result:.4f} Ω")
    input("\n  Press Enter to return.")


def parallel_resistance():
    print("\n============================================================")
    print("                   PARALLEL RESISTANCE")
    print("          1/R_total = 1/R₁ + 1/R₂ + 1/R₃ + ...")
    print("============================================================")
    resistances = []
    while True:
        raw = input(f"  Enter R{len(resistances)+1} (or press Enter to finish): ").strip()
        if raw == "":
            if len(resistances) < 2:
                print("  Please enter at least 2 resistors.")
                continue
            break
        try:
            resistances.append(float(raw))
        except ValueError:
            print("  Invalid input.")

    result = 1 / sum(1/r for r in resistances)
    print(f"\n  R_total = {result:.4f} Ω")
    input("\n  Press Enter to return.")


def electrical_power():
    while True:
        print("\n============================================================")
        print("                    ELECTRICAL POWER")
        print("============================================================")
        print("  [1] P = IV")
        print("  [2] P = I²R")
        print("  [3] P = V²/R")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect a formula: ")

        if choice == "1":
            p = get_float("\n  Enter power (P, W): ")
            i = get_float("  Enter current (I, A): ")
            v = get_float("  Enter voltage (V, V): ")
            unknowns = [val for val in [p, i, v] if val == "x"]
            if len(unknowns) != 1:
                print("\n  Error: please enter exactly one x.")
            elif p == "x":
                print(f"\n  P = {i * v:.4f} W")
            elif i == "x":
                print(f"\n  I = {p / v:.4f} A")
            else:
                print(f"\n  V = {p / i:.4f} V")
            input("\n  Press Enter to return.")

        elif choice == "2":
            p = get_float("\n  Enter power (P, W): ")
            i = get_float("  Enter current (I, A): ")
            r = get_float("  Enter resistance (R, Ω): ")
            unknowns = [val for val in [p, i, r] if val == "x"]
            if len(unknowns) != 1:
                print("\n  Error: please enter exactly one x.")
            elif p == "x":
                print(f"\n  P = {i**2 * r:.4f} W")
            elif i == "x":
                print(f"\n  I = {(p/r)**0.5:.4f} A")
            else:
                print(f"\n  R = {p / i**2:.4f} Ω")
            input("\n  Press Enter to return.")

        elif choice == "3":
            p = get_float("\n  Enter power (P, W): ")
            v = get_float("  Enter voltage (V, V): ")
            r = get_float("  Enter resistance (R, Ω): ")
            unknowns = [val for val in [p, v, r] if val == "x"]
            if len(unknowns) != 1:
                print("\n  Error: please enter exactly one x.")
            elif p == "x":
                print(f"\n  P = {v**2 / r:.4f} W")
            elif v == "x":
                print(f"\n  V = {(p*r)**0.5:.4f} V")
            else:
                print(f"\n  R = {v**2 / p:.4f} Ω")
            input("\n  Press Enter to return.")

        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def electrostatics_menu():
    while True:
        print("\n============================================================")
        print("                      ELECTROSTATICS")
        print("============================================================")
        print("  [1] Coulomb's Law     (F = kq₁q₂/r²)")
        print("  [2] Electric Field    (E = F/q = kq/r²)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            coulombs_law()
        elif choice == "2":
            electric_field()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def coulombs_law():
    print("\n============================================================")
    print("                     COULOMB'S LAW")
    print("                  F = k · q₁ · q₂ / r²")
    print("  k = 8.99×10⁹ N·m²/C²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    k = 8.99e9
    f = get_float("\n  Enter force (F, N): ")
    q1 = get_float("  Enter charge 1 (q₁, C): ")
    q2 = get_float("  Enter charge 2 (q₂, C): ")
    r = get_float("  Enter distance (r, m): ")

    unknowns = [i for i in [f, q1, q2, r] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if f == "x":
        result, label = k * q1 * q2 / r**2, "F (N)"
    elif q1 == "x":
        result, label = f * r**2 / (k * q2), "q₁ (C)"
    elif q2 == "x":
        result, label = f * r**2 / (k * q1), "q₂ (C)"
    else:
        result, label = (k * q1 * q2 / f) ** 0.5, "r (m)"

    print(f"\n  {label} = {result:.6e}")
    input("\n  Press Enter to return.")


def electric_field():
    print("\n============================================================")
    print("                     ELECTRIC FIELD")
    print("                  E = kq / r²  =  F / q")
    print("  k = 8.99×10⁹ N·m²/C²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    k = 8.99e9

    mode = input("\n  Solve using [1] E = kq/r²  or  [2] E = F/q? ")

    if mode == "1":
        e = get_float("\n  Enter electric field (E, N/C): ")
        q = get_float("  Enter charge (q, C): ")
        r = get_float("  Enter distance (r, m): ")
        unknowns = [i for i in [e, q, r] if i == "x"]
        if len(unknowns) != 1:
            print("\n  Error: please enter exactly one x.")
        elif e == "x":
            print(f"\n  E = {k * q / r**2:.6e} N/C")
        elif q == "x":
            print(f"\n  q = {e * r**2 / k:.6e} C")
        else:
            print(f"\n  r = {(k * q / e)**0.5:.4f} m")

    elif mode == "2":
        e = get_float("\n  Enter electric field (E, N/C): ")
        f = get_float("  Enter force (F, N): ")
        q = get_float("  Enter charge (q, C): ")
        unknowns = [i for i in [e, f, q] if i == "x"]
        if len(unknowns) != 1:
            print("\n  Error: please enter exactly one x.")
        elif e == "x":
            print(f"\n  E = {f / q:.6e} N/C")
        elif f == "x":
            print(f"\n  F = {e * q:.6e} N")
        else:
            print(f"\n  q = {f / e:.6e} C")
    else:
        print("\n  Invalid selection.")

    input("\n  Press Enter to return.")


# ============================================================
# THERMODYNAMICS
# ============================================================

def thermodynamics_menu():
    while True:
        print("\n============================================================")
        print("                     THERMODYNAMICS")
        print("============================================================")
        print("  [1] Ideal Gas Law   (PV = nRT)")
        print("  [2] Carnot Efficiency (η = 1 - Tc/Th)")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            ideal_gas_law()
        elif choice == "2":
            carnot_efficiency()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def ideal_gas_law():
    print("\n============================================================")
    print("                     IDEAL GAS LAW")
    print("                      PV = nRT")
    print("  R = 8.314 J/(mol·K)  —  T must be in Kelvin")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    R = 8.314
    p = get_float("\n  Enter pressure (P, Pa): ")
    v = get_float("  Enter volume (V, m³): ")
    n = get_float("  Enter moles (n, mol): ")
    t = get_float("  Enter temperature (T, K): ")

    unknowns = [i for i in [p, v, n, t] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if p == "x":
        result, label = n * R * t / v, "P (Pa)"
    elif v == "x":
        result, label = n * R * t / p, "V (m³)"
    elif n == "x":
        result, label = p * v / (R * t), "n (mol)"
    else:
        result, label = p * v / (n * R), "T (K)"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def carnot_efficiency():
    print("\n============================================================")
    print("                   CARNOT EFFICIENCY")
    print("                   η = 1 - Tc / Th")
    print("  Temperatures must be in Kelvin.")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    eta = get_float("\n  Enter efficiency (η, as decimal e.g. 0.4): ")
    tc = get_float("  Enter cold reservoir temp (Tc, K): ")
    th = get_float("  Enter hot reservoir temp (Th, K): ")

    unknowns = [i for i in [eta, tc, th] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if eta == "x":
        result, label = 1 - tc / th, "η"
    elif tc == "x":
        result, label = th * (1 - eta), "Tc (K)"
    else:
        result, label = tc / (1 - eta), "Th (K)"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")


def gravity_menu():
    while True:
        print("\n============================================================")
        print("                    GRAVITATIONAL FORCE")
        print("               F = G · m₁ · m₂ / r²")
        print("  G = 6.674×10⁻¹¹ N·m²/kg²")
        print("============================================================")
        print("  [1] Calculate gravitational force")
        print("  [0] Back")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            gravitational_force()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def gravitational_force():
    print("\n============================================================")
    print("                  GRAVITATIONAL FORCE")
    print("               F = G · m₁ · m₂ / r²")
    print("  G = 6.674×10⁻¹¹ N·m²/kg²")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")
    G = 6.674e-11
    f = get_float("\n  Enter force (F, N): ")
    m1 = get_float("  Enter mass 1 (m₁, kg): ")
    m2 = get_float("  Enter mass 2 (m₂, kg): ")
    r = get_float("  Enter distance (r, m): ")

    unknowns = [i for i in [f, m1, m2, r] if i == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if f == "x":
        result, label = G * m1 * m2 / r**2, "F (N)"
    elif m1 == "x":
        result, label = f * r**2 / (G * m2), "m₁ (kg)"
    elif m2 == "x":
        result, label = f * r**2 / (G * m1), "m₂ (kg)"
    else:
        result, label = (G * m1 * m2 / f) ** 0.5, "r (m)"

    print(f"\n  {label} = {result:.6e}")
    input("\n  Press Enter to return.")

def materials_menu():
    while True:
        print("\n============================================================")
        print("                    MATERIALS SCIENCE")
        print("============================================================")
        print("  [1] Engineering Stress")
        print("  [2] Engineering Strain")
        print("  [3] True Stress")
        print("  [4] True Strain")
        print("  [5] Lever Rule")
        print("  [6] Bimetallic Strip Deflection")
        print("  [7] Heat Capacity (Q = mcΔT)")
        print("  [8] Calorimetry (Two Substances)")
        print("  [0] Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect an option: ")

        if choice == "1":
            stress_calc()
        elif choice == "2":
            strain_calc()
        elif choice == "3":
            true_stress_calc()
        elif choice == "4":
            true_strain_calc()
        elif choice == "5":
            lever_rule()
        elif choice == "6":
            bimetallic_strip()
        elif choice == "7":
            heat_capacity_single()
        elif choice == "8":
            calorimetry_two_substance()
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")

def stress_calc():
    print("\n============================================================")
    print("                          STRESS")
    print("                      σ = F / A")
    print("  Enter x for the unknown you want to solve for.")
    print("  (Units depend on inputs, e.g. Pa = N/m², psi = lb/in²)")
    print("============================================================")

    stress = get_float("\n  Enter stress (σ): ")
    force = get_float("  Enter force (F): ")
    area = get_float("  Enter area (A): ")

    unknowns = [v for v in [stress, force, area] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if stress == "x":
        result = force / area
        label = "Stress"
    elif force == "x":
        result = stress * area
        label = "Force"
    else:
        result = force / stress
        label = "Area"

    print(f"\n  {label} = {result:.4f}")
    print("  (Units depend on inputs, e.g. Pa = N/m², psi = lb/in²)")
    input("\n  Press Enter to return.")


def strain_calc():
    print("\n============================================================")
    print("                          STRAIN")
    print("                   ε = ΔL / L₀")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    strain = get_float("\n  Enter strain (ε): ")
    delta_l = get_float("  Enter change in length (ΔL): ")
    original_l = get_float("  Enter original length (L₀): ")

    unknowns = [v for v in [strain, delta_l, original_l] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if strain == "x":
        result = delta_l / original_l
        label = "Strain"
        print(f"\n  {label} = {result:.6f}  (dimensionless)")
    elif delta_l == "x":
        result = strain * original_l
        label = "ΔL"
        print(f"\n  {label} = {result:.4f}")
    else:
        result = delta_l / strain
        label = "L₀"
        print(f"\n  {label} = {result:.4f}")

    input("\n  Press Enter to return.")

def true_stress_calc():
    print("\n============================================================")
    print("                       TRUE STRESS")
    print("                  σ_true = F / A_instant")
    print("============================================================")

    force = get_float("\n  Enter force (F): ")
    area = get_float("  Enter instantaneous area (A): ")

    if force == "x" or area == "x":
        print("\n  Error: please enter numbers only.")
    else:
        result = force / area
        print(f"\n  True Stress = {result:.4f}")

    input("\n  Press Enter to return.")


def true_strain_calc():
    print("\n============================================================")
    print("                       TRUE STRAIN")
    print("                  ε_true = ln(L / L₀)")
    print("============================================================")

    length = get_float("\n  Enter current length (L): ")
    original_length = get_float("  Enter original length (L₀): ")

    if length == "x" or original_length == "x":
        print("\n  Error: please enter numbers only.")
    else:
        result = math.log(length / original_length)
        print(f"\n  True Strain = {result:.6f}  (dimensionless)")

    input("\n  Press Enter to return.")

def lever_rule():
    print("\n============================================================")
    print("                       LEVER RULE")
    print("           Fraction α = (C_β - C₀) / (C_β - C_α)")
    print("  All compositions in the same units (e.g. wt%)")
    print("============================================================")

    c0 = get_float("\n  Enter overall composition (C₀): ")
    c_alpha = get_float("  Enter composition of α phase (C_α): ")
    c_beta = get_float("  Enter composition of β phase (C_β): ")

    if "x" in [c0, c_alpha, c_beta]:
        print("\n  Error: please enter numbers only.")
        input("\n  Press Enter to return.")
        return

    fraction_alpha = (c_beta - c0) / (c_beta - c_alpha)
    fraction_beta = 1 - fraction_alpha

    print(f"\n  Fraction of α phase = {fraction_alpha:.4f}")
    print(f"  Fraction of β phase = {fraction_beta:.4f}")
    input("\n  Press Enter to return.")

def bimetallic_strip():
    print("\n============================================================")
    print("                BIMETALLIC STRIP DEFLECTION")
    print("              dx = (L² / 8t) · (α₂ - α₁) · ΔT")
    print("  (Classroom approximation formula)")
    print()
    print("  Note: this is a simplified formula. The full Timoshenko")
    print("  bimetallic strip formula accounts for differing layer")
    print("  thicknesses and elastic moduli, and is not calculated here.")
    print("============================================================")

    length_unit, length_convertible = get_units("length")
    length = get_float(f"\n  Enter strip length (L, {length_unit}): ")
    thickness = get_float(f"  Enter layer thickness (t, {length_unit}): ")
    alpha2 = get_float("  Enter thermal expansion coefficient, layer 2 (α₂): ")
    alpha1 = get_float("  Enter thermal expansion coefficient, layer 1 (α₁): ")

    temp_unit, temp_convertible = get_units("temperature change", unit_type="temperature")
    delta_t = get_float(f"  Enter change in temperature (ΔT, °{temp_unit}): ")

    if "x" in [length, thickness, alpha2, alpha1, delta_t]:
        print("\n  Error: please enter numbers only (no solving for unknowns here).")
        input("\n  Press Enter to return.")
        return

    result = (length**2 / (8 * thickness)) * (alpha2 - alpha1) * delta_t
    print(f"\n  Deflection (dx) = {result:.6f} {length_unit}")

    if length_convertible:
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            unit_conversion(result, length_unit, power=1)

    input("\n  Press Enter to return.")

def heat_capacity_single():
    print("\n============================================================")
    print("                  HEAT CAPACITY")
    print("                  Q = m c ΔT")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    energy_unit, energy_convertible = get_units("heat energy", unit_type="energy")
    q = get_float(f"\n  Enter heat energy (Q, {energy_unit}): ")
    mass = get_float("  Enter mass (m): ")
    specific_heat = get_float("  Enter specific heat (c): ")
    delta_t = get_float("  Enter change in temperature (ΔT): ")

    unknowns = [v for v in [q, mass, specific_heat, delta_t] if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if q == "x":
        result = mass * specific_heat * delta_t
        label = f"Q ({energy_unit})"
    elif mass == "x":
        result = q / (specific_heat * delta_t)
        label = "Mass"
    elif specific_heat == "x":
        result = q / (mass * delta_t)
        label = "Specific Heat"
    else:
        result = q / (mass * specific_heat)
        label = "ΔT"

    print(f"\n  {label} = {result:.4f}")

    if energy_convertible and q == "x":
        convert = input("\n  Would you like to convert this result? (y/n): ")
        if convert.lower() == "y":
            unit_conversion(result, energy_unit, power=1, unit_type="energy")

    input("\n  Press Enter to return.")

def calorimetry_two_substance():
    print("\n============================================================")
    print("              CALORIMETRY — TWO SUBSTANCES")
    print("        m₁c₁(T_f - T₁) + m₂c₂(T_f - T₂) = 0")
    print("  Enter x for the unknown you want to solve for.")
    print("============================================================")

    m1 = get_float("\n  Enter mass 1 (m₁): ")
    c1 = get_float("  Enter specific heat 1 (c₁): ")
    t1 = get_float("  Enter initial temperature 1 (T₁): ")
    m2 = get_float("  Enter mass 2 (m₂): ")
    c2 = get_float("  Enter specific heat 2 (c₂): ")
    t2 = get_float("  Enter initial temperature 2 (T₂): ")
    tf = get_float("  Enter final equilibrium temperature (T_f): ")

    values = [m1, c1, t1, m2, c2, t2, tf]
    unknowns = [v for v in values if v == "x"]
    if len(unknowns) != 1:
        print("\n  Error: please enter exactly one x.")
        input("\n  Press Enter to return.")
        return

    if tf == "x":
        result = (m1 * c1 * t1 + m2 * c2 * t2) / (m1 * c1 + m2 * c2)
        label = "T_f"
    elif t1 == "x":
        result = tf + (m2 * c2 * (tf - t2)) / (m1 * c1)
        label = "T₁"
    elif t2 == "x":
        result = tf + (m1 * c1 * (tf - t1)) / (m2 * c2)
        label = "T₂"
    elif m1 == "x":
        result = -(m2 * c2 * (tf - t2)) / (c1 * (tf - t1))
        label = "m₁"
    elif m2 == "x":
        result = -(m1 * c1 * (tf - t1)) / (c2 * (tf - t2))
        label = "m₂"
    elif c1 == "x":
        result = -(m2 * c2 * (tf - t2)) / (m1 * (tf - t1))
        label = "c₁"
    else:
        result = -(m1 * c1 * (tf - t1)) / (m2 * (tf - t2))
        label = "c₂"

    print(f"\n  {label} = {result:.4f}")
    input("\n  Press Enter to return.")



def unit_conversion_menu():
    while True:
        print("\n============================================================")
        print("                    UNIT CONVERSION")
        print("============================================================")
        print("  [1]  Length")
        print("  [2]  Area")
        print("  [3]  Volume")
        print("  [4]  Temperature")
        print("  [5]  Energy")
        print("  [6]  Force")
        print("  [7]  Pressure")
        print("  [8]  Mass")
        print("  [9]  Time")
        print("  [10] Speed")
        print("  [11] Angle")
        print("  [12] Acceleration")
        print("  [0]  Back to Main Menu")
        print("============================================================")

        choice = input("\nSelect a unit type: ")

        if choice == "1":
            standalone_conversion("length", "length", power=1)
        elif choice == "2":
            standalone_conversion("area", "length", power=2)
        elif choice == "3":
            standalone_conversion("volume", "length", power=3)
        elif choice == "4":
            standalone_temperature_conversion()
        elif choice == "5":
            standalone_conversion("energy", "energy", power=1)
        elif choice == "6":
            standalone_conversion("force", "force", power=1)
        elif choice == "7":
            standalone_conversion("pressure", "pressure", power=1)
        elif choice == "8":
            standalone_conversion("mass", "mass", power=1)
        elif choice == "9":
            standalone_conversion("time", "time", power=1)
        elif choice == "10":
            standalone_conversion("speed", "speed", power=1)
        elif choice == "11":
            standalone_angle_conversion()
        elif choice == "12":
            standalone_conversion("acceleration", "acceleration", power=1)
        elif choice == "0":
            break
        else:
            print("\nInvalid selection. Please try again.")


def standalone_conversion(label, unit_type, power=1):
    print(f"\n  Enter the value and units to convert.")
    unit, convertible = get_units(label, unit_type=unit_type)
    if not convertible:
        print("\n  Cannot convert custom units.")
        input("  Press Enter to return.")
        return
    value = get_float(f"\n  Enter value ({unit}): ")
    if value == "x":
        print("\n  Error: please enter a number.")
        input("  Press Enter to return.")
        return
    unit_conversion(value, unit, power=power, unit_type=unit_type)


def standalone_temperature_conversion():
    print(f"\n  Enter the temperature and units to convert.")
    unit, _ = get_units("temperature", unit_type="temperature")
    value = get_float(f"\n  Enter temperature (°{unit}): ")
    if value == "x":
        print("\n  Error: please enter a number.")
        input("  Press Enter to return.")
        return
    unit_conversion(value, unit, unit_type="temperature")


def standalone_angle_conversion():
    print(f"\n  Enter the angle and units to convert.")
    unit, _ = get_units("angle", unit_type="angle")
    value = get_float(f"\n  Enter angle ({unit}): ")
    if value == "x":
        print("\n  Error: please enter a number.")
        input("  Press Enter to return.")
        return
    unit_conversion(value, unit, unit_type="angle")

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
        print("  [5] Differential Equations")
        print("  [6] Statics")
        print("  [7] Physics")
        print("  [8] Materials Science")
        print("  [9] Unit Conversion")
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
            diff_eq_menu()
        elif choice == "6":
            statics_menu()
        elif choice == "7":
            physics_menu()
        elif choice == "8":
            materials_menu()
        elif choice == "9":
            unit_conversion_menu()
        elif choice == "0":
            print("\nExiting calculator. Goodbye!")
            break
        else:
            print("\nInvalid selection. Please try again.")

main_menu()