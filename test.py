from pycricbuzz import Cricbuzz
import json
c = Cricbuzz()
matches = c.matches()
flag = False
cwc_match_list = list()
for match in matches:
    if match["srs"]=="ICC Cricket World Cup 2019":
        if match["mchstate"]=="inprogress":
            print(match["id"])            
            print(match["team1"]["name"],match["team2"]["name"])
            cwc_match_list.append((match["id"]))            
            flag = True

if not flag:
    print("No ICC CWC 2019 match is in progress")

for match in cwc_match_list:
    lscore = c.livescore(match)
    print(json.dumps(lscore, indent=4, sort_keys=True))


# print(type(matches))
# print (json.dumps(matches,indent=4)) #for pretty prinitng