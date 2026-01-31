import click
import subprocess
import os
import sys
import time
import shutil

VERSION = "2.0.0"

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
            elif choice == 'Q':
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
