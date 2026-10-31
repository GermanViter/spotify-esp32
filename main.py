import time
import display
import spotify
import wifi

POLL_INTERVAL = 5  # User requested 5s polling

def run():
    oled = display.init_display()
    display.show_text(oled, "Connecting...")

    last_track = None

    while True:
        try:
            info = spotify.get_currently_playing()
            track_id = info["name"] if info else None

            if track_id != last_track:
                last_track = track_id
                if info:
                    # Show: track name (wrapped), artist on last visible line
                    text = "{}\n{}".format(info["name"], info["artist"])
                    display.wrap_text(oled, text)
                else:
                    display.show_text(oled, "Nothing playing")

        except OSError as e:
            display.show_text(oled, "Err: " + str(e))
            last_track = None  # force refresh on recovery

        time.sleep(POLL_INTERVAL)

if __name__ in ("__main__", "main"):
    run()
