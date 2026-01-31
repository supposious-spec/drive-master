# 🚀 Drive Master

**Drive Master** is a professional CLI tool for Linux users to easily manage and auto-mount NTFS drives with an amazing animated interface. It eliminates manual mounting hassles with smart drive management and beautiful terminal UI.

---

## ✨ Features

- 🔍 **Auto-Detection**: Automatically finds all NTFS partitions on your system
- 🎨 **Beautiful UI**: Animated terminal interface with colors and professional styling
- 🛠️ **Smart Management**: Interactive menus for mounting/unmounting specific drives
- 🔌 **Selective Operations**: Mount only unmounted drives, unmount only mounted drives
- 📂 **Path Display**: Shows exact mount paths for easy access
- 📊 **Status Indicators**: Visual status with color-coded drive information
- 💾 **USB Formatter**: Format USB drives with FAT32/NTFS/EXT4 filesystems
- 🔄 **Auto-Update**: Built-in update functionality with version checking
- 🛡️ **Safe Operations**: Confirmation prompts for destructive actions
- ⚡ **Direct Mount**: Mount specific drives instantly by name
- 📂 **Permission Handling**: Automatically sets correct ownership (uid/gid)
- 🛠️ **Smart Fix**: Suggests fixes if drives fail to mount
- 🗑️ **Easy Uninstall**: Built-in uninstaller for clean removal
- 🔍 **Data Recovery**: Professional data recovery using TestDisk/PhotoRec

---

## 📥 Installation

### 🚀 Universal One-Line Install (Recommended)
Works on **any Linux distribution** - automatically detects your system and installs:

```bash
curl -sSL https://raw.githubusercontent.com/supposious-spec/drive-master/main/universal-install.sh | bash
```

### ⚡ Direct Binary Download
Download pre-built binary (no Python/pip required):

```bash
wget https://github.com/supposious-spec/drive-master/releases/latest/download/drive-master
chmod +x drive-master
sudo mv drive-master /usr/local/bin/
```

### 🐍 Install via pip
If you have Python and pip installed:

```bash
pip install git+https://github.com/supposious-spec/drive-master.git
```

### 💻 Windows Installation (Experimental)
**Note**: Drive Master is primarily designed for Linux. Windows support is limited.

**Requirements:**
- Python 3.7+ installed
- Git installed
- Windows Subsystem for Linux (WSL) recommended

**Method 1: Using WSL (Recommended)**
1. Install WSL2 from Microsoft Store
2. Open WSL terminal
3. Run the Linux installation command:
   ```bash
   curl -sSL https://raw.githubusercontent.com/supposious-spec/drive-master/main/universal-install.sh | bash
   ```

**Method 2: Native Windows (Limited)**
1. Install Python 3.7+ from python.org
2. Install Git from git-scm.com
3. Open Command Prompt as Administrator
4. Clone and install:
   ```cmd
   git clone https://github.com/supposious-spec/drive-master.git
   cd drive-master
   pip install -r requirements.txt
   pip install -e .
   ```
5. Run with: `python -m mount_drive`

**Windows Limitations:**
- No sudo support (some features may not work)
- Limited drive detection capabilities
- NTFS mounting handled by Windows automatically
- USB formatting may require administrator privileges

### 🛠️ Manual Installation
For developers or custom setups:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/supposious-spec/drive-master.git
   cd drive-master
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the tool**:
   ```bash
   pip install -e .
   ```

---

## 🚀 How to Use

Once installed, you can use the `drive-master` command from anywhere.

### 1️⃣ Interactive Mode
Simply run the command to open the beautiful animated menu:
```bash
drive-master
```
**Menu Options:**
- `1`: 📋 List all detected NTFS drives with status and paths
- `2`: 🔌 Mount a specific drive (interactive selection)
- `3`: 🔓 Unmount a specific drive (interactive selection)
- `4`: ⚡ Mount all unmounted drives (smart mounting)
- `5`: 🚫 Unmount all mounted drives (with confirmation)
- `6`: 🔄 Update Drive Master to latest version
- `7`: 💾 Format USB Drive (FAT32/NTFS/EXT4)
- `8`: 🗑️ Uninstall Drive Master
- `Q`: 🚪 Exit the tool

### 2️⃣ Direct Mounting
If you know your drive's label (e.g., "Coding"), mount it directly:
```bash
drive-master Coding
```

### 3️⃣ Check Version
```bash
drive-master --version
```

---

## 🔄 Updates

### **Auto-Update (Built-in)**
Use the built-in update feature from the menu:
1. Run `drive-master`
2. Select option `6` (🔄 Update Drive Master)
3. The tool will check if you have the latest version
4. If already updated, no restart needed
5. If updated, restart the application

### **Manual Update Methods**

**Method 1: Re-run installer**
```bash
curl -sSL https://raw.githubusercontent.com/supposious-spec/drive-master/main/universal-install.sh | bash
```

**Method 2: Pip upgrade**
```bash
pip3 install --user --upgrade git+https://github.com/supposious-spec/drive-master.git
```

**Method 3: Binary update**
```bash
wget https://github.com/supposious-spec/drive-master/releases/latest/download/drive-master -O /tmp/drive-master
chmod +x /tmp/drive-master
sudo mv /tmp/drive-master /usr/local/bin/drive-master
```

---

## 🗑️ Uninstallation

### **Method 1: Built-in Uninstaller (Recommended)**
Use the built-in uninstaller from the menu:
1. Run `drive-master`
2. Select option `8` (🗑️ Uninstall Drive Master)
3. Confirm removal

### **Method 2: Standalone Uninstaller**
```bash
curl -sSL https://raw.githubusercontent.com/supposious-spec/drive-master/main/uninstall.sh | bash
```

### **Method 3: Manual Removal**
```bash
# Remove via pip
pip3 uninstall drive-master -y

# Remove binaries
sudo rm -f /usr/local/bin/drive-master
rm -f ~/.local/bin/drive-master

# Clean up directories
rm -rf ~/.local/lib/python*/site-packages/drive_master*
```

---

## 🔢 Version History

- **v2.3.0** - Universal drive support, enhanced USB detection, back options, Ali Hamza credit
- **v2.2.0** - Advanced USB formatting & data recovery with TestDisk integration
- **v2.1.0** - USB formatting, built-in uninstaller, enhanced drive management
- **v2.0.0** - Enhanced UI, unmount functionality, smart drive management, auto-update
- **v1.0.0** - Initial release with basic mounting functionality

---

## 🔧 Prerequisites

- **Python 3.x**
- **ntfs-3g** (Usually pre-installed on most Linux distros)
- **Sudo access** (Required for mounting operations)

---

## 📱 Screenshots

```
╭──────────────────────────────────────────────────────────────────────────────╮
│                           🛠️  DRIVE MASTER CONTROL PANEL  🛠️                            │
╰──────────────────────────────────────────────────────────────────────────────╯
[1] 📋 List all NTFS drives
[2] 🔌 Mount a specific drive
[3] 🔓 Unmount a specific drive  
[4] ⚡ Mount all unmounted drives
[5] 🚫 Unmount all mounted drives
[6] 🔄 Update Drive Master
[7] 💾 Format USB Drive
[8] 🗑️ Uninstall Drive Master
[Q] 🚪 Quit
```

---

## 👤 Author

Developed by **supposious-spec**

---

## 📄 License
This project is licensed under the MIT License.
