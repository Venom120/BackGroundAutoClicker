# Maintainer: Your Name <your@email.com>
pkgname=bgclicker-gui
pkgver=1.0.0 # You might want to update this based on your project's versioning
pkgrel=1
pkgdesc="A simple Python application with a GUI for performing background mouse clicks and keyboard inputs."
arch=('any')
url="https://github.com/Venom120/bgclicker-gui" # Replace with your actual repo URL
license=('MIT') # Based on LICENSE file
depends=('python' 'tk' 'python-keyboard' 'xdotool')
makedepends=()
source=(
  "${pkgname}.desktop"
  "${pkgname}.svg"
  "main.py"
)
sha256sums=(
  'SKIP' # .desktop file might change, skip checksum for now
  'SKIP' # .svg file might change, skip checksum for now
  'SKIP' # main.py might change, skip checksum for now
)

build() {
  # No build step needed for this simple Python script
  # The source files are copied directly in the package() function
  :
}

package() {
  # Install the main script
  install -Dm755 main.py "/usr/bin/${pkgname}"

  # Install the desktop entry
  install -Dm644 "${pkgname}.desktop" "/usr/share/applications/${pkgname}.desktop"

  # Install the icon
  install -Dm644 "${pkgname}.svg" "/usr/share/icons/hicolor/scalable/apps/${pkgname}.svg"
}