import edgar
import multiprocessing
import os
from es_functions import *

#Uses set difference to take a difference of lines
def process_lines(new_lines, old_lines, output_queue):
    new_lines_set = set(new_lines)
    new_lines_set.difference_update(old_lines)
    output_queue.put(new_lines_set)

#Removes the last generated tsv file and the current updated file to replace
if os.path.exists('main-project/src/newfiles/2024-QTR2.tsv'):
    os.remove('main-project/src/newfiles/2024-QTR2.tsv')
if os.path.exists('main-project/src/newfiles/latest.tsv'):
    os.remove('main-project/src/newfiles/latest.tsv')

print("Generating TSV file...")
#Creates the tsv file
edgar.download_index("main-project/src/newfiles", 2024, "Stock-Finder aery.2@osu.edu", skip_all_present_except_last=False)

#Opens the old file and new file to take a difference
with open('main-project/src/newfiles/2024-QTR1_old.tsv', 'r') as old_file, \
         open('main-project/src/newfiles/2024-QTR2.tsv', 'r') as new_file:

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
if os.path.exists('main-project/src/newfiles/2024-QTR2_old.tsv'):
    os.remove('main-project/src/newfiles/2024-QTR2_old.tsv')
if os.path.exists('main-project/src/newfiles/2024-QTR2.tsv'):
    os.rename('main-project/src/newfiles/2024-QTR2.tsv', 'main-project/src/newfiles/2024-QTR2_old.tsv')

update_database()
