from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chat_helpers import *
from ipl_schedule import IplData
from bet_maker import BetMaker
from leaderboard import Leaderboard
from admin_ops import AdminOperations
import emoji


app = Flask(__name__)


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").upper()
    profile_name = request.values.get("ProfileName", "")

    phone_number = request.values.get("WaId", "")
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    print(incoming_msg)

    if incoming_msg:
        chat_type = parse_input(incoming_msg)
        if chat_type == "greeting":
            output = (
                f'{emoji.emojize(":sparkles:")} *IPL 2021 Fantasy Game Bot!*  {emoji.emojize(":sparkles:")}\n\n'
                f'{emoji.emojize(":dollar_banknote:")} Sample bet format : _KKR 40_\n\n'
                f'{emoji.emojize(":cricket_game:")} Today\'s match : _{IplData().get_today_match_names().title()}_\n\n'
                "Other options: \n 1. _Leaderboard_\n 2. _What is my Bet_\n 3. _Cancel bet_"
            )
            msg.body(output)
            responded = True

        if chat_type == "cancel":
            team_name = extract_team(incoming_msg)
            if team_name == "":
                output = "Please mention the team you bet on."
            else:
                cancel_team = IplData().get_team_code(team_name)
                is_canceled, err_resp = BetMaker().cancel_bet(phone_number, cancel_team)
                if is_canceled:
                    output = "Bet Canceled"
                else:
                    output = err_resp
            msg.body(output)
            responded = True

        if chat_type == "leaderboard":
            response = Leaderboard().display_leaderboard()
            msg.body(response)
            responded = True

        if chat_type == "mybet":
            response = BetMaker().get_todays_bet(phone_number)
            msg.body(response)
            responded = True

        if chat_type == "bet":
            bet_save_response = BetMaker().process_bet(
                incoming_msg, profile_name, phone_number
            )
            if bet_save_response.strip != "":
                msg.body(bet_save_response)
                responded = True

        if chat_type == "admin":
            if phone_number == "19195230176":
                response = AdminOperations().process(incoming_msg)
                msg.body(response)
                responded = True
            else:
                msg.body("YOU ARE NOT THE ADMIN, *Suck It!*")
                responded = True

    if not responded:
        msg.body("Please try again with a different bet")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
