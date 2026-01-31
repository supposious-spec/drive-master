#!/bin/bash

# Drive Master Universal Installer
# Works on any Linux distribution

set -e

REPO_URL="https://github.com/supposious-spec/drive-master"
BINARY_URL="https://github.com/supposious-spec/drive-master/releases/latest/download/drive-master"
INSTALL_DIR="/usr/local/bin"
TEMP_DIR="/tmp/drive-master-install"

echo "🚀 Drive Master Universal Installer"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect package manager and install python3-pip
install_pip() {
    echo "📦 Installing pip..."
    
    if command_exists apt-get; then
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif command_exists yum; then
        sudo yum install -y python3-pip
    elif command_exists dnf; then
        sudo dnf install -y python3-pip
    elif command_exists pacman; then
        sudo pacman -S --noconfirm python-pip
    elif command_exists zypper; then
        sudo zypper install -y python3-pip
    else
        echo "❌ Could not detect package manager. Please install python3-pip manually."
        exit 1
    fi
}

# Method 1: Try to download pre-built binary
install_binary() {
    echo "🔄 Attempting to download pre-built binary..."
    
    if command_exists wget; then
        wget -q "$BINARY_URL" -O "$TEMP_DIR/drive-master" 2>/dev/null || return 1
    elif command_exists curl; then
        curl -sL "$BINARY_URL" -o "$TEMP_DIR/drive-master" 2>/dev/null || return 1
    else
        return 1
    fi
    
    chmod +x "$TEMP_DIR/drive-master"
    sudo mv "$TEMP_DIR/drive-master" "$INSTALL_DIR/"
    echo "✅ Binary installed successfully!"
    return 0
}

# Method 2: Install via pip
install_via_pip() {
    echo "🐍 Installing via pip..."
    
    # Check if pip exists, install if not
    if ! command_exists pip3 && ! python3 -m pip --version >/dev/null 2>&1; then
        install_pip
    fi
    
    # Install the package with --break-system-packages if needed
    if command_exists pip3; then
        pip3 install --user --break-system-packages git+${REPO_URL}.git 2>/dev/null || pip3 install --user git+${REPO_URL}.git
    else
        python3 -m pip install --user --break-system-packages git+${REPO_URL}.git 2>/dev/null || python3 -m pip install --user git+${REPO_URL}.git
    fi
    
    # Add ~/.local/bin to PATH immediately
    export PATH="$HOME/.local/bin:$PATH"
    
    # Add to shell configs if not already there
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "📝 Adding ~/.local/bin to PATH..."
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc 2>/dev/null || true
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc 2>/dev/null || true
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile 2>/dev/null || true
    fi
    
    echo "✅ Installed via pip successfully!"
}

# Method 3: Manual installation
install_manual() {
    echo "🛠️ Manual installation..."
    
    # Install dependencies
    if ! command_exists git; then
        echo "❌ Git is required but not installed. Please install git first."
        exit 1
    fi
    
    if ! command_exists python3; then
        echo "❌ Python3 is required but not installed. Please install python3 first."
        exit 1
    fi
    
    # Clone repository
    git clone "$REPO_URL" "$TEMP_DIR/repo"
    cd "$TEMP_DIR/repo"
    
    # Install via pip if available, otherwise copy manually
    if command_exists pip3 || python3 -m pip --version >/dev/null 2>&1; then
        install_via_pip
    else
        # Manual copy method
        sudo cp mount_drive.py /usr/local/bin/drive-master
        sudo chmod +x /usr/local/bin/drive-master
        echo "✅ Manual installation complete!"
    fi
}

# Main installation logic
main() {
    # Create temp directory
    mkdir -p "$TEMP_DIR"
    
    # Try methods in order of preference
    if install_binary; then
        echo "🎉 Installation complete via binary!"
    elif install_via_pip; then
        echo "🎉 Installation complete via pip!"
    elif install_manual; then
        echo "🎉 Installation complete manually!"
    else
        echo "❌ All installation methods failed. Please check the documentation."
        exit 1
    fi
    
    # Cleanup
    rm -rf "$TEMP_DIR"
    
    echo ""
    echo "🚀 Drive Master is now installed!"
    echo "📋 Usage:"
    echo "   drive-master              # Interactive menu"
    echo "   drive-master MyDrive      # Mount specific drive"
    echo "   drive-master --version    # Show version"
    echo ""
    
    # Test if command works immediately
    if command_exists drive-master || [ -f "$HOME/.local/bin/drive-master" ]; then
        echo "✅ Command is ready to use!"
    else
        echo "💡 Restart terminal or run: export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
}

# Check if running as root (not recommended)
if [[ $EUID -eq 0 ]]; then
    echo "⚠️  Running as root is not recommended. Install as regular user."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

main "$@"