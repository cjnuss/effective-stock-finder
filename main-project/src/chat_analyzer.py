import requests
import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

#Loads the env file and gets the key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

#OpenAI Client 
client = OpenAI(api_key=openai_api_key)

#Function to make an Open AI request
def process_input(prompt, user_input):
    try:
        #Prompt, have to play with this to get optimal results, user_input are the footnotes
        prompt += f"Based on the following documents, can you explain in a few words why this stock might increase in price: {user_input}\n"
        #Gets and returns the response from Open AI
        gpt_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": prompt}]
        )
        content = gpt_response.choices[0].message.content
        return f"{content}\n"
    #Catches any exception and prints it but returns an empty string so the front end doesn't break
    except OpenAIError as e:
        print(f"Error from OpenAI API: {e}")
        return ""

def getInformation(top5stocks):
    #Original prompt, this does not need to change
    prompt = "You are a helpful assistant.\n"

    #Parallel lists of footnotes, tickers, company names and Open AI results 
    input_list = []
    tickers = []
    descriptions = []
    company_names = []

    #Loops through the stocks
    for stock in top5stocks:
        count = 1
        merged_footnotes = ""
        ticker_added = True
        #Loops through each document for the stock
        for entry in stock:
            #Makes sure ticker and company names are added to the list only once
            if ticker_added:
                tickers.append(entry[3])
                company_names.append(entry[2])
                ticker_added = False
            #Gets all footnotes from a single document into a list
            footnotes = entry[1].split("<footnote id=")[1:]
            #Loops through the footnotes, formats them and concatenates them
            for footnote in footnotes:
                merged_footnotes += "Document Number " + str(count) + ": " + footnote.split(">")[1].split("<")[0] + " "
                count += 1
        #Adds the resulting formatted footnotes to a list 
        input_list.append(merged_footnotes)

    print(tickers)
    print(company_names)
    #Loops through the formatted footnotes and has Open AI analyze them
    for user_input in input_list:
        #Comment this out when not in use to avoid hitting rate limits
        prompt = process_input(prompt, user_input)
        #Appends the results to a different list, change the parameter to prompt if you uncomment the line above
        descriptions.append(prompt)
    return tickers, descriptions, company_names