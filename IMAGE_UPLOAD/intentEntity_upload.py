import re,csv,json,os
from copy import deepcopy


#output folder is created 
#DEFAULT="../OUTPUTS"

stopwords=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your","what" ,"yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
FOLDER_NAME=input("Enter the name of the intent set :") #set name for folder
FOLDER1="intents"
SAVED_FOLDER1="../OUTPUTS/{}/{}".format(FOLDER_NAME,FOLDER1)
##
FOLDER2="entities"
SAVED_FOLDER2="../OUTPUTS/{}/{}".format(FOLDER_NAME,FOLDER2)

try:
    os.makedirs(SAVED_FOLDER1)
    os.makedirs(SAVED_FOLDER2)
except OSError as e:
    print(e)

file=open("../OUTPUTS/"+FOLDER_NAME+"/package.json","w")
file.write('{"version": "1.0.0"}')
file.close()



def shorten(sentance):
    sen_list=sentance.split()
    return list(set(sen_list)-set(stopwords))

def intentNameCreate(intentName):
    sen_list=shorten(intentName)
    intentName=".".join(sen_list)
    sp=['?','\\','']
    for c in sp:
        intentName=intentName.replace(c,'')
    return intentName


with open('../TEMPLATES/IMG/fake_img.json','r') as f:
    template_question=json.loads(f.read())
with open('../TEMPLATES/IMG/fake_img_usersays_en.json','r') as f:
    template_usersays=json.loads(f.read())

with open('../TEMPLATES/Entities/entity.json','r') as f:
    template_entity=json.loads(f.read())
with open('../TEMPLATES/Entities/entity_entries_en.json','r') as f:
    template_entries=json.loads(f.read())

with open('../CSV/intent_image.csv','r') as csv_file:
    csv_reader=csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        print(">>>>>")
        user_says=row[0].split("|")
        response=row[1]
        image_entity=row[2]
        image_url=row[3]
        display_prompt=row[4]

        # print(row[0])
        # print(row[1])
        # print(row[2])
        # print(row[3])
        # print(row[4])

        #set the intent Name
        intentName=FOLDER_NAME+"-"+user_says[0]
        intentName=intentNameCreate(intentName)

        # training_phrase=row[0]
        

        q_copy=deepcopy(template_question)
        u_copy=deepcopy(template_usersays)
        
        q_copy["name"]=intentName
        q_copy["responses"][0]["messages"][0]["speech"]="<speak>{}</speak>".format(response)
        q_copy["responses"][0]["parameters"][0]["name"]=image_entity
        q_copy["responses"][0]["parameters"][0]["value"]=image_url
        q_copy["responses"][0]["messages"][1]["payload"]["displayPrompt"][0]=display_prompt
    
        arr_list=[]
        for k in user_says:
            USER_SAYS_JSON={"data": [{"text": "","userDefined": False}],"isTemplate": False,"count": 0,"updated": 0}
            USER_SAYS_JSON["data"][0]["text"]="{}".format(k)
            arr_list.append(USER_SAYS_JSON)
        
        
        u_copy=deepcopy(arr_list)

        print(q_copy)
        with open(f'{SAVED_FOLDER}/{intentName}.json','w') as f:
            f.write(json.dumps(q_copy))
        with open(f'{SAVED_FOLDER}/{intentName}_usersays_en.json','w') as f:
            f.write(json.dumps(u_copy))
