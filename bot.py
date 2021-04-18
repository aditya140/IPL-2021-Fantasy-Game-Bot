from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from ipl_schedule import IplData

app = Flask(__name__)


def is_greeting(sentence):
    greeting_inputs = (
        "hello",
        "hi",
        "greetings",
        "sup",
        "what's up",
        "hey",
        "good morning",
    )

    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return True


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").upper()
    profile_name = request.values.get("ProfileName", "")

    phone_number = request.values.get("WaId", "")
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    print(phone_number)

    if incoming_msg and is_greeting(incoming_msg):
        output = 'Welcome to the IPL 2021 Fantasy Game Bot. Please enter your bet in this sample format : KKR 40'
        msg.body(output)
        responded = True
        return str(resp)
    else:
        ipl_schedule_data = IplData()
        bet_save_response = ipl_schedule_data.place_bets(incoming_msg, profile_name, phone_number)

        if(bet_save_response.strip != ''):
            msg.body(bet_save_response)
            responded = True

    if not responded:
        msg.body("Please try again with a different bet")

    print(str(resp))

    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
