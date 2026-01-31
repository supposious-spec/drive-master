import click
import subprocess
import os
import sys
import time
import shutil

VERSION = "2.2.0"

# Colors and styling
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BLINK = '\033[5m'

def get_terminal_width():
    return shutil.get_terminal_size().columns

def print_banner():
    """Print animated banner"""
    width = get_terminal_width()
    banner = f"""{Colors.CYAN}{Colors.BOLD}
╔{'═' * (width - 2)}╗
║{' ' * (width - 2)}║
║{Colors.MAGENTA}    ██████╗ ██████╗ ██╗██╗   ██╗███████╗    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ {Colors.CYAN}║
║{Colors.MAGENTA}    ██╔══██╗██╔══██╗██║██║   ██║██╔════╝    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗{Colors.CYAN}║
║{Colors.MAGENTA}    ██║  ██║██████╔╝██║██║   ██║█████╗      ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝{Colors.CYAN}║
║{Colors.MAGENTA}    ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝      ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗{Colors.CYAN}║
║{Colors.MAGENTA}    ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║{Colors.CYAN}║
║{Colors.MAGENTA}    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{Colors.CYAN}║
║{' ' * (width - 2)}║
║{Colors.YELLOW}{Colors.BOLD}{'Auto-Mount NTFS Drives with Style'.center(width - 2)}{Colors.CYAN}║
║{Colors.WHITE}{'v' + VERSION + ' | Professional Linux Drive Manager'.center(width - 2)}{Colors.CYAN}║
║{' ' * (width - 2)}║
║{Colors.GREEN}{Colors.BOLD}{'🚀 Developed by Ali Hamza 🚀'.center(width - 2)}{Colors.CYAN}║
║{' ' * (width - 2)}║
╚{'═' * (width - 2)}╝{Colors.END}
"""
    print(banner)

def print_loading(text, chars="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"):
    """Print loading animation"""
    for i in range(8):
        print(f"\r{Colors.CYAN}{chars[i % len(chars)]}{Colors.END} {text}", end="", flush=True)
        time.sleep(0.1)
    print(f"\r{Colors.GREEN}✓{Colors.END} {text}")

def print_separator():
    """Print decorative separator"""
    width = get_terminal_width()
    print(f"{Colors.CYAN}{'─' * width}{Colors.END}")

def print_menu_header():
    """Print stylized menu header"""
    width = get_terminal_width()
    print(f"\n{Colors.BLUE}{Colors.BOLD}╭{'─' * (width - 2)}╮{Colors.END}")
    print(f"{Colors.BLUE}│{Colors.YELLOW}{Colors.BOLD}{'🛠️  DRIVE MASTER CONTROL PANEL  🛠️'.center(width - 2)}{Colors.BLUE}│{Colors.END}")
    print(f"{Colors.BLUE}╰{'─' * (width - 2)}╯{Colors.END}")

def print_option(number, icon, text, color=Colors.WHITE):
    """Print stylized menu option"""
    print(f"{Colors.CYAN}[{Colors.YELLOW}{Colors.BOLD}{number}{Colors.CYAN}]{Colors.END} {color}{icon} {text}{Colors.END}")

def print_success(text):
    """Print success message with animation"""
    print(f"{Colors.GREEN}{Colors.BOLD}✅ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}{Colors.BOLD}❌ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}{Colors.BOLD}ℹ️  {text}{Colors.END}")

@click.command()
@click.argument('drive_name', required=False)
@click.option('--version', is_flag=True, help="Show version info")
def main(drive_name, version):
    """🚀 Drive Master: Auto-mount NTFS drives on Linux with ease."""
    # Clear screen and show banner
    os.system('clear' if os.name == 'posix' else 'cls')
    print_banner()
    
    if version:
        print_info(f"Drive Master v{VERSION}")
        return

    print_loading("Scanning for NTFS drives...")
    drives = get_ntfs_drives()

    if not drives:
        print_error("No NTFS drives found! Check 'lsblk' or 'blkid'.")
        return

    print_success(f"Found {len(drives)} NTFS drive(s)")

    if drive_name:
        # Direct mount mode
        drive_name = drive_name.capitalize()
        if drive_name not in drives:
            print_warning(f"Drive '{drive_name}' not found. Available: {', '.join(drives.keys())}")
            return
        mount_drive(drives[drive_name]['uuid'], drive_name, drives[drive_name]['dev'])
    else:
        # Interactive menu
        while True:
            print_menu_header()
            print_option("1", "📋", "List all NTFS drives", Colors.GREEN)
            print_option("2", "🔌", "Mount a specific drive", Colors.YELLOW)
            print_option("3", "🔓", "Unmount a specific drive", Colors.ORANGE)
            print_option("4", "⚡", "Mount all unmounted drives", Colors.MAGENTA)
            print_option("5", "🚫", "Unmount all mounted drives", Colors.RED)
            print_option("6", "🔄", "Update Drive Master", Colors.BLUE)
            print_option("7", "💾", "Format USB Drive (FAT32/NTFS/EXT4)", Colors.MAGENTA)
            print_option("8", "🔍", "Recover Data from Drive/USB", Colors.CYAN)
            print_option("9", "🗑️", "Uninstall Drive Master", Colors.RED)
            print_option("Q", "🚪", "Quit", Colors.RED)
            print_separator()
            
            choice = click.prompt(f"{Colors.CYAN}➤ Enter your choice{Colors.END}", type=str).strip().upper()

            if choice == '1':
                list_drives(drives)
            elif choice == '2':
                mount_menu(drives)
            elif choice == '3':
                unmount_menu(drives)
            elif choice == '4':
                mount_all_unmounted(drives)
            elif choice == '5':
                unmount_all_mounted(drives)
            elif choice == '6':
                update_drive_master()
            elif choice == '7':
                format_usb_drive()
            elif choice == '8':
                recover_data_menu()
            elif choice == '9':
                uninstall_drive_master()
                print(f"\n{Colors.CYAN}{Colors.BOLD}Thanks for using Drive Master! 👋{Colors.END}")
                sys.exit(0)
            else:
                print_error("Invalid option! Please try again.")
                
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def get_ntfs_drives():
    """Scan NTFS drives using blkid."""
    drives = {}
    try:
        blkid_output = subprocess.check_output(['sudo', 'blkid', '-o', 'export'], stderr=subprocess.DEVNULL).decode('utf-8')
    except subprocess.CalledProcessError:
        print_error("blkid failed. Run with sudo or check permissions.")
        return drives

    # blkid -o export separates devices by double newlines or single newlines depending on version
    # It's safer to split by DEVNAME= to separate blocks
    blocks = blkid_output.split('DEVNAME=')
    for block in blocks:
        if not block.strip(): continue
        full_block = 'DEVNAME=' + block
        if 'TYPE=ntfs' in full_block:
            dev = next((l.split('=')[1] for l in full_block.split('\n') if l.startswith('DEVNAME=')), None)
            uuid = next((l.split('=')[1] for l in full_block.split('\n') if l.startswith('UUID=')), None)
            label = next((l.split('=')[1] for l in full_block.split('\n') if l.startswith('LABEL=')), None)
            if dev and uuid:
                # Use Label if available, otherwise use device name
                drives[label or os.path.basename(dev)] = {'uuid': uuid, 'dev': dev}
    return drives

def list_drives(drives):
    """List drives with mount status."""
    print_separator()
    print(f"{Colors.BLUE}{Colors.BOLD}📋 NTFS DRIVES DETECTED{Colors.END}")
    print_separator()
    
    user = os.getlogin()
    for i, (name, info) in enumerate(drives.items(), 1):
        mount_point = f"/media/{user}/{name}"
        mounted = is_mounted(name)
        
        status_icon = "🟢" if mounted else "🔴"
        status_text = f"{Colors.GREEN}MOUNTED{Colors.END}" if mounted else f"{Colors.RED}NOT MOUNTED{Colors.END}"
        
        print(f"{Colors.CYAN}╭─ Drive #{i}{Colors.END}")
        print(f"{Colors.CYAN}├─{Colors.END} {Colors.YELLOW}{Colors.BOLD}📁 Name:{Colors.END} {name}")
        print(f"{Colors.CYAN}├─{Colors.END} {Colors.BLUE}🆔 UUID:{Colors.END} {info['uuid'][:8]}...")
        print(f"{Colors.CYAN}├─{Colors.END} {Colors.MAGENTA}💾 Device:{Colors.END} {info['dev']}")
        if mounted:
            print(f"{Colors.CYAN}├─{Colors.END} {Colors.GREEN}📂 Path:{Colors.END} {mount_point}")
        print(f"{Colors.CYAN}╰─{Colors.END} {Colors.WHITE}📊 Status:{Colors.END} {status_icon} {status_text}")
        print()

def mount_menu(drives):
    """Interactive mount menu"""
    unmounted = {name: info for name, info in drives.items() if not is_mounted(name)}
    
    if not unmounted:
        print_info("All drives are already mounted!")
        return
        
    print_separator()
    print(f"{Colors.YELLOW}{Colors.BOLD}🔌 SELECT DRIVE TO MOUNT{Colors.END}")
    print_separator()
    
    for i, name in enumerate(unmounted.keys(), 1):
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.WHITE}{name}{Colors.END}")
    
    try:
        choice = int(click.prompt(f"{Colors.YELLOW}Enter drive number{Colors.END}", type=int))
        if 1 <= choice <= len(unmounted):
            name = list(unmounted.keys())[choice - 1]
            info = unmounted[name]
            mount_drive(info['uuid'], name, info['dev'])
        else:
            print_error("Invalid choice!")
    except (ValueError, click.Abort):
        print_error("Invalid input!")

def unmount_menu(drives):
    """Interactive unmount menu"""
    mounted = {name: info for name, info in drives.items() if is_mounted(name)}
    
    if not mounted:
        print_info("No drives are currently mounted!")
        return
        
    print_separator()
    print(f"{Colors.ORANGE}{Colors.BOLD}🔓 SELECT DRIVE TO UNMOUNT{Colors.END}")
    print_separator()
    
    for i, name in enumerate(mounted.keys(), 1):
        user = os.getlogin()
        mount_point = f"/media/{user}/{name}"
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.WHITE}{name}{Colors.END} {Colors.BLUE}({mount_point}){Colors.END}")
    
    try:
        choice = int(click.prompt(f"{Colors.ORANGE}Enter drive number{Colors.END}", type=int))
        if 1 <= choice <= len(mounted):
            name = list(mounted.keys())[choice - 1]
            unmount_drive(name)
        else:
            print_error("Invalid choice!")
    except (ValueError, click.Abort):
        print_error("Invalid input!")

def mount_all_unmounted(drives):
    """Mount only unmounted drives"""
    unmounted = {name: info for name, info in drives.items() if not is_mounted(name)}
    
    if not unmounted:
        print_info("All drives are already mounted!")
        return
        
    print_loading(f"Mounting {len(unmounted)} unmounted drives...")
    for name, info in unmounted.items():
        mount_drive(info['uuid'], name, info['dev'])

def unmount_all_mounted(drives):
    """Unmount all mounted drives"""
    mounted = {name: info for name, info in drives.items() if is_mounted(name)}
    
    if not mounted:
        print_info("No drives are currently mounted!")
        return
        
    confirm = click.confirm(f"{Colors.RED}Unmount all {len(mounted)} mounted drives?{Colors.END}")
    if confirm:
        print_loading(f"Unmounting {len(mounted)} drives...")
        for name in mounted.keys():
            unmount_drive(name)

def is_mounted(name):
    """Check if drive is mounted"""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    return subprocess.run(['mountpoint', '-q', mount_point]).returncode == 0

def unmount_drive(name):
    """Unmount a drive"""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    
    print_separator()
    print(f"{Colors.ORANGE}{Colors.BOLD}🔓 UNMOUNTING: {name}{Colors.END}")
    print_separator()
    
    if not is_mounted(name):
        print_info(f"{name} is not mounted")
        return
    
    print_loading(f"Unmounting {name}...")
    result = subprocess.run(['sudo', 'umount', mount_point], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if result.returncode == 0:
        print_success(f"Successfully unmounted {name}")
        # Remove empty mount point directory
        try:
            os.rmdir(mount_point)
        except OSError:
            pass  # Directory not empty or doesn't exist
    else:
        print_error(f"Failed to unmount {name}")
def mount_drive(uuid, name, dev):
    """Mount the drive with enhanced UI."""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    
    print_separator()
    print(f"{Colors.YELLOW}{Colors.BOLD}🔌 MOUNTING: {name}{Colors.END}")
    print_separator()
    
    if not os.path.exists(mount_point):
        print_loading("Creating mount point...")
        subprocess.run(['sudo', 'mkdir', '-p', mount_point], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['sudo', 'chown', f'{user}:{user}', mount_point], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if is_mounted(name):
        print_info(f"{name} is already mounted at {mount_point}")
        return

    print_loading(f"Mounting {name}...")
    
    # Using -t ntfs-3g for better write support
    cmd = ['sudo', 'mount', '-t', 'ntfs-3g', '-o', f'uid={os.getuid()},gid={os.getgid()}', f'UUID={uuid}', mount_point]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if result.returncode == 0:
        print_success(f"Successfully mounted {name} at {mount_point}")
        print(f"{Colors.GREEN}📂 Access your drive: {Colors.BOLD}{mount_point}{Colors.END}")
    else:
        print_error(f"Mount failed for {name}")
        print(f"{Colors.YELLOW}💡 Suggestion:{Colors.END} Run 'sudo ntfsfix {dev}' to fix filesystem errors")

def get_usb_drives():
    """Get all USB drives (removable storage)"""
    usb_drives = {}
    try:
        # Get all block devices
        lsblk_output = subprocess.check_output(['lsblk', '-J', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,LABEL,HOTPLUG'], stderr=subprocess.DEVNULL).decode('utf-8')
        import json
        data = json.loads(lsblk_output)
        
        for device in data['blockdevices']:
            # Check if it's a removable/hotplug device (USB)
            if device.get('hotplug') == True or device.get('type') == 'disk':
                # Check children (partitions)
                if 'children' in device:
                    for child in device['children']:
                        name = child['name']
                        size = child.get('size', 'Unknown')
                        fstype = child.get('fstype', 'Unknown')
                        label = child.get('label', name)
                        mountpoint = child.get('mountpoint')
                        
                        usb_drives[label] = {
                            'device': f"/dev/{name}",
                            'size': size,
                            'fstype': fstype,
                            'mountpoint': mountpoint,
                            'parent': f"/dev/{device['name']}"
                        }
                else:
                    # Whole disk without partitions
                    name = device['name']
                    size = device.get('size', 'Unknown')
                    fstype = device.get('fstype', 'Unknown')
                    label = device.get('label', name)
                    mountpoint = device.get('mountpoint')
                    
                    usb_drives[label] = {
                        'device': f"/dev/{name}",
                        'size': size,
                        'fstype': fstype,
                        'mountpoint': mountpoint,
                        'parent': f"/dev/{name}"
                    }
    except Exception as e:
        print_error(f"Failed to detect USB drives: {str(e)}")
    
    return usb_drives

def format_usb_drive():
    """Format USB drives with different filesystems"""
    print_separator()
    print(f"{Colors.MAGENTA}{Colors.BOLD}💾 USB DRIVE FORMATTER{Colors.END}")
    print_separator()
    
    print_loading("Scanning for USB drives...")
    usb_drives = get_usb_drives()
    
    if not usb_drives:
        print_error("No USB drives detected!")
        return
    
    print_success(f"Found {len(usb_drives)} USB drive(s)")
    print_separator()
    
    # List USB drives
    for i, (label, info) in enumerate(usb_drives.items(), 1):
        mounted = "✅ Mounted" if info['mountpoint'] else "❌ Not Mounted"
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.YELLOW}{label}{Colors.END}")
        print(f"    📱 Device: {info['device']}")
        print(f"    📏 Size: {info['size']}")
        print(f"    💾 Format: {info['fstype']}")
        print(f"    📊 Status: {mounted}")
        print()
    
    try:
        choice = int(click.prompt(f"{Colors.MAGENTA}Select USB drive to format{Colors.END}", type=int))
        if 1 <= choice <= len(usb_drives):
            label = list(usb_drives.keys())[choice - 1]
            info = usb_drives[label]
            
            # Warning
            print_separator()
            print(f"{Colors.RED}{Colors.BOLD}⚠️  WARNING: This will ERASE ALL DATA on {label}!{Colors.END}")
            print(f"{Colors.RED}Device: {info['device']} ({info['size']}){Colors.END}")
            
            if not click.confirm(f"{Colors.RED}Are you absolutely sure?{Colors.END}"):
                print_info("Format cancelled")
                return
            
            # Choose format type
            print_separator()
            print(f"{Colors.BLUE}{Colors.BOLD}💾 FORMAT TYPE{Colors.END}")
            print(f"{Colors.CYAN}[1]{Colors.END} Quick Format (Fast)")
            print(f"{Colors.CYAN}[2]{Colors.END} Full Format (Secure, slower)")
            
            format_type = int(click.prompt(f"{Colors.BLUE}Select format type{Colors.END}", type=int))
            quick_format = format_type == 1
            
            # Choose filesystem
            print_separator()
            print(f"{Colors.BLUE}{Colors.BOLD}📁 SELECT FILESYSTEM{Colors.END}")
            print(f"{Colors.CYAN}[1]{Colors.END} FAT32 (Windows/Linux/Mac compatible)")
            print(f"{Colors.CYAN}[2]{Colors.END} NTFS (Windows/Linux compatible)")
            print(f"{Colors.CYAN}[3]{Colors.END} EXT4 (Linux only)")
            
            fs_choice = int(click.prompt(f"{Colors.BLUE}Select filesystem{Colors.END}", type=int))
            
            # Unmount if mounted
            if info['mountpoint']:
                print_loading(f"Unmounting {label}...")
                subprocess.run(['sudo', 'umount', info['device']], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Format based on choice
            format_msg = "Quick formatting" if quick_format else "Full formatting"
            if fs_choice == 1:  # FAT32
                print_loading(f"{format_msg} {label} as FAT32...")
                cmd = ['sudo', 'mkfs.fat', '-F', '32', '-n', label]
                if not quick_format:
                    cmd.extend(['-v'])  # Verbose for full format
                cmd.append(info['device'])
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif fs_choice == 2:  # NTFS
                print_loading(f"{format_msg} {label} as NTFS...")
                cmd = ['sudo', 'mkfs.ntfs', '-L', label]
                if quick_format:
                    cmd.extend(['-f'])  # Fast format
                else:
                    cmd.extend(['-z'])  # Zero entire disk
                cmd.append(info['device'])
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif fs_choice == 3:  # EXT4
                print_loading(f"{format_msg} {label} as EXT4...")
                cmd = ['sudo', 'mkfs.ext4', '-F', '-L', label]
                if not quick_format:
                    cmd.extend(['-c'])  # Check for bad blocks
                cmd.append(info['device'])
                result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print_error("Invalid filesystem choice!")
                return
            
            if result.returncode == 0:
                print_success(f"Successfully formatted {label}!")
                print(f"{Colors.GREEN}🎉 Your USB drive is ready to use{Colors.END}")
            else:
                print_error(f"Format failed for {label}")
                print(f"{Colors.YELLOW}💡 Suggestion:{Colors.END} Check if drive is write-protected")
        else:
            print_error("Invalid choice!")
    except (ValueError, click.Abort):
        print_error("Invalid input!")

def uninstall_drive_master():
    """Uninstall Drive Master completely"""
    print_separator()
    print(f"{Colors.RED}{Colors.BOLD}🗑️ UNINSTALL DRIVE MASTER{Colors.END}")
    print_separator()
    
    print(f"{Colors.RED}This will completely remove Drive Master from your system.{Colors.END}")
    
    if not click.confirm(f"{Colors.RED}Are you sure you want to uninstall?{Colors.END}"):
        print_info("Uninstall cancelled")
        return
    
    print_loading("Uninstalling Drive Master...")
    
    # Remove via pip
    try:
        if shutil.which('pip3'):
            subprocess.run(['pip3', 'uninstall', 'drive-master', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(['python3', '-m', 'pip', 'uninstall', 'drive-master', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Remove binaries
    try:
        subprocess.run(['sudo', 'rm', '-f', '/usr/local/bin/drive-master'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(os.path.expanduser('~/.local/bin/drive-master'))
    except:
        pass
    
    # Remove from PATH (optional)
    print_success("Drive Master has been uninstalled!")
    print(f"{Colors.YELLOW}💡 Note:{Colors.END} You may need to restart your terminal")
    print(f"{Colors.CYAN}Thanks for using Drive Master! 👋{Colors.END}")
    
def recover_data_menu():
    """Data recovery menu using testdisk"""
    print_separator()
    print(f"{Colors.CYAN}{Colors.BOLD}🔍 DATA RECOVERY CENTER{Colors.END}")
    print_separator()
    
    # Check if testdisk is installed
    if not shutil.which('testdisk'):
        print_error("TestDisk is not installed!")
        print_info("Installing TestDisk...")
        try:
            if shutil.which('apt-get'):
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'testdisk'], check=True)
            elif shutil.which('yum'):
                subprocess.run(['sudo', 'yum', 'install', '-y', 'testdisk'], check=True)
            elif shutil.which('dnf'):
                subprocess.run(['sudo', 'dnf', 'install', '-y', 'testdisk'], check=True)
            elif shutil.which('pacman'):
                subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'testdisk'], check=True)
            else:
                print_error("Please install testdisk manually: sudo apt install testdisk")
                return
            print_success("TestDisk installed successfully!")
        except subprocess.CalledProcessError:
            print_error("Failed to install TestDisk")
            return
    
    print(f"{Colors.BLUE}{Colors.BOLD}🔍 RECOVERY OPTIONS{Colors.END}")
    print(f"{Colors.CYAN}[1]{Colors.END} 💾 Recover from USB/External Drive")
    print(f"{Colors.CYAN}[2]{Colors.END} 💽 Recover from Internal Drive")
    print(f"{Colors.CYAN}[3]{Colors.END} 📂 Recover from Specific Directory")
    print(f"{Colors.CYAN}[4]{Colors.END} 🔍 Advanced Recovery (TestDisk GUI)")
    
    try:
        choice = int(click.prompt(f"{Colors.CYAN}Select recovery option{Colors.END}", type=int))
        
        if choice == 1:
            recover_from_usb()
        elif choice == 2:
            recover_from_internal()
        elif choice == 3:
            recover_from_directory()
        elif choice == 4:
            launch_testdisk_gui()
        else:
            print_error("Invalid choice!")
    except (ValueError, click.Abort):
        print_error("Invalid input!")

def recover_from_usb():
    """Recover data from USB drives"""
    print_separator()
    print(f"{Colors.MAGENTA}{Colors.BOLD}💾 USB DATA RECOVERY{Colors.END}")
    print_separator()
    
    print_loading("Scanning for USB drives...")
    usb_drives = get_usb_drives()
    
    if not usb_drives:
        print_error("No USB drives detected!")
        return
    
    print_success(f"Found {len(usb_drives)} USB drive(s)")
    print_separator()
    
    for i, (label, info) in enumerate(usb_drives.items(), 1):
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.YELLOW}{label}{Colors.END}")
        print(f"    📱 Device: {info['device']}")
        print(f"    📏 Size: {info['size']}")
        print(f"    💾 Format: {info['fstype']}")
        print()
    
    try:
        choice = int(click.prompt(f"{Colors.MAGENTA}Select USB drive to recover from{Colors.END}", type=int))
        if 1 <= choice <= len(usb_drives):
            label = list(usb_drives.keys())[choice - 1]
            info = usb_drives[label]
            
            # Create recovery directory
            recovery_dir = f"/home/{os.getlogin()}/Desktop/RecoveredData_{label}"
            os.makedirs(recovery_dir, exist_ok=True)
            
            print_info(f"Recovery directory: {recovery_dir}")
            print_loading(f"Starting recovery from {label}...")
            
            # Use photorec for file recovery
            cmd = ['sudo', 'photorec', '/d', recovery_dir, '/cmd', info['device'], 'search']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print_success(f"Recovery completed! Check: {recovery_dir}")
            else:
                print_error("Recovery failed. Launching interactive mode...")
                subprocess.run(['sudo', 'photorec', info['device']])
        else:
            print_error("Invalid choice!")
    except (ValueError, click.Abort):
        print_error("Invalid input!")

def recover_from_internal():
    """Recover data from internal drives"""
    print_separator()
    print(f"{Colors.BLUE}{Colors.BOLD}💽 INTERNAL DRIVE RECOVERY{Colors.END}")
    print_separator()
    
    # Get all drives
    try:
        lsblk_output = subprocess.check_output(['lsblk', '-J', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE'], stderr=subprocess.DEVNULL).decode('utf-8')
        import json
        data = json.loads(lsblk_output)
        
        drives = []
        for device in data['blockdevices']:
            if device.get('type') == 'disk':
                drives.append({
                    'name': device['name'],
                    'size': device.get('size', 'Unknown'),
                    'device': f"/dev/{device['name']}"
                })
        
        if not drives:
            print_error("No drives detected!")
            return
        
        print_success(f"Found {len(drives)} drive(s)")
        print_separator()
        
        for i, drive in enumerate(drives, 1):
            print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.YELLOW}{drive['name']}{Colors.END}")
            print(f"    📱 Device: {drive['device']}")
            print(f"    📏 Size: {drive['size']}")
            print()
        
        choice = int(click.prompt(f"{Colors.BLUE}Select drive to recover from{Colors.END}", type=int))
        if 1 <= choice <= len(drives):
            drive = drives[choice - 1]
            
            print_warning(f"This will scan {drive['device']} for recoverable data")
            if click.confirm(f"{Colors.YELLOW}Continue with recovery?{Colors.END}"):
                # Launch testdisk for partition recovery
                subprocess.run(['sudo', 'testdisk', drive['device']])
        else:
            print_error("Invalid choice!")
            
    except Exception as e:
        print_error(f"Failed to scan drives: {str(e)}")

def recover_from_directory():
    """Recover data from specific directory path"""
    print_separator()
    print(f"{Colors.GREEN}{Colors.BOLD}📂 DIRECTORY RECOVERY{Colors.END}")
    print_separator()
    
    print_info("This will scan a specific path for deleted files")
    
    # Get path from user
    scan_path = click.prompt(f"{Colors.GREEN}Enter path to scan (e.g., /home/user/Documents){Colors.END}", type=str)
    
    if not os.path.exists(scan_path):
        print_error(f"Path does not exist: {scan_path}")
        return
    
    # Create recovery directory
    recovery_dir = f"/home/{os.getlogin()}/Desktop/RecoveredData_Directory"
    os.makedirs(recovery_dir, exist_ok=True)
    
    print_info(f"Scanning: {scan_path}")
    print_info(f"Recovery directory: {recovery_dir}")
    
    print_loading("Starting directory scan...")
    
    # Use photorec to scan specific directory
    try:
        # Find the device containing the path
        df_output = subprocess.check_output(['df', scan_path], text=True)
        device = df_output.split('\n')[1].split()[0]
        
        print_info(f"Device: {device}")
        
        # Launch photorec with specific path
        subprocess.run(['sudo', 'photorec', '/d', recovery_dir, '/cmd', device, 'search'])
        
        print_success(f"Directory scan completed! Check: {recovery_dir}")
        
    except Exception as e:
        print_error(f"Directory scan failed: {str(e)}")
        print_info("Launching interactive recovery...")
        subprocess.run(['sudo', 'photorec'])

def launch_testdisk_gui():
    """Launch TestDisk interactive GUI"""
    print_separator()
    print(f"{Colors.YELLOW}{Colors.BOLD}🔍 ADVANCED RECOVERY (TestDisk){Colors.END}")
    print_separator()
    
    print_info("Launching TestDisk interactive interface...")
    print_warning("Use arrow keys to navigate, Enter to select")
    print_info("TestDisk can recover partitions and fix boot sectors")
    
    input(f"\n{Colors.CYAN}Press Enter to launch TestDisk...{Colors.END}")
    
    try:
        subprocess.run(['sudo', 'testdisk'])
    except KeyboardInterrupt:
        print_info("\nTestDisk session ended")
    except Exception as e:
        print_error(f"Failed to launch TestDisk: {str(e)}")
    """Update Drive Master to latest version"""
    print_separator()
    print(f"{Colors.BLUE}{Colors.BOLD}🔄 UPDATING DRIVE MASTER{Colors.END}")
    print_separator()
    
    print_loading("Checking for updates...")
    
    # Try pip update first
    try:
        if shutil.which('pip3'):
            result = subprocess.run(['pip3', 'install', '--user', '--upgrade', '--break-system-packages', 'git+https://github.com/supposious-spec/drive-master.git'], 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(['python3', '-m', 'pip', 'install', '--user', '--upgrade', '--break-system-packages', 'git+https://github.com/supposious-spec/drive-master.git'], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Drive Master updated successfully!")
            print_info("Restart the application to use the new version")
        else:
            print_error("Update failed via pip")
            print_info("Try running the universal installer again:")
            print(f"{Colors.CYAN}curl -sSL https://raw.githubusercontent.com/supposious-spec/drive-master/main/universal-install.sh | bash{Colors.END}")
    except Exception as e:
        print_error(f"Update failed: {str(e)}")
        print_info("Manual update: Re-run the installer script")

        print_error(f"Failed to launch TestDisk: {str(e)}")

def update_drive_master():
    """Update Drive Master to latest version"""
    print_separator()
    print(f"{Colors.BLUE}{Colors.BOLD}🔄 UPDATING DRIVE MASTER{Colors.END}")
    print_separator()
    
    print_loading("Checking for updates...")
    
    # Try pip update first
    try:
        if shutil.which('pip3'):
            result = subprocess.run(['pip3', 'install', '--user', '--upgrade', '--break-system-packages', 'git+https://github.com/supposious-spec/drive-master.git'], 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(['python3', '-m', 'pip', 'install', '--user', '--upgrade', '--break-system-packages', 'git+https://github.com/supposious-spec/drive-master.git'], 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Drive Master updated successfully!")
            print_info("Restart the application to use the new version")
        else:
            print_error("Update failed via pip")
            print_info("Try running the universal installer again:")
            print(f"{Colors.CYAN}curl -sSL https://raw.githubusercontent.com/supposious-spec/drive-master/main/universal-install.sh | bash{Colors.END}")
    except Exception as e:
        print_error(f"Update failed: {str(e)}")
        print_info("Manual update: Re-run the installer script")

if __name__ == '__main__':
    main()
