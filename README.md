# Terminal Rain

A Python script that creates a mesmerizing rain and lightning animation directly in your terminal using the `curses` library.

## Calm Rain
![Calm Rain](calmrain.gif)

## Thunderstorm
![Thunderstorm](thunderstorm.gif)

## Disclaimer

I'm a hobby coder and write most of my scripts with Cursor's help, apologies if anything is broken or especially wonky in the source code.

I'm relatively new to Linux and wanted to make something like this for fun after seeing some of the other projects like bash-pipes, asciiquarium, etc.

## Features

*   Smooth ASCII rain effect with varying drop characters.
*   Toggleable "Thunderstorm" mode for more intense rain and lightning.
*   Customizable rain and lightning colors via command-line arguments.
*   Responsive to terminal resizing (clears and redraws).
*   Lightweight and runs in most modern terminals.

## Requirements

*   Python 3.6+
*   A terminal that supports `curses` and color attributes (most modern terminals)

## Installation

The recommended way to install `terminal-rain-lightning` is using `pipx`. This will make the `terminal-rain` command available globally while keeping its dependencies isolated.

### Using `pipx` (Recommended)

`pipx` installs Python command-line applications into isolated environments and makes them globally available without polluting your global Python installation or requiring manual virtual environment activation to run.

1. **Install `pipx`** (if you haven't already):

The best way to install `pipx` on Linux is through your distribution's package manager, if available. This ensures proper system integration and updates.

Common distro installs pulled from the [pipx repo](https://github.com/pypa/pipx):

- Ubuntu 23.04 or above

```
sudo apt update
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

- Fedora:

```
sudo dnf install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

- Arch:

```
sudo pacman -S python-pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

- Using `pip` on other distributions:

```
python3 -m pip install --user pipx
python3 -m pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

2. **Install `terminal-rain-lightning`:**

    *   **From GitHub (directly):**
        ```bash
        pipx install git+https://github.com/rmaake1/terminal-rain-lightning.git
        ```
    *   **From a local clone:**
        ```bash
        git clone https://github.com/rmaake1/terminal-rain-lightning.git
        cd terminal-rain-lightning
        pipx install .
        ```
## Usage

Once installed:

*   If you used `pipx` simply type:
    ```bash
    terminal-rain
    ```

### Controls

*   `t` or `T`: Toggle thunderstorm mode on/off.
*   `q` or `Q` or `Esc`: Quit the animation.
*   `Ctrl+C`: Also quits the animation.
*   The animation will adapt if you resize your terminal window.

### Command-line Options

Customize the appearance of the animation:

```bash
terminal-rain [OPTIONS]
```

## Options:
* --rain-color COLOR: Set the color for the rain. Default: cyan.
* --lightning-color COLOR: Set the color for the lightning. Default: yellow.
* --help: Show this help message and exit.
* Available COLOR choices: black, red, green, yellow, blue, magenta, cyan, white.

Example:

```bash
terminal-rain --rain-color blue --lightning-color white
```

## Troubleshooting

"curses.error: ..." / Garbled Output / Colors Not Working:

* Ensure your terminal emulator fully supports curses, 256 colors, and attributes like bold/dim. Modern terminals like Alacritty or Kitty generally work well.
* Check your TERM environment variable (e.g., echo $TERM). Values like xterm-256color are good.
* The script attempts to use default terminal colors if color changing isn't supported, but full support provides the best experience.

## License

Distributed under the MIT License. See LICENSE file for more information. Do whatever you want with this script.

## Acknowledgements

Inspired by classic terminal screensavers and effects, asciiquarium, bash-pipes, etc.

Built with Python and the curses library.
