#!/bin/bash

# Drive Master Uninstaller
# Completely removes Drive Master from your system

echo "🗑️ Drive Master Uninstaller"
echo "============================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "⚠️  This will completely remove Drive Master from your system."
read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Uninstall cancelled"
    exit 1
fi

echo "🔄 Uninstalling Drive Master..."

# Method 1: Remove via pip
echo "📦 Removing pip installation..."
if command_exists pip3; then
    pip3 uninstall drive-master -y 2>/dev/null || true
elif command_exists python3; then
    python3 -m pip uninstall drive-master -y 2>/dev/null || true
fi

# Method 2: Remove binaries
echo "🗂️ Removing binary files..."
sudo rm -f /usr/local/bin/drive-master 2>/dev/null || true
rm -f ~/.local/bin/drive-master 2>/dev/null || true

# Method 3: Clean up directories
echo "🧹 Cleaning up directories..."
rm -rf ~/.local/lib/python*/site-packages/drive_master* 2>/dev/null || true
rm -rf ~/.local/lib/python*/site-packages/drive-master* 2>/dev/null || true

# Method 4: Remove from PATH (optional - user can keep)
echo "📝 PATH cleanup (optional)..."
echo "Note: You may want to remove the PATH export from your shell config files:"
echo "  ~/.bashrc, ~/.zshrc, ~/.profile"
echo "  Look for: export PATH=\"\$HOME/.local/bin:\$PATH\""

echo ""
echo "✅ Drive Master has been completely uninstalled!"
echo "🙏 Thanks for using Drive Master!"
echo ""
echo "💡 To reinstall later, run:"
echo "   curl -sSL https://raw.githubusercontent.com/supposious-spec/drive-master/main/universal-install.sh | bash"