from collections import defaultdict
from read_file_page import read_file

def LFU(pages, n, capacity): 
    s = []  # To store elements in memory of size capacity
    indexes = []  # To store recently used index of pages
    page_counter = defaultdict(int)  # To store frequency of pages
    page_faults = 0
    page_hits = 0
    history = []  # Initialize history list to keep track of the state of the page table at each step
    first_occurrence = [None] * 10  # List to store the first occurrence of each page
    list_page_faults=[]

    for i in range(n):  #iterate over the range of pages
        if pages[i] not in s:  #if the page is not in memory
            if len(s) < capacity: #if there is space in memory
                s.append(pages[i]) #add the page to memory
                indexes.append(i) #add the index to the indexes list
                if first_occurrence[int(pages[i])] is None: # If the page has not been referenced before
                    first_occurrence[int(pages[i])] = i # Set the first occurrence of the page to the current index
            else:
                lfu = min(s, key=lambda page: (page_counter[page], first_occurrence[int(page)])) #if there is no space in memory, find the least frequently used page
                lfu_index = s.index(lfu) #find the index of the least frequently used page
                s[lfu_index] = pages[i] #replace the least frequently used page with the current page
                indexes[lfu_index] = i #replace the index of the least frequently used page with the current index
                if first_occurrence[int(pages[i])] is None:  # If the page has not been referenced before
                    first_occurrence[int(pages[i])] = i  # Set the first occurrence of the page to the current index
            page_faults += 1
            list_page_faults.append('F')
        else: 
            page_hits += 1
            # Update recent index
            index = s.index(pages[i])
            indexes[index] = i
            list_page_faults.append('T')

        page_counter[pages[i]] += 1
        history.append(list(s))  # Append the current state of the page table to the history list

    return page_hits, page_faults, history, list_page_faults  # This line should be at the same indentation level as the for loop


reference_string, num_frames = read_file()
reference_list = list(map(str, reference_string.split()))
page_hits, page_faults, history, list_page_faults = LFU(reference_list, len(reference_list), num_frames)

# Print the number of page faults and the history
print("Number of page faults:", page_faults)
print("History of the page table:")
for i, state in enumerate(history, 1):
    print(f"Current number: {reference_list[i-1]}  After reference {i}: {state} -  {list_page_faults[i-1]}")