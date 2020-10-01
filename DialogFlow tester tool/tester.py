import os
import dialogflow_v2 as dialogflow
p1 = 'actions-codelab-5c540-6fb7bb165562.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = p1
session_client = dialogflow.SessionsClient()

project_id = 'actions-codelab-5c540'
session_id = '987654321'
session = session_client.session_path(project_id, session_id)
print('Session path: {}\n'.format(session))

def detect_intent_texts(project_id, session_id, item, texts, language_code, verbose=0):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    failed_counter = 0

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        if verbose == 1:
            print('=' * 40)
            print('Query text: {}'.format(response.query_result.query_text))
            print('Detected intent: {} (confidence: {})'.format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence))
         print('=' * 20)
         print(response.query_result.intent.display_name)
         print(item)

         print('=' * 20)
        if response.query_result.intent.display_name != item:
            print("FAILED: ",text)
            failed_counter = failed_counter + 1
            

    return(failed_counter)


with open('test.csv') as fp:
    for line in fp:
        line=line.replace("\"","")
        items = line.split(',')
        items[0]=items[0].replace(" ","")
        print(items[0])
        # print(items[1].split('|'))
        inputs = items[1].split('|')
        print("Failed count: ",detect_intent_texts(project_id,session_id, items[0], inputs, 'en-US',verbose=1))
        print("*"*50)
        print("\n")




# def detect_intent_texts(project_id, session_id, texts, language_code, verbose=0):
#     """Returns the result of detect intent with texts as inputs.

#     Using the same `session_id` between requests allows continuation
#     of the conversation."""
#     failed_counter = 0

#     # for text in texts:
#     text_input = dialogflow.types.TextInput(text=texts, language_code=language_code)

#     query_input = dialogflow.types.QueryInput(text=text_input)
#     response = session_client.detect_intent(session=session, query_input=query_input)
#     if verbose == 1:
#         print('=' * 20)
#         print('Query text: {}'.format(response.query_result.query_text))
#         print('Detected intent: {} (confidence: {})'.format(
#             response.query_result.intent.display_name,
#             response.query_result.intent_detection_confidence))
#     if (response.query_result.intent.display_name != item):
#         print("FAILED: ",texts)
#         failed_counter = failed_counter + 1
#     return(failed_counter)


# with open('../questions_refine/questions_refined.txt') as fp:
#     lines=fp.readlines()
#     for line in lines:
#         #items = line.split(',')
#         # print(items[0])
#         #print(items[1].split('|'))
#         # inputs = items[1].split('|')
#         print("Failed count: ",detect_intent_texts(project_id,session_id,line, 'en-US',verbose=0))

