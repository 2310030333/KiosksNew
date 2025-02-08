from twilio.rest import Client

# Replace with your correct SID and Auth Token
twilio_sid = "AC79122928b7cceeea2dba75e6ada22f06"
twilio_auth_token = "c4318d001aeaf999599bdb22b088307c"
client = Client(twilio_sid, twilio_auth_token)

# Test sending an SMS
message = client.messages.create(
    body="This is a test message from Twilio.",
    from_="+14133442339",
    to="+918978713888"
)
print("Message SID:", message.sid)
