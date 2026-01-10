import sys
import random
from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLineEdit, 
    QLabel, 
    QVBoxLayout, 
    QSpacerItem, 
    QSizePolicy,
    QFrame,
    QTextEdit,
    QGraphicsOpacityEffect
)
from PySide6.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    QEvent
)

from PySide6.QtGui import (
    QTextOption
)

words = [
    "apple", "table", "chair", "light", "phone", "screen", "paper", "book", "house", "window",
    "floor", "car", "road", "bridge", "cloud", "river", "ocean", "mountain", "tree", "garden",
    "field", "school", "student", "teacher", "class", "pencil", "notebook", "ruler", "desk", "bottle",
    "cup", "plate", "fork", "spoon", "knife", "meal", "bread", "cheese", "butter", "sugar", "salt",
    "pepper", "coffee", "tea", "juice", "water", "milk", "soda", "clock", "watch", "mirror", "jacket",
    "shirt", "pants", "shoes", "socks", "hat", "glove", "belt", "bag", "wallet", "coin", "key",
    "lock", "door", "handle", "box", "shelf", "frame", "wall", "ceiling", "roof", "fence", "yard",
    "path", "sign", "letter", "word", "number", "page", "list", "photo", "map", "card", "file",
    "code", "cable", "wire", "button", "switch", "case", "cover", "blanket", "pillow", "bed", "lamp",
    "sofa", "carpet", "basket", "gift", "candle", "soap", "towel", "comb", "brush", "razor", "nail",
    "hammer", "tool", "chain", "ring", "stone", "shell", "feather", "seed", "leaf", "branch", "trunk",
    "root", "dust", "fire", "smoke", "spark", "shadow", "noise", "sound", "voice", "whisper", "echo",
    "laugh", "tear", "smile", "dream", "hope", "fear", "doubt", "truth", "lie", "idea", "fact",
    "rule", "law", "right", "wrong", "chance", "risk", "point", "goal", "game", "match", "player",
    "team", "sport", "music", "song", "tune", "beat", "rhythm", "movie", "scene", "actor", "artist",
    "story", "book", "poem", "note", "letter", "symbol", "signal", "plan", "step", "move", "turn",
    "end", "start", "moment", "reason", "cause", "effect", "result", "meaning", "purpose", "thought"

]

def create_target(word_list):
    random.shuffle(word_list)
    words_string = " ".join(word_list)
    return words_string

class WPMApp(QWidget):
    def __init__(self):

        # time
        self.TIME = 30

        # initialize variables for line movement
        self.space = 0 # number of times user presses space
        self.line_count = 0 # number of lines user has completed

        self.original_text = create_target(words) # shuffle words

        # window properties
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setWindowTitle("WPMApp")
        self.setFixedSize(800, 500)
        self.setStyleSheet("background-color: #F8F3F2")

        # text box properties
        self.text_input = NoFocusLineEdit(self)
        self.text_input.textChanged.connect(self.user_text)
        self.text_input.installEventFilter(self)
        self.text_input.setMinimumSize(1, 1)
        self.text_input.setStyleSheet("""
            background: transparent;
            border: none;
            color: transparent;
            caret-color: transparent;
            selection-background-color: transparent;
        """)

        # target text properties
        self.target = NoScrollTextEdit(self)
        self.target.setText(f"<span style='color: #71756C;'>{self.original_text}</span>")
        self.target.setAlignment(Qt.AlignLeft)
        self.target.setWordWrapMode(QTextOption.WordWrap)
        self.target.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.target.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.target.setTextInteractionFlags(Qt.NoTextInteraction)
        self.target.setTextInteractionFlags(Qt.TextSelectableByMouse) 
        self.target.setReadOnly(True)
        self.target.move(15, 180)
        self.target.setFixedSize(770, 115)
        self.target.setStyleSheet("""
            font-family: Menlo, monospace; 
            font-size: 30px;
            letter-spacing: 0.05em;
            font-weight: normal;
            border: transparent;
        """)

        # text cover 1 properties 
        self.text_cover_1 = QFrame(self)
        self.text_cover_1.setFixedSize(800, 100)
        self.text_cover_1.move(0, 86) # cover any chars on the top that might show
        self.text_cover_1.setStyleSheet("""
            background-color: #F8F3F2;
        """)

        # text cover 2 properties 
        self.text_cover_2 = QFrame(self)
        self.text_cover_2.setFixedSize(800, 100)
        self.text_cover_2.move(0, 290) # cover any chars on the bottom that might show
        self.text_cover_2.setStyleSheet("""
            background-color: #F8F3F2;
        """)

        # text cover 3 properties
        self.text_cover_3 = QFrame(self)
        self.text_cover_3.setFixedSize(800, 600)
        self.text_cover_3.hide()
        self.text_cover_3.setStyleSheet("""
            background-color: #F8F3F2;
        """)

        ### count down
        # timer properties
        self.started = False
        self.timer = QTimer(self)
        self.remaining_time = self.TIME
        self.timer.timeout.connect(self.handle_timer)

        # countdown text properties
        self.countdown = QLabel(self)
        self.countdown.setText(f"<span style='color: #294551;'>{self.remaining_time}s</span>")
        self.countdown.setAlignment(Qt.AlignCenter)
        self.countdown.setStyleSheet("""
            font-family: Menlo, monospace;
            font-size: 50px;
            font-weight: 900;
            background: transparent;
        """)
    

        ### "begin typing" prompt
        # start text
        self.start_text = QLabel(self)
        self.start_text.setFixedSize(500, 100)
        self.start_text.setAlignment(Qt.AlignCenter)
        self.start_text.move(150, 290)
        self.start_text.setText(f"<span style='color: #294551;'>begin typing to start...</span><br><span style='color:rgba(41, 69, 81, 0.23); font-size: 15px;'>press (shift) to shuffle words</span>")
        self.start_text.setStyleSheet("""
            font-family: Menlo, monospace;
            font-size: 30px;
            background-color: rgba(0, 0, 0, 0);
        """)

        ### metrics display properties
        # WPM text
        self.user_WPM = 0 # initialize global WPM
        self.WPM = QLabel(self)
        self.WPM.setFixedSize(300, 100)
        self.WPM.hide()
        self.WPM.setStyleSheet("""
            font-family: Menlo, monospace;
            font-size: 35px;
            font-weight: 650;
            background-color rgba(0, 0, 0, 0);
        """)

        # accuracy % text
        self.user_accuracy = 0
        self.accuracy = QLabel(self)
        self.accuracy.setFixedSize(300, 100)
        self.accuracy.hide()
        self.accuracy.setStyleSheet("""
            font-family: Menlo, monospace;
            font-size: 35px;
            font-weight: 650;
            background-color: rgba(0, 0, 0, 0);
        """)

        # correct char information
        self.user_char_info = QLabel(self)
        self.user_char_info.setFixedSize(350, 100)
        self.user_char_info.hide()
        self.user_char_info.setStyleSheet("""
            font-family: Menlo, monospace;
            font-size: 35px;
            font-weight: 650;
            background-color: rgba(0, 0, 0, 0);
        """)

        # correct word information
        self.user_word_info = QLabel(self)
        self.user_word_info.setFixedSize(350, 100)
        self.user_word_info.hide()
        self.user_word_info.setStyleSheet("""
            font-family: Menlo, monospace;
            font-size: 35px;
            font-weight: 650;
            background-color: rgba(0, 0, 0, 0);
        """)

        # start again text properties
        self.restart = QLabel(self)
        self.restart.setFixedSize(600, 100)
        self.restart.setAlignment(Qt.AlignCenter)
        self.restart.hide()
        self.restart.setStyleSheet("""
            font-family: Menlo, monospace;
            font-size: 30px;
            background-color: rgba(0, 0, 0, 0);
        """)

        # layout properties
        layout = QVBoxLayout()
        layout.addWidget(self.countdown)
        layout.addItem(QSpacerItem(50, 800, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.text_input)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(15, 50, 20, 0)
        self.setLayout(layout)

    def fade_out_start_text(self):
        self.fade_effect = QGraphicsOpacityEffect()
        self.start_text.setGraphicsEffect(self.fade_effect)
        self.fade_effect.setOpacity(1)
        self.start_text.show()

        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.finished.connect(self.start_text.hide)
        self.fade_animation.start()

    def fade_in_start_text(self):
        self.start_text.show()
        fade_effect = QGraphicsOpacityEffect(self)
        self.start_text.setGraphicsEffect(fade_effect)
        fade_effect.setOpacity(0)

        animation = QPropertyAnimation(fade_effect, b"opacity", self)
        animation.setDuration(500)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)

        animation.start() 

    def show_user_metrics(self):
        correct_words = self.original_text.split(" ")
        correct_char = 0
        total_char = 0
        correct_w = 0
        total_w = 0
        total_extra = 0

        ### calculate
        # count correct words and chars
        for i in range(len(self.typed_words)):
            if i >= len(correct_words): # prevent out of bounds error
                break  
            # count extra chars
            if len(self.typed_words[i]) > len(correct_words[i]):
                total_extra = total_extra + (len(self.typed_words[i]) - len(correct_words[i]))
            # count correct words
            if self.typed_words[i] == correct_words[i]:
                correct_w = correct_w + 1
            total_w = total_w + 1
            # count correct chars
            for j in range(min(len(self.typed_words[i]), len(correct_words[i]))):
                if self.typed_words[i][j] == correct_words[i][j]:
                    correct_char = correct_char + 1
                total_char = total_char + 1
        
        ### display
        # WPM
            self.user_WPM = (correct_char / 5) * (60 / self.TIME)
            self.user_WPM = round(self.user_WPM, 1)
            self.WPM.setText(f"<span style='color: #294551;'>wpm:</span><br><span style='color: #71756C; font-size: 24px;'>{self.user_WPM}</span>")
            self.WPM.move(150,120)

            # accuracy %
            self.user_accuracy = (correct_char / total_char) * 100
            self.user_accuracy = round(self.user_accuracy, 1)
            self.accuracy.setText(f"<span style='color: #294551;'>accuracy:</span><br><span style='color: #71756C; font-size: 24px;'>{self.user_accuracy}%</span>")
            self.accuracy.move(415, 120)

            # word info
            self.user_word_info.setText(f"<span style='color: #294551;'>words:</span><br><span style='color: #71756C; font-size: 20px;'>{correct_w} corr./{total_w} att.</span>")
            self.user_word_info.move(150, 250)

            # char info
            self.user_char_info.setText(f"<span style='color: #294551;'>characters:</span><br><span style='color: #71756C; font-size: 20px;'>{correct_char} corr./{total_char} att./{total_extra} xtra.</span>")
            self.user_char_info.move(415, 250)

            # restart message
            self.restart.setText(f"<span style='color: #131B23;'>press (shift) to go again...</span>")
            self.restart.move(100, 350)
            
            # show all (except self.restart)
            self.accuracy.show()
            self.user_word_info.show()
            self.user_char_info.show()
            self.WPM.show()

            QTimer.singleShot(500, lambda: self.text_input.setDisabled(False))
            QTimer.singleShot(1000, lambda: self.text_input.setDisabled(False))

            # handle animation
            self.fade_group = QParallelAnimationGroup()
            for label in [self.WPM, self.accuracy, self.user_word_info, self.user_char_info]:
                fade_effect = QGraphicsOpacityEffect(self)
                label.setGraphicsEffect(fade_effect)
                fade_effect.setOpacity(0)

                animation = QPropertyAnimation(fade_effect, b"opacity", self)
                animation.setDuration(600)
                animation.setStartValue(0)
                animation.setEndValue(1)
                animation.setEasingCurve(QEasingCurve.InOutQuad)

                self.fade_group.addAnimation(animation)
            
            self.fade_group.start()

            # handle restart message animation
            self.fade_group.finished.connect(self.fade_in_restart_message())

    def fade_in_restart_message(self):
        self.restart.show()

        fade_effect = QGraphicsOpacityEffect(self)
        self.restart.setGraphicsEffect(fade_effect)
        fade_effect.setOpacity(0)

        animation = QPropertyAnimation(fade_effect, b"opacity", self)
        animation.setDuration(5000)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)

        animation.start()


    def fade_out_cover_text_3(self):
        self.fade_effect = QGraphicsOpacityEffect()
        self.text_cover_3.setGraphicsEffect(self.fade_effect)
        self.text_cover_3.setWindowOpacity(0)
        self.text_cover_3.show()
        self.text_cover_3.move(0, 105)

        self.fade_animation = QPropertyAnimation(self.fade_effect, b"opacity")
        self.fade_animation.setDuration(1000)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.start()

    # function to update timer
    def handle_timer(self):
        if not self.started:  
            self.timer.stop()  # kill timer if reset happened
            return

        if self.remaining_time > 5:
            self.remaining_time = self.remaining_time - 0.1
            remaining_string = f"{self.remaining_time:.0f}" 
            self.countdown.setText(f"<span style='color: #294551;'>{remaining_string}s</span>")
        elif self.remaining_time > 0.1:
            self.remaining_time = self.remaining_time - 0.1
            remaining_string = f"{self.remaining_time:.1f}"
            self.countdown.setText(f"<span style='color: #294551;'>{remaining_string}s</span>")
        else:
            self.countdown.setText(f"<span style='color: #294551;'>time's up.</span>")
            self.timer.stop()

            if not self.started:
                return

            self.text_input.setDisabled(True) # stop user from typing
    
            # fade text out
            self.fade_out_cover_text_3()
        

            ### calculate and show user's typing metrics
            self.show_user_metrics()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.restart_test()
        

    def mousePressEvent(self, event):
        ### force focus back to text_input to avoid mouse actions not allowing user to type
        self.text_input.setFocus()
        event.accept()

    def get_words_per_line(self):
        document = self.target.document()
        words_per_line = []

        for i in range(document.blockCount()): # i = block index
            block = document.findBlockByNumber(i)
            layout = block.layout()

            if layout:
                for j in range(layout.lineCount()): # j = line index
                    line = layout.lineAt(j)
                    text = block.text()[line.textStart(): line.textStart() + line.textLength()]
                    words = text.split()
                    words_per_line.append(len(words))

        return words_per_line
    
    def restart_test(self):
        self.started = False
        self.space = 0
        self.line_count = 0
        self.remaining_time = self.TIME
        self.original_text = create_target(words)
        self.typed_words = []

        self.text_input.setDisabled(False)
        self.text_input.setReadOnly(False)
        self.text_input.clear()

        self.text_input.clear()
        self.countdown.setText(f"<span style='color: #294551;'>{self.remaining_time}s</span>")
        self.target.setText(f"<span style='color: #71756C;'>{self.original_text}</span>")
        self.restart.hide()
        self.WPM.hide()
        self.accuracy.hide()
        self.user_word_info.hide()
        self.user_char_info.hide()
        self.text_cover_3.hide()
        self.timer.stop()
        self.fade_in_start_text()

        self.activateWindow()
        self.raise_()

        self.text_input.removeEventFilter(self)
        self.text_input.installEventFilter(self)
        QApplication.processEvents()

        # bug fix: enforce focus for on restart to allow user to type
        QTimer.singleShot(0, lambda: self.text_input.setFocus())
        QTimer.singleShot(100, lambda: self.text_input.setFocus())
        QTimer.singleShot(500, lambda: self.text_input.setFocus())

        QTimer.singleShot(500, lambda: self.user_text(self.text_input.text()))

    # handle scrolling animation
    def adjust_scroll(self):
        font_metrics = self.target.fontMetrics()
        line_height = font_metrics.height()
        new_scroll_value = (self.line_count - 1) * line_height # adjust scroll value according to the line the user is on

        # handle animation
        self.scroll_animation = QPropertyAnimation(self.target.verticalScrollBar(), b"value")
        self.scroll_animation.setDuration(250) # 250 mili seconds to complete
        self.scroll_animation.setStartValue(self.target.verticalScrollBar().value()) # start value = current pos of scrollbar
        self.scroll_animation.setEndValue(new_scroll_value) 
        self.scroll_animation.setEasingCurve(QEasingCurve.InOutQuad) 
        self.scroll_animation.start()

    # function to build string with correct colors/underlines according to user typing correctness and show it
    def user_text(self, typed_text):

        if not typed_text:
            return

        # save scroll bar pos
        saved_scrollbar = self.target.verticalScrollBar().value()

        
        # start timer when user begins typing
        if self.started == False and typed_text != "":
            self.timer.start(100) # tick every milisecond
            self.started = True
            self.fade_out_start_text()

        self.typed_words = typed_text.split(" ") # array of words user has typed
        correct_words = self.original_text.split(" ") # array of correct words

        words_per_line = self.get_words_per_line() # contains an array of num of words per line

        if len(self.typed_words) > 0 and self.typed_words[-1] == "": # user presses space
            self.typed_words.pop()
            current_word_index = None  # indicate that user is inbetween words
        else: # user is on a char
            current_word_index = len(self.typed_words) - 1 # set word index

        formatted_html = ""
        # iterate over each word
        for i in range(len(correct_words)): # i == index of word
            if i < len(self.typed_words):

                user_word = self.typed_words[i] # current word the user is on
                correct_word = correct_words[i] # correct spelling of the current word
                
                # iterate over each char of each word
                for j in range(len(correct_word)): # j = index of char
                    # check chars on that the user has typed so far
                    if j < len(user_word):
                        if user_word[j] == correct_word[j]:
                            # user typed correct char
                            formatted_html = formatted_html + "<span style='color: #131B23;'>" + correct_word[j] + "</span>"
                        else:
                            # user typed incorrect char
                            formatted_html = formatted_html + "<span style='color:#D64550;'>" + correct_word[j] + "</span>"
                    # handle chars the user has not yet typed
                    else:
                        # build remaining chars when user pressed space early
                        if current_word_index is None or i < current_word_index:
                            formatted_html = formatted_html + "<span style='color:#D64550;'>" + correct_word[j] + "</span>"
                        # build remaining chars of current word that user has not yet
                        else:
                            # handle underline on next char to type
                            if j == len(user_word) and i == current_word_index:
                                formatted_html = formatted_html + f"<u><span style='color: #71756C;'>{correct_word[j]}</span></u>"
                            else:
                                # build rest of chars on current word
                                formatted_html = formatted_html + f"<span style='color: #71756C;'>{correct_word[j]}</span>"
                
                # add extra chars if any
                if len(user_word) > len(correct_word):
                    extra_chars = user_word[len(correct_word):] # chars in an index longer than the correct word
                    formatted_html = formatted_html + "<span style='color:#751A21;'>" + extra_chars + "</span>"
                    if i == current_word_index:
                        # handle underline after extra chars
                        formatted_html = formatted_html + "<u><span style='color: #71756C;'> </span></u>"
                    else:
                        formatted_html = formatted_html + " "
                            
            else:
                # display remaining words user hasn't attempted yet in grey
                for j in range(len(correct_words[i])): # j == index of char
                    if i == len(self.typed_words) and j == 0 and current_word_index is None:
                        # handle underline on first char of next word after user presses space
                        formatted_html = formatted_html + "<u><span style='color:#71756C;'>" + correct_words[i][j] + "</span></u>"
                    else:
                        # make rest of words grey
                        formatted_html = formatted_html + "<span style='color:#71756C;'>" + correct_words[i][j] + "</span>"

            # handle underlines inbetween words
            if i < len(correct_words) - 1:
                if current_word_index is not None and len(self.typed_words[current_word_index]) == len(correct_words[current_word_index]) and i == len(self.typed_words) - 1:
                    formatted_html = formatted_html + "<u><span style='color: #71756C;'> </span></u>"
                else:
                    formatted_html = formatted_html + " "

        # set text
        self.target.setText(formatted_html)

        # maintain scroll value
        QTimer.singleShot(0, lambda: self.target.verticalScrollBar().setValue(saved_scrollbar))

        # detect when user has completed a line and scroll
        total_words_so_far = sum(words_per_line[:self.line_count + 1]) # num words on current line + all previous lines if any
        if current_word_index is None and len(self.typed_words) == total_words_so_far:
                self.line_count = self.line_count + 1
                # wait until after first line to scroll
                if self.line_count > 1:
                    QTimer.singleShot(0, self.adjust_scroll)
        # scroll when extra characters make word long enough to move to next line
        elif len(self.typed_words) > total_words_so_far:
            self.line_count = self.line_count + 1
            if self.line_count > 1:
                QTimer.singleShot(0, self.adjust_scroll)

    # bug fix: prevent user from breaking things
    def eventFilter(self, obj, event):
        # block these keys
        if obj == self.text_input and event.type() == QEvent.KeyPress:
            blocked_keys = {Qt.Key_Tab, Qt.Key_Backtab, Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right}
            if event.key() in blocked_keys:
                return True

        return super().eventFilter(obj, event)


# bug fix: custom class for QTextEdit to prevent user from breaking things
class NoScrollTextEdit(QTextEdit):
    # prevent user manual scrolling
    def keyPressEvent(self, event):
        blocked_keys = {
            Qt.Key_Tab, Qt.Key_Backtab, 
            Qt.Key_Up
            , Qt.Key_Down, Qt.Key_Left, 
            Qt.Key_Right, Qt.Key_Space
        }
        if event.key() in blocked_keys:
            event.ignore()
            return
        super().keyPressEvent(event)
    
    ### ignore all user mouse actions
    def mousePressEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()


# bug fix: custom class for QLineEdit to prevent user from breaking things
class NoFocusLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        blocked_keys = {
            Qt.Key_Tab, Qt.Key_Backtab,
            Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right
        }
        if event.key() in blocked_keys:
            event.ignore()
            return
        super().keyPressEvent(event)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WPMApp()
    window.show()
    sys.exit(app.exec_())
