import requests

def graphql_query(url, query, headers=None):
    payload = {"query": query}
    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if headers:
        default_headers.update(headers)

    response = requests.post(url, json=payload, headers=default_headers)
    
    if response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}: {response.text}")
    
    return response.json()

def get_teams_by_region(region, season=2024):
    """Get the active teams for a given season"""
    query = """
    query {
        teamsSearch (region: {region}) {
            name,
            number,
            events (season: {season}) {
            eventCode
            }
        }
    }
    """
    # Replace the placeholders with the actual values
    query = query.replace("{region}", region)
    query = query.replace("{season}", str(season))
    # Make the request to get all FTC teams
    all_teams = graphql_query("https://api.ftcscout.org/graphql", query)['data']['teamsSearch']
    # Filter out teams that haven't competed this season
    all_teams = [team for team in all_teams if len(team['events']) != 0]

    return all_teams

def get_teams_by_event(event_code, season=2024):
    """Get all teams that have played in a given event"""
    query = """
    query {
        eventByCode(code: "{event_code}", season: {season}) {
            teams {
                teamNumber
            }
        }
    }
    """
    # Replace the placeholders with the actual values
    query = query.replace("{event_code}", str(event_code))
    query = query.replace("{season}", str(season))
    # Make the request to get all teams at the event
    all_teams = graphql_query("https://api.ftcscout.org/graphql", query)['data']['eventByCode']['teams']
    
    return [team['teamNumber'] for team in all_teams]

def get_matches(event_code, season=2024, points_type="totalPointsNp"):
    """Get all matches played by a team in a given season"""
    query = """
    query {
        eventByCode(code: "{event_code}", season: {season}) {
            matches {
                scores {
                    ... on MatchScores2024 {
                            red {
                                {points_type}
                            }
                            blue {
                                {points_type}
                            }
                        }
                    }
                teams {
                alliance
                teamNumber
                }
            }
        }
    }
    """
    # Replace the placeholders with the actual values
    query = query.replace("{event_code}", str(event_code))
    query = query.replace("{season}", str(season))
    query = query.replace("{points_type}", points_type)
    # Make the request to get all matches played by the team
    all_matches = graphql_query("https://api.ftcscout.org/graphql", query)['data']['eventByCode']['matches']
    # Create a list of dictionaries with match scores and teams
    matches = []
    for i in range(len(all_matches)):
        # Red alliance
        red_alliance = [team['teamNumber'] for team in all_matches[i]['teams'] if team['alliance'] == 'Red']
        red_score = all_matches[i]['scores']['red'][points_type]
        matches.append({
            'teams': red_alliance,
            'score': red_score,
        })
        # Blue alliance
        blue_alliance = [team['teamNumber'] for team in all_matches[i]['teams'] if team['alliance'] == 'Blue']
        blue_score = all_matches[i]['scores']['blue'][points_type]
        matches.append({
            'teams': blue_alliance,
            'score': blue_score,
        })
    return matches

if __name__ == "__main__":
    event_code = "USAZTUQ"
    season = 2024
    # matches = get_matches(event_code, season)
    # print(f"Matches for event {event_code} in season {season}:")
    # for match in matches:
    #     print(f"Teams: {match['teams']}, Score: {match['score']}")
    teams = get_teams_by_event(event_code, season)
    print(f"Teams for event {event_code} in season {season}:")
    for team in teams:
        print(team)
