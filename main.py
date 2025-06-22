import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time

from hotkey_handler import HotkeyHandler

class AutoInputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Auto Input GUI")
        self.root.geometry("720x500")

        self.running = False

        try:
            # Store window titles and their corresponding IDs
            self.window_info = self.get_window_list()
            self.window_list = list(self.window_info.keys())
        except FileNotFoundError:
            messagebox.showerror("xdotool Not Found", "xdotool is not installed. Please install it using your package manager, e.g.,\nsudo apt install xdotool")
            self.window_list = ["No Windows"]
            self.window_info = {} # Ensure window_info is initialized

        for i in range(4): # Increased columnspan for the new button
            root.columnconfigure(i, weight=1)

        row = 0
        ttk.Label(root, text="CLICK").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(root, text="DELAY").grid(row=row, column=2, columnspan=2, sticky="w", padx=10)

        row += 1
        self.click_var = tk.StringVar(value="L")
        self.click_radio_buttons = [
            ttk.Radiobutton(root, text="Left", variable=self.click_var, value="L"),
            ttk.Radiobutton(root, text="Middle", variable=self.click_var, value="M"),
            ttk.Radiobutton(root, text="Right", variable=self.click_var, value="R")
        ]
        self.click_radio_buttons[0].grid(row=row, column=0, sticky="w", padx=10)
        self.click_radio_buttons[1].grid(row=row, column=0)
        self.click_radio_buttons[2].grid(row=row, column=0, sticky="e", padx=10)

        self.vertical_separator = ttk.Separator(root, orient="vertical")
        self.vertical_separator.grid(row=0, column=1, rowspan=3, sticky="ns", padx=10)

        self.delay_var = tk.IntVar(value=1000) # Default delay to 1000ms (1 second)
        self.delay_spinbox = tk.Spinbox(root, from_=1, to=1000, textvariable=self.delay_var, width=5)
        self.delay_spinbox.grid(row=row, column=2, sticky="w", padx=5)
        self.delay_unit = tk.StringVar(value="ms")
        self.delay_radio_buttons = [
            ttk.Radiobutton(root, text="ms", variable=self.delay_unit, value="ms"),
            ttk.Radiobutton(root, text="s", variable=self.delay_unit, value="s")
        ]
        self.delay_radio_buttons[0].grid(row=row, column=2)
        self.delay_radio_buttons[1].grid(row=row, column=3, sticky="w")

        row += 1
        self.click_type = tk.StringVar(value="single")
        self.click_type_radio_buttons = [
            ttk.Radiobutton(root, text="single", variable=self.click_type, value="single"),
            ttk.Radiobutton(root, text="hold", variable=self.click_type, value="hold")
        ]
        self.click_type_radio_buttons[0].grid(row=row, column=0, sticky="w", padx=10)
        self.click_type_radio_buttons[1].grid(row=row, column=0)

        row += 1
        ttk.Separator(root, orient="horizontal").grid(row=row, columnspan=4, sticky="ew", pady=10)

        row += 1
        ttk.Label(root, text="KEYBOARD").grid(row=row, column=0, sticky="w", padx=10)

        row += 1
        self.kb_enabled = tk.BooleanVar(value=False)
        self.kb_input = tk.Entry(root, state='disabled')
        self.kb_input.grid(row=row, column=1, columnspan=2, sticky="we", padx=10)
        self.kb_check = ttk.Checkbutton(root, text="Enable", variable=self.kb_enabled, command=self.toggle_keyboard_input)
        self.kb_check.grid(row=row, column=0, sticky="w", padx=10)

        row += 1
        ttk.Separator(root, orient="horizontal").grid(row=row, columnspan=4, sticky="ew", pady=10)

        row += 1
        ttk.Label(root, text="WINDOW").grid(row=row, column=0, sticky="w", padx=10)

        row += 1
        self.window_var = tk.StringVar()
        if self.window_list:
            self.window_var.set(self.window_list[-1])
        self.window_menu = ttk.Combobox(root, textvariable=self.window_var, values=self.window_list)
        self.window_menu.grid(row=row, column=0, columnspan=4, sticky="we", padx=10)

        row += 1
        ttk.Separator(root, orient="horizontal").grid(row=row, columnspan=4, sticky="ew", pady=10)

        row += 1
        self.start_button = ttk.Button(root, text="Start (F6)", command=self.toggle_input)
        self.start_button.grid(row=row, column=0, columnspan=4, pady=10)

        # Initialize HotkeyHandler
        self.hotkey_handler = HotkeyHandler(self.toggle_input)

        # Initialize state for getting coordinates
        self.getting_coords = False

        # Store references to widgets that need to be toggled
        self.widgets_to_toggle = [
            # Click options
            *self.click_radio_buttons,
            *self.click_type_radio_buttons,
            # Delay options
            self.delay_spinbox,
            *self.delay_radio_buttons,
            # Keyboard options
            self.kb_check, self.kb_input,
            # Window selection
            self.window_menu,
            # Start button
            self.start_button,
        ]

        # Set window closing protocol to stop the hotkey handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if hasattr(self, 'hotkey_handler') and self.hotkey_handler:
            self.hotkey_handler.stop()
        self.root.destroy()

    def toggle_keyboard_input(self):
        if self.kb_enabled.get():
            self.kb_input.config(state='normal')
        else:
            self.kb_input.config(state='disabled')

    def get_window_list(self):
        try:
            # Search for all windows (removed --name ".")
            result = subprocess.check_output(["xdotool", "search", "--all", ".*"]).decode().strip()
            win_ids = result.split('\n') if result else []
            window_info = {} # Use a dictionary to store title: id
            for wid in win_ids:
                try:
                    title = subprocess.check_output(["xdotool", "getwindowname", wid]).decode().strip()
                    if title: # Only include windows with a title
                        window_info[title] = wid
                except:
                    # Ignore windows that cause errors when getting the name
                    continue
            return window_info
        except FileNotFoundError:
            raise
        except subprocess.CalledProcessError:
            # Handle case where no windows are found
            return {} # Return empty dictionary

    def toggle_input(self):
        # Prevent starting input while getting coordinates
        if hasattr(self, 'getting_coords') and self.getting_coords:
            return

        if self.running:
            self.running = False
            self.start_button.config(text="Start (F6)")
        else:
            self.running = True
            self.start_button.config(text="Stop (F6)")
            threading.Thread(target=self.start_input, daemon=True).start()

    def start_input(self):
        window_name = self.window_var.get()
        if not window_name:
            messagebox.showerror("No Window Selected", "Please select a window to send input to.")
            self.toggle_input()
            return

        # Get window ID from the stored dictionary
        window_id = self.window_info.get(window_name)
        if not window_id:
             messagebox.showerror("Window Not Found", f"Could not find window with name: {window_name}")
             self.toggle_input()
             return

        delay = self.delay_var.get()
        delay_unit = self.delay_unit.get()
        delay = delay if delay_unit == "ms" else delay * 1000
        click = self.click_var.get()
        hold = self.click_type.get() == "hold"
        keyboard_key = self.kb_input.get() if self.kb_enabled.get() else None

        while self.running:
            if click:
                btn = {"L": 1, "M": 2, "R": 3}[click]
                if hold:
                    subprocess.call(["xdotool", "mousedown", "--window", window_id, str(btn)])
                    time.sleep(0.1)
                    subprocess.call(["xdotool", "mouseup", "--window", window_id, str(btn)])
                else:
                    # Use relative coordinates for click without moving the actual cursor
                    # Corrected xdotool click syntax for coordinates
                    subprocess.call(["xdotool", "click", "--window", window_id, "--clearmodifiers", "--delay", "1", str(btn)])


            if keyboard_key:
                subprocess.call(["xdotool", "key", "--window", window_id, keyboard_key])

            time.sleep(delay / 1000.0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoInputGUI(root)
    root.mainloop()
