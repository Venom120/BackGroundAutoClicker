import keyboard
import threading
import time

class HotkeyHandler:
    def __init__(self, toggle_callback):
        self.toggle_callback = toggle_callback
        self.hotkey_available = False
        self.listener_thread = None
        self.debug_mode = False  # Set to True to enable debug mode

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

    def _run_listener(self):
        if not self.hotkey_available:
            return

        try:
            # Attempt to add the F6 hotkey
            keyboard.add_hotkey('f6', self.toggle_callback)
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
        if self.hotkey_available and keyboard is not None:
            try:
                keyboard.unhook_all()
                print("Keyboard hotkeys and listeners unhooked.")
            except Exception as e:
                print(f"Error unhooking keyboard: {e}")

# Example usage (for testing the class independently if needed)
if __name__ == "__main__":
    def dummy_toggle():
        print("Toggle called!")

    handler = HotkeyHandler(dummy_toggle)
    print("HotkeyHandler initialized. Press F6 or any key.")
    try:
        # Keep the main thread alive for a bit to test
        time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        handler.stop()
        print("Exiting.")