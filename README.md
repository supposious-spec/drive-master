# 🚀 Drive Master

**Drive Master** is a lightweight, professional CLI tool designed for Linux users to easily manage and auto-mount NTFS drives. It eliminates the hassle of manual mounting and permission issues by providing a clean interactive menu and direct command-line support.

---

## ✨ Features

- 🔍 **Auto-Detection**: Automatically finds all NTFS partitions on your system.
- 🛠️ **Interactive Menu**: User-friendly menu for listing, mounting, and managing drives.
- ⚡ **Direct Mount**: Mount specific drives instantly by name.
- 📂 **Permission Handling**: Automatically sets correct ownership (`uid`/`gid`) for mounted drives.
- 🛠️ **Smart Fix**: Suggests fixes if a drive fails to mount (e.g., due to Windows fast startup).

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
Simply run the command to open the menu:
```bash
drive-master
```
**Options inside the menu:**
- `1`: List all detected NTFS drives and their status.
- `2`: Mount a specific drive by its label/name.
- `3`: Mount all detected NTFS drives at once.
- `Q`: Exit the tool.

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

## 🔧 Prerequisites

- **Python 3.x**
- **ntfs-3g** (Usually pre-installed on most Linux distros)
- **Sudo access** (Required for mounting operations)

---

## 📂 Repository Name Suggestion

Recommended GitHub Repo Name: `drive-master`

---

## 👤 Author

Developed by **supposious-spec**

---

## 📄 License
This project is licensed under the MIT License.
