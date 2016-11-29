from PyQt5.QtCore import Qt, pyqtSignal, QObject, QRect
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QDesktopWidget, QWidget,
                             QApplication,  QHBoxLayout, QLabel, QStackedLayout,
                             QVBoxLayout, )
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QCursor
import hearing_tests
import synthesizers

class Communicate(QObject):
    closeApp = pyqtSignal()

class MeiosteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.answer_active = False
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.main_menu_widget)
        self.z_test_widget = None
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        self.resize(self.sizeHint())
        self.soloud_handle = synthesizers.soloud_init()

    def initUI(self):
        y = 250
        x = 430

        self.c = Communicate()
        self.c.closeApp.connect(self.close)


        btn1 = QPushButton("Start session")
        btn1.move(50, y-50)

        btn2 = QPushButton("Progress")
        btn2.move(165, y-50)

        btn3 = QPushButton("Exit")
        btn3.move(280, y-50)

        btn1.clicked.connect(self.z_test)
        btn2.clicked.connect(self.buttonClicked)
        btn3.clicked.connect(self.exitWindow)

        self.main_menu_layout = QVBoxLayout()
        r = QRect(50, 50, x, y)
        self.main_menu_layout.setGeometry(r)
        self.main_menu_layout.addWidget(btn1)
        self.main_menu_layout.addWidget(btn2)
        self.main_menu_layout.addWidget(btn3)

        pixmap = QPixmap("logo.png")
        pixmap = pixmap.scaledToHeight(75)
        logo = QLabel()
        logo.setPixmap(pixmap)
        self.main_menu_layout.addWidget(logo)
        logo.setGeometry(20, 0, x, y)

        self.center()
        self.main_menu_widget = QWidget()
        self.main_menu_widget.setLayout(self.main_menu_layout)
        self.setWindowTitle('Meoiste')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def create_z_test_layout(self):
        if self.z_test_widget != None:
            print("Exists")
            return False
        x = 500
        y = 600
        btn1 = QPushButton("Replay sound")
        btn1.move(50, y - 50)
        btn1.setMaximumWidth(100)

        btn2 = QPushButton("Back")
        btn2.move(165, y - 50)
        btn2.setMaximumWidth(100)

        btn3 = QPushButton("Exit")
        btn3.move(280, y - 50)
        btn3.setMaximumWidth(100)

        btn1.clicked.connect(self.replay_sound)
        btn2.clicked.connect(self.go_back)
        btn3.clicked.connect(self.exitWindow)

        self.canvas = QLabel()
        self.paint_base()
        self.canvas.setGeometry(100, 100, 400-1, 400-1)
        self.canvas.mouseReleaseEvent = self.handleClick

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn1)
        button_layout.addWidget(btn2)
        button_layout.addWidget(btn3)
        self.z_test_layout = QVBoxLayout()

        self.z_test_layout.addWidget(self.canvas)
        self.z_test_layout.addStretch()
        self.z_test_layout.addLayout(button_layout)

        self.z_test_widget = QWidget()
        self.z_test_widget.setLayout(self.z_test_layout)
        return True

    def handleClick(self, event):
        if self.answer_active:
            self.answer_active = False
            self.z_test()
        else:
            predicted = [event.pos().x(), event.pos().y()]
            score = hearing_tests.get_z_score(predicted=predicted, actual=self.sound_source_cords)
            self.paint_sound_source()
            print(event.pos().x(), event.pos().y())

    def paint_base(self):
        pixmap = QPixmap(399, 399)
        pixmap.fill(QColor("transparent"))
        qp = QPainter(pixmap)
        brush = QBrush(Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, 399, 399)
        qp.setPen(QColor(168, 34, 3))
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(QColor(168, 34, 3))
        qp.setBrush(brush)
        qp.drawEllipse(200, 200, 5, 5)
        qp.end()
        self.canvas.setPixmap(pixmap)

    def paint_sound_source(self):
        qp = QPainter(self.canvas.pixmap())
        brush = QBrush(Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.setPen(QColor(38, 32, 3))
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(QColor(168, 34, 3))
        qp.setBrush(brush)
        print(self.sound_source_cords)
        qp.drawEllipse(self.sound_source_cords[0],self.sound_source_cords[1],10,10)
        qp.end()
        self.canvas.update()
        self.answer_active = True

    def replay_sound(self):
        x, y, z = self.sound_source_cords[0], self.sound_source_cords[1], self.sound_source_cords[2]
        synthesizers.play_sound(self.soloud_handle, x, y, z)

    def go_back(self):
        self.stacked_layout.setCurrentIndex(0)
        self.resize(self.sizeHint())

    def z_test(self):
        if self.create_z_test_layout():
            self.stacked_layout.addWidget(self.z_test_widget)
        self.paint_base()
        self.stacked_layout.setCurrentIndex(1)
        x, y, z = hearing_tests.random_z_test(one_shot=True)
        print (x,y,z)
        self.sound_source_cords = [200+200*x, 200+200*y, z]
        synthesizers.play_sound(self.soloud_handle, x, y, z)



        #self.resize(630, 630)

    def exitWindow(self):
        self.c.closeApp.emit()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')
        self.statusBar()