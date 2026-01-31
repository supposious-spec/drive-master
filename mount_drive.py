import click
import subprocess
import os
import sys
import time
import shutil

VERSION = "1.0.0"

# Colors and styling
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
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
            print_option("3", "⚡", "Mount all NTFS drives", Colors.MAGENTA)
            print_option("Q", "🚪", "Quit", Colors.RED)
            print_separator()
            
            choice = click.prompt(f"{Colors.CYAN}➤ Enter your choice{Colors.END}", type=str).strip().upper()

            if choice == '1':
                list_drives(drives)
            elif choice == '2':
                print_separator()
                name_input = click.prompt(f"{Colors.YELLOW}🔍 Enter drive name (e.g., Coding){Colors.END}", type=str).capitalize()
                if name_input in drives:
                    mount_drive(drives[name_input]['uuid'], name_input, drives[name_input]['dev'])
                else:
                    print_error(f"Drive '{name_input}' not found. Try option 1 to list.")
            elif choice == '3':
                print_loading("Mounting all drives...")
                for name, info in drives.items():
                    mount_drive(info['uuid'], name, info['dev'])
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
        is_mounted = subprocess.run(['mountpoint', '-q', mount_point]).returncode == 0
        
        status_icon = "🟢" if is_mounted else "🔴"
        status_text = f"{Colors.GREEN}MOUNTED{Colors.END}" if is_mounted else f"{Colors.RED}NOT MOUNTED{Colors.END}"
        
        print(f"{Colors.CYAN}╭─ Drive #{i}{Colors.END}")
        print(f"{Colors.CYAN}├─{Colors.END} {Colors.YELLOW}{Colors.BOLD}📁 Name:{Colors.END} {name}")
        print(f"{Colors.CYAN}├─{Colors.END} {Colors.BLUE}🆔 UUID:{Colors.END} {info['uuid'][:8]}...")
        print(f"{Colors.CYAN}├─{Colors.END} {Colors.MAGENTA}💾 Device:{Colors.END} {info['dev']}")
        print(f"{Colors.CYAN}╰─{Colors.END} {Colors.WHITE}📊 Status:{Colors.END} {status_icon} {status_text}")
        print()

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

    if subprocess.run(['mountpoint', '-q', mount_point]).returncode == 0:
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

if __name__ == '__main__':
    main()
