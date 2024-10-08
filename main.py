import SG_Offers as sg
import CACIB_Offers as cacib
import Excel_Setup as es
import Email_Sender as email
import pandas as pd
import datetime as dt


def main():
    day_date = str(dt.date.today())
    filename = "offres_de_stage_" + day_date + ".xlsx"
    
    df_SG = sg.main_SG()
    df_CACIB = cacib.main_CACIB()
    df = pd.concat([df_SG,df_CACIB], ignore_index=True)

    df.to_excel(filename, index=False)
    es.excel_settings(filename)
    email.email_sender(filename)


if __name__ == "__main__":
    main()
