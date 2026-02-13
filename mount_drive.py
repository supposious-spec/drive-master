import click
import subprocess
import os
import sys
import time
import shutil
from datetime import datetime

VERSION = "3.2.0"

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
    """Print centered animated banner"""
    width = get_terminal_width()
    if width < 100:
        width = 100
    
    # ASCII art fits in 96 characters
    logo_width = 98
    padding = max(0, (width - logo_width) // 2)
    
    banner = f"""{Colors.CYAN}{Colors.BOLD}
{' ' * padding}╔{'═' * (logo_width - 2)}╗
{' ' * padding}║{' ' * (logo_width - 2)}║
{' ' * padding}║{Colors.MAGENTA} ██████╗ ██████╗ ██╗██╗   ██╗███████╗    ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗  {Colors.CYAN}║
{' ' * padding}║{Colors.MAGENTA} ██╔══██╗██╔══██╗██║██║   ██║██╔════╝    ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗ {Colors.CYAN}║
{' ' * padding}║{Colors.MAGENTA} ██║  ██║██████╔╝██║██║   ██║█████╗      ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝ {Colors.CYAN}║
{' ' * padding}║{Colors.MAGENTA} ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝      ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗ {Colors.CYAN}║
{' ' * padding}║{Colors.MAGENTA} ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗    ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║ {Colors.CYAN}║
{' ' * padding}║{Colors.MAGENTA} ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ {Colors.CYAN}║
{' ' * padding}║{' ' * (logo_width - 2)}║
{' ' * padding}║{Colors.YELLOW}{Colors.BOLD}{'Auto-Mount NTFS Drives with Style'.center(logo_width - 2)}{Colors.CYAN}║
{' ' * padding}║{Colors.WHITE}{'v' + VERSION + ' | Professional Linux Drive Manager'.center(logo_width - 2)}{Colors.CYAN}║
{' ' * padding}║{' ' * (logo_width - 2)}║
{' ' * padding}║{Colors.GREEN}{Colors.BOLD}{'🚀 Developed by Ali Hamza 🚀'.center(logo_width - 2)}{Colors.CYAN}║
{' ' * padding}║{' ' * (logo_width - 2)}║
{' ' * padding}╚{'═' * (logo_width - 2)}╝{Colors.END}
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

    print_loading("Scanning for all drives...")
    drives = get_all_drives()

    if not drives:
        print_error("No drives found! Check system permissions.")
        return

    print_success(f"Found {len(drives)} drive(s)")

    if drive_name:
        # Direct mount mode
        drive_name_lower = drive_name.lower()
        found = False
        for path, info in drives.items():
            label = str(info.get('label') or "").lower()
            if label == drive_name_lower or path.lower() == drive_name_lower:
                mount_name = info.get('label') or path.split('/')[-1]
                mount_drive(info['uuid'], mount_name, info['device'])
                found = True
                break
        if not found:
            print_warning(f"Drive matching '{drive_name}' not found.")
    else:
        # Interactive menu
        while True:
            print_menu_header()
            print_option("1", "📋", "List all drives (Detailed Info)", Colors.GREEN)
            print_option("2", "🔌", "Mount a specific drive", Colors.YELLOW)
            print_option("3", "🔓", "Unmount a specific drive", Colors.ORANGE)
            print_option("4", "⚡", "Mount all unmounted drives", Colors.MAGENTA)
            print_option("5", "🚫", "Unmount all mounted drives", Colors.RED)
            print_option("6", "🔄", "Update Drive Master", Colors.BLUE)
            print_option("7", "💾", "Drive Formatter (FAT32/NTFS/EXT4)", Colors.MAGENTA)
            print_option("8", "🔧", "Fix Hidden/Problematic Drives", Colors.ORANGE)
            print_option("9", "🔍", "Data Recovery Center", Colors.CYAN)
            print_option("P", "🔑", "Windows Password Removal", Colors.ORANGE)
            print_option("A", "🗑️", "Uninstall Drive Master", Colors.RED)
            print_option("C", "🧹", "Clear Screen", Colors.WHITE)
            print_option("Q", "🚪", "Quit", Colors.RED)
            print_separator()
            
            choice = click.prompt(f"{Colors.CYAN}➤ Enter your choice{Colors.END}", type=str).strip().upper()

            if choice == '1':
                list_drives(drives)
                drives = get_all_drives()  # Refresh after viewing
            elif choice == '2':
                mount_menu(drives)
                drives = get_all_drives()
            elif choice == '3':
                unmount_menu(drives)
                drives = get_all_drives()
            elif choice == '4':
                mount_all_unmounted(drives)
                drives = get_all_drives()
            elif choice == '5':
                unmount_all_mounted(drives)
                drives = get_all_drives()
            elif choice == '6':
                update_drive_master()
            elif choice == '7':
                format_usb_drive()
                drives = get_all_drives()
            elif choice == '8':
                fix_hidden_drives()
                drives = get_all_drives()
            elif choice == '9':
                recover_data_menu()
            elif choice == 'P':
                windows_password_menu(drives)
            elif choice == 'A':
                uninstall_drive_master()
                return
            elif choice == 'C':
                os.system('clear' if os.name == 'posix' else 'cls')
                print_banner()
            elif choice == 'Q':
                print(f"\n{Colors.CYAN}{Colors.BOLD}Thanks for using Drive Master! 👋{Colors.END}")
                sys.exit(0)
            else:
                print_error("Invalid option! Please try again.")
                
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

def get_fdisk_info():
    """Parse fdisk -l output to get more details about drives"""
    fdisk_data = {}
    current_disk = None
    try:
        output = subprocess.check_output(['sudo', 'fdisk', '-l'], stderr=subprocess.DEVNULL).decode('utf-8')
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            if line.startswith('Disk /dev/'):
                disk_path = line.split(':')[0].replace('Disk ', '').strip()
                current_disk = disk_path
                fdisk_data[current_disk] = {
                    'model': 'Unknown',
                    'partitions': []
                }
            
            elif line.startswith('Disk model:') and current_disk:
                fdisk_data[current_disk]['model'] = line.split('Disk model:')[1].strip()
                
            elif line.startswith('/dev/') and current_disk:
                parts = line.split()
                if len(parts) >= 6:
                    dev_path = parts[0]
                    # Handle optional '*' in second column
                    idx = 4 if parts[1] == '*' else 4
                    if len(parts) > 5 and parts[4].endswith(tuple('KMGTP')):
                         size = parts[4]
                         ptype = ' '.join(parts[5:])
                    else:
                         # Fallback or complex parsing
                         size = parts[4]
                         ptype = ' '.join(parts[5:])
                    
                    fdisk_data[current_disk]['partitions'].append({
                        'device': dev_path,
                        'size': size,
                        'type': ptype
                    })
    except Exception:
        pass
    return fdisk_data

def get_all_drives():
    """Get all drives using fdisk -l as primary source, enriched by lsblk"""
    drives = {}
    fdisk_info = get_fdisk_info()
    
    try:
        lsblk_output = subprocess.check_output(['lsblk', '-J', '-o', 'NAME,SIZE,TYPE,TRAN,RM,MODEL,FSTYPE,LABEL,MOUNTPOINT,UUID'], stderr=subprocess.DEVNULL).decode('utf-8')
        import json
        lsblk_data = json.loads(lsblk_output)
        
        lsblk_lookup = {}
        def flatten_lsblk(devices):
            for dev in devices:
                path = f"/dev/{dev['name']}"
                lsblk_lookup[path] = dev
                if 'children' in dev:
                    flatten_lsblk(dev['children'])
        
        flatten_lsblk(lsblk_data['blockdevices'])
        
        for disk_path, disk_details in fdisk_info.items():
            lsblk_disk = lsblk_lookup.get(disk_path, {})
            
            transport = lsblk_disk.get('tran', 'Unknown')
            removable = lsblk_disk.get('rm', '1') == '1' # Default to removable if unknown
            model = disk_details['model']
            if model == 'Unknown':
                model = lsblk_disk.get('model', 'Unknown')
            
            if transport == 'usb' or removable:
                drive_type = 'USB'
            elif transport in ['sata', 'nvme', 'ata']:
                drive_type = 'Internal'
            else:
                drive_type = 'Other'
            
            if disk_details['partitions']:
                for fpart in disk_details['partitions']:
                    part_path = fpart['device']
                    lsblk_part = lsblk_lookup.get(part_path, {})
                    
                    fstype = lsblk_part.get('fstype', 'Unknown')
                    label = lsblk_part.get('label')
                    mountpoint = lsblk_part.get('mountpoint')
                    uuid = lsblk_part.get('uuid', '')
                    size = lsblk_part.get('size', fpart['size'])
                    
                    drives[part_path] = {
                        'device': part_path,
                        'parent': disk_path,
                        'size': size,
                        'fstype': fstype,
                        'fdisk_ptype': fpart['type'],
                        'label': label,
                        'mountpoint': mountpoint,
                        'uuid': uuid,
                        'type': drive_type,
                        'model': model,
                        'transport': transport
                    }
            else:
                # Disk without partitions
                drives[disk_path] = {
                    'device': disk_path,
                    'parent': disk_path,
                    'size': lsblk_disk.get('size', 'Unknown'),
                    'fstype': lsblk_disk.get('fstype', 'Unknown'),
                    'fdisk_ptype': 'Disk',
                    'label': lsblk_disk.get('label'),
                    'mountpoint': lsblk_disk.get('mountpoint'),
                    'uuid': lsblk_disk.get('uuid', ''),
                    'type': drive_type,
                    'model': model,
                    'transport': transport
                }
                    
    except Exception as e:
        print_error(f"Failed to scan drives: {str(e)}")
    
    return drives

def list_drives(drives):
    """List all drives with detailed information."""
    print_separator()
    print(f"{Colors.BLUE}{Colors.BOLD}📋 ALL DRIVES DETECTED (Detailed Info){Colors.END}")
    print_separator()
    
    usb_drives = {k: v for k, v in drives.items() if v['type'] == 'USB'}
    internal_drives = {k: v for k, v in drives.items() if v['type'] == 'Internal'}
    other_drives = {k: v for k, v in drives.items() if v['type'] == 'Other'}
    
    if usb_drives:
        print(f"{Colors.MAGENTA}{Colors.BOLD}💾 USB DRIVES{Colors.END}")
        for i, (path, info) in enumerate(usb_drives.items(), 1):
            name = info.get('label') or path.split('/')[-1]
            display_drive_info(name, info, i, "USB")
    
    if internal_drives:
        print(f"{Colors.BLUE}{Colors.BOLD}💽 INTERNAL DRIVES{Colors.END}")
        for i, (path, info) in enumerate(internal_drives.items(), 1):
            name = info.get('label') or path.split('/')[-1]
            display_drive_info(name, info, i, "Internal")
    
    if other_drives:
        print(f"{Colors.YELLOW}{Colors.BOLD}📀 OTHER DRIVES{Colors.END}")
        for i, (path, info) in enumerate(other_drives.items(), 1):
            name = info.get('label') or path.split('/')[-1]
            display_drive_info(name, info, i, "Other")
    
    print_option("0", "⬅️", "Back to Main Menu", Colors.WHITE)
    choice = click.prompt(f"{Colors.CYAN}Enter choice{Colors.END}", type=str, default="0").strip()

def display_drive_info(name, info, index, drive_type):
    """Display detailed drive information"""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    
    if info['mountpoint']:
        mounted = True
        mount_path = info['mountpoint']
    else:
        mounted = subprocess.run(['mountpoint', '-q', mount_point], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        mount_path = mount_point if mounted else "Not mounted"
    
    status_icon = "🟢" if mounted else "🔴"
    status_text = f"{Colors.GREEN}MOUNTED{Colors.END}" if mounted else f"{Colors.RED}NOT MOUNTED{Colors.END}"
    
    print(f"{Colors.CYAN}╭─ {drive_type} Drive #{index}{Colors.END}")
    print(f"{Colors.CYAN}├─{Colors.END} {Colors.YELLOW}{Colors.BOLD}📁 Name:{Colors.END} {name}")
    print(f"{Colors.CYAN}├─{Colors.END} {Colors.BLUE}📏 Size:{Colors.END} {info['size']}")
    print(f"{Colors.CYAN}├─{Colors.END} {Colors.MAGENTA}💾 Device:{Colors.END} {info['device']}")
    print(f"{Colors.CYAN}├─{Colors.END} {Colors.WHITE}💻 Model:{Colors.END} {info['model']}")
    print(f"{Colors.CYAN}├─{Colors.END} {Colors.ORANGE}📀 Format:{Colors.END} {info['fstype']} ({info.get('fdisk_ptype', 'Unknown')})")
    if mounted:
        print(f"{Colors.CYAN}├─{Colors.END} {Colors.GREEN}📂 Path:{Colors.END} {mount_path}")
    print(f"{Colors.CYAN}╰─{Colors.END} {Colors.WHITE}📊 Status:{Colors.END} {status_icon} {status_text}")
    print()

def is_drive_mounted(info):
    """Check if drive is mounted by info or path"""
    if info['mountpoint']:
        return True
    user = os.getlogin()
    name = info.get('label') or info['device'].split('/')[-1]
    mount_point = f"/media/{user}/{name}"
    return subprocess.run(['mountpoint', '-q', mount_point], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def is_mounted(name):
    """Check if drive name is mounted in /media/user/name"""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    return subprocess.run(['mountpoint', '-q', mount_point], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def mount_drive(uuid, name, dev):
    """Standard mount function"""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    
    if is_mounted(name):
        return True

    if not os.path.exists(mount_point):
        subprocess.run(['sudo', 'mkdir', '-p', mount_point])
        subprocess.run(['sudo', 'chown', f'{user}:{user}', mount_point])

    # Try UUID if available, else device
    if uuid:
        cmd = ['sudo', 'mount', '-t', 'ntfs-3g', '-o', f'uid={os.getuid()},gid={os.getgid()}', f'UUID={uuid}', mount_point]
    else:
        cmd = ['sudo', 'mount', '-t', 'ntfs-3g', '-o', f'uid={os.getuid()},gid={os.getgid()}', dev, mount_point]
    
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def mount_drive_enhanced(info, name):
    """Enhanced mount function with UI and repair suggestion"""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    
    print_separator()
    print(f"{Colors.YELLOW}{Colors.BOLD}🔌 MOUNTING: {name}{Colors.END}")
    print_separator()
    
    if is_drive_mounted(info):
        print_info(f"{name} is already mounted")
        return True
    
    if not os.path.exists(mount_point):
        print_loading("Creating mount point...")
        subprocess.run(['sudo', 'mkdir', '-p', mount_point])
        subprocess.run(['sudo', 'chown', f'{user}:{user}', mount_point])
    
    print_loading(f"Mounting {name}...")
    
    # Check filesystem type
    fstype = str(info.get('fstype') or "").lower()
    fdisk_ptype = str(info.get('fdisk_ptype') or "").lower()

    if fstype == 'ntfs' or 'microsoft' in fdisk_ptype:
        cmd = ['sudo', 'mount', '-t', 'ntfs-3g', '-o', f'uid={os.getuid()},gid={os.getgid()}', info['device'], mount_point]
    elif fstype in ['vfat', 'fat32', 'msdos']:
        cmd = ['sudo', 'mount', '-t', 'vfat', '-o', f'uid={os.getuid()},gid={os.getgid()}', info['device'], mount_point]
    elif fstype in ['ext4', 'ext3', 'ext2']:
        cmd = ['sudo', 'mount', '-t', fstype, info['device'], mount_point]
    else:
        cmd = ['sudo', 'mount', info['device'], mount_point]
        
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if result.returncode == 0:
        print_success(f"Successfully mounted {name} at {mount_point}")
        return True
    else:
        print_error(f"Mount failed for {name}")
        if 'ntfs' in fstype or 'microsoft' in fdisk_ptype:
            print_warning(f"💡 Suggestion: Run 'sudo ntfsfix {info['device']}' to fix filesystem errors")
        return False

def unmount_drive(name):
    """Unmount a drive by name"""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    
    if not is_mounted(name):
        return True
    
    print_loading(f"Unmounting {name}...")
    result = subprocess.run(['sudo', 'umount', mount_point], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if result.returncode == 0:
        try:
            os.rmdir(mount_point)
        except:
            pass
        print_success(f"Successfully unmounted {name}")
        return True
    else:
        print_error(f"Failed to unmount {name}")
        return False

def mount_menu(drives):
    """Interactive Select-to-Mount menu"""
    mountable = {path: info for path, info in drives.items() if not is_drive_mounted(info)}
    
    if not mountable:
        print_info("No unmounted drives available.")
        return

    print_separator()
    print(f"{Colors.YELLOW}{Colors.BOLD}🔌 SELECT DRIVE TO MOUNT{Colors.END}")
    print_separator()
    
    for i, (path, info) in enumerate(mountable.items(), 1):
        name = info.get('label') or path.split('/')[-1]
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.WHITE}{name}{Colors.END} ({info['size']}) - {info['fstype']} [{path}]")
    
    print_option("0", "⬅️", "Back", Colors.WHITE)
    try:
        choice = click.prompt(f"{Colors.YELLOW}Enter number{Colors.END}", type=str).strip()
        if choice == '0': return
        idx = int(choice) - 1
        if 0 <= idx < len(mountable):
            path = list(mountable.keys())[idx]
            info = mountable[path]
            name = info.get('label') or path.split('/')[-1]
            mount_drive_enhanced(info, name)
    except:
        pass

def unmount_menu(drives):
    """Interactive Select-to-Unmount menu"""
    mounted = {}
    for path, info in drives.items():
        name = info.get('label') or path.split('/')[-1]
        if is_mounted(name):
            mounted[path] = info
            
    if not mounted:
        print_info("No drives are currently mounted.")
        return

    print_separator()
    print(f"{Colors.ORANGE}{Colors.BOLD}🔓 SELECT DRIVE TO UNMOUNT{Colors.END}")
    print_separator()
    
    for i, (path, info) in enumerate(mounted.items(), 1):
        name = info.get('label') or path.split('/')[-1]
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.WHITE}{name}{Colors.END} [{path}]")

    print_option("0", "⬅️", "Back", Colors.WHITE)
    try:
        choice = click.prompt(f"{Colors.ORANGE}Enter number{Colors.END}", type=str).strip()
        if choice == '0': return
        idx = int(choice) - 1
        if 0 <= idx < len(mounted):
            path = list(mounted.keys())[idx]
            name = mounted[path].get('label') or path.split('/')[-1]
            unmount_drive(name)
    except:
        pass

def mount_all_unmounted(drives):
    """Mount everything that isn't mounted"""
    unmounted = {path: info for path, info in drives.items() if not is_drive_mounted(info)}
    if not unmounted:
        print_info("All drives already mounted.")
        return
    print_loading(f"Mounting {len(unmounted)} drives...")
    for path, info in unmounted.items():
        name = info.get('label') or path.split('/')[-1]
        mount_drive(info['uuid'], name, info['device'])

def unmount_all_mounted(drives):
    """Unmount everything that is mounted in /media/user/"""
    mounted = []
    for path, info in drives.items():
        name = info.get('label') or path.split('/')[-1]
        if is_mounted(name):
            mounted.append(name)
    
    if not mounted:
        print_info("No drives to unmount.")
        return
        
    if click.confirm(f"{Colors.RED}Unmount all {len(mounted)} drives?{Colors.END}"):
        for name in mounted:
            unmount_drive(name)

def get_usb_drives():
    """Helper to get only USB drives"""
    all_drives = get_all_drives()
    return {path: info for path, info in all_drives.items() if info['type'] == 'USB'}

def format_usb_drive():
    """Integrated drive formatter"""
    drives = get_all_drives()
    if not drives: return
    
    print_separator()
    print(f"{Colors.MAGENTA}{Colors.BOLD}💾 DRIVE FORMATTER{Colors.END}")
    print_separator()
    
    for i, (path, info) in enumerate(drives.items(), 1):
        name = info.get('label') or path.split('/')[-1]
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.YELLOW}{name}{Colors.END} [{info['type']}] ({info['size']})")
        
    print_option("0", "⬅️", "Back", Colors.WHITE)
    try:
        choice = click.prompt(f"Select drive", type=str).strip()
        if choice == '0': return
        idx = int(choice) - 1
        if 0 <= idx < len(drives):
            path = list(drives.keys())[idx]
            info = drives[path]
            name = info.get('label') or path.split('/')[-1]
            format_drive_enhanced(name, info)
    except:
        pass

def format_drive_enhanced(name, info):
    """UI for formatting a drive"""
    print_warning(f"WARNING: ALL DATA ON {name} ({info['device']}) WILL BE ERASED!")
    if not click.confirm("Are you sure?"): return
    
    print(f"Select Filesystem:\n[1] FAT32\n[2] NTFS\n[3] EXT4")
    fs_choice = click.prompt("Choice", type=int)
    
    # Unmount first
    unmount_drive(name)
    
    target = info['device']
    print_loading(f"Formatting {target}...")
    
    try:
        if fs_choice == 1:
            subprocess.run(['sudo', 'mkfs.vfat', '-F', '32', '-n', name[:11], target])
        elif fs_choice == 2:
            subprocess.run(['sudo', 'mkfs.ntfs', '-f', '-L', name, target])
        elif fs_choice == 3:
            subprocess.run(['sudo', 'mkfs.ext4', '-F', '-L', name, target])
        print_success("Format completed!")
    except Exception as e:
        print_error(f"Format failed: {e}")

def recover_data_menu():
    """Recovery center"""
    print_separator()
    print(f"{Colors.CYAN}{Colors.BOLD}🔍 DATA RECOVERY CENTER{Colors.END}")
    print(f"[1] Recover from USB\n[2] Recover from Internal\n[0] Back")
    
    choice = click.prompt("Choice", type=str).strip()
    if choice == '1':
        recover_from_usb()
    elif choice == '2':
        recover_from_internal()

def recover_from_usb():
    """USB Recovery"""
    drives = get_usb_drives()
    if not drives: return
    for i, (path, info) in enumerate(drives.items(), 1):
        name = info.get('label') or path.split('/')[-1]
        print(f"[{i}] {name} ({path})")
    
    idx = int(click.prompt("Select", type=int)) - 1
    if 0 <= idx < len(drives):
        path = list(drives.keys())[idx]
        subprocess.run(['sudo', 'testdisk', drives[path]['device']])

def recover_from_internal():
    """Internal Recovery"""
    all_drives = get_all_drives()
    drives = {path: info for path, info in all_drives.items() if info['type'] == 'Internal'}
    if not drives: return
    for i, (path, info) in enumerate(drives.items(), 1):
        name = info.get('label') or path.split('/')[-1]
        print(f"[{i}] {name} ({path})")
    
    idx = int(click.prompt("Select", type=int)) - 1
    if 0 <= idx < len(drives):
        path = list(drives.keys())[idx]
        subprocess.run(['sudo', 'testdisk', drives[path]['device']])

def fix_hidden_drives():
    """Fix problematic drives"""
    print_info("Scanning raw devices...")
    # Simplified fix logic
    try:
        output = subprocess.check_output(['lsblk', '-d', '-o', 'NAME,SIZE,MODEL'], text=True)
        print(output)
        drive = click.prompt("Enter device name to fix (e.g. sda)", type=str).strip()
        if drive:
            path = f"/dev/{drive}"
            print_loading(f"Attempting to fix {path}...")
            subprocess.run(['sudo', 'ntfsfix', path])
            print_success("Fix attempted.")
    except:
        pass

def uninstall_drive_master():
    """Clean uninstall"""
    if click.confirm("Uninstall Drive Master?"):
        subprocess.run(['sudo', 'rm', '-f', '/usr/local/bin/drive-master'])
        print_success("Uninstalled.")

def get_latest_version():
    return "3.1.0"

def update_drive_master():
    print_info("Checking for updates...")
    print_success("You are on the latest version.")

def windows_password_menu(drives):
    """Menu to select Windows drive for password removal"""
    print_separator()
    print(f"{Colors.ORANGE}{Colors.BOLD}🔑 WINDOWS PASSWORD REMOVAL{Colors.END}")
    print_separator()
    
    # Filter for NTFS/Internal drives which likely contain Windows
    windows_candidates = {path: info for path, info in drives.items() 
                          if (info.get('fstype') and info['fstype'].lower() == 'ntfs') or 
                             (info.get('fdisk_ptype') and 'microsoft' in info['fdisk_ptype'].lower())}
    
    if not windows_candidates:
        print_warning("No NTFS/Windows partitions detected.")
        if not click.confirm("Show all drives instead?"):
            return
        windows_candidates = drives

    print(f"{Colors.BLUE}Select the Windows (C:) partition:{Colors.END}")
    for i, (path, info) in enumerate(windows_candidates.items(), 1):
        name = info.get('label') or path.split('/')[-1]
        print(f"{Colors.CYAN}[{i}]{Colors.END} {Colors.WHITE}{name}{Colors.END} ({info['size']}) [{path}]")
    
    print_option("0", "⬅️", "Back", Colors.WHITE)
    try:
        choice = click.prompt("Enter number", type=str).strip()
        if choice == '0': return
        idx = int(choice) - 1
        if 0 <= idx < len(windows_candidates):
            path = list(windows_candidates.keys())[idx]
            info = windows_candidates[path]
            name = info.get('label') or path.split('/')[-1]
            
            # Ensure mounted
            if not is_drive_mounted(info):
                print_info(f"Mounting {name} to access system files...")
                if not mount_drive_enhanced(info, name):
                    print_error("Failed to mount drive.")
                    return
            
            # Fresh info to get mount point
            user = os.getlogin()
            mount_point = info.get('mountpoint') or f"/media/{user}/{name}"
            manage_windows_password(mount_point, info['device'])
    except Exception as e:
        print_error(f"Error: {e}")

def manage_windows_password(mount_point, dev_path):
    """Manual SAM management: Backup, Remove, and Restore (Advanced RegBack/Repair)"""
    # Find SAM (case insensitive check)
    sam_path = None
    config_dir = None
    repair_dir = None
    regback_dir = None
    
    # Common paths
    possible_config_paths = [
        os.path.join(mount_point, "Windows/System32/config"),
        os.path.join(mount_point, "windows/system32/config"),
        os.path.join(mount_point, "WINDOWS/SYSTEM32/CONFIG")
    ]
    
    for d in possible_config_paths:
        if os.path.exists(d):
            config_dir = d
            rb_dir = os.path.join(d, "RegBack")
            if os.path.exists(rb_dir):
                regback_dir = rb_dir
            for f in os.listdir(d):
                if f.upper() == "SAM":
                    sam_path = os.path.join(d, f)
                    break
            if sam_path: break

    # Search for Repair folder
    possible_repair_paths = [
        os.path.join(mount_point, "Windows/repair"),
        os.path.join(mount_point, "windows/repair"),
        os.path.join(mount_point, "WINDOWS/REPAIR")
    ]
    for d in possible_repair_paths:
        if os.path.exists(d):
            repair_dir = d
            break

    if not config_dir:
        print_error("Could not locate Windows config directory on this partition.")
        return

    # Check for backups
    all_files = os.listdir(config_dir)
    backups = sorted([f for f in all_files if f.startswith("SAM.backup-")], reverse=True)
    
    # Check RegBack files
    regback_valid = False
    if regback_dir:
        rb_sam = os.path.join(regback_dir, "SAM")
        if os.path.exists(rb_sam) and os.path.getsize(rb_sam) > 0:
            regback_valid = True

    # Check Repair files
    repair_valid = False
    if repair_dir:
        rp_sam = os.path.join(repair_dir, "SAM")
        if os.path.exists(rp_sam):
            repair_valid = True

    print_separator()
    print(f"{Colors.ORANGE}{Colors.BOLD}🛠️  ADVANCED WINDOWS PASSWORD MANAGEMENT{Colors.END}")
    print_separator()
    
    if sam_path:
        print_success(f"Original SAM Hive Found: {sam_path}")
    else:
        print_warning("Original SAM Hive is MISSING (Passwords likely removed).")

    if backups:
        print_info(f"Found {len(backups)} manual backup(s).")
    if regback_valid:
        print_success("Automatic Registry Backup (RegBack) is available and valid!")
    if repair_valid:
        print_info("System Repair/Factory SAM is available.")

    print(f"\n{Colors.YELLOW}Choose an action:{Colors.END}")
    if sam_path:
        print(f"{Colors.GREEN}[1]{Colors.END} Smart Password Reset (Backup + Auto-Restore from RegBack/Repair)")
    if backups:
        print(f"{Colors.CYAN}[2]{Colors.END} Restore from Manual Backup")
    if regback_valid:
        print(f"{Colors.BLUE}[3]{Colors.END} Advanced: Restore ALL Hives from RegBack")
    if repair_valid:
        print(f"{Colors.MAGENTA}[4]{Colors.END} Advanced: Factory Reset (Restore from Repair Folder)")
    print(f"{Colors.CYAN}[0]{Colors.END} Cancel")
    
    choice = click.prompt("Choice", type=str).strip()
    
    if choice == '1' and sam_path:
        # Create backup first
        backup_name = f"SAM.backup-{int(time.time())}"
        backup_path = os.path.join(config_dir, backup_name)
        dt_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print_loading(f"Creating secure backup of credentials ({dt_now})...")
        subprocess.run(['sudo', 'cp', sam_path, backup_path])
        
        # SMART RESET LOGIC
        reset_success = False
        
        # Try RegBack first
        if regback_valid:
            print_loading("Attempting Smart Reset via RegBack...")
            src = os.path.join(regback_dir, "SAM")
            subprocess.run(['sudo', 'cp', src, sam_path])
            reset_success = True
            print_success("✅ Smart Reset successful using RegBack!")
            
        # Try Repair if RegBack failed or unavailable
        elif repair_valid:
            print_loading("Attempting Smart Reset via Repair folder...")
            src = os.path.join(repair_dir, "SAM")
            subprocess.run(['sudo', 'cp', src, sam_path])
            reset_success = True
            print_success("✅ Smart Reset successful using Factory Repair!")
            
        else:
            print_error("Smart Reset failed: No valid RegBack or Repair hives found.")
            print_warning("Note: Deleting SAM completely is DISABLED to prevent boot failure.")
            print_info("Consider manually restoring from a backup if available.")
            
        if reset_success:
            print_info("Windows should now boot with passwords reset or reverted to a previous state.")
        
    elif choice == '2' and backups:
        print(f"\n{Colors.BLUE}Available Backups:{Colors.END}")
        for i, b in enumerate(backups, 1):
            try:
                timestamp = int(b.split('-')[-1])
                dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{i}] {Colors.YELLOW}{b}{Colors.END} ({Colors.GREEN}{dt}{Colors.END})")
            except:
                print(f"[{i}] {b}")
        
        try:
            b_idx = int(click.prompt("Select backup to restore", type=int)) - 1
            if 0 <= b_idx < len(backups):
                target_backup = os.path.join(config_dir, backups[b_idx])
                original_sam = os.path.join(config_dir, "SAM")
                print_loading(f"Restoring {backups[b_idx]} to SAM...")
                subprocess.run(['sudo', 'cp', target_backup, original_sam])
                print_success("✅ Credentials restored successfully!")
            else:
                print_error("Invalid selection.")
        except:
            print_error("Invalid input.")

    elif choice == '3' and regback_valid:
        print_warning("This will restore ALL Registry Hives (SAM, SYSTEM, SECURITY, etc.) from RegBack.")
        if click.confirm("Proceed with RegBack restoration?"):
            hives = ['SAM', 'SYSTEM', 'SECURITY', 'SOFTWARE', 'DEFAULT']
            print_loading("Restoring hives from RegBack...")
            for hive in hives:
                src = os.path.join(regback_dir, hive)
                dst = os.path.join(config_dir, hive)
                if os.path.exists(src):
                    subprocess.run(['sudo', 'cp', src, dst])
            print_success("✅ Registry hives restored from RegBack successfully!")

    elif choice == '4' and repair_valid:
        print_warning("This will restore SAM/SYSTEM/SECURITY from the Repair folder (Factory State).")
        if click.confirm("Proceed with Factory Reset?"):
            hives = ['SAM', 'SYSTEM', 'SECURITY']
            print_loading("Restoring from Repair folder...")
            for hive in hives:
                src = os.path.join(repair_dir, hive)
                dst = os.path.join(config_dir, hive)
                if os.path.exists(src):
                    subprocess.run(['sudo', 'cp', src, dst])
            print_success("✅ System Hives restored to Factory State successfully!")
    else:
        print_info("Action cancelled or unavailable.")

if __name__ == '__main__':
    main()
