from utils import *
from opr_calculator import *

event_code = "USAZGOQ"
all_teams = get_teams_by_event(event_code)
matches = get_matches(event_code)

A = []
b = []
for match in matches:
    teams = match['teams']
    score = match['score']
    A.append([1 if team in teams else 0 for team in all_teams])
    b.append(score)

# Calculate the OPRs
oprs = calculate_opr(A, b)
print("OPRs:")
for team, opr in zip(all_teams, oprs):
    print(f"Team {team}: OPR {round(opr, 2)}")
