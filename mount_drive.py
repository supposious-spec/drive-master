import click
import subprocess
import os
import sys

VERSION = "1.0.0"

@click.command()
@click.argument('drive_name', required=False)
@click.option('--version', is_flag=True, help="Show version info")
def main(drive_name, version):
    """🚀 Drive Master: Auto-mount NTFS drives on Linux with ease."""
    if version:
        click.echo(f"Drive Master v{VERSION}")
        return

    drives = get_ntfs_drives()

    if not drives:
        click.echo("❌ No NTFS drives found! Check 'lsblk' or 'blkid'.")
        return

    if drive_name:
        # Direct mount mode
        drive_name = drive_name.capitalize()
        if drive_name not in drives:
            click.echo(f"⚠️ Drive '{drive_name}' not found. Available: {', '.join(drives.keys())}")
            return
        mount_drive(drives[drive_name]['uuid'], drive_name, drives[drive_name]['dev'])
    else:
        # Interactive menu
        while True:
            click.echo("\n--- 🛠️ Drive Master Menu ---")
            click.echo("1: 📋 List all NTFS drives")
            click.echo("2: 🔌 Mount a specific drive")
            click.echo("3: ⚡ Mount all NTFS drives")
            click.echo("Q: 🚪 Quit")
            choice = click.prompt("Enter option", type=str).strip().upper()

            if choice == '1':
                list_drives(drives)
            elif choice == '2':
                name_input = click.prompt("Enter drive name (e.g., Coding)", type=str).capitalize()
                if name_input in drives:
                    mount_drive(drives[name_input]['uuid'], name_input, drives[name_input]['dev'])
                else:
                    click.echo(f"❌ Drive '{name_input}' not found. Try option 1 to list.")
            elif choice == '3':
                for name, info in drives.items():
                    mount_drive(info['uuid'], name, info['dev'])
            elif choice == 'Q':
                sys.exit(0)
            else:
                click.echo("Invalid option! Try again.")

def get_ntfs_drives():
    """Scan NTFS drives using blkid."""
    drives = {}
    try:
        blkid_output = subprocess.check_output(['sudo', 'blkid', '-o', 'export']).decode('utf-8')
    except subprocess.CalledProcessError:
        click.echo("Error: blkid failed. Run with sudo or check permissions.")
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
    click.echo("\n--- NTFS Drives Found ---")
    user = os.getlogin()
    for name, info in drives.items():
        mount_point = f"/media/{user}/{name}"
        is_mounted = subprocess.run(['mountpoint', '-q', mount_point]).returncode == 0
        status = "✅ Mounted" if is_mounted else "❌ Not Mounted"
        click.echo(f"📍 {name:15} | UUID: {info['uuid']} | Dev: {info['dev']} | {status}")

def mount_drive(uuid, name, dev):
    """Mount the drive."""
    user = os.getlogin()
    mount_point = f"/media/{user}/{name}"
    
    if not os.path.exists(mount_point):
        subprocess.run(['sudo', 'mkdir', '-p', mount_point])
        subprocess.run(['sudo', 'chown', f'{user}:{user}', mount_point])

    if subprocess.run(['mountpoint', '-q', mount_point]).returncode == 0:
        click.echo(f"ℹ️ {name} is already mounted at {mount_point}")
        return

    # Using -t ntfs-3g for better write support
    cmd = ['sudo', 'mount', '-t', 'ntfs-3g', '-o', f'uid={os.getuid()},gid={os.getgid()}', f'UUID={uuid}', mount_point]
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        click.echo(f"✅ Successfully mounted {name} at {mount_point}")
    else:
        click.echo(f"❌ Mount failed for {name}.")
        click.echo(f"💡 Suggestion: Run 'sudo ntfsfix {dev}' to fix filesystem errors.")

if __name__ == '__main__':
    main()
