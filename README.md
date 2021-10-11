# py-cellular-automata

This project started life sometime in 2018 or 2019 as a way to explore Python, tkinter and Conway's Game of Life.
It expanded a bit to allow for other rulesets for cellular automata besides game of life, as well as colors that would change based on the lifetime of a cell for interesting visualizations. It underwent a very large refactor in 2021 to try and despaghettify the code.

![image](https://user-images.githubusercontent.com/45133114/133729513-750e3b43-0861-4eaf-8cf0-4c15d5fd9e68.png)

To run, clone the repository and ensure that your Python 3.8+ distribution has tkinter. From the top-level project directory, run `python3 -m app`

To achieve interesting mandala-like effects, ensure that '1' is selected in the birth rules, and place symmetrical pixels. When run, the result should stay symmetrical, and the rules can be changed and pixels added or subtracted to create interesting effects.
