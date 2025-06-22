#!/bin/bash

# Make start.sh executable
echo "Making start.sh executable..."
chmod +x start.sh
echo "start.sh is now executable."

# Ask for username
read -p "Please enter your username: " USERNAME

# Define icon source and destination
ICON_SOURCE="assets/BackgroundAutoClicker.svg"
ICON_DEST="/home/$USERNAME/Pictures/Thumbnails/BackgroundAutoClicker.svg"

# Create the icon destination directory if it doesn't exist
echo "Creating icon directory: $(dirname "$ICON_DEST")..."
mkdir -p "$(dirname "$ICON_DEST")"
echo "Icon directory created."

# Copy the application icon
echo "Copying application icon..."
cp "$ICON_SOURCE" "$ICON_DEST"
echo "Application icon copied to $ICON_DEST."

# Define desktop file source and destination
DESKTOP_SOURCE="BackgroundClicker.desktop"
DESKTOP_DEST="$HOME/.local/share/applications/"

# Copy the desktop file
echo "Copying desktop entry file..."
cp "$DESKTOP_SOURCE" "$DESKTOP_DEST"
echo "Desktop entry file copied to $DESKTOP_DEST."

echo "Setup complete. You can now find 'Background Auto Clicker' in your application menu."