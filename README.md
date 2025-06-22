# Background Auto Input GUI

A simple Python application with a GUI for performing background mouse clicks and keyboard inputs.

**- Hold feature and keyboard feature has not been tested yet!!!**

## Setup
1. **Install using yay**
    If you are on Arch Linux or a derivative, you can directly install the software system wide using
    ```bash
    yay -S bgclicker-git
    ```

    A desktop entry named "bgclicker-git" will be created and can be used system wide. This is the recommended method for desktop integration.

2.  **Install using PKGBUILD (Arch Linux):**

    If you are on Arch Linux or a derivative, you can build and install the package system-wide using the provided `PKGBUILD` file.

    ```bash
    makepkg
    ```

These methods will install the application executable to `/usr/bin/bgclicker-git` and the desktop entry to `/usr/share/applications/`.

## Running the Application

### From the Application Menu

The application should appear in your desktop environment's application menu. Search for "bgclicker-git" and launch it.

### From the Terminal

Open a terminal and run the executable:

```bash
sudo bgclicker-git
```

### Running without Installation (for Development/Testing)

If you do not wish to install the application system-wide, you can run it directly from the cloned repository directory after installing dependencies in a virtual environment or system-wide:

#### Dependencies (can install using pacman)
*   python
*   tk
*   python-keyboard

#### To run
```bash
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

*   **Hotkey (F6) not working**:
    *   Global hotkeys on Linux can sometimes require special permissions. Running the application with `sudo` might work as a test (`sudo bgclicker-git`).
    *   The `keyboard` library might have compatibility issues with certain display servers (e.g., Wayland). It generally works better with X11.
    *   Another application or your window manager might be using the F6 hotkey.