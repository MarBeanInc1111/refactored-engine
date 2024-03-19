import unittest
from pilot.utils.style import style_config, Theme, ColorName, get_color_function

# TestColorStyle class inherits from unittest.TestCase and contains methods for testing
# the functionality of the color styles in the 'pilot.utils.style' module.
class TestColorStyle(unittest.TestCase):
    def test_initialization(self):
        # This test method checks the initialization of the theme in style_config.
        print("\n[INFO] Testing Theme Initialization...")
        style_config.set_theme(Theme.DARK)  # Set the theme to DARK
        print(f"[INFO] Set theme to: {Theme.DARK}, Current theme: {style_config.theme}")
        self.assertEqual(style_config.theme, Theme.DARK)  # Assert that the current theme is DARK

        style_config.set_theme(Theme.LIGHT)  # Set the theme to LIGHT
        print(f"[INFO] Set theme to: {Theme.LIGHT}, Current theme: {style_config.theme}")
        self.assertEqual(style_config.theme, Theme.LIGHT)  # Assert that the current theme is LIGHT

    def test_color_function(self):
        # This test method checks the functionality of the color functions in the 'pilot.utils.style' module.
        dark_color_codes = {
            ColorName.RED: "\x1b[31m",
            ColorName.GREEN: "\x1b[32m",
            # ... other colors
        }
        light_color_codes = {
            ColorName.RED: "\x1b[91m",
            ColorName.GREEN: "\x1b[92m",
            # ... other colors
        }
        reset = "\x1b[0m"

        # Test DARK theme
        print("\n[INFO] Testing DARK Theme Colors...")
        style_config.set_theme(Theme.DARK)  # Set the theme to DARK
        for color_name, code in dark_color_codes.items():
            with self.subTest(color=color_name):
                # Test the color function for each color in DARK theme
                color_func = get_color_function(color_name, bold=False)
                print(f"[INFO] Testing color: {color_name}, Expect: {code}Test, Got: {color_func('Test')}")
                self.assertEqual(color_func("Test"), f"{code}Test{reset}")  # Assert that the color function returns the correct color code

                color_func = get_color_function(color_name, bold=True)
                print(f"[INFO] Testing color (bold): {color_name}, Expect: {code}\x1b[1mTest, Got: {color_func('Test')}")
                self.assertEqual(color_func("Test"), f"{code}\x1b[1mTest{reset}")  # Assert that the color function returns the correct color code with bold

        # Test LIGHT theme
        print("\n[INFO] Testing LIGHT Theme Colors...")
        style_config.set_theme(Theme.LIGHT)  # Set the theme to LIGHT
        for color_name, code in light_color_codes.items():
            with self.subTest(color=color_name):
                # Test the color function for each color in LIGHT theme
                color_func = get_color_function(color_name, bold=False)
                print(f"[INFO] Testing color: {color_name}, Expect: {code}Test, Got: {color_func('Test')}")
                self.assertEqual(color_func("Test"), f"{code}Test{reset}")  # Assert that the color function returns the correct color code

                color_func = get_color_function(color_name, bold=True)
                print(f"[INFO] Testing color (bold): {color_name}, Expect: {code}\x1b[1mTest, Got: {color_func('Test')}")
                self.assertEqual(color_func("Test"), f"{code}\x1b[1mTest{reset}")  # Assert that the
