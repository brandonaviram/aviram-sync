# Aviram Sync 📸

> Backup your camera's memory card and organize photos/videos by trip - no tech skills needed!

## Super Easy Setup (5 minutes)

### Step 1: Open Terminal
- **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
- **Windows**: Press `Win + R`, type "cmd", press Enter  
- **Linux**: Press `Ctrl + Alt + T`

### Step 2: Download the Tool
Copy and paste this into Terminal, then press Enter:
```bash
git clone https://github.com/brandonaviram/aviram-sync.git
```

### Step 3: Go to the Folder
Copy and paste this, then press Enter:
```bash
cd aviram-sync
```

### Step 4: Run It!
Copy and paste this, then press Enter:
```bash
python3 aviram-sync.py
```

**That's it!** The tool will ask you simple questions and do the rest.

## What Happens Next?

The tool will ask you 3 easy questions:

1. **"Where's your memory card?"** 
   - Just press Enter (it finds it automatically)
   - Or type the path if it's somewhere else

2. **"Where should I save your files?"**
   - Type `1` for Movies folder
   - Type `2` for Pictures folder  
   - Type `3` for somewhere else

3. **"What should I call this trip?"**
   - Type something like "Tokyo Vacation" or "Wedding Photos"

Then it copies and organizes everything automatically!

## What You Get

Your files will be organized like this:
```
TOKYO VACATION DECEMBER 2025/
├── VIDEOS/          ← All your videos here
└── IMAGES/          ← All your photos here
```

## What It Does

- 🚀 **Fast backup** - Uses professional tools under the hood
- 📁 **Auto-organizes** - Creates folders by trip name and date  
- 🎯 **Finds everything** - Gets all your photos/videos automatically
- 🔧 **Works with any camera** - Canon, Nikon, Sony, Fujifilm, iPhone, etc.
- 💻 **Works everywhere** - Mac, Windows, Linux

## Troubleshooting

**"Command not found" error?**
- Try `python aviram-sync.py` instead of `python3`

**"No such file or directory"?** 
- Make sure you did Step 3 (`cd aviram-sync`)

**Not finding your memory card?**
- Run: `python3 aviram-sync.py --debug` to see what it finds

**Still stuck?** [Ask for help here](https://github.com/brandonaviram/aviram-sync/issues) - we're friendly!

---

## Advanced Options (Optional)

Want more control? Add these flags:

```bash
# See exactly what files it finds
python3 aviram-sync.py --debug

# Organize by file type (JPG/, RAF/, etc.)
python3 aviram-sync.py --breakout
```

## What File Types Work?

**Photos**: JPG, PNG, HEIC, plus RAW files from any camera (Canon CR2/CR3, Nikon NEF, Sony ARW, Fujifilm RAF, etc.)

**Videos**: MP4, MOV, AVI, MKV, and more

---

**Made with ❤️ by** [@brandonaviram](https://github.com/brandonaviram) for stress-free photo backups ✈️ 