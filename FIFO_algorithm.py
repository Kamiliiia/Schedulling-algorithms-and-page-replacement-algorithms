from collections import defaultdict
from read_file_page import read_file

def FIFO(pages, n, capacity): 
    s = []  # To store elements in memory of size capacity
    indexes = []  # To store recently used index of pages
    page_faults = 0
    page_hits = 0
    history = []  # Initialize history list to keep track of the state of the page table at each step
    list_page_faults=[]

    for i in range(n):  #iterate over the range of pages
        if pages[i] not in s:  #if the page is not in memory
            if len(s) < capacity: #if there is space in memory
                s.append(pages[i]) #add the page to memory
                indexes.append(i) #add the index to the indexes list
            else:
                oldest_page_index = indexes.index(min(indexes)) #find the index of the oldest page
                s[oldest_page_index] = pages[i] #replace the oldest page with the current page
                indexes[oldest_page_index] = i #replace the index of the oldest page with the current index
            page_faults += 1
            list_page_faults.append('F')
        else: 
            page_hits += 1
            list_page_faults.append('T')

        history.append(list(s))  # Append the current state of the page table to the history list

    return page_hits, page_faults, history, list_page_faults  # This line should be at the same indentation level as the for loop


reference_string, num_frames = read_file()
reference_list = list(map(str, reference_string.split()))
page_hits, page_faults, history, list_page_faults = FIFO(reference_list, len(reference_list), num_frames)

# Print the number of page faults and the history
print("Number of page faults:", page_faults)
print("History of the page table:")
for i, state in enumerate(history, 1):
    print(f"Current number: {reference_list[i-1]}  After reference {i}: {state} -  {list_page_faults[i-1]}")