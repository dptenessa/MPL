import pandas as pd
import os


def set_prices_for_phones_not_sold_by_A1(df,tariffs_discounts):
    for i, row in tariffs_discounts.iterrows():
        tariff_discount = row["Tariff_Discount"]*24
        df.loc[(df["Final HS price"] == 0) & (df["Tariff Name"] == row["Tariff Name"]),
               "Final HS price"] = df["PRP/Mkt Price"] + tariff_discount
    return df

def Add_exceptions(df):
    for index, row in exception.iterrows():
        search_string = []
        if pd.notnull(row.SAPcode):
            search_string.append('(df["SAPcode"]==row.SAPcode)')
        if pd.notnull(row.Name):
            search_string.append('(df["Name"]==row.Name)')
        if pd.notnull(row.Manufacturer):
            search_string.append('(df["Manufacturer"]==row.Manufacturer)')
        if pd.notnull(row.Model):
            search_string.append('(df["Model"]==row.Model)')
        if pd.notnull(row.Memory):
            search_string.append('(df["Memory"]==row.Memory)')
        if pd.notnull(row.Segment):
            search_string.append('(df["Segment"]==row.Segment)')
        if pd.notnull(row.Tariff):
            search_string.append('(df["Tariff Name"]==row.Tariff)')
        if pd.notnull(row.Commitment):
            search_string.append('(df["Commitment"]==row.Commitment)')
        if pd.notnull(row.Channel):
            search_string.append('(df["Channel"]==row.Channel)')
        if pd.notnull(row.Transaction):
            search_string.append('(df["Transaction"]==row.Transaction)')
        if pd.notnull(row.Finance_Conditions):
            search_string.append('(df["Finance_Conditions"]==row.Finance_Conditions)')
        joint_search_string = " & ".join(search_string)
        cadena = "df.loc[" + joint_search_string + ",'Additional_Discounts']+=row.Correction"
        exec(cadena)


# BASIC CONDITIONS:
VAT = 1.25
recommended_market_prices = pd.read_excel("Recommended prices.xlsx")
recommended_market_prices = recommended_market_prices.loc[(recommended_market_prices['Company'] =="T")]
#recommended_market_prices.rename(columns={"Tariff Name": "Tariff"})
recommended_market_prices.drop(columns=['Ideal MRC', 'Company','Ideal HS price','Ideal TCO'],inplace=True)
discounts_commitment = pd.read_excel("MPL dashboard.xlsx", "Commitment Discounts")
tariffDiscounts = pd.read_excel("MPL dashboard.xlsx", "Tariff Discounts")
discounts_finance = pd.read_excel("MPL dashboard.xlsx", "Finance Discounts")
discounts_channel = pd.read_excel("MPL dashboard.xlsx", "Channel Discounts")
discounts_transactions = pd.read_excel("MPL dashboard.xlsx", "Transaction Discounts")
phones_df = pd.read_excel("MPL dashboard.xlsx", "Phones")
exception = pd.read_excel("MPL dashboard.xlsx", "Exceptions")
phones_df.MAP.apply(float)
#phones_df['Reference_Price'] = (phones_df.MAP + phones_df.Credit_Note) * VAT
discounts_commitment['link'], tariffDiscounts['link'], discounts_finance['link'], discounts_channel['link'], \
discounts_transactions['link']= ["1", "1", "1", "1", "1"]


def return_phome_info(phone="", memory="", tariff="", channel="", transaction="", commitment="", finance_conditions=""):
    if phone != "":
        phones = phones_df.loc[(phones_df["Name"] == phone) & (phones_df["Memory"] == int(memory))]
    else:
        phones = phones_df
    if tariff != "":
        tariff_discounts_selection = tariffDiscounts.loc[tariffDiscounts["Tariff"] == tariff]
    else:
        tariff_discounts_selection = tariffDiscounts
    if channel != "":
        channel_discounts_selection = discounts_channel.loc[discounts_channel["Channel"] == channel]
    else:
        channel_discounts_selection = discounts_channel
    if commitment != "":
        commitment_discounts_selection = discounts_commitment.loc[discounts_commitment["Commitment"] == int(commitment)]
    else:
        commitment_discounts_selection = discounts_commitment
    if transaction != "":
        transactions_discounts_selection = discounts_transactions.loc[
            discounts_transactions["Transaction"] == transaction]
    else:
        transactions_discounts_selection = discounts_transactions
    if finance_conditions != "":
        finance_discounts_selection = discounts_finance.loc[
            discounts_finance["Finance_Conditions"] == finance_conditions]
    else:
        finance_discounts_selection = discounts_finance

    web_conditions = int(discounts_channel.loc[discounts_channel["Channel"] == "WebShop"]["Channel_Discount"])
    recommended_market_prices_plus = set_prices_for_phones_not_sold_by_A1(recommended_market_prices, tariffDiscounts)
    df0 = pd.merge(phones,recommended_market_prices_plus,on=["Manufacturer","Model","Memory"])
    df1 = pd.merge(df0, tariff_discounts_selection, on="Tariff Name")
    df1['Reference_Price'] = df1["PRP/Mkt Price"]
    df1["Mkt Adjustment"] = -(df1["PRP/Mkt Price"]-df1["Final HS price"])/24 - df1["Tariff_Discount"]
    df1["Final HS price"] -= web_conditions
    df2 = pd.merge(df1, channel_discounts_selection, on="link")
    df3 = pd.merge(df2, commitment_discounts_selection, on="link")
    df4 = pd.merge(df3, transactions_discounts_selection, on="link")
    df5 = pd.merge(df4, finance_discounts_selection, on="link").drop("link", axis=1)
    df5['Additional_Discounts'], df5['Instalment rounded'] = [0, 0]
    Add_exceptions(df5)
    df5['Net Price After All Discounts'] = ((df5['Final HS price'] + df5['Commitment_Discount'] + df5[
        'Finance_Discount'] + df5['Channel_Discount'] + df5['Additional_Discounts'])/24).astype(int)*24
    for i, row in df5.iterrows():
        if row['Net Price After All Discounts'] > row['HO']:
            row['Net Price After All Discounts'] = row['HO']
    df5['Instalment rounded'] = (df5['Net Price After All Discounts'] / 24).astype(int)


    # For the entire table
    book_open=True
    while book_open:
        try:
            df5.to_excel("output.xlsx", index=False)
            os.startfile("output.xlsx")
            book_open = False
        except:
            answer = input("Please close the output.xlsx file so data can be refreshed and press Enter")

    # json = df5.to_json(orient='index')
    # return json

return_phome_info()
