import json

with open("./data/team_mapping.json", "r") as f:
    team_mapping = json.load(f)


def is_greeting(sentence):
    greeting_inputs = (
        "hello",
        "hi",
        "greetings",
        "sup",
        "what's up",
        "hey",
        "good morning",
        "yo",
    )

    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return True


def is_cancel(inp):
    cancel_formats = (
        "cancel my bet on",
        "cancel bet on",
        "remove my bet",
        "cancel bet",
    )
    for cancel_str in cancel_formats:
        if cancel_str in inp.lower():
            return True


def asking_leaderboard(inp):
    if "leaderboard" in inp.lower():
        return True


def asking_my_bet(inp):
    my_bet_ask_formats = (
        "whats my bet",
        "what is my bet",
        "get my bet",
        "my bet",
        "what have i bet",
    )
    if inp.lower() in my_bet_ask_formats:
        return True


def asking_my_past_bets(inp):
    my_bet_ask_formats = (
        "what were my bets",
        "get my past bets",
    )
    if inp.lower() in my_bet_ask_formats:
        return True


def admin_update_results(inp):
    my_bet_ask_formats = (
        "what were my bets",
        "get my past bets",
    )
    if inp.lower() in my_bet_ask_formats:
        return True


def extract_team(inp):
    inp = inp.lower()
    cancel_words = ["cancel", "my", "bet", "on", "remove"]
    for i in cancel_words:
        if i in inp:
            inp = inp.replace(i, "")
    return inp.strip()


def is_bet_input(inp):
    if not any(map(str.isdigit, inp)):
        return False
    inp = inp.lower()
    teams = list(team_mapping.keys()) + list(set(team_mapping.values()))
    for team in teams:
        if team in inp.upper():
            return True
    return False


def parse_input(inp):
    if inp[0:5].lower() == "admin":
        return "admin"
    elif is_greeting(inp):
        return "greeting"
    elif asking_leaderboard(inp):
        return "leaderboard"
    elif asking_my_bet(inp):
        return "mybet"
    elif asking_my_past_bets(inp):
        return "pastbets"
    elif is_cancel(inp):
        return "cancel"
    elif is_bet_input(inp):
        return "bet"
    else:
        return "unk"
