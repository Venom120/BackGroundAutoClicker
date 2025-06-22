# Background Auto Input GUI

A simple Python application with a GUI for performing background mouse clicks and keyboard inputs.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Venom120/BackGroundAutoClicker.git
    cd BackGroundAutoClicker
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r req.txt
    ```

## Running the Application

The application can be run using the provided `start.sh` script or the `BackgroundClicker.desktop` file.

### Using `start.sh`

The `start.sh` script is a simple shell script that:
- Navigates to the application directory.
- Activates the Python virtual environment (`.venv`).
- Runs the main application script (`main.py`).

To run the application using `start.sh`:

1.  Make the script executable:
    ```bash
    chmod +x start.sh
    ```
2.  Execute the script:
    ```bash
    sudo ./start.sh
    ```

### Using `setup.sh`

The `setup.sh` script automates the process of setting up the application for desktop integration. It will:
- Make the `start.sh` script executable.
- Copy the application icon to a recognized location (`/home/your_username/Pictures/Thumbnails/`).
- Copy the `BackgroundClicker.desktop` file to your applications directory (`~/.local/share/applications/`).

To run the setup script:

1.  Make the script executable:
    ```bash
    chmod +x setup.sh
    ```
2.  Execute the script:
    ```bash
    ./setup.sh
    ```
    The script will prompt you to enter your username.

### Using `BackgroundClicker.desktop`

The `BackgroundClicker.desktop` file is a desktop entry file for Linux. It allows you to launch the application from your desktop environment's application menu or by double-clicking the file. It is configured to execute the `start.sh` script.

To use the `.desktop` file:

Before using the `.desktop` file, you need to run the `setup.sh` script to perform the necessary setup steps (making `start.sh` executable, copying the icon and desktop files). See the "Using `setup.sh`" section for instructions.

After running `setup.sh`, the application should appear in your desktop environment's application menu. You can also double-click the `.desktop` file to launch it.

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
    *   Global hotkeys on Linux can sometimes require special permissions. Running the script with `sudo` might work as a test (`sudo ./start.sh`), but is generally not recommended for security.
    *   The `keyboard` library might have compatibility issues with certain display servers (e.g., Wayland). It generally works better with X11.
    *   Another application or your window manager might be using the F6 hotkey.