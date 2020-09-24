import re,csv,json,os 
from copy import deepcopy


#output folder is created 
#DEFAULT="../OUTPUTS"

stopwords=["i","me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your","what" ,"yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
FOLDER_NAME=input("Enter the name of the intent set :") #set name for folder
FOLDER="intents"
SAVED_FOLDER="../OUTPUTS/{}/{}".format(FOLDER_NAME,FOLDER)

try:
    os.makedirs(SAVED_FOLDER)
except OSError as e:
    print(e)

file=open("../OUTPUTS/"+FOLDER_NAME+"/package.json","w")
file.write('{"version": "1.0.0"}')
file.close()

def shorten(sentance):
    sen_list=sentance.split()
    return [item for item in sen_list if item not in stopwords]

def intentNameCreate(intentName):
    sen_list=shorten(intentName)
    intentName=".".join(sen_list)
    sp=['?','\\',' ']
    for c in sp:
        intentName=intentName.replace(c,'')
    return intentName

 
with open('../TEMPLATES/Basic/fake.json','r') as f:
    template_question=json.loads(f.read())
with open('../TEMPLATES/Basic/fake_usersays_en.json','r') as f:
    template_usersays=json.loads(f.read())

with open('../CSV/test.csv','r') as csv_file:
    csv_reader=csv.reader(csv_file,delimiter=',')
    for row in csv_reader:
        print(">>>>>")
        user_says=row[0].split("|")
        responses=row[1].split("|")

        #set the intent Name
        intentName=user_says[0]
        intentName=intentNameCreate(intentName)
        intentName=FOLDER_NAME+"."+intentName

        # training_phrase=row[0]
        # response=row[1]

        q_copy=deepcopy(template_question)
        u_copy=deepcopy(template_usersays)
        
        q_copy["name"]=intentName
        
        response_list=[]
        for k in responses:
            response_list.append("<speak>{}</speak>".format(k))
        q_copy["responses"][0]["messages"][0]["speech"]=response_list
    
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
