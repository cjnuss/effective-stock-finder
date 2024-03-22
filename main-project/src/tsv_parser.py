import csv
import requests
import multiprocessing

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
    #Get everything from the row of the TSV into a list
    elements = row.split('|')
    #Filter forms by type and date (if needed)
    if elements[2] == "4":
        url = "https://www.sec.gov/Archives/" + elements[4]
        #Get txt file
        response = get_response(url, headers)
        if response != "":
            #Get the transaction code 
            start_pos = response.find("<transactionCode>")
            end_pos = response.find("</transactionCode>")
            if start_pos != -1 and end_pos != -1:
                result_text = response[start_pos + len("<transactionCode>"):end_pos].strip()
                #Filter transaction code A
                if result_text == "A" or result_text == "P":
                    data.append(result_text)

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
                    data.append(elements[3])
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
                everything.append(result)

    return everything
