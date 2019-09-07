import pandas as pd
import os

class phone():

    def __init__(self, SAPcode, name, manufacturer, model, memory,segment, MAP, HO):
        self.SAPcode = SAPcode
        self.manufacturer = manufacturer
        self.name = name
        self.model = model
        self.memory = memory
        self.segment = segment
        self.MAP = MAP
        self.MAPVAT = MAP*(1+VAT)
        self.HO = HO
        self.priceFor24 = int(self.MAPVAT / 24) * 24  # adds 24hrk to price in exact cases -> need to find solution

    def add_discount_tariff(self, tariff_dicount):
        self.tariff_discount = tariff_dicount

    def add_discount_commitment(self, commitment_discount):
        self.commitment_discount = commitment_discount

    def add_discount_finance(self, finance_discount):
        self.discount_finance = finance_discount

    def add_discount_channel(self, channel_discount):
        self.discount_channel = channel_discount

    def final_price(self, exception):
        final_price = self.priceFor24 + self.tariff_discount + self.commitment_discount + self.discount_finance\
                      + self.discount_channel + exception
        if final_price > self.HO:
            final_price = self.HO
        return final_price

def collect_exceptions(SAPcode,name,manufacturer,model,memory,segment,tariff,commitment,fin_disc,ch_disc,tran_disc):  ### DRAFT
    compare_to=[SAPcode,name,manufacturer,model,memory,segment,tariff,commitment,ch_disc,tran_disc, fin_disc,-999999999]
    conditions_to_check=len(compare_to)-1
    additional_discounts=0
    for index, row in exception.iterrows():
        count=0
        for i, element in enumerate(row):
            if pd.isnull(element):
                count += 1
            elif element == compare_to[i]:
                count += 1
        if count == conditions_to_check:
            additional_discounts = additional_discounts+int(row['Correction'])
    return additional_discounts

###BASIC CONDITIONS:
VAT=.25
discounts_commitment = pd.read_excel("MPL dashboard.xlsx","Commitment Discounts") #{"jednokratko": -100, 12: 200, 24: 0}
tariffDiscounts = pd.read_excel("MPL dashboard.xlsx","Tariff Discounts") #{"M": 0, "L": -216, "Unlimited": -504, "Hybrid": 120}
discounts_finance = pd.read_excel("MPL dashboard.xlsx","Finance Discounts") #{"None":0,"ebill": -200, "Standing Order": -200, "ebill and standing order":-200}
discounts_channel = pd.read_excel("MPL dashboard.xlsx","Channel Discounts") #{"T Centers":0,"TS IN": 0, "TS OUT":-200, "WebShop": -120, "Save Desk":-320 }
discounts_transactions = pd.read_excel("MPL dashboard.xlsx","Transaction Discounts")
phones_df = pd.read_excel("MPL dashboard.xlsx","Phones")
exception = pd.read_excel("MPL dashboard.xlsx","Exceptions")

phones = []
for index, row in phones_df.iterrows():
    phones.append(phone(row.SAPcode, row.Name, row.Manufacturer, row.Model, row.Memory,row.Segment, row.MAP, row.HO))
total_phones=phones.__len__()
phones_to_go = total_phones
df = pd.DataFrame(columns=['SAP code', 'SKU','Manufacturer','Model','Memory','Segment', 'Tariff', 'Commitment','Financial Conditions','Channel',"Transaction","Final Price"])
row = 0
print("% completion:")
for SKU in phones:
    for not_used1, tariff in tariffDiscounts.iterrows():
        for not_used2, commitment in discounts_commitment.iterrows():
            for not_used3, ch_disc in discounts_channel.iterrows():
                for not_used4, tran_disc in discounts_transactions.iterrows():
                    for not_used5, fin_disc in discounts_finance.iterrows():
                        SAPcode = SKU.SAPcode
                        name = SKU.name
                        manufacturer = SKU.manufacturer
                        model = SKU.model
                        memory = SKU.memory
                        segment = SKU.segment
                        SKU.add_discount_tariff(tariff['Discount'])
                        SKU.add_discount_commitment(commitment['Discount'])
                        SKU.add_discount_finance(fin_disc['Discount'])
                        SKU.add_discount_channel(ch_disc['Discount'])
                        SKU.add_discount_channel(tran_disc['Discount'])
                        additional_discounts = collect_exceptions(SAPcode, name, manufacturer, model, memory, segment, tariff.Type, commitment.Type, fin_disc.Type, ch_disc.Type,tran_disc.Type)
                        final_price = SKU.final_price(additional_discounts)
                        df.loc[row] =[SAPcode, name,manufacturer,model,memory,segment, tariff.Type, commitment.Type, fin_disc.Type, ch_disc.Type,tran_disc.Type, final_price]
                        row += 1
    phones_to_go = phones_to_go-1
    print('{:.0%}'.format(phones_to_go/total_phones))
df.to_excel("output.xlsx", index=False)
os.startfile("output.xlsx")