import webbrowser
import os


# 고객으로부터 받은 choice값을 바탕으로 대리점 위치 정보를 웹페이지로 전달
def openMap(loc):
    if (loc == 'incheon'):
        webbrowser.open('file://' + os.path.realpath('./Geomaster/incheon.html'))
    elif (loc == 'daejeon'):
        webbrowser.open('file://' + os.path.realpath('./Geomaster/daejeon.html'))
    elif (loc == 'kwangju'):
        webbrowser.open('file://' + os.path.realpath('./Geomaster/kwangju.html'))
