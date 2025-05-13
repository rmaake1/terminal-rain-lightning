#!/usr/bin/env python3

import curses
import time
import random
import os
import argparse # Added for command-line arguments

UPDATE_INTERVAL = 0.015 # Speed up slightly again w/o clouds/complex bolts

# --- Rain Configuration ---
RAIN_CHARS = ['|', '.', '`'] # Characters for raindrops
COLOR_PAIR_RAIN_NORMAL = 1
COLOR_PAIR_LIGHTNING = 4

# Defined curses color names (lowercase) for argument parsing
CURSES_COLOR_MAP = {
    'black': curses.COLOR_BLACK,
    'red': curses.COLOR_RED,
    'green': curses.COLOR_GREEN,
    'yellow': curses.COLOR_YELLOW,
    'blue': curses.COLOR_BLUE,
    'magenta': curses.COLOR_MAGENTA,
    'cyan': curses.COLOR_CYAN,
    'white': curses.COLOR_WHITE,
}


class Raindrop:
    def __init__(self, x, y, speed, char):
        self.x = x
        self.y = y
        self.speed = speed # How many steps to fall per update
        self.char = char

# --- Lightning ---
LIGHTNING_COLOR_ATTR = None # Will be set in setup_colors
LIGHTNING_CHANCE = 0.005 # Slightly higher chance
LIGHTNING_CHARS = ['*', '+', '#'] # Different intensity characters [dimmest -> brightest]
LIGHTNING_GROWTH_DELAY = 0.002 # Grow slightly faster
LIGHTNING_MAX_BRANCHES = 2
LIGHTNING_BRANCH_CHANCE = 0.3
FORK_CHANCE = 0.15 # Chance for a side fork to spawn during growth
FORK_HORIZONTAL_SPREAD = 3 # Max horizontal distance a fork segment can jump
SEGMENT_LIFESPAN = 0.8 # Seconds for a segment to fade from # to invisible


class LightningBolt:
    def __init__(self, start_row, start_col, max_y, max_x):
        self.start_col = start_col
        self.target_length = random.randint(max_y // 2, max_y - 2) # Random length
        # Segments store: (y, x, creation_time)
        self.segments = [(start_row, start_col, time.time())]
        self.last_growth_time = time.time() # Renamed from last_segment_time
        self.is_growing = True
        self.max_y = max_y # Store for boundary checks
        self.max_x = max_x # Store for boundary checks

    def update(self):
        """Updates bolt growth and checks if it should be removed."""
        current_time = time.time()

        # --- Growth ---
        if self.is_growing and (current_time - self.last_growth_time >= LIGHTNING_GROWTH_DELAY):
            self.last_growth_time = current_time
            new_segments_this_step = [] # Store segments added *this* step
            added_segment = False
            last_y, last_x, _ = self.segments[-1] # Ignore creation_time for position

            if len(self.segments) < self.target_length and last_y < self.max_y - 1 :
                 branches = 1
                 if random.random() < LIGHTNING_BRANCH_CHANCE:
                     branches = random.randint(1, LIGHTNING_MAX_BRANCHES + 1)

                 current_x = last_x
                 next_primary_x = current_x # Track primary path for fork check
                 for i in range(branches):
                     offset = random.randint(-2, 2)
                     next_x = max(0, min(self.max_x - 1, current_x + offset))
                     # Allow reaching bottom row (max_y - 1)
                     next_y = min(self.max_y - 1, last_y + 1)
                     # Add new segment with current time
                     new_segments_this_step.append((next_y, next_x, current_time))
                     if i == 0: next_primary_x = next_x # Store first path pos
                     current_x = next_x
                     added_segment = True

                 # --- Add Secondary Forks --- #
                 if random.random() < FORK_CHANCE:
                     fork_offset = random.randint(-FORK_HORIZONTAL_SPREAD, FORK_HORIZONTAL_SPREAD)
                     if fork_offset == 0: fork_offset = random.choice([-1, 1])
                     fork_x = max(0, min(self.max_x - 1, last_x + fork_offset))
                     # Allow fork reaching bottom row
                     fork_y = min(self.max_y - 1, last_y + 1)
                     if fork_x != next_primary_x:
                          # Add new fork segment with current time
                          new_segments_this_step.append((fork_y, fork_x, current_time))
                          added_segment = True

            # Stop growing if no new segments were added or target length reached
            # Also stop if we hit the bottom edge
            if not added_segment or len(self.segments) >= self.target_length or last_y >= self.max_y -1:
                self.is_growing = False

            # Add the newly created segments to the main list
            if new_segments_this_step:
                 # Optional: Add only unique positions added this step?
                 unique_new = list({(s[0], s[1]): s for s in new_segments_this_step}.values())
                 self.segments.extend(unique_new)


        # --- Check for Removal ---
        # Bolt should be removed if all its segments have exceeded their lifespan
        all_expired = True
        if not self.segments: # Should not happen, but safe check
            return False # Remove empty bolt

        for _, _, creation_time in self.segments:
            if (current_time - creation_time) <= SEGMENT_LIFESPAN:
                all_expired = False
                break
        # Return False if all segments are expired (signal removal)
        return not all_expired


    def draw(self, stdscr):
        """Draws segments based on their individual age."""
        current_time = time.time()
        max_char_index = len(LIGHTNING_CHARS) - 1

        for y, x, creation_time in self.segments:
            segment_age = current_time - creation_time
            is_visible = True
            char = ' ' # Default to invisible

            if segment_age <= SEGMENT_LIFESPAN:
                # Determine character based on age progress through lifespan
                # Normalize age (0.0 = new, 1.0 = lifespan reached)
                norm_age = segment_age / SEGMENT_LIFESPAN

                # Map normalized age (0->1) to char index (max->0)
                # Example mapping: 0-0.33 -> #, 0.33-0.66 -> +, 0.66-1.0 -> *
                if norm_age < 0.33:
                    char_index = 2 # '#'
                elif norm_age < 0.66:
                    char_index = 1 # '+'
                else:
                    char_index = 0 # '*'

                # Ensure index is valid (should be by logic)
                char_index = max(0, min(max_char_index, char_index))
                char = LIGHTNING_CHARS[char_index]
                is_visible = True
            else:
                is_visible = False # Segment is older than lifespan

            if not is_visible:
                continue

            # Apply attributes (always bold for now)
            attr = LIGHTNING_COLOR_ATTR

            try:
                max_r, max_c = stdscr.getmaxyx()
                if y < max_r and x < max_c:
                   stdscr.addstr(int(y), int(x), char, attr)
            except curses.error:
                pass


def setup_colors(rain_color_str='cyan', lightning_color_str='yellow'):
    """Initializes color pairs for the rain and lightning based on input strings."""
    global LIGHTNING_COLOR_ATTR
    if curses.has_colors():
        curses.start_color()
        if curses.can_change_color():
             curses.use_default_colors()
             bg = -1
        else:
             bg = curses.COLOR_BLACK # Fallback background

        # --- Get curses color constants from strings --- #
        rain_fg = CURSES_COLOR_MAP.get(rain_color_str.lower(), curses.COLOR_CYAN)
        lightning_fg = CURSES_COLOR_MAP.get(lightning_color_str.lower(), curses.COLOR_YELLOW)
        # ------------------------------------------------ #

        curses.init_pair(COLOR_PAIR_RAIN_NORMAL, rain_fg, bg)
        curses.init_pair(COLOR_PAIR_LIGHTNING, lightning_fg, bg)
        LIGHTNING_COLOR_ATTR = curses.color_pair(COLOR_PAIR_LIGHTNING) | curses.A_BOLD

        return True
    else:
        # --- Non-color fallback --- #
        # We still need LIGHTNING_COLOR_ATTR for non-color bold
        rain_fg = curses.COLOR_WHITE # Ignored, but keep variable
        lightning_fg = curses.COLOR_WHITE # Ignored, but keep variable
        bg = curses.COLOR_BLACK
        # -------------------------- #

        curses.init_pair(COLOR_PAIR_RAIN_NORMAL, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIR_LIGHTNING, curses.COLOR_WHITE, curses.COLOR_BLACK)
        LIGHTNING_COLOR_ATTR = curses.color_pair(COLOR_PAIR_LIGHTNING) | curses.A_BOLD
        return False

def simulate_rain(stdscr, rain_color_str='cyan', lightning_color_str='yellow'):
    """Main curses visualization loop for rain simulation."""
    curses.curs_set(0) # Hide cursor
    stdscr.nodelay(True) # Non-blocking input
    stdscr.timeout(1) # ms, minimal timeout

    has_colors = setup_colors(rain_color_str, lightning_color_str)
    raindrops = []
    active_bolts = [] # List of active LightningBolt objects
    rows, cols = stdscr.getmaxyx()
    is_thunderstorm = False

    last_update_time = time.time()

    while True:
        # --- Input --- #
        key = stdscr.getch()
        if key == curses.KEY_RESIZE:
             rows, cols = stdscr.getmaxyx()
             stdscr.clear()
             raindrops.clear()
             active_bolts.clear()
        elif key == ord('q') or key == ord('Q') or key == 27:
            break
        elif key == ord('t') or key == ord('T'):
            is_thunderstorm = not is_thunderstorm
            stdscr.clear()

        # --- Frame Rate Control --- #
        current_time = time.time()
        delta_time = current_time - last_update_time
        if delta_time < UPDATE_INTERVAL:
             time.sleep(UPDATE_INTERVAL - delta_time)
        last_update_time = time.time() # Use the time *after* sleep for age calcs

        # --- Update --- #

        # 1. Lightning Bolts
        next_bolts = []
        if is_thunderstorm and len(active_bolts) < 3 and random.random() < LIGHTNING_CHANCE:
             start_col = random.randint(cols // 4, 3 * cols // 4)
             start_row = random.randint(0, rows // 5)
             active_bolts.append(LightningBolt(start_row, start_col, rows, cols))

        for bolt in active_bolts:
             if bolt.update(): # update now returns True if bolt should *keep* existing
                 next_bolts.append(bolt)
        active_bolts = next_bolts

        # 2. Raindrops (generation and update)
        generation_chance = 0.5 if is_thunderstorm else 0.3
        max_new_drops = cols // 8 if is_thunderstorm else cols // 15
        min_speed = 0.3 if is_thunderstorm else 0.3
        max_speed = 1.0 if is_thunderstorm else 0.6

        if random.random() < generation_chance:
            num_new_drops = random.randint(1, max(1, max_new_drops))
            for _ in range(num_new_drops):
                 x = random.randint(0, cols - 1)
                 y = 0 # Start at top row
                 speed = random.uniform(min_speed, max_speed)
                 char = random.choice(RAIN_CHARS)
                 raindrops.append(Raindrop(x, y, speed, char))

        next_raindrops = []
        for drop in raindrops:
            drop.y += drop.speed
            if int(drop.y) < rows:
                next_raindrops.append(drop)
        raindrops = next_raindrops

        # --- Drawing --- #
        stdscr.clear()

        # 1. Lightning
        for bolt in active_bolts:
             bolt.draw(stdscr)

        # 2. Raindrops
        for drop in raindrops:
             try:
                 attr = curses.color_pair(COLOR_PAIR_RAIN_NORMAL)
                 if is_thunderstorm:
                     attr |= curses.A_BOLD
                 elif drop.speed < 0.8:
                     attr |= curses.A_DIM
                 if int(drop.y) < rows:
                    stdscr.addstr(int(drop.y), drop.x, drop.char, attr)
             except curses.error:
                 pass
                
        stdscr.noutrefresh()
        curses.doupdate()


def main():
    if not os.isatty(1) or os.environ.get('TERM') == 'dumb':
        print("Error: This script requires a TTY with curses support.")
        return

    # --- Argument Parsing --- #
    parser = argparse.ArgumentParser(description="Simulates rain and thunderstorms in the terminal.")
    valid_colors = list(CURSES_COLOR_MAP.keys())
    parser.add_argument(
        '--rain-color',
        type=str,
        default='cyan',
        choices=valid_colors,
        help=f"Color for the rain. Default: cyan. Choices: {', '.join(valid_colors)}"
    )
    parser.add_argument(
        '--lightning-color',
        type=str,
        default='yellow',
        choices=valid_colors,
        help=f"Color for the lightning. Default: yellow. Choices: {', '.join(valid_colors)}"
    )
    args = parser.parse_args()
    # ------------------------ #

    try:
        # Pass parsed colors to the main simulation function
        curses.wrapper(simulate_rain, args.rain_color, args.lightning_color)
    except curses.error as e:
        try: curses.endwin()
        except Exception: pass
        print(f"\nA curses error occurred: {e}")
        print("Terminal might not fully support curses features (like color/attributes).")
        print("Try resizing the terminal or using a different terminal emulator.")
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        try: curses.endwin()
        except Exception: pass
        print(f"\nAn unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 