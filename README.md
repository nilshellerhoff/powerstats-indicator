# powerstats-indicator
The battery indicator on Gnome3 seems to be broken when using a laptop with two separate batteries (i.e. it shows remaining time calculated only on one of the batteries). This is an alternative battery indicator.

It shows the battery percentage, status (charging, discharging or idle) and the remaining time until empty or full respectively. When the menu is opened, the current power consumption is shown.

![Indicator](https://github.com/nilshellerhoff/powerstats-indicator/blob/master/indicator.png)
![Indicator menu](https://github.com/nilshellerhoff/powerstats-indicator/blob/master/indicator-menu.png)

## Dependencies
Install `python-appindicator`, `libappindicator3-1` and `gir1.2-appindicator3-0.1` packages.

## How to use
Clone the repository and run `python powerstats.py` (or make the `powerstats.py` executable with `chmod +x powerstats.py` and execute with `./powerstats.py`)
