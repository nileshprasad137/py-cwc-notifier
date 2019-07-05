from pycricbuzz import Cricbuzz
import datetime, threading, time
import notify2
import json
import requests
c = Cricbuzz()
matches = c.matches()
flag = False
cwc_match_list = list()
big_events = ["W", "4", "6"]
# Can be user parametrised. Like 10 runs in over and more events
match_id = None
for match in matches:
    if match["srs"]=="ICC Cricket World Cup 2019":
        if match["mchstate"]=="inprogress":
            # print(match["id"])
            # match_id = match["id"]
            print(match["team1"]["name"],match["team2"]["name"])
            cwc_match_list.append((match["id"]))
            match_id = match["id"]
            flag = True

if not flag:
    print("No ICC CWC 2019 match is in progress")

# for match in cwc_match_list:
#     lscore = c.livescore(match)
#     print(json.dumps(lscore, indent=4, sort_keys=True))

# notification_flag = False

# overs_detail_list = list() # This need to be persisted through multiple HTTP calls

# over_notification_dict = {
#     "over_no":None,
#     "is_notification_needed":False,
#     "is_notified" : False
# }

#   get user input on which match to follow!

final_json = dict()
final_json["inning1"] = dict()
final_json["inning2"] = dict()

next_call = time.time()

def notify(over_no,current_score):
    notify2.init('ICC Cricket World Cup Notifier')
    notification_title = "ICC CWC Notification"
    notification_summary = "Big moment in over"+over_no+"\nCurrent Score : "+current_score
    n = notify2.Notification(notification_title, notification_summary)
    n.timeout = 3000  # display duration
    # n.set_urgency(2)
    n.show()

def get_scores(match_id):
    global next_call
    print(datetime.datetime.now())
    next_call += 1
    final_notification_status = False
    leanback_url = "http://mapps.cricbuzz.com/cbzios/match/" + match_id + "/leanback.json"
    detailed_leanback = requests.get(leanback_url).json()
    previous_over = detailed_leanback["prev_overs"]
    print(previous_over)
    commentary_url = "http://mapps.cricbuzz.com/cbzios/match/" + match_id + "/watch-mini-commentary.json"
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
            "over_no": over_no,
            "is_notification_needed": notification_flag,
            "is_notified": False
        }
        recent_over_no.append(over_no)
        # overs_detail_list.append(over_notification_dict)


        if inning_no=='1':
            if over_no not in final_json["inning1"].keys():
                final_json["inning1"][over_no] = over_notification_dict
                if over_notification_dict["is_notification_needed"] and not over_notification_dict["is_notified"]:
                    final_notification_status = True
                    print("notification for over ", over_no)
                    # Call a function to notify
                    notify(over_no)
                    final_json["inning1"][over_no]["is_notified"] = True

            else:
                is_current_over_notified = final_json["inning1"][over_no]["is_notified"]
                is_notification_needed_for_over = final_json["inning1"][over_no]["is_notification_needed"]
                if is_notification_needed_for_over and not is_current_over_notified:
                    final_notification_status = True
                    print("notification for over ", over_no)
                    # Call a function to notify
                    notify(over_no)
                    final_json["inning1"][over_no]["is_notified"] = True


        if inning_no == '2':
            if over_no not in final_json["inning2"].keys():
                final_json["inning2"][over_no] = over_notification_dict
                if over_notification_dict["is_notification_needed"] and not over_notification_dict["is_notified"]:
                    final_notification_status = True
                    print("notification for over ", over_no)
                    notify(over_no)
                    final_json["inning2"][over_no]["is_notified"] = True
            else:
                is_current_over_notified = final_json["inning2"][over_no]["is_notified"]
                is_notification_needed_for_over = final_json["inning2"][over_no]["is_notification_needed"]
                if is_notification_needed_for_over and not is_current_over_notified:
                    final_notification_status = True
                    print("notification for over ", over_no)
                    # Call a function to notify
                    notify(over_no)
                    final_json["inning2"][over_no]["is_notified"] = True


        #     final_json["inning1"]

    # print(recent_over_no)
    # current_over = max(recent_over_no)
    print(final_json)
    # print(time.ctime())
    threading.Timer(20, get_scores,args=[match_id]).start()


get_scores(match_id)



# print(type(matches))
# print (json.dumps(matches,indent=4)) #for pretty prinitng
#
# import json
# with open('data.json', 'w', encoding='utf-8') as outfile:
#     json.dump(data, outfile, ensure_ascii=False, indent=2)