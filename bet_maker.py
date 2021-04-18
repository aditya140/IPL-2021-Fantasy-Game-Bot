import pandas as pd
import datetime


class BetMaker:

    def __init__(self):
        pass

    def place_bet(self, args):
        match, final_team_name, bet_int, profile_name, phone_number = args

        print(f'args - {args}')

        data_list = [match['ID'], match['Match'], match['Date'], match['Time'], profile_name, final_team_name, bet_int,
                     int(phone_number), datetime.datetime.now()]
        print(data_list)

        new_bet_data = pd.DataFrame(data=[data_list], columns=['ID','Match', 'Date', 'Time', 'Person', 'Bet Amount',
                                                             'Bet Team', 'Phone number', 'Timestamp'])

        bet_data = self.get_bet_data()

        print('bet data before append')
        print(bet_data)

        bet_data = bet_data.append(new_bet_data)

        print('bet data after append')
        print(bet_data)


        # resetting index
        bet_data.reset_index(inplace=True, drop=True)

        #bet_data = bet_data.drop(columns=['Unnamed: 0','Unnamed: 0.1'])

        bet_data.to_excel('./data/Bets.xlsx')


        return True

    def get_bet_data(self):
        data = pd.read_excel('./data/Bets.xlsx', index_col=0)

        return data



