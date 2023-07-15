import math, random, requests

def generateOTP() :
    digits = "0123456789"
    otp = ""
    for i in range(6) :
        otp += digits[math.floor(random.random() * 10)]
    return otp

def sendOtp(phone_no):
    SMS_GATEWAY_API_KEY = "0Y5JdaJXpE2ug1gqBk5jIA"
    SMS_GATEWAY_SENDER_ID = "VTALKI"
    SMS_GATEWAY_CHANNEL = 2
    SMS_GATEWAY_DCS = 0
    SMS_GATEWAY_FLASHSMS = 0
    SMS_GATEWAY_ROUTE = 31

    otp = generateOTP()
    message = str(str(otp) + " is your one time password (OTP) for VTALKIES signup")
    try:
        url = f'https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey={SMS_GATEWAY_API_KEY}&senderid={SMS_GATEWAY_SENDER_ID}&channel={SMS_GATEWAY_CHANNEL}&DCS={SMS_GATEWAY_DCS}&flashsms={SMS_GATEWAY_FLASHSMS}&number={phone_no}&text={message}&route={SMS_GATEWAY_ROUTE}'
        result = requests.post(url).json()
        print(result)
        return otp
    except Exception as e:
        print(e)
        return e