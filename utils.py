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
    response.raise_for_status()
    return response.json()

def get_teams():
    """Get the active teams for a given season"""
    query = """
    query {
        teamsSearch (region: USAZ) {
            name,
            number,
            events (season: 2024) {
            eventCode
            }
        }
    }
    """
    # Make the request to get all FTC teams
    all_teams = graphql_query("https://api.ftcscout.org/graphql", query)['data']['teamsSearch']
    # Filter out teams that haven't competed this season
    all_teams = [team for team in all_teams if len(team['events']) != 0]

    return all_teams

def get_matches(team_number, season):
    """Get all matches played by a team in a given season"""
    query = """
    query {
        
    }
    """

    '''
    query {
        teamByNumber(number: 14584) {
            matches (season: 2024) {
            alliance
            match {
                scores {
                    ... on MatchScores2024 {
                    red {
                    totalPoints
                    }
                    blue {
                    totalPoints
                    }
                }
                }
            }
            }
        }
    }
    '''
