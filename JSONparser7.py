import pandas as pd
import orjson as json
from tqdm import tqdm
import numpy as np
from tabulate import tabulate
import os

# insert the filepath destination for the JSON file on your computer between the "" of the FILEPATH variable
FILEPATH = r"C:\Users\nkudamik\Desktop\JSONparser\export-2024-03-08-2033-2279373-21924290757783feb7.json"
COLS = ["id", "subject", "created_at", "updated_at", "via.source.from.name"]
COL_NAMES = ["#", "ID", "Subject", "Requested", "Updated", "Requester"]

def search_tickets(t, df):  
    temp_subject = df['subject']
    
    #easy fix way of formatting this... 
    df['subject'] = df['subject'].str[:35] #limit subject string to 30 characters
    df['created_at'] = df['created_at'].str[:10]
    df['updated_at'] = df['updated_at'].str[:10]
    
    mask = np.column_stack([df[col].astype(str).str.contains(t, na=False, case=False) for col in tqdm(df)])
    print(tabulate(df[COLS].loc[mask.any(axis=1)], headers=COL_NAMES, tablefmt='fancy_grid'))

    df['subject'] = temp_subject
    
    while True:
        try:
            selection = int(input("Enter ticket Index (#) to display or 0 to search again: "))
            if selection == 0:
                break
            print_tickets(selection, df)
        except ValueError:
            print("Invalid Input.")

def print_tickets(s, df): 
    id = df.iloc[s].loc['id']
    subject = df.iloc[s].loc['subject']
    comment = df.iloc[s].loc['comments']
    
    print_list = [f"Ticket: {id} \nSubject: {subject} \nComments:"]
    
    with open("Expand_Ticket.txt", "w", buffering=1, encoding="utf-8") as f:
        os.startfile("Expand_Ticket.txt")
        for item in print_list:
            f.write(f"{item}\n")
        for item in print_comments(comment):
            f.write(f"{item}\n")

def print_comments(comment):
    comment_list = []
    for i in range(0, len(comment)):
        comment_list.append("\u0332".join(f"\nENTRY {i+1}:"))
        comment_list.append(f"\nAuthor ID: {comment[i].get('author_id')}")
        comment_list.append(f"Public: {comment[i].get('public')}")
        comment_list.append(f"\nComment Body:\n {comment[i].get('body')}")
    return comment_list
        
def main():    
    data = [json.loads(line) for line in tqdm(open(FILEPATH, encoding='utf8'), desc="Loading...")]
    print("...normalizing the data...")
    data = pd.json_normalize(data)  
    df = pd.DataFrame(data)

    token = input("Search: ")
    while token !="0":
        search_tickets(token, df)
        token = input("Search (or 0 to quit): ")

    print("Goodbye!")
    os.remove("Expand_Ticket.txt")
    exit()

if __name__ == "__main__":
    main()
