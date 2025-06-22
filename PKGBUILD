# Maintainer: Your Name <youremail@domain.com>
pkgname=bgclicker-gui
pkgver=1.0
pkgrel=1
pkgdesc="A simple Python GUI application for performing background mouse clicks and keyboard inputs."
arch=('any')
url="https://github.com/Venom120/BackGroundAutoClicker" # Assuming this is the correct URL
license=('MIT')
depends=('python' 'tk' 'xdotool' 'python-keyboard') # Translating req.txt dependencies to Arch packages
source=(
  "${pkgname}-${pkgver}.tar.gz::https://github.com/Venom120/BackGroundAutoClicker/archive/refs/tags/v${pkgver}.tar.gz" # Assuming a tag exists or will be created
  "BackgroundClicker.desktop"
  "assets/BackgroundAutoClicker.svg" # Assuming icon location
)
sha256sums=('SKIP' # Need to generate checksum for the tarball
            'SKIP' # Need to generate checksum for BackgroundClicker.desktop
            'SKIP') # Need to generate checksum for the icon

package() {
  # Install main scripts
  install -Dm755 main.py "$pkgdir"/usr/bin/bgclicker-gui

  # Install desktop file
  install -Dm644 BackgroundClicker.desktop "$pkgdir"/usr/share/applications/bgclicker-gui.desktop

  # Install icon
  install -Dm644 assets/BackgroundAutoClicker.svg "$pkgdir"/usr/share/icons/hicolor/scalable/apps/bgclicker-gui.svg # Standard icon location
}