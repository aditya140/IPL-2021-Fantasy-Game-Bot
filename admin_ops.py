from ipl_schedule import IplData
import pandas as pd
from datetime import datetime, timedelta
from dateutil.tz import gettz
import json


class AdminOperations:
    """
    Admin Operations:
    1. Get ID of each match.
    2. Modify Winner of each match by ID.
    3. Get Summary of next 5 and past 5 matchs.
    4. Get Todays bets.

    Examples:
    Admin around <dur>
    Admin Winner <id> <WinnerTeam>

    ToDo:
    WinnerTeam must match with the teams playing in match_id
    """

    def __init__(self):
        self.ipl_data = IplData()

    def process(self, incoming_message):
        if incoming_message[:5].lower() != "admin":
            return "First argument should be admin"
        message = incoming_message[6:].lower()
        if "around" in message:
            dur = int(message.split(" ")[1])
            return self.get_nearby_matches(dur)
        if "winner" in message:
            match_id, team_name = message.split(" ")[1:]
            if team_name == "none":
                self.set_winner(match_id, "NONE")
                return f"Winner for Match {match_id} updated as None"
            else:
                team_name_code = self.ipl_data.get_team_code(team_name)
                self.set_winner(match_id, team_name_code)
            return f"Winner for Match {match_id} updated as {team_name_code}"

    def get_winner_json(self):
        with open("./data/winner.json", "r") as f:
            data = json.load(f)
        return data

    def set_winner_json(self, data):
        with open("./data/winner.json", "w") as f:
            json.dump(data, f)

    def set_winner(self, match_id, team_name):
        winners = self.get_winner_json()
        winners[match_id] = team_name
        self.set_winner_json(winners)
        return True

    def get_nearby_matches(self, dur):
        df = self.around_today(dur)
        df = df[["Match", "Date", "ID"]]
        resp = ""
        for index, row in df.iterrows():
            if pd.to_datetime(row["Date"]) == pd.to_datetime(
                datetime.now(tz=gettz("Asia/Kolkata")).replace(tzinfo=None).date()
            ):
                resp += "------\n"
                resp += f"*{row['Match']}, {row['Date'].to_pydatetime().date()}, {row['ID']}*\n"
                resp += "------\n"
            else:
                resp += f"{row['Match']}, {row['Date'].to_pydatetime().date()}, {row['ID']}\n"
        return resp

    def around_today(self, d=2):
        df = self.ipl_data.ipl_df
        date_future = pd.to_datetime(
            datetime.now(tz=gettz("Asia/Kolkata")).replace(tzinfo=None).date()
            + timedelta(days=d)
        )
        date_past = pd.to_datetime(
            datetime.now(tz=gettz("Asia/Kolkata")).replace(tzinfo=None).date()
            + timedelta(days=-1 * d)
        )
        mask = (df["Date"] > date_past) & (df["Date"] <= date_future)
        return df[mask]
