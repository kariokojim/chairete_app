import requests
from flask import current_app


def format_phone(phone):
    phone = str(phone).strip().replace(" ", "")

    if phone.startswith("07"):
        return "254" + phone[1:]

    if phone.startswith("01"):
        return "254" + phone[1:]

    if phone.startswith("+254"):
        return phone[1:]

    return phone


def send_sms(phone, message):
    try:
        phone = format_phone(phone)

        url = current_app.config["CELCOM_SMS_URL"]
        partner_id = current_app.config["CELCOM_PARTNER_ID"]
        api_key = current_app.config["CELCOM_API_KEY"]
        shortcode = current_app.config["CELCOM_SHORTCODE"]

        payload = {
            "partnerID": partner_id,
            "apikey": api_key,
            "mobile": phone,
            "message": message,
            "shortcode": shortcode,
            "pass_type": "plain"
        }

        response = requests.post(
            url,
            data=payload,
            timeout=20
        )

        return {
            "success": response.status_code == 200,
            "response": response.text
        }

    except Exception as e:
        return {
            "success": False,
            "response": str(e)
        }