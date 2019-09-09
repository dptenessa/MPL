import pandas as pd
import os

def priceFor24():
    for rownum,row in phones_df.iterrows():
        if row.MAPVAT % 24 == 0:
            phones_df.at[rownum, 'Price24'] = row.MAPVAT
        else:
            phones_df.at[rownum, 'Price24'] = int(row.MAPVAT / 24) * 24 + 24

def final_price(HO,priceFor24,tariff_discount,commitment_discount,discount_finance,discount_channel,exceptions):
        final_pr = priceFor24 + tariff_discount + commitment_discount + discount_finance + discount_channel + exceptions
        if final_pr > HO:
            final_pr = HO
        return final_pr

def collect_exceptions(SAPcode,name,manufacturer,model,memory,segment,tariff,commitment,fin_disc,ch_disc,tran_disc):  ### DRAFT
    compare_to=[SAPcode,name,manufacturer,model,memory,segment,tariff,commitment,ch_disc,tran_disc, fin_disc,-999999999]
    conditions_to_check = len(compare_to)-1
    additional_discounts = 0
    for index, row in exception.iterrows():
        count=0
        for i, element in enumerate(row):
            if pd.isnull(element):
                count += 1
            elif str(element) == str(compare_to[i]):
                count += 1
        if count == conditions_to_check:
            additional_discounts = additional_discounts+int(row['Correction'])
    return additional_discounts

###BASIC CONDITIONS:
VAT=1.25
discounts_commitment = pd.read_excel("MPL dashboard.xlsx","Commitment Discounts") #{"jednokratko": -100, 12: 200, 24: 0}
tariffDiscounts = pd.read_excel("MPL dashboard.xlsx","Tariff Discounts") #{"M": 0, "L": -216, "Unlimited": -504, "Hybrid": 120}
discounts_finance = pd.read_excel("MPL dashboard.xlsx","Finance Discounts") #{"None":0,"ebill": -200, "Standing Order": -200, "ebill and standing order":-200}
discounts_channel = pd.read_excel("MPL dashboard.xlsx","Channel Discounts") #{"T Centers":0,"TS IN": 0, "TS OUT":-200, "WebShop": -120, "Save Desk":-320 }
discounts_transactions = pd.read_excel("MPL dashboard.xlsx","Transaction Discounts")
phones_df = pd.read_excel("MPL dashboard.xlsx","Phones")
exception = pd.read_excel("MPL dashboard.xlsx","Exceptions")
phones_df.MAP.apply(float)
phones_df['MAPVAT'] = phones_df.MAP*VAT
priceFor24()
discounts_commitment['link'] = "1"
tariffDiscounts['link'] = "1"
discounts_finance['link'] = "1"
discounts_channel['link'] = "1"
discounts_transactions['link'] = "1"
phones_df['link'] = "1"


def return_phome_info(phone_name_i, memory_i, tariff_i, channel_i, transaction_i, finance_i, commitment_i):    #,memory,tariff,commitment,fin_conditions,channel,transaction):

    if phone_name_i != "":
        phones = phones_df.loc[(phones_df["Name"] == phone_name_i) & (phones_df["Memory"] == int(memory_i))]
    else:
        phones=phones_df
    if tariff_i != "":
        tariff_discounts_selection = tariffDiscounts.loc[tariffDiscounts["Tariff"] == tariff_i]
    else:
        tariff_discounts_selection = tariffDiscounts
    if channel_i != "":
        channel_discounts_selection = discounts_channel.loc[discounts_channel["Channel"] == channel_i]
    else:
        channel_discounts_selection = discounts_channel
    if commitment_i != "":
        commitment_discounts_selection = discounts_commitment.loc[discounts_commitment["Commitment"] == int(commitment_i)]
    else:
        commitment_discounts_selection = discounts_commitment
    if transaction_i != "":
        transactions_discounts_selection = discounts_transactions.loc[discounts_transactions["Transaction"] == transaction_i]
    else:
        transactions_discounts_selection = discounts_transactions
    if finance_i != "":
        finance_discounts_selection = discounts_finance.loc[discounts_finance["Finance_Conditions"] == finance_i]
    else:
        finance_discounts_selection = discounts_finance

    df1 = pd.merge(phones,tariff_discounts_selection, on="link")
    df2 = pd.merge(df1,channel_discounts_selection, on="link")
    df3 = pd.merge(df2, commitment_discounts_selection, on="link")
    df4 = pd.merge(df3, transactions_discounts_selection, on="link")
    df5 = pd.merge(df4, finance_discounts_selection, on="link").drop("link", axis=1)

    for rownum, row in df5.iterrows():
        #SAPcode,name,manufacturer,model,memory,segment,tariff,commitment,fin_disc,ch_disc,tran_disc
        Additional_dicounts = collect_exceptions(row.SAPcode, row.Name, row.Manufacturer,
                                                                    row.Model, row.Memory, row.Segment, row.Tariff,
                                                                    row.Commitment, row.Channel, row.Transaction,
                                                                    row.Finance_Conditions)
        df5.at[rownum, 'Additional_Discounts'] = Additional_dicounts
        df5.at[rownum,'Final_Price'] = final_price(row.HO, row.Price24, row.Tariff_Discount, row.Commitment_Discount,
                                                   row.Finance_Discount, row.Channel_Discount, Additional_dicounts)
    json = df5.to_json(orient='index')
    return json

##a=(return_phome_info("iPhone XS white",128,"L","","","",""))

### For the entire table
##a.to_excel("output.xlsx", index=False)
##os.startfile("output.xlsx")
