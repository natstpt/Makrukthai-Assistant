# Makrukthai Assistant
![Makrukthai Assistant Screenshot](https://raw.githubusercontent.com/natstpt/Makrukthai-Assistant/main/screencapture3.png)

Makrukthai Assistant is a Python application that helps users analyze Makrukthai (Thai Chess) positions by suggesting the best moves using the Fairy-Stockfish chess engine. It captures a screenshot of the Makrukthai board, detects the pieces, and displays the suggested moves as transparent colored dots on the board.

## Features

- Captures a screenshot of the Makrukthai board.
- Detects the pieces on the board using OpenCV and template matching.
- Generates a FEN (Forsyth-Edwards Notation) string representing the board position.
- Passes the FEN string to the Fairy-Stockfish chess engine to get the best moves.
- Displays the suggested moves as transparent colored dots on the board using PyQt5.

## Prerequisites

To use the Makrukthai Assistant, you need to have the following installed:

- Python 3.9.13 or newer
- PyQt5
- pyautogui
- OpenCV

Additionally, you will need:

- Fairy-Stockfish chess variant engine: [Download](https://github.com/ianfab/Fairy-Stockfish) store in engine directory
- Template images of the Makrukthai pieces: from [PlayOK](https://www.playok.com/th/makruk/).

## Installation

1. Clone the repository or download the source code.
2. Navigate to the project directory.

```bash
cd makruk-assistant
```

3. Install the required Python packages.

```bash
pip install -r requirements.txt
```

4. Place the Fairy-Stockfish chess engine, grayscale template images, and NNUE evaluation file in the appropriate directories within the project.

## Usage

1. Make sure the paths to the Fairy-Stockfish chess engine, template images, and NNUE evaluation file are correct in the script.

2. Run the script.

```bash
python makruk_assistant_white.py
```

or

```bash
python makruk_assistant_black.py
```

3. The script will capture the Makruk board, detect the pieces, and display the suggested moves as transparent colored dots on the board.

## Contributing

Contributions are welcome! If you have any ideas or suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

I would like to express our gratitude to the following resources:

1. **Pieces image**: The piece images used in this project are sourced from [PlayOK](https://www.playok.com/th/makruk/).
2. **Chess Variant Engine**: This project utilizes the [Fairy Stockfish](https://github.com/ianfab/Fairy-Stockfish) engine, a powerful and highly configurable chess variant engine developed by Fabian Fichter. I would like to express our gratitude to Fabian and the entire Fairy Stockfish community for their incredible work and for making this project possible.
