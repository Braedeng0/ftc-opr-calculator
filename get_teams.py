from utils import graphql_query

def get_teams(season="2025"):
    """Get the active teams for a given season"""
    query = """
    query {
        teamsSearch {
            name,
            number
        }
    }
    """

    all_teams = graphql_query("https://api.ftcscout.org/graphql", query)
    print(all_teams)

if __name__ == "__main__":
    get_teams()
