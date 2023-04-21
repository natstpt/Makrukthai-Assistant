import sys
import time
import concurrent.futures
import subprocess
import pyautogui
import cv2
import numpy as np
import re
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont


class TransparentGreenDotOverlay(QWidget):
    def __init__(self, x, y, w, h, source_square, destination_square, dot_color, score):
        super().__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.source_square = source_square
        self.destination_square = destination_square
        self.dot_color = dot_color
        self.score = score

        self.init_ui()
        self.calculate_centers()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(self.x, self.y, self.w, self.h)

    def calculate_centers(self):
        x_offset, y_offset = 56, 56
        x0, y0 = self.x + x_offset // 2, self.y + y_offset // 2

        source_x, source_y = ord(
            self.source_square[0]) - ord('a'), 8 - int(self.source_square[1])
        self.source_center_x, self.source_center_y = x0 + \
            source_x * x_offset, y0 + source_y * y_offset

        destination_x, destination_y = ord(
            self.destination_square[0]) - ord('a'), 8 - int(self.destination_square[1])
        self.destination_center_x, self.destination_center_y = x0 + \
            destination_x * x_offset, y0 + destination_y * y_offset

    def text_color_for_dot_color(self, dot_color):
        r, g, b = dot_color
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        # Black text for light colors, white text for dark colors
        return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QColor(0, 255, 0), 5, Qt.SolidLine))
        painter.drawRect(0, 0, self.w - 1, self.h - 1)

        painter.setBrush(QBrush(QColor(*self.dot_color), Qt.SolidPattern))
        dot_radius = 25

        source_dot_x = self.source_center_x - self.x - dot_radius + 20
        source_dot_y = self.source_center_y - self.y - dot_radius + 20
        destination_dot_x = self.destination_center_x - self.x - dot_radius + 20
        destination_dot_y = self.destination_center_y - self.y - dot_radius + 20

        painter.drawEllipse(source_dot_x, source_dot_y,
                            2 * dot_radius, 2 * dot_radius)
        painter.drawEllipse(destination_dot_x, destination_dot_y,
                            2 * dot_radius, 2 * dot_radius)

        source_dot_x = self.source_center_x - self.x - dot_radius + 20
        source_dot_y = self.source_center_y - self.y - dot_radius + 20
        destination_dot_x = self.destination_center_x - self.x - dot_radius + 20
        destination_dot_y = self.destination_center_y - self.y - dot_radius + 20

        text_color = self.text_color_for_dot_color(self.dot_color)
        painter.setPen(QPen(QColor(*text_color), 2, Qt.SolidLine))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(source_dot_x + dot_radius,
                         source_dot_y + dot_radius, str(self.score))
        painter.drawText(destination_dot_x + dot_radius,
                         destination_dot_y + dot_radius, str(self.score))

        painter.end()

        # Close the widget after a delay of 0.5 seconds
        QTimer.singleShot(1000, self.close)

    def mousePressEvent(self, event):
        self.close()


def main():

    start_time = time.time()

    # Define the region to capture the Makruk board
    x, y, w, h = 97, 147, 465, 465

    # Capture a screenshot of the board and save it
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot.save('makrukthaiboard.png')

    # Load the saved image and convert to grayscale
    image = cv2.imread("makrukthaiboard.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load grayscale template images of the pieces
    templates = {
        # Black pieces (lowercase)
        "s": cv2.imread("extractImages/bs.png", cv2.IMREAD_GRAYSCALE),
        "k": cv2.imread("extractImages/bk.png", cv2.IMREAD_GRAYSCALE),
        "n": cv2.imread("extractImages/bn.png", cv2.IMREAD_GRAYSCALE),
        "p": cv2.imread("extractImages/bp.png", cv2.IMREAD_GRAYSCALE),
        "m": cv2.imread("extractImages/bm.png", cv2.IMREAD_GRAYSCALE),
        "m2": cv2.imread("extractImages/bm2.png", cv2.IMREAD_GRAYSCALE),
        "r": cv2.imread("extractImages/br.png", cv2.IMREAD_GRAYSCALE),
        # White pieces (uppercase)
        "S": cv2.imread("extractImages/ws.png", cv2.IMREAD_GRAYSCALE),
        "K": cv2.imread("extractImages/wk.png", cv2.IMREAD_GRAYSCALE),
        "N": cv2.imread("extractImages/wn.png", cv2.IMREAD_GRAYSCALE),
        "P": cv2.imread("extractImages/wp.png", cv2.IMREAD_GRAYSCALE),
        "M": cv2.imread("extractImages/wm.png", cv2.IMREAD_GRAYSCALE),
        "M2": cv2.imread("extractImages/wm2.png", cv2.IMREAD_GRAYSCALE),
        "R": cv2.imread("extractImages/wr.png", cv2.IMREAD_GRAYSCALE)
    }

    # Define a threshold value for template matching
    threshold = 0.973

    # Function to match the templates of pieces on the grayscale board image
    def match_piece(name, template, gray):
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        matches = []
        for pt in zip(*loc[::-1]):
            matches.append((pt, name))
        return matches

    # Use ThreadPoolExecutor to run the match_piece function concurrently
    matches = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for name, template in templates.items():
            futures.append(executor.submit(match_piece, name, template, gray))
        for future in concurrent.futures.as_completed(futures):
            matches += future.result()

    # Initialize an empty 8x8 board and fill it with the matched pieces
    board = [['' for _ in range(8)] for _ in range(8)]

    # Update the size (px) of each board space
    template_size = 56
    border_size = 2
    space_size = template_size + border_size

    for match in matches:
        pt, name = match
        row, col = pt[1] // space_size, pt[0] // space_size
        board[row][col] = name

    # Generate the FEN string representing the board position
    fen = ''
    for row in board:
        empty = 0
        for cell in row:
            if cell == '':
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                fen += cell[0]
        if empty > 0:
            fen += str(empty)
        fen += '/'

    # Remove the trailing '/' and add 'w' to indicate it's white's turn
    fen = fen[:-1] + ' w'

    # Print the FEN string
    print("fen : ", fen)

    engine = subprocess.Popen("engine/fairy-stockfish_x86-64-bmi2.exe", universal_newlines=True,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    engine.stdin.write("setoption name UCI_Variant value makruk\n")
    engine.stdin.flush()

    engine.stdin.write("setoption name MultiPV value 3\n")
    engine.stdin.flush()

    engine.stdin.write("setoption name Threads value 4\n")
    engine.stdin.flush()

    engine.stdin.write("setoption name Hash value 1024\n")
    engine.stdin.flush()

    """ engine.stdin.write("setoption name SyzygyPath value egtb\n")
    engine.stdin.flush() """

    engine.stdin.write("setoption name Use NNUE value true\n")
    engine.stdin.flush()

    engine.stdin.write(
        "setoption name EvalFile value makruk-a8c621e24a8c.nnue\n")
    engine.stdin.flush()

    engine.stdin.write(f"position fen {fen}\n")
    engine.stdin.write("go depth 15\n")
    engine.stdin.flush()

    # Variables to store the extracted information
    multipv_moves = {}

    # Wait for the engine to respond with the suggested move
    while True:
        response = engine.stdout.readline().strip()

        # Extract multipv scores and moves
        if "multipv" in response and "score cp" in response and "pv" in response:
            move_number = int(re.search(r"multipv (\d+)", response).group(1))
            move_score = int(re.search(r"score cp (-?\d+)", response).group(1))
            move = re.search(r"(?<!multi)pv (\S+)", response).group(1)
            multipv_moves[move_number] = {"score": move_score, "move": move}

        # Stop processing output when the "bestmove" line is encountered
        if response.startswith("bestmove"):
            break

    app = QApplication(sys.argv)
    overlays = []

    for move_number, move_data in multipv_moves.items():
        print(
            f"multipv{move_number}: score cp{move_data['score']}, move {move_data['move']}")

        move = move_data['move']
        score = move_data['score']

        source_square = move[:2]
        destination_square = move[2:]

        dot_colors = {
            1: (255, 0, 0),  # Red
            2: (0, 0, 255),  # Blue
            3: (0, 255, 0)   # Green
        }
        dot_color = dot_colors.get(
            move_number, (255, 255, 255))  # Default: White

        # Prevent showing gray on titles name.
        pyautogui.click()

        overlay = TransparentGreenDotOverlay(
            x, y, w, h, source_square, destination_square, dot_color, score)
        overlays.append(overlay)
        overlay.show()

    # Prevent showing gray on titles name.
        pyautogui.click()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
