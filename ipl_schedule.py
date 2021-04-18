import pandas as pd
from datetime import date
import re
from bet_maker import BetMaker
import emoji

class IplData:

    def __init__(self):
        self.ipl_df = pd.read_excel('./data/IPL_Schedule.xlsx')
        self.bet_maker = BetMaker()

    def get_team_code(self, team_name):

        team_name = team_name.upper()

        if team_name=='MI' or team_name=='MUM' or team_name=='MUMBAI' or team_name=='MUMBAI INDIANS':
            return 'MUMBAI INDIANS'

        elif team_name=='RCB' or team_name=='BANGALORE' or team_name=='ROYAL CHALLENGERS BANGALORE':
            return 'ROYAL CHALLENGERS BANGALORE'

        elif team_name=='CSK' or team_name=='CHENNAI' or team_name=='CHENNAI SUPER KINGS':
            return 'CHENNAI SUPER KINGS'

        elif team_name=='DC' or team_name=='DEL' or team_name=='DELHI CAPITALS':
            return 'DELHI CAPITALS'

        elif team_name=='RR' or team_name=='RAJASTHAN ROYALS':
            return 'RAJASTHAN ROYALS'

        elif team_name=='KKR' or team_name=='KOLKATA KNIGHT RIDERS':
            return 'KOLKATA KNIGHT RIDERS'

        elif team_name=='PUN' or team_name=='PBKS' or team_name=='PUNJAB' or team_name=='PUNJAB KINGS':
            return 'PUNJAB KINGS'

        elif team_name=='SRH' or team_name=='HYD' or team_name=='SUNRISERS HYDERABAD':
            return 'SUNRISERS HYDERABAD'

        else:
            return ''


    def get_todays_match(self):
        today = date.today()

        # Month abbreviation, day and year
        d4 = today.strftime("%d-%b-%y")
        print("d4 =", d4)

        todays_matches = self.ipl_df.loc[self.ipl_df['Date'] == d4]

        #print(todays_matches)
        #match_list = todays_matches['Match'].tolist()

        #return ''.join(match_list)

        return todays_matches

    def get_match(self, bet_team):

        today_match = self.get_todays_match()

        print(f'today match : {today_match}')
        for i in range(today_match.shape[0]):

            match = today_match.iloc[i]
            print(match)
            if bet_team in match['Match']:
                print(f'bet team : {bet_team} and match : {match["Match"]}')
                return today_match.iloc[i]

        return None


    def get_today_match_names(self):

        today_match = self.get_todays_match()

        match_list =  today_match['Match'].values

        return '\n'.join(match_list)



    def place_bets(self, bet, profile_name, phone_number):

        regex = (
            r"(?P<Team>[A-Za-z ].+)\s+"  # 2 capital letters
            r"(?P<Bet>\d+)")

        match_pattern = re.match(regex, bet)

        if match_pattern:

            team_name = match_pattern.group('Team')

            print(team_name)

            if team_name.strip() == '':
                return 'Team name is invalid.'

            final_team_name = self.get_team_code(team_name)

            if final_team_name.strip() == '':
                return 'Team name is invalid.'

            print(final_team_name)
            bet_int = int(match_pattern.group('Bet'))

            if bet_int < 40:
                return f"{emoji.emojize(':cross_mark:')}Minimum bet is 40"

            match = self.get_match(bet_team=final_team_name)

            if match is None:
                #error = emoji.emojize(':cross_mark:')

                error = emoji.emojize(':cross_mark:')
                return f"{error} No match for {final_team_name.title()} today.\n\nToday's match:\n\n" \
                    f"{emoji.emojize(':cricket_game:')} {self.get_today_match_names().title()} "


            isBetPlaced = self.bet_maker.place_bet([match, final_team_name, bet_int, profile_name, phone_number])

            if isBetPlaced:
                match_string = emoji.emojize(':cricket_game:')
                money_bag = emoji.emojize(':money_with_wings:')
                white_check_mark = emoji.emojize(':check_mark_button:')
                response = f'{white_check_mark} Bet placed! ' \
                    f'\n\n{money_bag} {final_team_name.title()} *₹{bet_int}*\n\n' \
                    f'{match_string} {match["Match"].title()}'
            else:
                response = 'Error placing your bet. Please try again.'
           # data = [[match, final_team_name, bet_int, profile_name, phone_number]]
           #
           #  df = pd.DataFrame(columns=['Match', 'Team', 'Bet', 'Person', 'Phone number'], data=data)
           #  print(df)
           #  df.to_excel(r"Bet1.xlsx", index=False)

            return response

        else:
            return f"{emoji.emojize(':cross_mark:')} Format invalid. " \
                f"Please enter data in this sample format : MI 50"


