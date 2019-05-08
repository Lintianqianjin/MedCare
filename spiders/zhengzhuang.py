import json

with open("medic.json", "r", encoding="utf-8") as f:
    json_str = f.read()
medicine_list = json.loads(json_str)
symptom = []

for s in medicine_list:
    if ('zhengzhuang' in s.keys()):
        print(s['zhengzhuang'])
        for m in s['zhengzhuang']:
            if(not m in symptom):
                symptom.append(m)

print(symptom)

with open("症状.txt", "w", encoding="utf-8") as f:
    for s in symptom:
        f.write(s+',无\n')
    f.close()