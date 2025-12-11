import sys
import tty
import termios
import time
import os
import string

class Libraries:
    def _getch(self):
        """
        Gets a single character from standard input without requiring Enter.
        Works on Unix-like systems only.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)  # Read 3 bytes to capture arrow key sequences
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def select(self, question: str, choices: list):
        """
        Displays an interactive menu and allows the user to select an option
        using up/down arrow keys and Enter.
        Args:
            question (str): The question to display above the menu.
            choices (list): A list of strings representing the choices.
        Returns:
            str: The selected choice.
        """
        selected_index = 0
        CURSOR_UP = '\x1b[1A'
        CLEAR_LINE = '\x1b[2K'
        while True:
            self.print_color(question, "cyan")
            for i, choice in enumerate(choices):
                if i == selected_index:
                    self.print_color(f"> {choice}", "yellow")
                else:
                    print(f"  {choice}")
            key = self._getch()
            if key and key.startswith('\x1b') and key[-1] == 'A':  # Up arrow
                selected_index = (selected_index - 1 + len(choices)) % len(choices)
            elif key and key.startswith('\x1b') and key[-1] == 'B':  # Down arrow
                selected_index = (selected_index + 1) % len(choices)
            elif key and (key[0] == '\r' or key[0] == '\n' or ord(key[0]) in (10, 13)):
                for _ in range(len(choices) + 1):
                    sys.stdout.write(CURSOR_UP + CLEAR_LINE)
                sys.stdout.flush()
                return choices[selected_index]
            for _ in range(len(choices) + 1):
                sys.stdout.write(CURSOR_UP)
            sys.stdout.flush()

    COLORS = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "purple": "35",
        "yellow-green": "92",
    }

    PREFIX = "\x1b["
    SUFFIX = "\x1b[0m"

    def print_color(self, text: str, color: str):
        """
        Prints text to the console in a specified color.
        Args:
            text (str): The text to print.
            color (str): The name of the color to use (e.g., "red", "green").
        """
        color_code = self.COLORS.get(color.lower())
        if color_code:
            styled_text = f"{self.PREFIX}{color_code}m{text}{self.SUFFIX}"
            print(styled_text)
        else:
            print(text)
    def print_color_font(self, text: str, color: str, font_name: str):
        """
        Prints text to the console in a specified color and font.
        Args:
            text (str): The text to print.
            color (str): The name of the color to use (e.g., "red", "green").
            font_name (str): The name of the font to use (e.g., "Fancy", "Bold", "Glitch").
        """
        font_mapping = {
            "Fancy": self.FancyFont(),
            "Bold": self.BoldFont(),
            "Glitch": self.GlitchFont()
            "Monospace": self.MonospaceFont(),
            "Handwriting": self.HandwritingFont()
        }
        font = font_mapping.get(font_name)
        if font:
            transformed_text = font.apply(text)
            self.print_color(transformed_text, color)
        else:
            print(f"Font '{font_name}' not found.")

    def slow_type(self, text, speed=0.05, color=None):
        """
        Prints text to the console with a typing effect.
        Args:
            text (str): The text to be printed.
            speed (float): The delay between each character in seconds.
            color (str|None): Optional color name from the `COLORS` map (e.g., 'red', 'cyan').
        """
        color_code = None
        if color:
            color_code = self.COLORS.get(color.lower())

        if color_code:
            sys.stdout.write(f"{self.PREFIX}{color_code}m")

        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)

        if color_code:
            sys.stdout.write(self.SUFFIX)
            sys.stdout.write("\n")

    # Font classes
    class Font:
        def __init__(self, name, mapping):
            self.name = name
            self.mapping = mapping

        def apply(self, text):
            return ''.join(self.mapping.get(char, char) for char in text)

    class FancyFont(Font):
        def __init__(self):
            mapping = {
                'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴',
                'F': '𝙵', 'G': '𝙶', 'H': '𝙷', 'I': '𝙸', 'J': '𝙹',
                'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽', 'O': '𝙾',
                'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃',
                'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉',
                'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': '𝑒',
                'f': '𝒻', 'g': '𝑔', 'h': '𝒽', 'i': '𝒾', 'j': '𝒿',
                'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃', 'o': '𝑜',
                'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉',
                'u': '𝓊', 'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏'
            }
            super().__init__('Fancy', mapping)

    class BoldFont(Font):
        def __init__(self):
            mapping = {
                'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼',
                'F': '𝔽', 'G': '𝔾', 'H': 'ℍ', 'I': '𝕀', 'J': '𝕁',
                'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ', 'O': '𝕆',
                'P': 'ℙ', 'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋',
                'U': '𝕌', 'V': '𝕍', 'W': '𝕎', 'X': '𝕏', 'Y': '𝕐', 'Z': '𝕏',
                'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖',
                'f': '𝕗', 'g': '𝕘', 'h': '𝕙', 'i': '𝕚', 'j': '𝕛',
                'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟', 'o': '𝕠',
                'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥',
                'u': '𝕦', 'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫'
            }
            super().__init__('Bold', mapping)

    class GlitchFont(Font):
        def __init__(self):
            mapping = {
                'A': 'ꋫ', 'B': 'ꃃ', 'C': 'ꏸ', 'D': 'ꁕ', 'E': 'ꍟ',
                'F': 'ꄘ', 'G': 'ꁍ', 'H': 'ꑛ', 'I': 'ꂑ', 'J': 'ꀭ',
                'K': 'ꀗ', 'L': '꒒', 'M': 'ꁒ', 'N': 'ꁹ', 'O': 'ꆂ',
                'P': 'ꉣ', 'Q': 'ꋫ', 'R': '꒓', 'S': 'ꌚ', 'T': '꓅',
                'U': 'ꐇ', 'V': 'ꏝ', 'W': 'ꅐ', 'X': 'ꇓ', 'Y': 'ꐟ', 'Z': 'ꁴ',
                'a': 'ꋫ', 'b': 'ꃃ', 'c': 'ꏸ', 'd': 'ꁕ', 'e': 'ꍟ',
                'f': 'ꄘ', 'g': 'ꁍ', 'h': 'ꑛ', 'i': 'ꂑ', 'j': 'ꀭ',
                'k': 'ꀗ', 'l': '꒒', 'm': 'ꁒ', 'n': 'ꁹ', 'o': 'ꆂ',
                'p': 'ꉣ', 'q': 'ꋫ', 'r': '꒓', 's': 'ꌚ', 't': '꓅',
                'u': 'ꐇ', 'v': 'ꏝ', 'w': 'ꅐ', 'x': 'ꇓ', 'y': 'ꐟ', 'z': 'ꁴ'
            }
            super().__init__('Glitch', mapping)

    class MonospaceFont(Font):
        def __init__(self):
            mapping = {
                'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶', 'H': '𝙷',
                'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽' 'O': '𝙾', 'P': '𝙿',
                'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄', 'V': '𝚅', 'W': '𝚆', 'X': '𝚇',
                'Y': '𝚈', 'Z': '𝚉', 'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏',
                'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗',
                'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟',
                'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣'
            }
            super().__init__('Monospace', mapping)

    class HandwritingFont(Font):
        def __init__(self):
            mapping = {
                'A': '𝒜', 'B': 'ℬ', 'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢', 'H': 'ℋ',
                'I': 'ℐ', 'J': '𝒥', 'K': '𝒦', 'L': 'ℒ', 'M': 'ℳ', 'N': '𝒩', 'O': '𝒪', 'P': '𝒫',
                'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰', 'V': '𝒱', 'W': '𝒲', 'X': '𝒳',
                'Y': '𝒴', 'Z': '𝒵', 'a': '𝒶', 'b': '𝒷',  'c': '𝒸',  'd': '𝒹',  'e': 'ℯ',
                'f': '𝒻',  'g': 'ℊ',  'h': '𝒽',  'i': '𝒾',  'j': '𝒿',  'k': '𝓀',
                'l': '𝓁',  'm': '𝓂',  'n': '𝓃',  'o': 'ℴ',  'p': '𝓅',  'q': '𝓆',
                'r': '𝓇',  's':  '𝓈',  't':  '𝓉',  'u':  '𝓊',  'v':  '𝓋',
                'w':  '𝓌',  'x':  '𝓍',  'y':  '𝓎',  'z':  '𝓏'
            }
            super().__init__('Handwriting', mapping)

    


    def slow_type_font_color(self, color: str, font_name: str, text: str, speed: float = 0.1):
        """
        Prints text to the console with a typing effect using the specified font and color.
        Args:
            color (str): The color of the text (e.g., "magenta").
            font_name (str): The name of the font to use (e.g., "Fancy", "Bold", "Glitch").
            text (str): The text to be printed.
            speed (float): The delay between each character in seconds (default is 0.1).
        """
        font_mapping = {
            "Fancy": self.FancyFont(),
            "Bold": self.BoldFont(),
            "Glitch": self.GlitchFont()
            "Monospace": self.MonospaceFont(),
            "Handwriting": self.HandwritingFont()
        }
        font = font_mapping.get(font_name)
        if font:
            transformed_text = font.apply(text)
            self.slow_type(transformed_text, speed=speed, color=color)
        else:
            print(f"Font '{font_name}' not found.")

    def slow_type_color(self, color: str, text: str, speed: float = 0.1):
        """
        Prints text to the console with a typing effect using the specified color.
        Args:
            color (str): The color of the text (e.g., "magenta").
            text (str): The text to be printed.
            speed (float): The delay between each character in seconds (default is 0.1).
        """
        self.slow_type(text, speed=speed, color=color)
    def slow_type_font(self, font_name: str, text: str, speed: float = 0.1):
        """
        Prints text to the console with a typing effect using the specified font.
        Args:
            font_name (str): The name of the font to use (e.g., "Fancy", "Bold", "Glitch").
            text (str): The text to be printed.
            speed (float): The delay between each character in seconds (default is 0.1).
        """
        font_mapping = {
            "Fancy": self.FancyFont(),
            "Bold": self.BoldFont(),
            "Glitch": self.GlitchFont(),
            "Monospace": self.MonospaceFont(),
            "Handwriting": self.HandwritingFont()
        }
        font = font_mapping.get(font_name)
        if font:
            transformed_text = font.apply(text)