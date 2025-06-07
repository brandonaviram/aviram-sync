# Aviram Sync - Travel Media Sync Tool

A minimalist rsync-based tool for syncing photos and videos from memory cards. Organizes files by location, date, and media type for travel campaigns.

## Features

- **Universal RAW Support**: Supports RAW files from all major camera manufacturers (Canon, Nikon, Sony, Fujifilm, etc.)
- **Automatic Organization**: Creates organized folder structure by location and date
- **Type Separation**: Separates videos and images into dedicated folders
- **Optional Breakout**: Organize images by file type (JPG, RAF, CR2, etc.) with `--breakout` flag
- **Debug Mode**: Detailed logging with `--debug` flag
- **Fast Transfer**: Uses rsync for efficient, reliable file transfers
- **Smart Detection**: Automatically detects and filters media files
- **Cross-Platform**: Works on macOS, Linux, and Windows (with WSL)

## Requirements

- Python 3.6 or higher
- `rsync` (automatically installed on macOS/Linux if missing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/brandonaviram/aviram-sync.git
cd aviram-sync
```

2. Make the script executable:
```bash
chmod +x aviram-sync.py
```

3. Optional: Create a symlink for easy access:
```bash
ln -s $(pwd)/aviram-sync.py /usr/local/bin/aviram-sync
```

## Usage

### Basic Usage
```bash
python3 aviram-sync.py
```

### With Options
```bash
python3 aviram-sync.py --debug --breakout
```

### Interactive Prompts
1. **Source Directory**: Default is `/Volumes/Untitled` (typical SD card mount)
2. **Destination**: Choose Movies folder, Pictures folder, or custom path
3. **Location Name**: Enter shoot location (e.g., "Tokyo Street Photography")

### Output Structure
```
TOKYO STREET PHOTOGRAPHY JUNE 2025/
├── VIDEOS/
│   ├── DSCF1819.MOV
│   ├── DSCF1820.MOV
│   └── DSCF1867.MOV
└── IMAGES/
    ├── DSCF1765.JPG
    ├── DSCF1765.RAF
    ├── DSCF1766.JPG
    ├── DSCF1766.RAF
    └── ...
```

### With `--breakout` Flag
```
TOKYO STREET PHOTOGRAPHY JUNE 2025/
├── VIDEOS/
│   └── ...
└── IMAGES/
    ├── JPG/
    │   ├── DSCF1765.JPG
    │   └── DSCF1766.JPG
    └── RAF/
        ├── DSCF1765.RAF
        └── DSCF1766.RAF
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--debug` | Enable detailed debug output showing all files found and processed |
| `--breakout` | Organize images by file type into separate subfolders |

## Supported File Formats

### Video Formats
- MP4, MOV, AVI, MKV, M4V, WMV, FLV, WebM, 3GP

### Image Formats
- **Standard**: JPG, PNG, GIF, BMP, TIFF, HEIC, WebP
- **RAW Formats**: 
  - Canon: CR2, CR3, CRW
  - Nikon: NEF, NRW
  - Sony: ARW, SRF, SR2
  - Fujifilm: RAF
  - Olympus: ORF
  - Pentax: PEF, PTX, PXN
  - Panasonic/Leica: RW2, RWL, RWZ, RAW
  - Phase One: IIQ, EIP
  - Hasselblad: 3FR, FFF
  - RED: R3D
  - And 30+ more RAW formats

## Examples

### Sync SD Card to Pictures Folder
```bash
python3 aviram-sync.py
# Source: [Enter] (uses /Volumes/Untitled)
# Destination: 2 (Pictures folder)
# Location: "Kyoto Temples"
```

### Debug Mode with Breakout
```bash
python3 aviram-sync.py --debug --breakout
# Shows detailed file discovery and organizes by type
```

### Custom Source and Destination
```bash
python3 aviram-sync.py
# Source: /Volumes/SONY_SD
# Destination: 3 (custom path)
# Custom path: /Users/brandon/Photography/2025
# Location: "Iceland Landscapes"
```

## Troubleshooting

### rsync Not Found
The tool will automatically attempt to install rsync using your system's package manager:
- **macOS**: Homebrew or MacPorts
- **Linux**: apt, yum, dnf, or pacman
- **Windows**: Requires WSL or manual installation

### Files Not Detected
Use `--debug` flag to see exactly which files are found and whether they're recognized as media files.

### Permission Issues
Ensure you have read access to the source directory and write access to the destination.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use and modify for your needs.

## Author

Brandon Aviram - [@brandonaviram](https://github.com/brandonaviram) 