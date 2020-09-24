import re,csv,json,os
from copy import deepcopy


FOLDER_NAME=input("Enter the name of the entity set :") #set name for folder
FOLDER="entities"
SAVED_FOLDER="../OUTPUTS/{}/{}".format(FOLDER_NAME,FOLDER)
 
try:
    os.makedirs(SAVED_FOLDER)
except OSError as e:
    print(e)

file=open("../OUTPUTS/"+FOLDER_NAME+"/package.json","w")
file.write('{"version": "1.0.0"}')
file.close()

with open('../TEMPLATES/Entities/entity.json','r') as f:
    template_entity=json.loads(f.read())
with open('../TEMPLATES/Entities/entity_entries_en.json','r') as f:
    template_entries=json.loads(f.read())

def gapfill(sentance):
    sentance=sentance.split()
    sentance="_".join(sentance)
    return sentance


with open('../CSV/services.csv','r') as csv_file:
    csv_reader=csv.reader(csv_file,delimiter=',')
    entry_list=[]
    entity_copy=deepcopy(template_entity)
    entity_copy["name"]=FOLDER_NAME
    for row in csv_reader:
        value=row[0]
        synonyms=row[1].split("|")

        entries_copy={"value": "FAKE_VALUE","synonyms": [  "FAKE SYNONYM 1",  "FAKE SYNONYM 2"]}
        entries_copy["value"]=value
        entries_copy["synonyms"]=synonyms

        entry_list.append(entries_copy)

        
    entries_copy=deepcopy(entry_list)

    with open(f'{SAVED_FOLDER}/{FOLDER_NAME}.json','w') as f:
        f.write(json.dumps(entity_copy))
    with open(f'{SAVED_FOLDER}/{FOLDER_NAME}_entries_en.json','w') as f:
        f.write(json.dumps(entries_copy))
