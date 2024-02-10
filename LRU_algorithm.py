from read_file_page import read_file

def LRU(pages, n, capacity): 
    s = []  # Initialize an empty list
    indexes = []  # To store recently used index of pages
    page_faults = 0
    page_hits = 0
    history = []  # Initialize history list to keep track of the state of the page table at each step
    list_page_faults = []

    for i in range(n): 
        if pages[i] not in s: 
            if len(s) < capacity:
                s.append(pages[i])
                indexes.append(i)
            else:
                # Find least recently used and replace it
                lru = min(indexes)
                lru_index = indexes.index(lru)
                s[lru_index] = pages[i]
                indexes[lru_index] = i
            page_faults += 1
            list_page_faults.append('F')
        else: 
            page_hits += 1
            list_page_faults.append('T')
            # Update recent index
            index = s.index(pages[i])
            indexes[index] = i

        history.append(list(s))  # Append the current state of the page table to the history list

    return page_hits, page_faults, history, list_page_faults


reference_string, num_frames = read_file()
reference_list = list(map(str, reference_string.split()))
page_hits, page_faults, history, list_page_faults = LRU(reference_list, len(reference_list), num_frames)

# Print the number of page faults and the history
print("Number of page faults:", page_faults)
print("History of the page table:")
for i, state in enumerate(history, 1):
    print(f"Current number: {reference_list[i-1] }  After reference {i}: {state} - {list_page_faults[i-1]}")