# Background Auto Input GUI

A simple Python application with a GUI for performing background mouse clicks and keyboard inputs.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Venom120/BackGroundAutoClicker.git
    cd BackGroundAutoClicker
    ```

3.  **Install using PKGBUILD (Arch Linux):**

    If you are on Arch Linux or a derivative, you can build and install the package system-wide using the provided `PKGBUILD` file. This is the recommended method for desktop integration.

    ```bash
    makepkg -si
    ```

    This will install the application executable to `/usr/bin/bgclicker-gui` and the desktop entry to `/usr/share/applications/`.

## Running the Application

After installing the application using the `PKGBUILD` (recommended for Arch Linux users), you can run it in two ways:

### From the Application Menu

The application should appear in your desktop environment's application menu. Search for "Background Auto Input GUI" and launch it.

### From the Terminal

Open a terminal and run the executable:

```bash
bgclicker-gui
```

### Running without Installation (for Development/Testing)

If you do not wish to install the application system-wide, you can run it directly from the cloned repository directory after installing dependencies in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r req.txt
python main.py
```

## Features

*   Background mouse clicking (Left, Middle, Right)
*   Configurable click delay (ms or seconds)
*   Single click or hold click types
*   Relative click coordinates within a selected window
*   Background keyboard input
*   Global hotkey (F6) to start/stop (requires `keyboard` library and appropriate permissions)
*   Select target window by title

## Troubleshooting

*   **`ModuleNotFoundError: No module named 'keyboard'`**: Ensure you have installed the dependencies using `pip install -r req.txt` and are running the script within the activated virtual environment.
*   **Hotkey (F6) not working**:
    *   Check the terminal for any error or warning messages related to hotkey binding when the application starts.
    *   Global hotkeys on Linux can sometimes require special permissions. Running the application with `sudo` might work as a test (`sudo bgclicker-gui`), but is generally not recommended for security.
    *   The `keyboard` library might have compatibility issues with certain display servers (e.g., Wayland). It generally works better with X11.
    *   Another application or your window manager might be using the F6 hotkey.