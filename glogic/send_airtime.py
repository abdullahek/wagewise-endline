import pandas as pd
import africastalking
import numpy as np




def send_airtime_after_survey(num, amt=5):
    username = "ASIS038"
    api_key = "27977c5e42f686f7e2097b296f42ca041a2bd45bed94489ee3ef1c0d11779ae3"
    africastalking.initialize(username, api_key)

    airtime = africastalking.Airtime

    phone_number = num
    currency_code = "ZAR"
    amount = amt

    try:
        response = airtime.send(phone_number=phone_number, amount=amount, currency_code=currency_code)
        print('*'*20)
        print(f"Airtime sent to {num}")
        print(response)
        return 1
    except Exception as e:
        print(f"Encountered an error while sending airtime. More error details below\n {e}")
        return -1



def send_many_retrospective():
    """
    For multiple sending of airtime with a list of numbers. To run just run this as the main file (python send_airtime.py)
    """
    import os

    absolute_path = os.path.dirname(__file__)
    relative_path = "AirtimeTransactions-2023-04-06.xlsx"
    full_path = os.path.join(absolute_path, relative_path)
    print(full_path)
    sheet = pd.read_excel(full_path)
    print(sheet)
    nums =sheet["Recipient"]

    nums_l = []
    for i in nums:
        if i is not None:
            i = "+" + str(i)[:-2]
            nums_l.append(i)
    print(nums_l)
    print(len(nums_l))


    for i in nums_l[:-1]:
        print(nums_l[:-1])
        send_airtime_after_survey(i, 17)






if __name__ == "__main__":
    send_many_retrospective()