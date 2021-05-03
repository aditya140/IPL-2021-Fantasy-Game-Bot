import pandas as pd
import datetime
import emoji
from ipl_schedule import IplData
from datetime import datetime
from dateutil.tz import gettz
import re


class BetMaker:
    def __init__(self):
        self.ipl_data = IplData()

    def process_bet(self, bet, profile_name, phone_number):
        regex = r"(?P<Team>[A-Za-z ].+)\s+" r"(?P<Bet>\d+)"  # 2 capital letters
        match_pattern = re.match(regex, bet)
        if match_pattern:
            team_name = match_pattern.group("Team")
            final_team_name = self.ipl_data.get_team_code(team_name)
            if final_team_name.strip() == "":
                return "Team name is invalid."
            bet_int = int(match_pattern.group("Bet"))
            if bet_int < 1:
                return f"{emoji.emojize(':cross_mark:')}Minimum bet is 1$"
            if bet_int > 5:
                return f"{emoji.emojize(':cross_mark:')}Maximum bet is 5$"
            match = self.ipl_data.get_match(bet_team=final_team_name)
            if match is None:
                error = emoji.emojize(":cross_mark:")
                return (
                    f"{error} No match for {final_team_name.title()} today.\n\nToday's match:\n\n"
                    f"{emoji.emojize(':cricket_game:')} {self.ipl_data.get_today_match_names().title()} "
                )

            isBetPlaced, bet_response = self.place_bet(
                match, final_team_name, bet_int, profile_name, phone_number
            )

            if isBetPlaced:
                match_string = emoji.emojize(":cricket_game:")
                money_bag = emoji.emojize(":money_with_wings:")
                white_check_mark = emoji.emojize(":check_mark_button:")
                response = (
                    f"{white_check_mark} Bet placed! "
                    f"\n\n{money_bag} {final_team_name.title()} *${bet_int}*\n\n"
                    f'{match_string} {match["Match"].title()}'
                )
            else:
                response = bet_response
            return response

        else:
            return (
                f"{emoji.emojize(':cross_mark:')} Format invalid. "
                f"Please enter data in this sample format : MI 5"
            )

    def place_bet(self, match, final_team_name, bet_int, profile_name, phone_number):
        data_list = [
            match["ID"],
            match["Match"],
            match["Date"].date(),
            match["Time"],
            profile_name,
            final_team_name,
            bet_int,
            int(phone_number),
            datetime.now(tz=gettz("Asia/Kolkata")).replace(tzinfo=None),
            # (datetime.date(2021, 5, 3), datetime.time(1, 23, 3, 50285)),
        ]
        new_bet_data = pd.DataFrame(
            data=[data_list],
            columns=[
                "ID",
                "Match",
                "Date",
                "Time",
                "Person",
                "Bet Team",
                "Bet Amount",
                "Phone number",
                "Timestamp",
            ],
        )
        if self.match_over_check(new_bet_data):
            return False, "Match has already started. Cant Place a bet now"

        bet_data = self.get_bet_data()
        if self.muliple_bet_check(bet_data, new_bet_data):
            bet_data = bet_data.append(new_bet_data)
            return self.save_bet_table(bet_data), None
        else:
            return (
                False,
                "You have already placed a bet. Cancel your previous bet to place a new bet",
            )

    def save_bet_table(self, bet_data):
        bet_data.reset_index(inplace=True, drop=True)
        bet_data.to_csv("./data/Bets.csv")
        return True

    def match_over_check(self, new_bet_data):
        if (
            new_bet_data["Time"].values[0]
            < pd.to_datetime(new_bet_data["Timestamp"].values[0]).to_pydatetime().time()
        ):
            # match started
            return True
        return False

    def muliple_bet_check(self, bet_data, new_bet_data):
        bet_data_filtered = bet_data[["Match", "Date", "Phone number"]]
        # rows with same phone number
        bet_data_filtered = bet_data_filtered[
            bet_data_filtered["Phone number"] == new_bet_data["Phone number"].values[0]
        ]
        # rows with same match
        bet_data_filtered = bet_data_filtered[
            bet_data_filtered["Match"] == new_bet_data["Match"].values[0]
        ]
        if bet_data_filtered.shape[0] == 1:
            return False
        return True

    def cancel_bet(self, phone_number, bet_team):
        bet_data = self.get_bet_data()
        todays_date = datetime.now(tz=gettz("Asia/Kolkata")).replace(tzinfo=None).date()
        print(bet_data)
        print(phone_number)
        filtered_data = bet_data[bet_data["Phone number"] == int(phone_number)]
        print(filtered_data)
        is_todays_bet = filtered_data.apply(
            lambda x: pd.to_datetime(x["Date"]).to_pydatetime().date() == todays_date,
            axis=1,
        )
        filtered_data = filtered_data[is_todays_bet]
        filtered_data = filtered_data[filtered_data["Bet Team"] == bet_team]
        if filtered_data.shape[0] == 0:
            return False, "No Bet Found"
        bet_data = bet_data.drop(filtered_data[is_todays_bet].index[0])
        self.save_bet_table(bet_data)
        return True, None

    def get_todays_bet(self, phone_number):
        phone_number = int(phone_number)
        bet_data = self.get_bet_data()
        todays_date = datetime.now(tz=gettz("Asia/Kolkata")).replace(tzinfo=None).date()
        filtered_data = bet_data[bet_data["Phone number"] == phone_number]
        is_todays_bet = filtered_data.apply(
            lambda x: pd.to_datetime(x["Date"]).to_pydatetime().date() == todays_date,
            axis=1,
        )
        my_bet = filtered_data[is_todays_bet][["Match", "Bet Amount", "Bet Team"]]
        my_bet_list = my_bet.to_dict(orient="records")
        response = ""
        for bet in my_bet_list:
            response += "\n\n\n"
            response += f"Match: {bet['Match']}\n"
            response += f"You bet {bet['Bet Amount']}$ on {bet['Bet Team']}\n"
        if response == "":
            response = "You do not have any upcooming bets"
        return response

    def get_bet_data(self):
        data = pd.read_csv("./data/Bets.csv", index_col=0)
        return data
