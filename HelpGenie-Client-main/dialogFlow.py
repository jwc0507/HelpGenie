from google.cloud import dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./kt-helpgenie-mqjf-888ca127377d.json"

# 문장을 자연어 처리하여 핵심 키워드로 추출하는 함수
def detect_intent_texts(texts):
    if (texts == "" or texts is None):
        return ""
        
    # 구글 다이얼로그 플로우 프로젝트 경로
    project_id = 'kt-helpgenie-mqjf'
    session_id = '123456789'
    language_code = 'ko'
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    #print("Session path: {}\n".format(session))

    # 자연어 처리
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    
    return response.query_result.fulfillment_text
