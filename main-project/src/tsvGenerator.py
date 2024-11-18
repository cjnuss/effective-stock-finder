import edgar
import multiprocessing
import os
from es_functions import *
from datetime import datetime, timedelta

#Uses set difference to take a difference of lines
def process_lines(new_lines, old_lines, output_queue):
    new_lines_set = set(new_lines)
    new_lines_set.difference_update(old_lines)
    output_queue.put(new_lines_set)

#Gets the current year and quarter 
def get_current_year_and_quarter():
    today = datetime.now()
    year = today.year
    month = today.month
    quarter = (month - 1) // 3 + 1
    return year, quarter

if __name__ == '__main__':

    #Get current year and quarter
    current_year, current_quarter = get_current_year_and_quarter()

    #Removes the last generated tsv file and the current updated file to replace
    if os.path.exists(f'main-project/src/newfiles/{current_year}-QTR{current_quarter}.tsv'):
        os.remove(f'main-project/src/newfiles/{current_year}-QTR{current_quarter}.tsv')
    if os.path.exists('main-project/src/newfiles/latest.tsv'):
        os.remove('main-project/src/newfiles/latest.tsv')

    print("Generating TSV file...")
    #Creates the tsv file
    edgar.download_index("main-project/src/newfiles", current_year, "Stock-Finder aery.2@osu.edu", skip_all_present_except_last=False)


    #Gets today's date
    today = datetime.now()

    #Checks for a quarter change day
    if today.month in {1, 4, 7, 10} and today.day == 1:
        previous_day = today - timedelta(days=1)
    else:
        previous_day = today

    #Gets the year of quarter of yesterday 
    prev_year = previous_day.year
    prev_quarter = (previous_day.month - 1) // 3 + 1
    
    #Opens the old file and new file to take a difference
    with open(f'main-project/src/newfiles/{prev_year}-QTR{prev_quarter}_old.tsv', 'r') as old_file, \
            open(f'main-project/src/newfiles/{current_year}-QTR{current_quarter}.tsv', 'r') as new_file:

        #Gets all the lines in both files and converts old one to a set for easy manipulation
        old_lines = set(old_file.readlines())
        new_lines = new_file.readlines()
        num_processes = multiprocessing.cpu_count()

        #Calculates the amount of parallel processes to run 
        chunk_size = len(new_lines) // num_processes

        #Creates the queue
        output_queue = multiprocessing.Manager().Queue()

        processes = []

        #Loops through the available CPU cores 
        for i in range(num_processes):
            #Gets the starting index and ending index of the chunk of lines to be processed by a particular core
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < num_processes - 1 else len(new_lines)

            #Creates a new process for the cpu core with the chunk of lines
            process = multiprocessing.Process(target=process_lines, args=(new_lines[start_idx:end_idx], old_lines, output_queue))
            process.start()

            #Adds the running processes to a list 
            processes.append(process)

        #Makes sure all processes end before the remaining code is run 
        for process in processes:
            process.join()

        #Makes 1 set of resulting lines after taking a difference from all processes
        result_set = set()
        while not output_queue.empty():
            result_set.update(output_queue.get())

        #Writes the resulting lines into a new tsv
        with open('main-project/src/newfiles/latest.tsv', 'w') as output_file:
            for line in result_set:
                output_file.write(line)

    #Removes the old file and renames the new file to old file 
    if os.path.exists(f'main-project/src/newfiles/{prev_year}-QTR{prev_quarter}_old.tsv'):
        os.remove(f'main-project/src/newfiles/{prev_year}-QTR{prev_quarter}_old.tsv')
    if os.path.exists(f'main-project/src/newfiles/{current_year}-QTR{current_quarter}.tsv'):
        os.rename(f'main-project/src/newfiles/{current_year}-QTR{current_quarter}.tsv', f'main-project/src/newfiles/{current_year}-QTR{current_quarter}_old.tsv')

    #Loops through previous quarters and removes the files 
    for quarter in range(1, current_quarter):
        previous_file = f"main-project/src/newfiles/{current_year}-QTR{quarter}.tsv"
        if os.path.exists(previous_file):
            os.remove(previous_file)

    update_database()
