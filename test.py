# %%
from bet_maker import BetMaker

# %%
a = BetMaker()
# %%
print(a.process_bet("RCB 4", "aditya", 9195230176))
# %%
print(a.get_todays_bet(9195230176))
# %%
print(a.cancel_bet(19195230176, "KOLKATA KNIGHT RIDERS"))
