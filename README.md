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
*   Optional startup flag for launching directly into thunderstorm mode.
*   Slow-motion mode to observe the rain and lightning in detail.
*   Optional rain and thunder sounds.
*   Customizable rain and lightning colors via command-line arguments.
*   Responsive to terminal resizing (clears and redraws).
*   Lightweight and runs in most modern terminals.

## Requirements

*   Python 3.6+
*   A terminal that supports `curses` and color attributes (most modern terminals)
*   Optional: `ffplay` from FFmpeg for sound playback

## Installation

### Using `pipx`

`pipx` installs Python command-line applications into isolated environments and makes them globally available without polluting your global Python installation or requiring manual virtual environment activation to run.

Install `pipx` first if you do not already have it:

The best way to install `pipx` on Linux is through your distribution's package manager, if available. This ensures proper system integration and updates.

Common distro installs pulled from the [pipx repo](https://github.com/pypa/pipx):

Ubuntu 23.04 or above:

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

Fedora:

```bash
sudo dnf install pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

Arch:

```bash
sudo pacman -S python-pipx
pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

Using `pip` on other distributions:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
sudo pipx ensurepath --global # optional to allow pipx actions with --global argument
```

Then install `terminal-rain-lightning` from GitHub:

```bash
pipx install git+https://github.com/rmaake1/terminal-rain-lightning.git
```

Or install it from a local clone:

```bash
git clone https://github.com/rmaake1/terminal-rain-lightning.git
cd terminal-rain-lightning
pipx install .
```

### Using the Arch AUR

On Arch-based systems with an AUR helper:

```bash
yay -S terminal-rain-lightning
```

### Using Nix

From inside a local clone:

```bash
nix-build
./result/bin/terminal-rain
```

## Usage

Once installed:

```bash
terminal-rain
```

### Controls

*   `t` or `T`: Toggle thunderstorm mode on/off.
*   `s` or `S`: Toggle slow-motion mode on/off.
*   `m` or `M`: Toggle sound on/off.
*   `q` or `Q` or `Esc`: Quit the animation.
*   `Ctrl+C`: Also quits the animation.
*   The animation will adapt if you resize your terminal window.

### Command-line Options

```bash
terminal-rain [OPTIONS]
```

*   `--rain-color COLOR`: Set the color for the rain. Default: `cyan`.
*   `--lightning-color COLOR`: Set the color for the lightning. Default: `yellow`.
*   `-t`, `--thunder`: Start in thunderstorm mode.
*   `--sound`: Enable rain and thunder sounds. Requires `ffplay` from FFmpeg.
*   `--help`: Show help text and exit.

Available color choices: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.

Examples:

```bash
terminal-rain --rain-color blue --lightning-color white
```

```bash
terminal-rain --thunder --sound
```

## Troubleshooting

### `curses.error`, Garbled Output, or Colors Not Working

* Ensure your terminal emulator fully supports curses, 256 colors, and attributes like bold/dim. Modern terminals like Alacritty or Kitty generally work well.
* Check your `TERM` environment variable. Values like `xterm-256color` are good.
* The script attempts to use default terminal colors if color changing isn't supported, but full support provides the best experience.

### Sound Not Working

* Install FFmpeg so `ffplay` is available on your PATH.
* Sound is opt-in. Start with `terminal-rain --sound` or press `m` while the animation is running.

## License

Distributed under the MIT License. See LICENSE file for more information. Do whatever you want with this script.

## Acknowledgements

Inspired by classic terminal screensavers and effects, asciiquarium, bash-pipes, etc.

Built with Python and the curses library.
