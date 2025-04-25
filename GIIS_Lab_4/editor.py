from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QToolBar, QComboBox, QCheckBox
from PyQt5.QtGui import QPainter, QPen, QImage, QColor
from PyQt5.QtCore import Qt, QTimer

from polygon import Polygon
from fill_algorithms import scanline_fill, seed_fill
from debug import log_step

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 600)
        self.image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        self.image.fill(QColor('white').rgb())
        self.polygon = Polygon()
        self.current_algo = 'scanline'
        self.debug = False
        self.fill_generator = None


        self.timer = QTimer(self)
        self.timer_interval = 100  # Задержка в откладке
        self.timer.timeout.connect(self.next_step)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.polygon.closed:
                self.image.fill(QColor('white').rgb())
                if self.timer.isActive():
                    self.timer.stop()
                self.fill_generator = None
            x, y = event.x(), event.y()
            self.polygon.add_point(x, y)
            self.update()
        elif event.button() == Qt.RightButton:
            self.polygon.close()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        pts = self.polygon.points
        if pts:
            for i in range(len(pts) - 1):
                painter.drawLine(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])
            if self.polygon.closed and len(pts) > 2:
                painter.drawLine(pts[-1][0], pts[-1][1], pts[0][0], pts[0][1])

    def draw_polygon_on_image(self):
        painter = QPainter(self.image)
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        pts = self.polygon.points
        if pts:
            for i in range(len(pts) - 1):
                painter.drawLine(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])
            if self.polygon.closed and len(pts) > 2:
                painter.drawLine(pts[-1][0], pts[-1][1], pts[0][0], pts[0][1])
        painter.end()

    def set_algorithm(self, algo_name):
        self.current_algo = algo_name

    def set_debug(self, debug_on):
        self.debug = debug_on

    def fill(self):
        if not self.polygon.closed:
            return
        self.image.fill(QColor('white').rgb())
        self.draw_polygon_on_image()
        if self.timer.isActive():
            self.timer.stop()
        if self.current_algo == 'scanline':
            gen = scanline_fill(self.polygon.points, self.image, debug=self.debug)
        else:
            gen = seed_fill(self.polygon.points, self.image, debug=self.debug)
        if self.debug:
            self.fill_generator = gen
            self.timer.start(self.timer_interval)
        else:
            for _ in gen:
                pass
            self.update()

    def next_step(self):
        if not self.fill_generator:
            return
        try:
            step_info = next(self.fill_generator)
            log_step(f"Step: {step_info}")
            self.update()
        except StopIteration:
            self.fill_generator = None
            if self.timer.isActive():
                self.timer.stop()

class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Polygon Editor")
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)

        toolbar = self.addToolBar("Algorithms")

        combo = QComboBox()
        combo.addItems(["scanline", "seed"])
        combo.currentTextChanged.connect(self.canvas.set_algorithm)
        toolbar.addWidget(combo)

        fill_act = QAction("Fill", self)
        fill_act.triggered.connect(self.canvas.fill)
        toolbar.addAction(fill_act)

        debug_chk = QCheckBox("Debug")
        debug_chk.stateChanged.connect(lambda state: self.canvas.set_debug(state == Qt.Checked))
        toolbar.addWidget(debug_chk)