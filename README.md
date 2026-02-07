# 📻 NMS Starship Immersive Radio (External Tool)

**A standalone Python tool that adds a real-time, immersive cockpit radio to No Man's Sky.** 🎶

## 🚀 What is this?
This is a simple external script (Python) that plays online radio stations when you are inside your starship. It uses memory reading to detect your ship's state—no game files are modified, making it compatible with most game versions.

### ✨ Key Features
* **Context Aware:** Music automatically plays when you enter the ship and fades out when you leave.
* **Immersive Audio:** Simulates "Cockpit Speakers" using EQ filters (cuts bass/treble for a Lo-Fi radio feel).
* **Static Transitions:** Plays static noise (shhh...) when switching stations, just like a real radio.
* **Pairing System:** Works with any save file and handles game restarts gracefully (Press a key to "link" to your current ship).
* **Fully Customizable:** Add your own radio stations and adjust volumes via `config.json`.

---

## 🛠️ Requirements
* **OS:** Windows 10/11 (64-bit)
* **Game:** No Man's Sky (Steam, another platform aren't tested)
* **Software:**
    * [Python 3.10+](https://www.python.org/downloads/)
    * [VLC Media Player](https://www.videolan.org/vlc/) (Must be installed! The script uses VLC's engine)

---
## 🎥Video Demo
[![NMS Radio Demo](https://img.youtube.com/vi/olyZUqzuAbM/maxresdefault.jpg)](https://youtu.be/olyZUqzuAbM)
## 📥 Installation

1.  **Clone or Download** this repository.
2.  Open a terminal in the folder and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Dependencies: `pymem`, `python-vlc`, `keyboard`)*
3.  Make sure you have a `static.mp3` file in the folder (for the static noise effect).

---

## 🎮 How to Use

1.  **Launch No Man's Sky** and load your save.
2.  **Run the script:**
    ```bash
    python main.py
    ```
3.  **In-Game Setup (Do this every time you play):**
    * Walk to your ship and **get inside**.
    * Wait for the "Game Connected" message in the terminal.
    * Press **`F7`** to **PAIR** the radio when you sitting in your ship.
    * *You should see a message: "SHIP PAIRED! ID: XXXXX"*

4.  **Controls (Default):**
    | Key | Function | Description |
    | :---: | :--- | :--- |
    | **F5** | Power Toggle | Turn the radio ON / OFF |
    | **F6** | Prev Station | Switch to the previous radio station |
    | **F7** | **Pair Ship** | Link radio to your current ship (Press once) |
    | **F8** | Next Station | Switch to the next radio station |
NOTE: You can change these config anytime in `config.json`


---

## ⚙️ Configuration (`config.json`)

You can add your own stations or change keybinds in the `config.json` file.


```json
{
    "audio": {
        "max_volume": 90,          // Global max volume
        "static_volume": 100,      // Volume of the static noise
        "fade_speed": 0.05         // How fast the music fades in/out
    },
    "stations": [
        {
            "name": "Lofi Girl",
            "url": "[https://play.streamafrica.net/lofiradio](https://play.streamafrica.net/lofiradio)",
            "volume": 85           // Volume trim for this specific station
        },
        {
            "name": "My Custom Station",
            "url": "[http://stream-url-here.mp3](http://stream-url-here.mp3)",
            "volume": 100
        }
    ]
}
```

### 🌐 Where to find Radio Stations?
Need more stations? You can find thousands of direct stream URLs from the community database:

* **Recommended:** [Radio-Browser.info](https://www.radio-browser.info/)
* **Alternative:** [Internet-Radio.com](https://www.internet-radio.com/)

**💡 Pro Tip:**
Make sure you copy the **Direct Stream URL** (often ends in `.mp3`, `.aac`, `.m3u8`, or looks like `http://ip:port/stream`).
* ❌ **Don't use:** The radio station's website URL (e.g., `www.coolism.net`).
* ✅ **Do use:** The stream URL (e.g., `https://coolism-web.cdn.byteark.com/;stream/1`).
* *Test the link in VLC Player first to make sure it works!*

## ⚠️ Disclaimer & Safety
* Read-Only: This tool only reads the game's memory to check if you are in a ship. It does not write or inject code into the game.

* External: It does not modify `.pak` or `.mbin` files, so it won't conflict with other mods.

* Use at your own risk: While safe, using external tools is always at the user's discretion.
* This tool only test in **Steam (Windows)** version Other store like gamepass or GOG may not work
* Console platform are not supported
