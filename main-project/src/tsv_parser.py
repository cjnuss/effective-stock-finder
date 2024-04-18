import csv
import requests
import multiprocessing
import yfinance as yf
from datetime import datetime, timedelta

#Gets the txt file content 
def get_response(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        
        #Catch a possible response error
        else:
            print(f"Error: {response.status_code}")
            return ""
        
    #Catch a request exception 
    except requests.RequestException as e:
        print(f"Error: {e}")
        return ""

#Returns the list containing information from a single row
def process_row(row, headers):
    data = []
    transaction_code = ""
    counter = 0

    #Get everything from the row of the TSV into a list
    elements = row.split('|')
    #Filter forms by type and date (if needed)
    if elements[2] == "4":
        url = "https://www.sec.gov/Archives/" + elements[4]
        #Get txt file
        response = get_response(url, headers)
        if response != "":
            check = False
            start_pos = response.find("<transactionCode>")

            #Check if any of the codes are S or P instead of just the first code
            while start_pos != -1:
                end_pos = response.find("</transactionCode>", start_pos)
                result_text = response[start_pos + len("<transactionCode>"):end_pos].strip()
                #Filter transaction code S and P
                if result_text == "S" or result_text == "P":
                    check = True
                    #Store the transaction code
                    transaction_code = result_text
                start_pos = response.find("<transactionCode>", end_pos)

            if check:
                data.append(transaction_code)

                #Get the footnotes 
                start_pos = response.find("<footnotes>")
                end_pos = response.find("</footnotes>")
                if start_pos != -1 and end_pos != -1:
                    result_text = response[start_pos + len("<footnotes>"):end_pos].strip()
                    data.append(result_text)
                else:
                    data.append("")

                #Get the issuer name 
                start_pos = response.find("<issuerName>")
                end_pos = response.find("</issuerName>")
                if start_pos != -1 and end_pos != -1:
                    result_text = response[start_pos + len("<issuerName>"):end_pos].strip()
                    data.append(result_text)
                else:
                    data.append("")

                #Get the issuer trading symbol 
                start_pos = response.find("<issuerTradingSymbol>")
                end_pos = response.find("</issuerTradingSymbol>")
                if start_pos != -1 and end_pos != -1:
                    result_text = response[start_pos + len("<issuerTradingSymbol>"):end_pos].strip()
                    data.append(result_text)
                else:
                    data.append("")
                    
                #Get transaction share price 
                valueFind = response.find("<transactionPricePerShare>")
                price = "0"

                #Loop until a value is found or no more transactionPricePerShare tags are left
                while valueFind != -1:
                    end_pos = response.find("</transactionPricePerShare>", valueFind)
                    if end_pos != -1:
                        value_start_pos = response.find("<value>", valueFind, end_pos)
                        value_end_pos = response.find("</value>", valueFind, end_pos)
                        if value_start_pos != -1 and value_end_pos != -1:
                            result_text = response[value_start_pos + len("<value>"):value_end_pos].strip()
                            if result_text.replace('.', '', 1).isdigit():
                                price = result_text
                                break

                    valueFind = response.find("<transactionPricePerShare>", end_pos)
                    
                data.append(price)

                #Divide file into multiple smaller files for each transaction code in the larger file
                transactions = response.split("<transactionCode>")
                volume = 0

                #Loop through all the smaller files to find volume and sum them up 
                for transaction in transactions[1:]:
                    code = transaction.split("</transactionCode>")[0]
                    valueFind = transaction.find("<transactionShares>")
                    end_pos = transaction.find("</transactionShares>", valueFind)
                    if code.strip() == transaction_code:
                        counter += 1
                        if valueFind and end_pos != -1:
                            value_start_pos = transaction.find("<value>", valueFind, end_pos)
                            value_end_pos = transaction.find("</value>", value_start_pos, end_pos)
                            if value_start_pos != -1 and value_end_pos != -1:
                                result_text = transaction[value_start_pos + len("<value>"):value_end_pos].strip()
                                volume += float(result_text)
                    
                data.append(str(volume))

                #Append date
                data.append(elements[3])

                #Append the number of P/S
                data.append(counter)

    return data

def tsv_to_data():

    #TSV file name 
    tsv_file_path = 'main-project/src/newfiles/latest.tsv'
    everything = []
    #Headers to access SEC txt files 
    headers = {
    'User-Agent': 'Stock-Finder aery.2@osu.edu' 
    }

    #Opens the files and gets the rows and total number of rows
    with open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        lines = list(reader)

    #Creates a pool of processes which is equal to the number of CPU cores
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        #Iterate through every row in TSV
        for row in lines:

            #Executes the function as a seperate process and makes sure it ends before everything is returned 
            result = pool.apply(process_row, args=(row[0], headers))
            if result and result != []:
                ticker = result[3]
                footnotes = result[1]

                #Check if the stock is listed
                try: 
                    #Get last trading day
                    last_day = datetime.today().date()

                    #Set the last trading day to Friday if its Saturday or Sunday
                    if last_day.weekday() == 5:  
                        last_day = last_day - timedelta(days=1)
                    elif last_day.weekday() == 6:  
                        last_day = last_day - timedelta(days=2)

                    #Get historical data
                    response = yf.Ticker(ticker)
                    price = response.history(period="1d")["Close"].iloc[-1]

                except Exception as e:
                    price = ""

                if price != "" and ticker != "NONE" and not((footnotes.__contains__("purchasing") or footnotes.__contains__("Purchasing")) and footnotes.__contains__("plan")):
                    #print(result)
                    everything.append(result)
                    
    return everything