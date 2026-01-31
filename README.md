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
- 🔄 **Auto-Update**: Built-in update functionality
- 🛡️ **Safe Operations**: Confirmation prompts for destructive actions
- ⚡ **Direct Mount**: Mount specific drives instantly by name
- 📂 **Permission Handling**: Automatically sets correct ownership (uid/gid)
- 🛠️ **Smart Fix**: Suggests fixes if drives fail to mount

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
3. Restart the application

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

## 🔢 Version History

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
[Q] 🚪 Quit
```

---

## 👤 Author

Developed by **supposious-spec**

---

## 📄 License
This project is licensed under the MIT License.
