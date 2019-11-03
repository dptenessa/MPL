import requests
from tkinter import *
import pandas as pd

discounts_commitment = pd.read_excel("MPL dashboard.xlsx", "Commitment Discounts") #{"jednokratko": -100, 12: 200, 24: 0}
tariffDiscounts = pd.read_excel("MPL dashboard.xlsx", "Tariff Discounts") #{"M": 0, "L": -216, "Unlimited": -504, "Hybrid": 120}
discounts_finance = pd.read_excel("MPL dashboard.xlsx", "Finance Discounts") #{"None":0,"ebill": -200, "Standing Order": -200, "ebill and standing order":-200}
discounts_channel = pd.read_excel("MPL dashboard.xlsx", "Channel Discounts") #{"T Centers":0,"TS IN": 0, "TS OUT":-200, "WebShop": -120, "Save Desk":-320 }
discounts_transactions = pd.read_excel("MPL dashboard.xlsx", "Transaction Discounts")
phones_df = pd.read_excel("MPL dashboard.xlsx", "Phones")

commitments = discounts_commitment['Commitment'].drop_duplicates()
tariffs = tariffDiscounts['Tariff'].drop_duplicates()
finance_conditions = discounts_finance['Finance_Conditions'].drop_duplicates()
channels = discounts_channel['Channel'].drop_duplicates()
transactions = discounts_transactions['Transaction'].drop_duplicates()
phones = phones_df['Name'].drop_duplicates()
memories = phones_df['Memory'].drop_duplicates()

FRONT= "http://127.0.0.1:5000/events?"

param = {}
url = ""

root = Tk()
root.title("Main interface")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 20, padx = 20)

# Create a Tkinter variable
phones_var = StringVar(root)
memory_var = StringVar(root)
tariffs_var = StringVar(root)
commitments_var = StringVar(root)
channels_var = StringVar(root)
transactions_var = StringVar(root)
finance_conditions_var = StringVar(root)

# Dictionary with options
#choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
phones_var.set(phones[0]) # set the default option
memory_var.set(memories[0]) # set the default option
tariffs_var.set("") # set the default option
commitments_var.set("") # set the default option
channels_var.set("") # set the default option
transactions_var.set("") # set the default option
finance_conditions_var.set("") # set the default option

###dropdowns
phonesMenu = OptionMenu(mainframe, phones_var, *phones)
Label(mainframe, text="Choose a phone").grid(row = 1, column = 1)
phonesMenu.grid(row = 2, column =1)
memoryMenu = OptionMenu(mainframe, memory_var, *memories)
Label(mainframe, text="Choose a memory").grid(row = 1, column = 2)
memoryMenu.grid(row = 2, column =2)
tariffMenu = OptionMenu(mainframe, tariffs_var, *tariffs)
Label(mainframe, text="Choose a tariff").grid(row = 1, column = 3)
tariffMenu.grid(row = 2, column =3)
channelMenu = OptionMenu(mainframe, channels_var, *channels)
Label(mainframe, text="Choose a channel").grid(row = 1, column = 4)
channelMenu.grid(row = 2, column =4)
transactionMenu = OptionMenu(mainframe, transactions_var, *transactions)
Label(mainframe, text="Choose a transaction type").grid(row = 1, column = 5)
transactionMenu.grid(row = 2, column =5)
commitmentMenu = OptionMenu(mainframe, commitments_var, *commitments)
Label(mainframe, text="Choose a commitment duration").grid(row=1, column=6)
commitmentMenu.grid(row=2, column=6)
finance_conditionsMenu = OptionMenu(mainframe, finance_conditions_var, *finance_conditions)
Label(mainframe, text="Choose a Finance condition").grid(row = 1, column = 7)
finance_conditionsMenu.grid(row = 2, column =7)

#phone_name, memory, tariff, channel, transaction, commitment, finance
# B = Button(root, text = "send request", command = sendrequest(param))
# B.place(x = 1050,y = 200)

# on change dropdown value
def change_dropdown(*args):
    param[1] = "param1=iPhone XS white"
    if args[0] == 'PY_VAR0':
        param[1] = "param1=" + phones_var.get()
    param[2] = "param2=128"
    if args[0] == 'PY_VAR1':
        param[2] = "param2=" + memory_var.get()
    if args[0] == 'PY_VAR2':
        param[3] = "param3=" + tariffs_var.get()
    if args[0] == 'PY_VAR3':
        param[4] = "param4=" + channels_var.get()
    if args[0] == 'PY_VAR4':
        param[5] = "param5=" + transactions_var.get()
    if args[0] == 'PY_VAR5':
        param[6] = "param6=" + commitments_var.get()
    if args[0] == 'PY_VAR6':
        param[7] = "param7=" + finance_conditions_var.get()
    parameters = []
    for item in param.values():
        if item[-8:] == "dropdown":
            pass
        else:
            parameters.append(item)
    url=FRONT+"&".join(parameters)
    print(url)
    response = requests.get(url)
    text = response.text
    print(text)
    return

# link function to change dropdown
param[1] = phones_var.trace('w', change_dropdown)
param[2] = memory_var.trace('w', change_dropdown)
param[3] = tariffs_var.trace('w', change_dropdown)
param[4] = channels_var.trace('w', change_dropdown)
param[5] = transactions_var.trace('w', change_dropdown)
param[6] = commitments_var.trace('w', change_dropdown)
param[7] = finance_conditions_var.trace('w', change_dropdown)

root.mainloop()