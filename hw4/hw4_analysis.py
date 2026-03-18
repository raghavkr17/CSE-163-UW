# hw4_analysis.py
# CSE 163 THA4 – Facebook Network Analysis
# Implements friend recommendation algorithms.

import networkx as nx

FACEBOOK_PATH = "facebook-links-small.txt"


def read_facebook(facebook: nx.Graph, filename: str) -> None:
    """
    Given a graph and file path, reads the file and
    adds every entry as an edge in the graph.
    """
    with open(filename) as f:
        for row in f:
            items = row.split()
            person1, person2 = items[0], items[1]
            facebook.add_edge(int(person1), int(person2))


def friends(graph: nx.Graph, user: int) -> set[int]:
    """Returns the set of friends of a user."""
    return set(graph.neighbors(user))


def friends_of_friends(graph: nx.Graph, user: int) -> set[int]:
    """Returns the set of friends of friends of a user."""
    f_of_f = set()
    user_friends = friends(graph, user)

    for friend in user_friends:
        f_of_f |= friends(graph, friend)

    return f_of_f - user_friends - {user}


# ---------------------------------------------------
# REQUIRED FUNCTIONS
# ---------------------------------------------------

def common_friends(graph: nx.Graph,
                   user1: int,
                   user2: int) -> set[int]:
    """
    Returns the set of mutual friends between two users.
    """
    return friends(graph, user1) & friends(graph, user2)


def recs_by_common_friends(graph: nx.Graph,
                           user: int) -> list[int]:
    """
    Returns friend recommendations sorted by
    number of common friends (descending).
    """
    scores: dict[int, int] = {}

    for person in friends_of_friends(graph, user):
        mutuals = common_friends(graph, user, person)

        if mutuals:
            scores[person] = len(mutuals)

    return sorted(scores, key=lambda x: (-scores[x], x))


def recs_by_influence(graph: nx.Graph,
                      user: int) -> list[int]:
    """
    Returns friend recommendations sorted by
    influence score (descending).
    """
    scores: dict[int, float] = {}

    for person in friends_of_friends(graph, user):
        mutuals = common_friends(graph, user, person)

        if not mutuals:
            continue

        influence = 0.0

        for f in mutuals:
            influence += 1 / len(friends(graph, f))

        scores[person] = influence

    return sorted(scores, key=lambda x: (-scores[x], x))


# ---------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------

def main() -> None:
    g = nx.Graph()
    read_facebook(g, FACEBOOK_PATH)

    print("Recommendations by common friends:\n")

    users = sorted(g.nodes())

    for user in users:
        if user % 1000 == 0:
            recs = recs_by_common_friends(g, user)[:10]
            print(f"{user} (by num_common_friends): {recs}")

    print("\nRecommendations by influence:\n")

    for user in users:
        if user % 1000 == 0:
            recs = recs_by_influence(g, user)[:10]
            print(f"{user} (by influence): {recs}")

    # Compare algorithms
    same = 0
    different = 0

    for user in users:
        if user % 1000 == 0:
            recs1 = recs_by_common_friends(g, user)[:10]
            recs2 = recs_by_influence(g, user)[:10]

            if recs1 == recs2:
                same += 1
            else:
                different += 1

    print("\nDifference in Algorithm Recommendations:", different)


if __name__ == "__main__":
    main()
