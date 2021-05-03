import json
import pandas as pd


class Leaderboard:
    def __init__(self):
        self.bet_table = pd.read_csv("./data/Bets.csv")
        with open("./data/winner.json", "r") as f:
            self.winners = json.load(f)

    def display_leaderboard(self):
        gain, win_per = self.get_leaderboard()
        results = {i: [gain[i], win_per[i]] for i in gain.keys()}
        res_sorted = sorted(results.items(), key=lambda x: x[1][0], reverse=True)
        response = "*Leaderboard*\n\n"
        for i, v in enumerate(res_sorted):
            response += f"*{i+1}.* _{v[0]}_\t\t----- {v[1][0]}$ ({v[1][1]}% win rate)\n"
        return response

    def get_leaderboard(self):
        decisive_matches = self.bet_table["ID"].isin(
            list(map(int, self.winners.keys()))
        )

        bet_df = self.bet_table[decisive_matches]
        players = list(set(self.bet_table["Person"].values))
        gain = {i: 0 for i in players}
        wins_per = {i: [0, 0] for i in players}
        match_ids = list(map(int, self.winners.keys()))
        for m_id in match_ids:
            match_bets = bet_df[bet_df["ID"] == m_id][
                ["Person", "Bet Amount", "Bet Team"]
            ]
            if match_bets.shape[0] > 0:
                match_winner = self.winners[str(m_id)]
                pools = (
                    match_bets.groupby(by=["Bet Team"])["Bet Amount"].sum().to_dict()
                )
                looser = [i for i in pools.keys() if i != match_winner][0]
                winner_gain_per_dollar = pools[looser] / pools[match_winner]
                for index, row in match_bets.iterrows():
                    if row["Bet Team"] == match_winner:
                        gain[row["Person"]] += (
                            winner_gain_per_dollar * row["Bet Amount"]
                        )
                        wins_per[row["Person"]][0] += 1
                        wins_per[row["Person"]][1] += 1
                    else:
                        gain[row["Person"]] -= row["Bet Amount"]
                        wins_per[row["Person"]][1] += 1

        win_percentage = {
            i: 100 * wins_per[i][0] / wins_per[i][1] for i in wins_per.keys()
        }
        return gain, win_percentage
