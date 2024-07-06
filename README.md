# 3D MUSIC VIZ

This repository contains a 3D music visualization tool written in Python. The main file, `3D_MUSIC_VIZ.py`, is the latest version of the tool. Previous versions of the tool are included as well for reference.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The 3D Music Visualization tool is designed to create visual representations of music in three dimensions. It leverages Python libraries to process audio files and generate dynamic visual effects that sync with the music.

## Features

- Real-time 3D visualization of music.
- Multiple versions with incremental improvements and new features.
- Customizable visual effects.

## Installation

To get started with the 3D Music Visualization tool, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/3d-music-viz.git
    ```
2. Navigate to the project directory:
    ```bash
    cd 3d-music-viz
    ```
3. Install the required dependencies:
    ```bash
    pip install numpy pygame PyOpenGL scipy PyQt5
    ```

## Usage

To run the latest version of the 3D Music Visualization tool, execute the following command:

```bash
python3 3D_MUSIC_VIZ.py
```

For previous versions, replace `3D_MUSIC_VIZ.py` with the appropriate file name, such as `viz1.py`, `viz2.py`, etc.

## File Descriptions

- `viz1.py`: A blue sphere that reacts to music. Requires 2 audiofiles: a `.wav` for the viz and a `.mp3` for the playback.
- `viz2.py`: An experiment with a different visualization technique.
- `viz3.py`: Iteration over `viz1.py`. Now the viz multiple colours.
- `viz4.py`: Now opens the viz in fullscreen.
- `viz5.py`: Add the functionality to quit with the escape key.
- `3D_MUSIC_VIZ.py`: The main file containing the latest version of the 3D Music Visualization tool. Requires only 1 `.wav` audiofile that the user can select from the dialog box

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
