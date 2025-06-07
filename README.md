# Aviram Sync 📸

> Simple tool to backup your camera's SD card and organize photos/videos by trip

## Quick Start

1. **Install**: `git clone https://github.com/brandonaviram/aviram-sync.git`
2. **Run**: `python3 aviram-sync.py`
3. **Follow prompts**: Choose where to save files and name your trip
4. **Done!** Your files are organized like: `TOKYO JUNE 2025/IMAGES/` and `TOKYO JUNE 2025/VIDEOS/`

## What It Does

- 🚀 **Fast backup** using rsync 
- 📁 **Auto-organizes** by trip name and date
- 🎯 **Smart detection** - finds all your photos/videos automatically
- 🔧 **RAW support** - Works with Canon, Nikon, Sony, Fujifilm, etc.
- 💻 **Works everywhere** - macOS, Linux, Windows

## Usage

```bash
# Basic usage
python3 aviram-sync.py

# With debug info
python3 aviram-sync.py --debug

# Organize by file type (JPG/, RAF/, etc.)
python3 aviram-sync.py --breakout
```

**That's it!** The tool will:
1. Ask for your SD card location (defaults to `/Volumes/Untitled`)
2. Ask where to save files (Movies or Pictures folder)
3. Ask for trip name (e.g., "Tokyo Street Photography")
4. Copy and organize everything

## Example Output

```
TOKYO STREET PHOTOGRAPHY JUNE 2025/
├── VIDEOS/          # All your videos here
└── IMAGES/          # All your photos here
```

---

## Installation Details

```bash
git clone https://github.com/brandonaviram/aviram-sync.git
cd aviram-sync
chmod +x aviram-sync.py
```

**Requirements**: Python 3.6+ and rsync (auto-installed if missing)

## Supported Files

**Photos**: JPG, PNG, HEIC, plus RAW files from Canon (CR2/CR3), Nikon (NEF), Sony (ARW), Fujifilm (RAF), Olympus (ORF), and 30+ more

**Videos**: MP4, MOV, AVI, MKV, and more

## Command Options

| Flag | What it does |
|------|-------------|
| `--debug` | Shows detailed info about what files are found |
| `--breakout` | Separates file types: `IMAGES/JPG/`, `IMAGES/RAF/`, etc. |

## Troubleshooting

**Files not detected?** Use `--debug` to see what's happening

**No rsync?** The tool will try to install it automatically

**Permission errors?** Make sure you can read the SD card and write to your chosen folder

---

## Contributing

Found a bug or want a feature? [Open an issue](https://github.com/brandonaviram/aviram-sync/issues) or submit a PR!

## License

MIT License - use it however you want

**Made by** [@brandonaviram](https://github.com/brandonaviram) for hassle-free photo backups ✈️ 