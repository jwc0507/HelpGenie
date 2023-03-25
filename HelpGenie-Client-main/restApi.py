import requests


# upload / num

# 수어 녹화 영상을 서버로 업로드하는 함수
def uploadVideo(filename, division_str):  # 파일명, AI 모델 구분 인자값(행동, 숫자)
    url = 'http://49.247.212.224:8000/' + division_str + '/'
    video = open(('./' + filename), 'rb')

    upload = {'document': video}

    res = requests.post(url, files=upload)

    print(res)
    data = res.content
    print("받은 데이터:{}".format(data))
    result_data = data.decode('utf-8')
    print("해석된 데이터:{}".format(result_data))

    video.close()
    return result_data
