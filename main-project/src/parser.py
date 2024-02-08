import csv
import requests
import test

#TSV file name 
tsv_file_path = './src/2024-QTR1.tsv'
data = []
#Headers to access SEC txt files 
headers = {
    'User-Agent': 'Stock-Finder aery.2@osu.edu' 
}

with open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    #Iterate through every row in TSV
    for row in reader:
        if row:
            #Get everything from the row of the TSV into a list
            elements = row[0].split('|')
            #Filter forms by type and date
            if elements[2] == "4" and elements[3] == "2024-02-05":
                url = "https://www.sec.gov/Archives/" + elements[4]
                try:
                    #Get txt file
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        file_content = response.text
                        #Get the transaction code 
                        start_pos = file_content.find("<transactionCode>")
                        end_pos = file_content.find("</transactionCode>")
                        if start_pos != -1 and end_pos != -1:
                            result_text = file_content[start_pos + len("<transactionCode>"):end_pos].strip()
                            #Filter transaction code A
                            if result_text == "A" or result_text == "P":
                                data.append(result_text)

                                #Get the footnotes 
                                start_pos = file_content.find("<footnotes>")
                                end_pos = file_content.find("</footnotes>")
                                if start_pos != -1 and end_pos != -1:
                                    result_text = file_content[start_pos + len("<footnotes>"):end_pos].strip()
                                    data.append(result_text)
                                else:
                                    data.append("")

                                #Get the issuer name 
                                start_pos = file_content.find("<issuerName>")
                                end_pos = file_content.find("</issuerName>")
                                if start_pos != -1 and end_pos != -1:
                                    result_text = file_content[start_pos + len("<issuerName>"):end_pos].strip()
                                    data.append(result_text)
                                else:
                                    data.append("")
                                
                                #Get the issuer trading symbol 
                                start_pos = file_content.find("<issuerTradingSymbol>")
                                end_pos = file_content.find("</issuerTradingSymbol>")
                                if start_pos != -1 and end_pos != -1:
                                    result_text = file_content[start_pos + len("<issuerTradingSymbol>"):end_pos].strip()
                                    data.append(result_text)
                                else:
                                    data.append("")
                                
                                #Pass it to a different python file 
                                test.receive(data)
                                #Reset the list
                                data = []

                    #Catch a possible response error
                    else:
                        print(f"Error: {response.status_code}")
                        print(response.text)

                #Catch a request exception 
                except requests.RequestException as e:
                    print(f"Error: {e}")