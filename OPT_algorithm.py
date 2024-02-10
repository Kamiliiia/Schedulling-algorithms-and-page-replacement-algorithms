from read_file_page import read_file

def opt_algorithm(pages, frames):
    page_faults = 0  # Initialize page faults to 0
    page_table = []  # Initialize page table as an empty list
    page_table_history = []  # Initialize page table history as an empty list
    list_page_faults = []

    for page in pages:
        if page not in page_table:  # If the page is not in the page table
            if len(page_table) < frames:  # If the page table is not full
                page_table.append(page)
            else:  # If the page table is full
                future_pages = pages[pages.index(page) + 1:]  # Get the future pages
                if future_pages:  # If there are future pages
                    # Find the page in page_table that will be used the farthest in the future
                    page_to_replace = max(page_table, key=lambda p: future_pages.index(p) if p in future_pages else float('inf'))
                else:  # If there are no future pages, replace the first page in the page table
                    page_to_replace = page_table[0]
                # Replace the page to replace with the current page
                page_table[page_table.index(page_to_replace)] = page
            page_faults += 1  # Increment the page faults
            list_page_faults.append('F')
        else:
            list_page_faults.append('T')
        page_table_history.append(list(page_table))  # Append the page table to the page table history

    return page_faults, page_table_history, list_page_faults

# Read from file
reference_string, num_frames = read_file()

# Convert reference string to list
reference_list = list(map(str, reference_string.split()))

# Run OPT algorithm
page_faults, page_table_history, list_page_faults = opt_algorithm(reference_list, num_frames)

# Print results
print("Number of page faults:", page_faults)
print("Page table history:")
for i, state in enumerate(page_table_history, 1):
    print(f"Current number: {reference_list[i-1] }  After reference {i}: {state} - {list_page_faults[i-1]}")