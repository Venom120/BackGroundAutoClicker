# Maintainer: Yatharth Jain <yatharth3194@gmail.com>

_tag = latest # Replace with the actual tag if needed

pkgname=bgclicker-gui
pkgver=1.0.0
pkgrel=1
pkgdesc="A simple Python application with a GUI for performing background mouse clicks and keyboard inputs."
arch=('any')
url="https://github.com/Venom120/bgclicker-gui" # Replace with your actual repo URL
license=('MIT') # Based on LICENSE file
depends=('python' 'tk' 'python-keyboard' 'xdotool')
makedepends=(git)
source=($pkgname-$pkgver.tar.gz)
sha256sums=(
  'SKIP' # .desktop file might change, skip checksum for now
  'SKIP' # .svg file might change, skip checksum for now
  'SKIP' # main.py might change, skip checksum for now
)

pkgver() {
  # Use git to determine the version based on tags
  cd "$srcdir/$pkgname-$pkgver"
  git describe --tags | sed 's/^v//;s/-/./g'
}

package() {
  # Install the main script
  install -Dm755 main.py "/usr/bin/${pkgname}"

  # Install the desktop entry
  install -Dm644 "${pkgname}.desktop" "/usr/share/applications/${pkgname}.desktop"

  # Install the icon
  install -Dm644 "${pkgname}.svg" "/usr/share/icons/hicolor/scalable/apps/${pkgname}.svg"
}