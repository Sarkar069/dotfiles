#!/usr/bin/env python3
"""
SwayFX Fader Script
Smooth fade-in/out opacity transitions for focused, unfocused, and floating windows.
"""

from i3ipc import Connection, Event
from threading import Thread, Lock
from time import sleep

# ======================
# Configurable Settings
# ======================
FRAME_T = 0.01  # seconds between frames

# Opacity levels
CON_AC     = 1.0   # active tiled
CON_INAC   = 0.88  # inactive tiled
FLOAT_AC   = 1.0   # active floating
FLOAT_INAC = 0.88  # inactive floating
BOT_INAC   = 0.88  # bottom window

# Fade durations (seconds)
FADE_TIME      = 0.20
ALT_FADE_TIME  = 0.12
CON_OUT        = FADE_TIME
CON_IN         = 0.15
FLOAT_OUT      = ALT_FADE_TIME
FLOAT_IN       = ALT_FADE_TIME
BOT_OUT        = ALT_FADE_TIME
BOT_IN         = ALT_FADE_TIME
BOT_SWITCH_IN  = FADE_TIME
BOT_SWITCH_OUT = FADE_TIME
FLOAT_BOT_OUT  = FADE_TIME
FLOAT_BOT_IN   = FADE_TIME


# ======================
# Helper Functions
# ======================
def change_opacity(win, opacity):
    """Safely set opacity via sway command."""
    try:
        win.command(f"opacity {opacity:.3f}")
    except Exception as e:
        print(f"[WARN] Failed to set opacity for {win.name or win.id}: {e}")


# ======================
# Main Class
# ======================
class Fader:
    def __init__(self):
        self.floating_windows = set()
        self.fade_queue = {}
        self.fade_lock = Lock()
        self.fader_running = False
        self.bottom_win = None
        self.old_win = None
        self.active_win = None

        self.ipc = Connection()
        self.ipc.on(Event.WINDOW_FOCUS, self.on_window_focus)
        self.ipc.on(Event.WINDOW_NEW, self.on_window_new)
        self.ipc.on(Event.WINDOW_FLOATING, self.on_window_floating)

        # Initialize window tree
        self.init_existing_windows()

        print("[INFO] swayfader started successfully.")
        self.ipc.main()

    # ---------------------
    def init_existing_windows(self):
        """Initialize all existing windows with base opacity."""
        tree = self.ipc.get_tree()
        for win in tree.descendants():
            if not hasattr(win, "type") or win.type not in ("con", "floating_con"):
                continue

            if win.floating:
                self.floating_windows.add(win.id)
                if win.focused:
                    self.active_win = win
                    change_opacity(win, FLOAT_AC)
                else:
                    change_opacity(win, FLOAT_INAC)
            else:
                if win.focused:
                    self.active_win = win
                    change_opacity(win, CON_AC)
                else:
                    change_opacity(win, CON_INAC)

    # ---------------------
    def add_fade(self, win, start, target, duration):
        """Add or update a fade animation."""
        if not win:
            return
        if not duration or start == target:
            change_opacity(win, target)
            return

        with self.fade_lock:
            change = (FRAME_T / duration) * (target - start)
            self.fade_queue[win.id] = {
                "opacity": start,
                "change": change,
                "target": target,
                "win": win,
            }

        if not self.fader_running:
            self.start_fader()

    # ---------------------
    def start_fader(self):
        self.fader_running = True
        Thread(target=self.fader_loop, daemon=True).start()

    # ---------------------
    def fader_loop(self):
        """Worker thread that updates all fading windows."""
        while True:
            with self.fade_lock:
                if not self.fade_queue:
                    break

                finished = []
                for win_id, f in list(self.fade_queue.items()):
                    f["opacity"] += f["change"]
                    done = (f["change"] > 0 and f["opacity"] >= f["target"]) or \
                           (f["change"] < 0 and f["opacity"] <= f["target"])

                    if done:
                        change_opacity(f["win"], f["target"])
                        finished.append(win_id)
                    else:
                        change_opacity(f["win"], f["opacity"])

                for fid in finished:
                    self.fade_queue.pop(fid, None)

            sleep(FRAME_T)

        self.fader_running = False

    # ---------------------
    def on_window_focus(self, ipc, e):
        """Handle focus changes."""
        if not self.active_win or self.active_win.id == e.container.id:
            return

        old, new = self.active_win, e.container

        if old.type == "con" and new.type == "con":
            self.add_fade(new, CON_INAC, CON_AC, CON_IN)
            self.add_fade(old, CON_AC, CON_INAC, CON_OUT)

        elif old.type == "con" and new.type != "con":
            self.add_fade(new, FLOAT_INAC, FLOAT_AC, FLOAT_IN)
            self.add_fade(old, CON_AC, BOT_INAC, BOT_OUT)
            self.bottom_win = old

        elif old.type != "con" and new.type == "con":
            self.add_fade(old, FLOAT_AC, FLOAT_INAC, FLOAT_BOT_OUT)
            if not self.bottom_win:
                self.add_fade(new, CON_INAC, CON_AC, CON_IN)
            elif new.id != self.bottom_win.id:
                self.add_fade(self.bottom_win, BOT_INAC, CON_INAC, BOT_SWITCH_OUT)
                self.add_fade(new, CON_INAC, CON_AC, BOT_SWITCH_IN)
                self.bottom_win = new
            else:
                self.add_fade(self.bottom_win, BOT_INAC, CON_AC, BOT_IN)

        else:
            self.add_fade(old, FLOAT_AC, FLOAT_INAC, FLOAT_OUT)
            self.add_fade(new, FLOAT_INAC, FLOAT_AC, FLOAT_IN)

        self.active_win = new

    # ---------------------
    def on_window_new(self, ipc, e):
        """Handle new window appearing."""
        if self.active_win:
            if self.active_win.type == "con":
                change_opacity(self.active_win, CON_INAC)
            else:
                change_opacity(self.active_win, FLOAT_INAC)

        if self.bottom_win:
            change_opacity(self.bottom_win, CON_INAC)
        elif self.active_win and self.active_win.type == "con":
            self.bottom_win = self.active_win
            change_opacity(self.bottom_win, CON_INAC)

        change_opacity(e.container, CON_AC)
        self.old_win = self.active_win
        self.active_win = e.container

    # ---------------------
    def on_window_floating(self, ipc, e):
        """Handle window floating toggle."""
        cid = e.container.id
        if cid not in self.floating_windows:
            self.floating_windows.add(cid)
            if self.active_win.id != cid:
                change_opacity(e.container, FLOAT_INAC)
            else:
                if self.old_win and self.bottom_win:
                    if self.old_win.type == "con":
                        self.bottom_win = self.old_win
                    change_opacity(self.bottom_win, BOT_INAC)
                change_opacity(e.container, FLOAT_AC)
        else:
            self.floating_windows.remove(cid)
            if self.active_win.id != cid:
                change_opacity(e.container, CON_INAC)
            else:
                if self.old_win and self.old_win.type == "con":
                    change_opacity(self.old_win, CON_INAC)
                change_opacity(self.active_win, CON_AC)

        self.active_win = e.container


# ======================
# Entry Point
# ======================
if __name__ == "__main__":
    Fader()

