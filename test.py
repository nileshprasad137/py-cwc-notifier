from pycricbuzz import Cricbuzz
import json
import requests
c = Cricbuzz()
matches = c.matches()
flag = False
cwc_match_list = list()
big_events = ["W", "4", "6"]
# Can be user parametrised. Like 10 runs in over and more events
for match in matches:
    if match["srs"]=="ICC Cricket World Cup 2019":
        if match["mchstate"]=="inprogress":
            # print(match["id"])
            # match_id = match["id"]
            print(match["team1"]["name"],match["team2"]["name"])
            cwc_match_list.append((match["id"]))            
            flag = True

if not flag:
    print("No ICC CWC 2019 match is in progress")

# for match in cwc_match_list:
#     lscore = c.livescore(match)
#     print(json.dumps(lscore, indent=4, sort_keys=True))

# notification_flag = False
overs_detail_list = list() # This need to be persisted through multiple HTTP calls

# over_notification_dict = {
#     "over_no":None,
#     "is_notification_needed":False,
#     "is_notified" : False
# }

for match in cwc_match_list:
    leanback_url = "http://mapps.cricbuzz.com/cbzios/match/"+match+"/leanback.json"
    detailed_leanback = requests.get(leanback_url).json()
    previous_over = detailed_leanback["prev_overs"]
    print(previous_over)
    commentary_url = "http://mapps.cricbuzz.com/cbzios/match/"+match+"/watch-mini-commentary.json"
    recent_commentary_json = requests.get(commentary_url).json()
    recent_commentary_list = recent_commentary_json["comm_lines"]
    recent_over_no = list()
    for over_detail in recent_commentary_list:
        over_no = over_detail["o_no"]
        over_summary = over_detail["o_summary"]
        inning_no = over_detail["i_id"]
        notification_flag = False
        for event in over_summary:
            if event in big_events:
                notification_flag = True

        over_notification_dict = {
            "inning_no":inning_no,
            "over_no": over_no,
            "is_notification_needed": notification_flag,
            "is_notified": False
        }
        recent_over_no.append(over_no)
        overs_detail_list.append(over_notification_dict)
    print(recent_over_no)
    # current_over = max(recent_over_no)
    print(overs_detail_list)



# print(type(matches))
# print (json.dumps(matches,indent=4)) #for pretty prinitng
#
# import json
# with open('data.json', 'w', encoding='utf-8') as outfile:
#     json.dump(data, outfile, ensure_ascii=False, indent=2)