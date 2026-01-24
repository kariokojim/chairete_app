from datetime import datetime

def generate_receipt_no():
    return "RCT-" + datetime.now().strftime("%Y%m%d%H%M%S")
