#########################
#### 메인 프로그램 파일 ####
#########################
import userInterface as ui
import sys


def initService():
    # UI 화면 출력
    app = ui.QtWidgets.QApplication([""])
    window = ui.MainWindow()
    window.show()
    sys.exit(app.exec_())
    

def main():
    initService()


if __name__ == '__main__':
    main()
