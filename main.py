import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time
import keyboard

class AutoInputGUI(tk.Tk): # Inherit from tk.Tk for main window
    def __init__(self):
        super().__init__() # Call parent constructor
        self.title("Background Auto Input GUI")
        self.geometry("720x500")

        self.running = False
        self.hotkey_available = False
        self.listener_thread = None
        self.debug_mode = False # Set to True to enable debug mode

        # Initialize HotkeyHandler logic
        try:
            import keyboard
            self.hotkey_available = True
        except ImportError:
            print("Keyboard library not available. Global hotkeys disabled.")
        except Exception as e:
            print(f"Error importing keyboard library: {e}")
            self.hotkey_available = False

        if self.hotkey_available:
            self.listener_thread = threading.Thread(target=self._run_listener, daemon=True)
            self.listener_thread.start()

        try:
            # Store window titles and their corresponding IDs
            self.window_info = self.get_window_list()
            self.window_list = list(self.window_info.keys())
        except FileNotFoundError:
            messagebox.showerror("xdotool Not Found", "xdotool is not installed. Please install it using your package manager, e.g.,\nsudo apt install xdotool")
            self.window_list = ["No Windows"]
            self.window_info = {} # Ensure window_info is initialized

        for i in range(4): # Increased columnspan for the new button
            self.columnconfigure(i, weight=1) # Use self.columnconfigure

        row = 0
        ttk.Label(self, text="CLICK").grid(row=row, column=0, sticky="w", padx=10, pady=5) # Use self
        ttk.Label(self, text="DELAY").grid(row=row, column=2, columnspan=2, sticky="w", padx=10) # Use self

        row += 1
        self.click_var = tk.StringVar(value="L")
        self.click_radio_buttons = [
            ttk.Radiobutton(self, text="Left", variable=self.click_var, value="L"), # Use self
            ttk.Radiobutton(self, text="Middle", variable=self.click_var, value="M"), # Use self
            ttk.Radiobutton(self, text="Right", variable=self.click_var, value="R") # Use self
        ]
        self.click_radio_buttons[0].grid(row=row, column=0, sticky="w", padx=10)
        self.click_radio_buttons[1].grid(row=row, column=0)
        self.click_radio_buttons[2].grid(row=row, column=0, sticky="e", padx=10)

        self.vertical_separator = ttk.Separator(self, orient="vertical") # Use self
        self.vertical_separator.grid(row=0, column=1, rowspan=3, sticky="ns", padx=10)

        self.delay_var = tk.IntVar(value=1000) # Default delay to 1000ms (1 second)
        self.delay_spinbox = tk.Spinbox(self, from_=1, to=1000, textvariable=self.delay_var, width=5) # Use self
        self.delay_spinbox.grid(row=row, column=2, sticky="w", padx=5)
        self.delay_unit = tk.StringVar(value="ms")
        self.delay_radio_buttons = [
            ttk.Radiobutton(self, text="ms", variable=self.delay_unit, value="ms"), # Use self
            ttk.Radiobutton(self, text="s", variable=self.delay_unit, value="s") # Use self
        ]
        self.delay_radio_buttons[0].grid(row=row, column=2)
        self.delay_radio_buttons[1].grid(row=row, column=3, sticky="w")

        row += 1
        self.click_type = tk.StringVar(value="single")
        self.click_type_radio_buttons = [
            ttk.Radiobutton(self, text="single", variable=self.click_type, value="single"), # Use self
            ttk.Radiobutton(self, text="hold", variable=self.click_type, value="hold") # Use self
        ]
        self.click_type_radio_buttons[0].grid(row=row, column=0, sticky="w", padx=10)
        self.click_type_radio_buttons[1].grid(row=row, column=0)

        row += 1
        ttk.Separator(self, orient="horizontal").grid(row=row, columnspan=4, sticky="ew", pady=10) # Use self

        row += 1
        ttk.Label(self, text="KEYBOARD").grid(row=row, column=0, sticky="w", padx=10) # Use self

        row += 1
        self.kb_enabled = tk.BooleanVar(value=False)
        self.kb_input = tk.Entry(self, state='disabled') # Use self
        self.kb_input.grid(row=row, column=1, columnspan=2, sticky="we", padx=10)
        self.kb_check = ttk.Checkbutton(self, text="Enable", variable=self.kb_enabled, command=self.toggle_keyboard_input) # Use self
        self.kb_check.grid(row=row, column=0, sticky="w", padx=10)

        row += 1
        ttk.Separator(self, orient="horizontal").grid(row=row, columnspan=4, sticky="ew", pady=10) # Use self

        row += 1
        ttk.Label(self, text="WINDOW").grid(row=row, column=0, sticky="w", padx=10) # Use self

        row += 1
        self.window_var = tk.StringVar()
        if self.window_list:
            self.window_var.set(self.window_list[-1])
        self.window_menu = ttk.Combobox(self, textvariable=self.window_var, values=self.window_list) # Use self
        self.window_menu.grid(row=row, column=0, columnspan=4, sticky="we", padx=10)

        row += 1
        ttk.Separator(self, orient="horizontal").grid(row=row, columnspan=4, sticky="ew", pady=10) # Use self

        row += 1
        self.start_button = ttk.Button(self, text="Start (F6)", command=self.toggle_input) # Use self
        self.start_button.grid(row=row, column=0, columnspan=4, pady=10)

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
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Use self.protocol

    def _run_listener(self):
        if not self.hotkey_available:
            return

        try:
            # Attempt to add the F6 hotkey
            keyboard.add_hotkey('f6', self.toggle_input) # Use self.toggle_input as callback
            print("Global hotkey 'F6' registered.")
        except Exception as e:
            print(f"Failed to bind global hotkey 'F6': {e}")
            # In a GUI application, you might want to signal the main thread to show a warning here
            # For now, we'll just print to console.

        # Add debug listener for any key press
        if self.debug_mode:
            self._start_debug_listener()

    def _start_debug_listener(self):
        if not self.hotkey_available:
            return
        try:
            keyboard.on_press(lambda event: print(f"Key pressed: {event.name}"))
            print("Debug listener for key presses started.")
        except Exception as e:
            print(f"Failed to start debug listener: {e}")

    def stop(self):
        if self.hotkey_available: # Removed redundant keyboard is not None check
            try:
                keyboard.unhook_all()
                print("Keyboard hotkeys and listeners unhooked.")
            except Exception as e:
                print(f"Error unhooking keyboard: {e}")

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


    def on_closing(self):
        self.stop() # Call self.stop()
        self.destroy()


if __name__ == "__main__":
    app = AutoInputGUI() # Instantiate AutoInputGUI directly
    app.mainloop() # Use app.mainloop()
