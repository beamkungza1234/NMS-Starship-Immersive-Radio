import os
import sys
import time
import json
import pymem
import vlc
import keyboard

# config loader
def load_config():
    config_file = 'config.json'
    default_config = {
        "system": {"pointer_offset_hex": "0x596F740"},
        "audio": {
            "max_volume": 90, 
            "fade_speed": 0.05, 
            "static_duration": 0.8,
            "static_volume": 100 
        },
        "keys": {"next_station": "f8", "prev_station": "f6", "pair_ship": "f7"},
        "stations": []
    }
    
    if not os.path.exists(config_file):
        print(f"Config file not found! Creating default...")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        return default_config

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config

# load config
CONFIG = load_config()
STATIONS = CONFIG['stations']
KEYS = CONFIG['keys']
AUDIO_CFG = CONFIG['audio']
SYS_CFG = CONFIG['system']
POINTER_OFFSET = int(SYS_CFG['pointer_offset_hex'], 16)

# Setup VLC
vlc_path = SYS_CFG.get('vlc_path', r"C:\Program Files\VideoLAN\VLC")
if os.path.exists(vlc_path):
    os.add_dll_directory(vlc_path)
    os.environ['PATH'] = vlc_path + ";" + os.environ['PATH']

# Global Vars
current_station_index = 0
station_changed = False
target_ship_id = None

# Helper functions
def get_current_station_volume():
    global_max = AUDIO_CFG['max_volume']
    
    station_vol_percent = STATIONS[current_station_index].get('volume', 100)
    
    final_vol = int(global_max * (station_vol_percent / 100))
    return max(0, min(final_vol, 100)) # volume between 0-100

def next_station():
    global current_station_index, station_changed
    if target_ship_id is None: return
    current_station_index = (current_station_index + 1) % len(STATIONS)
    station_changed = True

def prev_station():
    global current_station_index, station_changed
    if target_ship_id is None: return
    current_station_index = (current_station_index - 1) % len(STATIONS)
    station_changed = True

def set_volume_smooth(player, start_vol, end_vol):
    if start_vol == end_vol: return
    step = 5 if end_vol > start_vol else -5
    
    if end_vol > 0 and not player.is_playing(): 
        player.play()
        
    for vol in range(start_vol, end_vol + step, step):
        vol = max(0, min(vol, 100))
        player.audio_set_volume(vol)
        time.sleep(AUDIO_CFG['fade_speed'])
        
    if end_vol == 0: 
        player.pause()

def play_static_transition(instance, player):
    static_file = AUDIO_CFG.get('static_sound_file', 'static.mp3')
    static_vol = AUDIO_CFG.get('static_volume', 100) # set volume of static sound

    if os.path.exists(static_file):
        print("   (shhh... tuning...)")
        media = instance.media_new(static_file)
        player.set_media(media)
        player.play()
        
        # Set static sound
        player.audio_set_volume(static_vol)
        
        time.sleep(AUDIO_CFG.get('static_duration', 0.8))
    else:
        time.sleep(0.2)

def main():
    global station_changed, target_ship_id, current_station_index
    
    print(f"--- NMS RADIO: VOLUME CONTROL EDITION ---")
    print(f"Controls: Next[{KEYS['next_station']}] | Prev[{KEYS['prev_station']}] | Pair[{KEYS['pair_ship']}]")
    
    try:
        keyboard.add_hotkey(KEYS['next_station'], next_station)
        keyboard.add_hotkey(KEYS['prev_station'], prev_station)
    except Exception as e:
        print(f"Key binding error: {e}")

    # VLC Setup
    cockpit_args = "--input-repeat=-1 --audio-filter=equalizer --equalizer-preamp=12 --equalizer-bands=-20,-20,-10,0,8,12,8,-5,-20,-20"
    instance = vlc.Instance(cockpit_args)
    player = instance.media_player_new()
    
    if STATIONS:
        media = instance.media_new(STATIONS[current_station_index]['url'])
        player.set_media(media)
        player.audio_set_volume(0)

    current_volume = 0
    nms = None
    current_mem_val = 0

    try:
        while True:
            # 1. Connect
            if nms is None:
                try:
                    nms = pymem.Pymem("NMS.exe")
                    target_addr = nms.process_base.lpBaseOfDll + POINTER_OFFSET
                    print(f"Game Connected.")
                except:
                    time.sleep(2)
                    continue

            # 2. Read Memory (NOTE: Memory value may unstable when game have updated / NOTE2: This address test only in Stream version (Another platform may not work))
            try:
                current_mem_val = nms.read_int(target_addr)
            except:
                nms = None
                continue

            # 3. Pairing
            if keyboard.is_pressed(KEYS['pair_ship']):
                if current_mem_val != 0:
                    target_ship_id = current_mem_val
                    print(f"\nSHIP PAIRED! ID: {target_ship_id}")
                    time.sleep(0.5)
                else:
                    print(f"\nValue is 0. Enter ship first.")
                    time.sleep(0.5)

            # Logic
            should_play = (target_ship_id is not None) and (current_mem_val == target_ship_id)
            
            # Radio Station Volume
            target_station_vol = get_current_station_volume()

            if should_play:
                if station_changed:
                    print(f"[RADIO] Tuning: {STATIONS[current_station_index]['name']} (Vol: {STATIONS[current_station_index].get('volume', 100)}%)")
                    
                    player.stop()
                    play_static_transition(instance, player) # เล่นเสียงซ่าดังๆ
                    
                    # โหลดเพลงใหม่
                    new_media = instance.media_new(STATIONS[current_station_index]['url'])
                    player.set_media(new_media)
                    player.play()
                    
                    # Set Volume
                    player.audio_set_volume(target_station_vol)
                    
                    current_volume = target_station_vol
                    station_changed = False

                elif current_volume != target_station_vol:
                    # Fade in radio playback when enter the starship
                    print(f"Cockpit Entered -> Fade In to {target_station_vol}%")
                    set_volume_smooth(player, current_volume, target_station_vol)
                    current_volume = target_station_vol
            else:
                if current_volume != 0:
                    print(f"Value Change -> Fade Out")
                    set_volume_smooth(player, current_volume, 0)
                    current_volume = 0
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nShutdown")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()