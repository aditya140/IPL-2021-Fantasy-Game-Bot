import pandas as pd
from datetime import date
import re
import emoji
import json
from datetime import datetime
from dateutil.tz import gettz
from typing import TypeVar, Generic

T = TypeVar("T")


class IplData(Generic[T]):
    def __init__(self) -> None:
        self.ipl_df = pd.read_excel("./data/IPL_Schedule.xlsx")
        with open("./data/team_mapping.json", "r") as f:
            self.team_mapping = json.load(f)

    def get_team_code(self, team_name: str) -> str:
        team_name = team_name.upper()
        if team_name in self.team_mapping.keys():
            return self.team_mapping[team_name]
        else:
            return ""

    def get_todays_match(self) -> None:
        today = datetime.now(tz=gettz("Asia/Kolkata"))
        d4 = today.strftime("%d-%b-%y")
        todays_matches = self.ipl_df.loc[self.ipl_df["Date"] == d4]
        return todays_matches

    def get_match(self, bet_team: str) -> str:
        today_match = self.get_todays_match()
        for i in range(today_match.shape[0]):
            match = today_match.iloc[i]
            if bet_team in match["Match"]:
                return today_match.iloc[i]
        return None

    def get_today_match_names(self):
        today_match = self.get_todays_match()
        match_list = today_match["Match"].values
        return "\n".join(match_list)
