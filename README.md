# Makruk Assistant

Makruk Assistant is a Python application that helps users analyze Makruk (Thai Chess) positions by suggesting the best moves using the Fairy-Stockfish chess engine. It captures a screenshot of the Makruk board, detects the pieces, and displays the suggested moves as transparent colored dots on the board.

## Features

- Captures a screenshot of the Makruk board.
- Detects the pieces on the board using OpenCV and template matching.
- Generates a FEN (Forsyth-Edwards Notation) string representing the board position.
- Passes the FEN string to the Fairy-Stockfish chess engine to get the best moves.
- Displays the suggested moves as transparent colored dots on the board using PyQt5.

## Prerequisites

To use the Makruk Assistant, you need to have the following installed:

- Python 3.9 or higher
- PyQt5
- pyautogui
- OpenCV

Additionally, you will need:

- Fairy-Stockfish chess engine
- Grayscale template images of the Makruk pieces
- NNUE evaluation file for Makruk

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
