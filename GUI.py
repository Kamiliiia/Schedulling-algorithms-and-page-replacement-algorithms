import tkinter as tk 
from FCFS import FCFS_algorithm
from SJF import SJF_algorithm   
from FCFS_with_priority import FCFS_with_priority
from read_file_processes import read_processes
from read_file_page import read_file
from FIFO_algorithm import FIFO as FIFO_algorithm
from OPT_algorithm import opt_algorithm
from LRU_algorithm import LRU as LRU_algorithm
from LFU_algorithm import LFU as LFU_algorithm
import time
import threading
import sys
import random
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#FCFS
def FCFS_GUI():
    for widget in window.winfo_children():
        widget.destroy()

    # Create a main frame
    window.configure(bg='red')
    main_frame = tk.Frame(window, bg='red')
    main_frame.pack(fill='both', expand=1)

    # Create a canvas inside the main frame
    canvas = tk.Canvas(main_frame, bg='red')
    canvas.pack(side='left', fill='both', expand=1)

    # Add a scrollbar to the main frame, and link it to the canvas
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to place the labels
    frame = tk.Frame(canvas, bg='red')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    #stop button
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')

    ad_process=0
    def add_process():
        # Create a new window
        add_window = tk.Toplevel(window)
        add_window.title("Add Process")

        # Create an entry field for the execution time
        execution_label = tk.Label(add_window, text="Execution Time: ")
        execution_label.pack(side='left')
        execution_entry = tk.Entry(add_window)
        execution_entry.pack(side='left')

        # Create a function to confirm the addition of the new process
        def confirm():
            ad_process=1 #set add_process to 1 to indicate that a new process has been added
            # Validate the input
            execution_time = int(execution_entry.get())
            if execution_time <= 0:
                messagebox.showerror("Error", "Execution time must be greater than 0.")
                return
            with open("input.txt", "r") as file:
                lines = file.readlines()
            priority=6 #set priority to 6 for FCFS
            # Add the new process to the file
            with open("input.txt", "w") as file:
                for i, line in enumerate(lines):
                    if i == 0:
                        file.write(line.strip() + f" {max(arriving_times) + 1}\n")
                    elif i == 1:
                        file.write(line.strip() + f" {execution_time}\n")
                    elif i == 2:
                        file.write(line.strip() + f" {priority}\n")
                    else:
                        file.write(line)


            if ad_process==1:
                #create a label for the new process
                process_label = tk.Label(frame, text=f"Process P{len(number_process)} added. Refresh to see results.")
                process_label.grid(row=len(number_process)+5, column=4, columnspan=5, padx=100, pady=5, sticky='ew')

            # Start the simulation of the new process
            threading.Thread(target=simulate_process, args=(len(number_process), max(arriving_times) + 1, execution_time, max(arriving_times) + 1 + execution_time)).start()


            # Close the add window
            add_window.destroy()

        # Create a confirm button
        confirm_button = tk.Button(add_window, text="Confirm", command=confirm)
        confirm_button.pack()

        

    # Create a button for adding processes
    add_button = tk.Button(window, text='Add Process', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=add_process)
    add_button.place(relx=0.0, rely=0.0, anchor='nw')

    

    #create a label for the algorithm name
    label = tk.Label(frame, text="FCFS ", font=('Cambria', 20), bg='red' )
    label.grid(row=0, column=4, columnspan=5, padx=500, sticky='ew')

    #read calculated values from FCFS_algorithm()
    number_process, arriving_times, execution_times, exit_times, turnaround_times, waiting_times, average_turnaround_time, average_waiting_time = FCFS_algorithm()

    #create a list of labels for the processes
    process_labels = [tk.Label(frame, text=f"Process {number_process[i]}: waiting for arrive at time {arriving_times[i]} ") for i in range(len(exit_times))]
    for i, process_label in enumerate(process_labels):
        process_label.grid(row=i+1, column=4, columnspan=5, padx=100, pady=5, sticky='ew')
    

    #Display the results in the GUI
    def simulate_process(i, arrival_time, execution_time, exit_time):
        # Wait for the process to arrive
        time.sleep(arrival_time)

        # Update the label to show the process has arrived
        process_labels[i].config(text=f"Process {number_process[i]}: arrived. Waiting for execution")
        window.update()

        # Pause for the execution time of the process
        time.sleep(exit_time - arrival_time - execution_time)
        process_labels[i].config(text=f"Process {number_process[i]} executing {execution_times[i]} ")
        window.update()
        time.sleep(exit_time - arrival_time - waiting_times[i])
        # Update the label to show the process has finished
        process_labels[i].config(text=f"Process {number_process[i]} finished at time {exit_time}")
        window.update()

    #Display the results in the GUI
    for i, (arrival_time, execution_time, exit_time) in enumerate(zip(arriving_times, execution_times, exit_times)):
        threading.Thread(target=simulate_process, args=(i, arrival_time, execution_time, exit_time)).start()


    #display the average turnaround time and average waiting time
    average_turnaround_time_label = tk.Label(frame, text="Average turnaround time: " + str(average_turnaround_time), font=('Cambria', 15), bg='red' )  
    average_turnaround_time_label.grid(row=i+2, column=4, columnspan=5, pady=5, sticky='ew')
    average_waiting_time_label = tk.Label(frame, text="Average waiting time: " + str(average_waiting_time), font=('Cambria', 15), bg='red' )
    average_waiting_time_label.grid(row=i+3, column=4, columnspan=5, pady=5, sticky='ew')
    window.update()

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

    def display_gantt_chart(processes):
        # Create a new top-level window
        gantt_window = tk.Toplevel(window)
        gantt_window.title("Gantt Chart")

        fig, ax = plt.subplots(figsize=(10, 5))

        processes.sort(key=lambda x: x[3])  # Sort by finish time
        current_y = 0

        for process in processes:
            ax.barh(y=current_y, width=process[2], left=process[3] - process[2], label=f"Process {process[0]}")
            current_y += 1

        ax.set_xlabel("Time")
        ax.set_ylabel("Process ID")
        ax.set_title("Gantt Chart")

        ax.legend(loc="upper right")
        ax.invert_yaxis()  # Display processes from top to bottom

        # Create a canvas and add the plot to it
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    #sumarise the results in a table
    #Define the summary function
    def summary(number_process, arriving_times, execution_times, exit_times, turnaround_times, waiting_times, average_turnaround_time, average_waiting_time):
        for widget in window.winfo_children():
            widget.destroy()

        # Create a main frame
        window.configure(bg='red')
        main_frame = tk.Frame(window, bg='red')
        main_frame.pack(fill='both', expand=1)

        # Create a canvas inside the main frame
        canvas = tk.Canvas(main_frame, bg='red')
        canvas.pack(side='left', fill='both', expand=1)

        # Add a scrollbar to the main frame, and link it to the canvas
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to place the labels
        frame = tk.Frame(canvas, bg='red')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        #create a label for the algorithm name
        label = tk.Label(frame, text="FCFS ", font=('Cambria', 20), bg='red' )
        label.grid(row=0, column=0, columnspan=5, padx=500, sticky='ew')

        #create table headers
        headers = ['Process', 'Arriving time', 'Execution time', 'Exit time', 'Turnaround', 'Waiting']
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Cambria', 15), bg='red' ).grid(row=1, column=i, padx=10, pady=5, sticky='ew')

        #create table rows
        for i, (arrival_time, execution_time, exit_time, turnaround_time, waiting_time) in enumerate(zip(arriving_times, execution_times, exit_times, turnaround_times, waiting_times)):
            values = [number_process[i], arrival_time, execution_time, exit_time, turnaround_time, waiting_time]
            for j, value in enumerate(values):
                tk.Label(frame, text=value, font=('Cambria', 15), bg='red' ).grid(row=i+2, column=j)

        #display the average turnaround time and average waiting time
        tk.Label(frame, text="Average turnaround time: " + str(average_turnaround_time), font=('Cambria', 15), bg='red' ).grid(row=i+3, column=2, columnspan=5, pady=5, sticky='ew')
        tk.Label(frame, text="Average waiting time: " + str(average_waiting_time), font=('Cambria', 15), bg='red' ).grid(row=i+4, column=2, columnspan=5, pady=5, sticky='ew')

        #make a button to go back to the main menu
        button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=main)
        button1.grid(row=i+5, column=0, columnspan=5, pady=5, padx=50, sticky='ew')

        #make a button to display the gantt chart
        button4 = tk.Button(frame, text='View Gantt Chart', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=lambda: display_gantt_chart(list(zip(number_process, arriving_times, execution_times, exit_times))))
        button4.grid(row=i+6, column=4, columnspan=5, pady=5, sticky='ew')

        #update the scrollregion
        window.update()
        canvas.config(scrollregion=canvas.bbox('all'))


    #make a button to view summary
    button3=tk.Button(frame, text='View summary', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=lambda: summary(number_process, arriving_times, execution_times, exit_times, turnaround_times, waiting_times, average_turnaround_time, average_waiting_time))
    button3.grid(row=i+4, column=4, columnspan=5, pady=5, sticky='ew')
    window.update()

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))  

#SJF
def SJF_GUI():
    for widget in window.winfo_children():
        widget.destroy()

    # Create a main frame
    window.configure(bg='red')
    main_frame = tk.Frame(window, bg='red')
    main_frame.pack(fill='both', expand=1)

    # Create a canvas inside the main frame
    canvas = tk.Canvas(main_frame, bg='red')
    canvas.pack(side='left', fill='both', expand=1)

    # Add a scrollbar to the main frame, and link it to the canvas
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to place the labels
    frame = tk.Frame(canvas, bg='red')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    #stop button
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')

    #create a label for the algorithm name
    label = tk.Label(frame, text="SJF ", font=('Cambria', 20), bg='red' )
    label.grid(row=0, column=4, columnspan=5, padx=500, sticky='ew')

    #read calculated values from SJF_algorithm()
    gantt_chart, completed, average_turnaround_time, average_waiting_time = SJF_algorithm()

    #create a list of labels for the processes
    process_labels = [tk.Label(frame, text=f"Process {gantt_chart[i]}: Waiting ") for i in range (0,(len(gantt_chart)))]
    for i, process_label in enumerate(process_labels):
        #if number of process is idle then display next process which is not idle
        if gantt_chart[i] == "Idle":
            process_labels[i].config(text=f"Process {gantt_chart[i+1]}: Waiting ")

        process_label.grid(row=i+1, column=4, columnspan=5, padx=100, pady=5, sticky='ew')

     #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

    #Display the results in the GUI
    def simulate_process(i, process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time):
        # Wait for the process to arrive
        time.sleep(arrival_time)

        # Update the label to show the process has arrived
        process_labels[i].config(text=f"Process {process_id}: arrived. Waiting for execution")
        window.update()
        time.sleep(completion_time - arrival_time - execution_time)
        # Update the label to show the process has started executing
        process_labels[i].config(text=f"Process {process_id} executing {execution_time} ")
        window.update()
        time.sleep(completion_time - arrival_time - waiting_time)
        # Update the label to show the process has finished
        process_labels[i].config(text=f"Process {process_id} finished at time {completion_time}")
        window.update()

    #Display the results in the GUI
    for i, (process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time) in enumerate(completed.values()):
        threading.Thread(target=simulate_process, args=(i, process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time)).start()
    
    #display the average turnaround time and average waiting time
    average_turnaround_time_label = tk.Label(frame, text="Average turnaround time: " + str(average_turnaround_time), font=('Cambria', 15), bg='red' )
    average_turnaround_time_label.grid(row=i+2, column=4, columnspan=5, pady=5, sticky='ew')
    average_waiting_time_label = tk.Label(frame, text="Average waiting time: " + str(average_waiting_time), font=('Cambria', 15), bg='red' )
    average_waiting_time_label.grid(row=i+3, column=4, columnspan=5, pady=5, sticky='ew')
    window.update()

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

    def display_gantt_chart(processes):
        # Create a new top-level window
        gantt_window = tk.Toplevel(window)
        gantt_window.title("Gantt Chart")

        fig, ax = plt.subplots(figsize=(10, 5))

        processes.sort(key=lambda x: x[3])  # Sort by finish time
        current_y = 0

        for process in processes:
            ax.barh(y=current_y, width=process[2], left=process[3] - process[2], label=f"Process {process[0]}")
            current_y += 1

        ax.set_xlabel("Time")
        ax.set_ylabel("Process ID")
        ax.set_title("Gantt Chart")

        ax.legend(loc="upper right")
        ax.invert_yaxis()  # Display processes from top to bottom

        # Create a canvas and add the plot to it
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    #sumarise the results in a table
    #Define the summary function
    def summary(process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time, average_turnaround_time, average_waiting_time):
        for widget in window.winfo_children():
            widget.destroy()

        # Create a main frame
        window.configure(bg='red')
        main_frame = tk.Frame(window, bg='red')
        main_frame.pack(fill='both', expand=1)

        # Create a canvas inside the main frame
        canvas = tk.Canvas(main_frame, bg='red')
        canvas.pack(side='left', fill='both', expand=1)

        # Add a scrollbar to the main frame, and link it to the canvas
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to place the labels
        frame = tk.Frame(canvas, bg='red')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        #create a label for the algorithm name
        label = tk.Label(frame, text="SJF ", font=('Cambria', 20), bg='red' )
        label.grid(row=0, column=0, columnspan=5, padx=500, sticky='ew')

        #create table headers
        headers = ['Process', 'Arriving time', 'Execution time', 'Exit time', 'Turnaround', 'Waiting']
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Cambria', 15), bg='red' ).grid(row=1, column=i, padx=10, pady=5, sticky='ew')

        # Create an empty list to store the process details
        all_processes = []
        #create table rows
        for i, (process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time) in enumerate(completed.values()):
            values = [process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time]
            for j, value in enumerate(values):
                tk.Label(frame, text=value, font=('Cambria', 15), bg='red' ).grid(row=i+2, column=j)
            
            # Add the process details to the list
            all_processes.append((process_id, arrival_time, execution_time, completion_time))   

        #display the average turnaround time and average waiting time
        tk.Label(frame, text="Average turnaround time: " + str(average_turnaround_time), font=('Cambria', 15), bg='red' ).grid(row=i+3, column=2, columnspan=5, pady=5, sticky='ew')
        tk.Label(frame, text="Average waiting time: " + str(average_waiting_time), font=('Cambria', 15), bg='red' ).grid(row=i+4, column=2, columnspan=5, pady=5, sticky='ew')

        #make a button to go back to the main menu
        button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=main)
        button1.grid(row=i+5, column=0, columnspan=5, pady=5, padx=50, sticky='ew')

        button4 = tk.Button(frame, text='View Gantt Chart', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=lambda: display_gantt_chart(all_processes))    
        button4.grid(row=i+6, column=4, columnspan=5, pady=5, sticky='ew')

        #update the scrollregion
        window.update()
        canvas.config(scrollregion=canvas.bbox('all'))

    #make a button to view summary
    button3=tk.Button(frame, text='View summary', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=lambda: summary(process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time, average_turnaround_time, average_waiting_time))
    button3.grid(row=i+4, column=4, columnspan=5, pady=5, sticky='ew')
    window.update()

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

#priority FCFS
def priority_FCFS_GUI():
    for widget in window.winfo_children():
        widget.destroy()

    #read calculated values from FCFS_with_priority()
    completed_processes, exit_times, turnaround_times, waiting_times, average_turnaround_time, average_waiting_time = FCFS_with_priority()

    for i, process in enumerate(completed_processes):
        process_id, arrival_time, execution_time, priority, quantum, waiting_time, old_priority, turnaround_time, exit_time = process

    # Create a main frame
    window.configure(bg='red')
    main_frame = tk.Frame(window, bg='red')
    main_frame.pack(fill='both', expand=1)

    # Create a canvas inside the main frame
    canvas = tk.Canvas(main_frame, bg='red')
    canvas.pack(side='left', fill='both', expand=1)

    # Add a scrollbar to the main frame, and link it to the canvas
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to place the labels
    frame = tk.Frame(canvas, bg='red')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    #stop button
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')

    #create a label for the algorithm name
    label = tk.Label(frame, text="Priority FCFS - quantum - " + str(quantum), font=('Cambria', 20), bg='red' )
    label.grid(row=0, column=4, columnspan=5, padx=500, sticky='ew')

    #create a list of labels for the processes
    process_labels = [tk.Label(frame, text=f"Process {completed_processes[i][0]}: Waiting ") for i in range (0,(len(completed_processes)))]
    for i, process_label in enumerate(process_labels):
        process_label.grid(row=i+1, column=4, columnspan=5, padx=100, pady=5, sticky='ew')

    

    #Define the function to simulate processes
    def simulate_process(i, process_id, arrival_time, execution_time, priority, quantum, waiting_time, old_priority, turnaround_time, completion_time):
        # Wait for the process to arrive
        time.sleep(arrival_time)
        # Update the label to show the process has arrived
        process_labels[i].config(text=f"Process {process_id}: arrived at {arrival_time}. Waiting for execution. Priority: {old_priority}")
        window.update()
        time.sleep(completion_time - arrival_time - execution_time)
        # Update the label to show the process has started executing
        process_labels[i].config(text=f"Process {process_id} executing {execution_time} with priority: {priority} ")
        window.update()
        time.sleep(execution_time)
        # Update the label to show the process has finished
        process_labels[i].config(text=f"Process {process_id} finished at time {completion_time}")
        window.update()

    #Display the results in the GUI
    for i, (process) in enumerate(completed_processes):
        process_id, arrival_time, execution_time, priority, quantum, waiting_time, old_priority, turnaround_time, exit_time = process
        threading.Thread(target=simulate_process, args=(i, process_id, arrival_time, execution_time, priority, quantum, waiting_time, old_priority, turnaround_time, exit_time)).start()
    
    #display the average turnaround time and average waiting time
    average_turnaround_time_label = tk.Label(frame, text="Average turnaround time: " + str(average_turnaround_time), font=('Cambria', 15), bg='red' )
    average_turnaround_time_label.grid(row=i+2, column=4, columnspan=5, pady=5, sticky='ew')
    average_waiting_time_label = tk.Label(frame, text="Average waiting time: " + str(average_waiting_time), font=('Cambria', 15), bg='red' )
    average_waiting_time_label.grid(row=i+3, column=4, columnspan=5, pady=5, sticky='ew')
    window.update()

    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

    def display_gantt_chart(processes):
        # Create a new top-level window
        gantt_window = tk.Toplevel(window)
        gantt_window.title("Gantt Chart")

        fig, ax = plt.subplots(figsize=(10, 5))

        processes.sort(key=lambda x: x[3])  # Sort by finish time
        current_y = 0

        for process in processes:
            ax.barh(y=current_y, width=process[2], left=process[3] - process[2], label=f"Process {process[0]}")
            current_y += 1

        ax.set_xlabel("Time")
        ax.set_ylabel("Process ID")
        ax.set_title("Gantt Chart")

        ax.legend(loc="upper right")
        ax.invert_yaxis()  # Display processes from top to bottom

        # Create a canvas and add the plot to it
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    

    #sumarise the results in a table
    #Define the summary function
    def summary(process_id, arrival_time, execution_time, priority, quantum, waiting_time, old_priority, turnaround_time, completion_time, average_turnaround_time, average_waiting_time):
        for widget in window.winfo_children():
            widget.destroy()

        # Create a main frame
        window.configure(bg='red')
        main_frame = tk.Frame(window, bg='red')
        main_frame.pack(fill='both', expand=1)

        # Create a canvas inside the main frame
        canvas = tk.Canvas(main_frame, bg='red')
        canvas.pack(side='left', fill='both', expand=1)

        # Add a scrollbar to the main frame, and link it to the canvas
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to place the labels
        frame = tk.Frame(canvas, bg='red')
        canvas.create_window((0, 0), window=frame, anchor='nw')
        
        label = tk.Label(frame, text="Priority FCFS - quantum - " + str(quantum), font=('Cambria', 20), bg='red' )
        label.grid(row=0, column=0, columnspan=8, padx=500, sticky='ew')

        #create table headers
        headers = ['Process', 'Arrive', 'Execute', 'Old priority', 'New priority', 'Waiting', 'Turnaround', 'Exit']
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Cambria', 15), bg='red' ).grid(row=1, column=i, padx=(10 if i==0 else 20), pady=5, sticky='ew')


        # Create an empty list to store the process details
        all_processes = []

        #create table rows
        for i, (process) in enumerate(completed_processes):
            process_id, arrival_time, execution_time, priority, quantum, waiting_time, old_priority, turnaround_time, exit_time = process
            values = [process_id, arrival_time, execution_time, old_priority, priority, waiting_time, turnaround_time, exit_time]
            for j, value in enumerate(values):
                tk.Label(frame, text=value, font=('Cambria', 15), bg='red' ).grid(row=i+2, column=j)

            # Add the process details to the list
            all_processes.append((process_id, arrival_time, execution_time, exit_time))

        #display the average turnaround time and average waiting time
        tk.Label(frame, text="Average turnaround time: " + str(average_turnaround_time), font=('Cambria', 15), bg='red' ).grid(row=i+3, column=2, columnspan=5, pady=5, sticky='ew')
        tk.Label(frame, text="Average waiting time: " + str(average_waiting_time), font=('Cambria', 15), bg='red' ).grid(row=i+4, column=2, columnspan=5, pady=5, sticky='ew')

        #make a button to go back to the main menu
        button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=main)
        button1.grid(row=i+5, column=2, columnspan=4, pady=5, padx=50, sticky='ew')

        button4 = tk.Button(frame, text='View Gantt Chart', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=lambda: display_gantt_chart(all_processes))
        button4.grid(row=i+6, column=4, columnspan=5, pady=5, sticky='ew')

        #update the scrollregion
        window.update()
        canvas.config(scrollregion=canvas.bbox('all'))

    
    
    #make a button to view summary
    button3=tk.Button(frame, text='View summary', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=lambda: summary(process_id, arrival_time, execution_time, priority, quantum, waiting_time, old_priority, turnaround_time, exit_time, average_turnaround_time, average_waiting_time))
    button3.grid(row=i+4, column=4, columnspan=5, pady=5, sticky='ns')
    
    window.update()
    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

def generate_processes():
    label = tk.Label(window, text="How many processes do you want to generate?", font=('Cambria', 20), bg='red' )
    label.grid(row=5, column=2, pady=15, sticky='ns')
    entry = tk.Entry(window, font=('Cambria', 20), bg='#ccc', width=15)
    entry.grid(row=6, column=2, pady=15, sticky='ns')
    button = tk.Button(window, text='Generate', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=lambda: generate_processes_to_file(entry.get()))
    button.grid(row=7, column=2, pady=15, sticky='ns')

    def generate_processes_to_file(number_processes):
        try:
            number_processes = int(number_processes)
            if number_processes >= 15:
                
                with open('input.txt', 'w') as f:

                    # Generate arrival times
                    plus_or_minus = [random.randint(0, 1) for _ in range(number_processes)]
                    # Generate first arrival time
                    arrival_times = [random.randint(0, 5)]

                    # Generate execution times - if plus_or_minus is 1 then subtract, else add
                    for i in range(1,number_processes):
                        if plus_or_minus[i] == 1 and arrival_times[i-1] >= 2:
                            arrival_times.append(arrival_times[i-1] - random.randint(0, 2))
                        else:
                            arrival_times.append(arrival_times[i-1] + random.randint(0, 2))

                    f.write(' '.join(map(str, arrival_times)) + '\n')

                    # Generate execution times
                    plus_or_minus = [random.randint(0, 1) for _ in range(number_processes)]
                    # Generate first execution time
                    execution_times = [random.randint(0, 5)]

                    # Generate execution times - if plus_or_minus is 1 then subtract, else add
                    for i in range(1,number_processes):
                        if plus_or_minus[i] == 1 and execution_times[i-1] >= 2:
                            execution_times.append(execution_times[i-1] - random.randint(0, 2))
                        else:
                            execution_times.append(execution_times[i-1] + random.randint(0, 2))

                    f.write(' '.join(map(str, execution_times)) + '\n')

                    # Generate priority
                    priority = [random.randint(1, 20)]
                    plus_or_minus = [random.randint(0, 1) for _ in range(number_processes)]

                    # Generate priority - if plus_or_minus is 1 then subtract, else add
                    for i in range(1,number_processes):
                        if plus_or_minus[i] == 1 and priority[i-1] >= 2:
                            priority.append(priority[i-1] - random.randint(0, 2))
                        else:
                            priority.append(priority[i-1] + random.randint(0, 2))

                    f.write(' '.join(map(str, priority)) + '\n')

                    # Generate quantum
                    quantum = [random.randint(1, 10)]
                    f.write(' '.join(map(str, quantum)) + '\n')

                    # Generate a random value
                    random_value = [random.randint(1, 10)]
                    f.write(' '.join(map(str, random_value)) + '\n')

                label = tk.Label(window, text="Processes generated!", font=('Cambria', 20), bg='red' )
                label.grid(row=8, column=2, pady=15, sticky='ns')
                window.after(2000, lambda: [widget.grid_forget() for widget in window.grid_slaves() if 5 <= int(widget.grid_info()["row"]) <= 8 and int(widget.grid_info()["column"]) == 2])

            else:
                label = tk.Label(window, text="Number of processes must be greater than 15!", font=('Cambria', 20), bg='red' )
                label.grid(row=8, column=2, pady=15, sticky='ns')
                label.after(2000, lambda: label.config(text=''))
        
        except Exception as e:
            label = tk.Label(window, text="Error generating processes!", font=('Cambria', 20), bg='red' )
            label.grid(row=8, column=2, pady=15, sticky='ns')
            print(e)

#FIFO
def FIFO():
    for widget in window.winfo_children():
        widget.destroy()

    # Create a main frame
    window.configure(bg='red')
    main_frame = tk.Frame(window, bg='red')
    main_frame.pack(fill='both', expand=1)

    # Create a canvas inside the main frame
    canvas = tk.Canvas(main_frame, bg='red')
    canvas.pack(side='left', fill='both', expand=1)

    # Add a scrollbar to the main frame, and link it to the canvas
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to place the labels
    frame = tk.Frame(canvas, bg='red')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    #stop button
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')

    #create a label for the algorithm name
    label = tk.Label(frame, text="FIFO ", font=('Cambria', 20), bg='red' )
    label.grid(row=0, column=6, columnspan=3, padx=500, sticky='ns')

    #read calculated values from FIFO_algorithm()
    reference_string, num_frames = read_file()
    reference_list = list(map(str, reference_string.split()))
    page_hits, page_faults, history, list_page_faults = FIFO_algorithm(reference_list, len(reference_list), num_frames)

    # Create a list of labels for the pages
    page_labels = [tk.Label(frame, text=f"Page {i}: Not loaded", width=50, bg='pink', font=('Cambria',15)) for i in range(len(reference_list))]
    for i, page_label in enumerate(page_labels):
        page_label.grid(row=i+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    #Create a list of labels for the reference string
    ref_string_labels = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_string_label in enumerate(ref_string_labels):
        ref_string_label.grid(row=i+1, column=4, columnspan=3, padx=50, pady=5, sticky='ns')
    
    # Create a list of labels for the page faults
    ref_page_faults = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_page_fault in enumerate(ref_page_faults):
        ref_page_fault.grid(row=i+1, column=8, columnspan=3, padx=50, pady=5, sticky='ns')

    # Create labels for total page hits and page faults
    total_page_hits_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_hits_label.grid(row=len(reference_list)+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    total_page_faults_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_faults_label.grid(row=len(reference_list)+2, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    # Define the function to simulate page loading
    def simulate_page_loading(i, current_number, page_table, page_fault):
        # Update the label to show the current reference string
        ref_string_labels[i].config(text=f" {reference_list[i]}")
        window.update()
        # Schedule the next update after 1 second
        window.after(1000, update_page_table, i, page_table, page_fault)

    def update_page_table(i, page_table, page_fault):
        #convert page table to string
        page_table_str = '  '.join(map(str, page_table))
        # Update the label to show the state of the page table after the reference
        page_labels[i].config(text=f"                                                         {page_table_str}   ", anchor='w')
        # Update the label to show the page fault
        ref_page_faults[i].config(text=f"{str(page_fault)}") 
        window.update()
        # Schedule the next page loading after 1 second if there are more pages
        if i + 1 < len(reference_list):
            window.after(1000, simulate_page_loading, i + 1, reference_list[i + 1], history[i + 1], list_page_faults[i + 1])
        else:
            # Update the total page hits and page faults labels
            total_page_hits_label.config(text=f"Total page hits: {page_hits}")
            total_page_faults_label.config(text=f"Total page faults: {(page_faults)}")

    # Start the page loading simulation
    simulate_page_loading(0, reference_list[0], history[0], list_page_faults[0])

    #make a button to go back to the main menu
    button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
    button1.grid(row=len(reference_list)+3, column=6, columnspan=3, pady=5, padx=50, sticky='ns')
    
    def show_summary():
        #clear window
        for widget in window.winfo_children():
            widget.destroy()

        # Create a main frame
        window.configure(bg='red')
        main_frame = tk.Frame(window, bg='red')
        main_frame.pack(fill='both', expand=1)

        # Create a canvas inside the main frame
        canvas = tk.Canvas(main_frame, bg='red')
        canvas.pack(side='left', fill='both', expand=1)

        # Add a scrollbar to the main frame, and link it to the canvas
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to place the labels
        frame = tk.Frame(canvas, bg='red')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        #stop button
        stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
        stop_button.place(relx=1.0, rely=0.0, anchor='ne')

        #make a button to go back to the main menu
        button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
        button1.grid(row=len(reference_list)+7, column=8, columnspan=3, pady=5, padx=50, sticky='ns')

        # Create table headers
        headers = ['Reference', 'History', 'Page faults']
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Cambria', 15), bg='red' ).grid(row=1, column=i+8, padx=200, pady=5, sticky='ns')

        # Create table rows
        for i in range(len(reference_list)):
            values = [reference_list[i], history[i], list_page_faults[i]]
            for j, value in enumerate(values):
                tk.Label(frame, text=value, font=('Cambria', 15), bg='red' ).grid(row=i+2, column=j+8, sticky = 'ns')
        
        # Create summary labels
        total_references = len(reference_list)
        total_faults = page_faults
        total_hits = page_hits
        summary_labels = ['Total References: ' + str(total_references), 'Total Faults: ' + str(total_faults), 'Total Hits: ' + str(total_hits), 'Page Fault Rate: ' + str(total_faults/total_references*100)+'%', 'Hit Rate: ' + str(total_hits/total_references*100)+'%']
        for i, label in enumerate(summary_labels):
            tk.Label(frame, text=label, font=('Cambria', 15), bg='red' ).grid(row=len(reference_list) +i+2, column=9, sticky='ns')


        #update the scrollregion
        window.update()
        canvas.config(scrollregion=canvas.bbox('all'))
        

     # Create the summary button
    summary_button = tk.Button(frame, text="View Summary", font=('Cambria', 15), bg='#ccc', width=40, height=1, command=show_summary)
    summary_button.grid(row=len(reference_list)+4, column=6, columnspan=3, pady=5, padx=50, sticky='ns')

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))


#OPT
def OPT():
    for widget in window.winfo_children():
        widget.destroy()

    # Create a main frame
    window.configure(bg='red')
    main_frame = tk.Frame(window, bg='red')
    main_frame.pack(fill='both', expand=1)

    # Create a canvas inside the main frame
    canvas = tk.Canvas(main_frame, bg='red')
    canvas.pack(side='left', fill='both', expand=1)

    # Add a scrollbar to the main frame, and link it to the canvas
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to place the labels
    frame = tk.Frame(canvas, bg='red')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    #stop button
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')

    #create a label for the algorithm name
    label = tk.Label(frame, text="OPT ", font=('Cambria', 20), bg='red' )
    label.grid(row=0, column=6, columnspan=3, padx=500, sticky='ns')

    #read calculated values from opt_algorithm()
    reference_string, num_frames = read_file()
    reference_list = list(map(str, reference_string.split()))
    page_faults, history, list_page_faults = opt_algorithm(reference_list, num_frames)

    # Create a list of labels for the pages
    page_labels = [tk.Label(frame, text=f"Page {i}: Not loaded", width=50, bg='pink', font=('Cambria',15)) for i in range(len(reference_list))]
    for i, page_label in enumerate(page_labels):
        page_label.grid(row=i+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    #Create a list of labels for the reference string
    ref_string_labels = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_string_label in enumerate(ref_string_labels):
        ref_string_label.grid(row=i+1, column=4, columnspan=3, padx=50, pady=5, sticky='ns')
    
    # Create a list of labels for the page faults
    ref_page_faults = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_page_fault in enumerate(ref_page_faults):
        ref_page_fault.grid(row=i+1, column=8, columnspan=3, padx=50, pady=5, sticky='ns')

    # Create labels for total page hits and page faults
    total_page_hits_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_hits_label.grid(row=len(reference_list)+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    total_page_faults_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_faults_label.grid(row=len(reference_list)+2, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    # Define the function to simulate page loading
    def simulate_page_loading(i, current_number, page_table, page_fault):
        # Update the label to show the current reference string
        ref_string_labels[i].config(text=f" {reference_list[i]}")
        window.update()
        # Schedule the next update after 1 second
        window.after(1000, update_page_table, i, page_table, page_fault)

    def update_page_table(i, page_table, page_fault):
        #convert page table to string
        page_table_str = '  '.join(map(str, page_table))
        # Update the label to show the state of the page table after the reference
        page_labels[i].config(text=f"                                                         {page_table_str}   ", anchor='w')
        # Update the label to show the page fault
        ref_page_faults[i].config(text=f"{str(page_fault)}") 
        window.update()
        # Schedule the next page loading after 1 second if there are more pages
        if i + 1 < len(reference_list):
            window.after(1000, simulate_page_loading, i + 1, reference_list[i + 1], history[i + 1], list_page_faults[i + 1])
        else:
            # Update the total page hits and page faults labels
            total_page_hits_label.config(text=f"Total page hits: {len(reference_list) - page_faults})")
            total_page_faults_label.config(text=f"Total page faults: {(page_faults)}")

    # Start the page loading simulation
    simulate_page_loading(0, reference_list[0], history[0], list_page_faults[0])

    #make a button to go back to the main menu
    button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
    button1.grid(row=len(reference_list)+3, column=6, columnspan=3, pady=5, padx=50, sticky='ns')
    
    def show_summary():
        #clear window
        for widget in window.winfo_children():
            widget.destroy()

        # Create a main frame
        window.configure(bg='red')
        main_frame = tk.Frame(window, bg='red')
        main_frame.pack(fill='both', expand=1)

        # Create a canvas inside the main frame
        canvas = tk.Canvas(main_frame, bg='red')
        canvas.pack(side='left', fill='both', expand=1)

        # Add a scrollbar to the main frame, and link it to the canvas
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to place the labels
        frame = tk.Frame(canvas, bg='red')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        #stop button
        stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
        stop_button.place(relx=1.0, rely=0.0, anchor='ne')

        #make a button to go back to the main menu
        button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
        button1.grid(row=len(reference_list)+7, column=8, columnspan=3, pady=5, padx=50, sticky='ns')

        # Create table headers
        headers = ['Reference', 'History', 'Page faults']
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Cambria', 15), bg='red' ).grid(row=1, column=i+8, padx=200, pady=5, sticky='ns')

        # Create table rows
        for i in range(len(reference_list)):
            values = [reference_list[i], history[i], list_page_faults[i]]
            for j, value in enumerate(values):
                tk.Label(frame, text=value, font=('Cambria', 15), bg='red' ).grid(row=i+2, column=j+8, sticky = 'ns')
        
        # Create summary labels
        total_references = len(reference_list)
        total_faults = page_faults
        total_hits = len(reference_list) - page_faults
        summary_labels = ['Total References: ' + str(total_references), 'Total Faults: ' + str(total_faults), 'Total Hits: ' + str(total_hits), 'Page Fault Rate: ' + str(total_faults/total_references*100)+'%', 'Hit Rate: ' + str(total_hits/total_references*100)+'%']
        for i, label in enumerate(summary_labels):
            tk.Label(frame, text=label, font=('Cambria', 15), bg='red' ).grid(row=len(reference_list) +i+2, column=9, sticky='ns')


        #update the scrollregion
        window.update()
        canvas.config(scrollregion=canvas.bbox('all'))
        

     # Create the summary button
    summary_button = tk.Button(frame, text="View Summary", font=('Cambria', 15), bg='#ccc', width=40, height=1, command=show_summary)
    summary_button.grid(row=len(reference_list)+4, column=6, columnspan=3, pady=5, padx=50, sticky='ns')

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

#LRU
def LRU():
    for widget in window.winfo_children():
        widget.destroy()

    # Create a main frame
    window.configure(bg='red')
    main_frame = tk.Frame(window, bg='red')
    main_frame.pack(fill='both', expand=1)

    # Create a canvas inside the main frame
    canvas = tk.Canvas(main_frame, bg='red')
    canvas.pack(side='left', fill='both', expand=1)

    # Add a scrollbar to the main frame, and link it to the canvas
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to place the labels
    frame = tk.Frame(canvas, bg='red')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    #stop button
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')

    #create a label for the algorithm name
    label = tk.Label(frame, text="LRU ", font=('Cambria', 20), bg='red' )
    label.grid(row=0, column=6, columnspan=3, padx=500, sticky='ns')

    #read calculated values from FIFO_algorithm()
    reference_string, num_frames = read_file()
    reference_list = list(map(str, reference_string.split()))
    page_hits, page_faults, history, list_page_faults = LRU_algorithm(reference_list, len(reference_list), num_frames)

    # Create a list of labels for the pages
    page_labels = [tk.Label(frame, text=f"Page {i}: Not loaded", width=50, bg='pink', font=('Cambria',15)) for i in range(len(reference_list))]
    for i, page_label in enumerate(page_labels):
        page_label.grid(row=i+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    #Create a list of labels for the reference string
    ref_string_labels = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_string_label in enumerate(ref_string_labels):
        ref_string_label.grid(row=i+1, column=4, columnspan=3, padx=50, pady=5, sticky='ns')
    
    # Create a list of labels for the page faults
    ref_page_faults = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_page_fault in enumerate(ref_page_faults):
        ref_page_fault.grid(row=i+1, column=8, columnspan=3, padx=50, pady=5, sticky='ns')

    # Create labels for total page hits and page faults
    total_page_hits_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_hits_label.grid(row=len(reference_list)+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    total_page_faults_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_faults_label.grid(row=len(reference_list)+2, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    # Define the function to simulate page loading
    def simulate_page_loading(i, current_number, page_table, page_fault):
        # Update the label to show the current reference string
        ref_string_labels[i].config(text=f" {reference_list[i]}")
        window.update()
        # Schedule the next update after 1 second
        window.after(1000, update_page_table, i, page_table, page_fault)

    def update_page_table(i, page_table, page_fault):
        #convert page table to string
        page_table_str = '  '.join(map(str, page_table))
        # Update the label to show the state of the page table after the reference
        page_labels[i].config(text=f"                                                         {page_table_str}   ", anchor='w')
        # Update the label to show the page fault
        ref_page_faults[i].config(text=f"{str(page_fault)}") 
        window.update()
        # Schedule the next page loading after 1 second if there are more pages
        if i + 1 < len(reference_list):
            window.after(1000, simulate_page_loading, i + 1, reference_list[i + 1], history[i + 1], list_page_faults[i + 1])
        else:
            # Update the total page hits and page faults labels
            total_page_hits_label.config(text=f"Total page hits: {page_hits}")
            total_page_faults_label.config(text=f"Total page faults: {(page_faults)}")

    # Start the page loading simulation
    simulate_page_loading(0, reference_list[0], history[0], list_page_faults[0])

    #make a button to go back to the main menu
    button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
    button1.grid(row=len(reference_list)+3, column=6, columnspan=3, pady=5, padx=50, sticky='ns')
    
    def show_summary():
        #clear window
        for widget in window.winfo_children():
            widget.destroy()

        # Create a main frame
        window.configure(bg='red')
        main_frame = tk.Frame(window, bg='red')
        main_frame.pack(fill='both', expand=1)

        # Create a canvas inside the main frame
        canvas = tk.Canvas(main_frame, bg='red')
        canvas.pack(side='left', fill='both', expand=1)

        # Add a scrollbar to the main frame, and link it to the canvas
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to place the labels
        frame = tk.Frame(canvas, bg='red')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        #stop button
        stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
        stop_button.place(relx=1.0, rely=0.0, anchor='ne')

        #make a button to go back to the main menu
        button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
        button1.grid(row=len(reference_list)+7, column=8, columnspan=3, pady=5, padx=50, sticky='ns')

        # Create table headers
        headers = ['Reference', 'History', 'Page faults']
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Cambria', 15), bg='red' ).grid(row=1, column=i+8, padx=200, pady=5, sticky='ns')

        # Create table rows
        for i in range(len(reference_list)):
            values = [reference_list[i], history[i], list_page_faults[i]]
            for j, value in enumerate(values):
                tk.Label(frame, text=value, font=('Cambria', 15), bg='red' ).grid(row=i+2, column=j+8, sticky = 'ns')
        
        # Create summary labels
        total_references = len(reference_list)
        total_faults = page_faults
        total_hits = page_hits
        summary_labels = ['Total References: ' + str(total_references), 'Total Faults: ' + str(total_faults), 'Total Hits: ' + str(total_hits), 'Page Fault Rate: ' + str(total_faults/total_references*100)+'%', 'Hit Rate: ' + str(total_hits/total_references*100)+'%']
        for i, label in enumerate(summary_labels):
            tk.Label(frame, text=label, font=('Cambria', 15), bg='red' ).grid(row=len(reference_list) +i+2, column=9, sticky='ns')


        #update the scrollregion
        window.update()
        canvas.config(scrollregion=canvas.bbox('all'))
        

     # Create the summary button
    summary_button = tk.Button(frame, text="View Summary", font=('Cambria', 15), bg='#ccc', width=40, height=1, command=show_summary)
    summary_button.grid(row=len(reference_list)+4, column=6, columnspan=3, pady=5, padx=50, sticky='ns')

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

#LFU
def LFU():
    for widget in window.winfo_children():
        widget.destroy()

    # Create a main frame
    window.configure(bg='red')
    main_frame = tk.Frame(window, bg='red')
    main_frame.pack(fill='both', expand=1)

    # Create a canvas inside the main frame
    canvas = tk.Canvas(main_frame, bg='red')
    canvas.pack(side='left', fill='both', expand=1)

    # Add a scrollbar to the main frame, and link it to the canvas
    scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
    scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to place the labels
    frame = tk.Frame(canvas, bg='red')
    canvas.create_window((0, 0), window=frame, anchor='nw')

    #stop button
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')

    #create a label for the algorithm name
    label = tk.Label(frame, text="LFU ", font=('Cambria', 20), bg='red' )
    label.grid(row=0, column=6, columnspan=3, padx=500, sticky='ns')

    #read calculated values from LFU_algorithm()
    reference_string, num_frames = read_file()
    reference_list = list(map(str, reference_string.split()))
    page_hits, page_faults, history, list_page_faults = LFU_algorithm(reference_list, len(reference_list), num_frames)

    # Create a list of labels for the pages
    page_labels = [tk.Label(frame, text=f"Page {i}: Not loaded", width=50, bg='pink', font=('Cambria',15)) for i in range(len(reference_list))]
    for i, page_label in enumerate(page_labels):
        page_label.grid(row=i+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    #Create a list of labels for the reference string
    ref_string_labels = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_string_label in enumerate(ref_string_labels):
        ref_string_label.grid(row=i+1, column=4, columnspan=3, padx=50, pady=5, sticky='ns')
    
    # Create a list of labels for the page faults
    ref_page_faults = [tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=10) for i in range(len(reference_list))]
    for i, ref_page_fault in enumerate(ref_page_faults):
        ref_page_fault.grid(row=i+1, column=8, columnspan=3, padx=50, pady=5, sticky='ns')

    # Create labels for total page hits and page faults
    total_page_hits_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_hits_label.grid(row=len(reference_list)+1, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    total_page_faults_label = tk.Label(frame, text=f" ", bg='pink', font=('Cambria',15), width=50)
    total_page_faults_label.grid(row=len(reference_list)+2, column=6, columnspan=3, padx=50, pady=5, sticky='ns')

    # Define the function to simulate page loading
    def simulate_page_loading(i, current_number, page_table, page_fault):
        # Update the label to show the current reference string
        ref_string_labels[i].config(text=f" {reference_list[i]}")
        window.update()
        # Schedule the next update after 1 second
        window.after(1000, update_page_table, i, page_table, page_fault)

    def update_page_table(i, page_table, page_fault):
        #convert page table to string
        page_table_str = '  '.join(map(str, page_table))
        # Update the label to show the state of the page table after the reference
        page_labels[i].config(text=f"                                                         {page_table_str}   ", anchor='w')
        # Update the label to show the page fault
        ref_page_faults[i].config(text=f"{str(page_fault)}") 
        window.update()
        # Schedule the next page loading after 1 second if there are more pages
        if i + 1 < len(reference_list):
            window.after(1000, simulate_page_loading, i + 1, reference_list[i + 1], history[i + 1], list_page_faults[i + 1])
        else:
            # Update the total page hits and page faults labels
            total_page_hits_label.config(text=f"Total page hits: {page_hits}")
            total_page_faults_label.config(text=f"Total page faults: {(page_faults)}")

    # Start the page loading simulation
    simulate_page_loading(0, reference_list[0], history[0], list_page_faults[0])

    #make a button to go back to the main menu
    button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
    button1.grid(row=len(reference_list)+3, column=6, columnspan=3, pady=5, padx=50, sticky='ns')
    
    def show_summary():
        #clear window
        for widget in window.winfo_children():
            widget.destroy()

        # Create a main frame
        window.configure(bg='red')
        main_frame = tk.Frame(window, bg='red')
        main_frame.pack(fill='both', expand=1)

        # Create a canvas inside the main frame
        canvas = tk.Canvas(main_frame, bg='red')
        canvas.pack(side='left', fill='both', expand=1)

        # Add a scrollbar to the main frame, and link it to the canvas
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview, bg='red')
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to place the labels
        frame = tk.Frame(canvas, bg='red')
        canvas.create_window((0, 0), window=frame, anchor='nw')

        #stop button
        stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
        stop_button.place(relx=1.0, rely=0.0, anchor='ne')

        #make a button to go back to the main menu
        button1=tk.Button(frame, text='Main menu', font=('Cambria', 15), bg='#ccc', width=40, height=1, command=main)
        button1.grid(row=len(reference_list)+7, column=8, columnspan=3, pady=5, padx=50, sticky='ns')

        # Create table headers
        headers = ['Reference', 'History', 'Page faults']
        for i, header in enumerate(headers):
            tk.Label(frame, text=header, font=('Cambria', 15), bg='red' ).grid(row=1, column=i+8, padx=200, pady=5, sticky='ns')

        # Create table rows
        for i in range(len(reference_list)):
            values = [reference_list[i], history[i], list_page_faults[i]]
            for j, value in enumerate(values):
                tk.Label(frame, text=value, font=('Cambria', 15), bg='red' ).grid(row=i+2, column=j+8, sticky = 'ns')
        
        # Create summary labels
        total_references = len(reference_list)
        total_faults = page_faults
        total_hits = page_hits
        summary_labels = ['Total References: ' + str(total_references), 'Total Faults: ' + str(total_faults), 'Total Hits: ' + str(total_hits), 'Page Fault Rate: ' + str(total_faults/total_references*100)+'%', 'Hit Rate: ' + str(total_hits/total_references*100)+'%']
        for i, label in enumerate(summary_labels):
            tk.Label(frame, text=label, font=('Cambria', 15), bg='red' ).grid(row=len(reference_list) +i+2, column=9, sticky='ns')


        #update the scrollregion
        window.update()
        canvas.config(scrollregion=canvas.bbox('all'))
        

     # Create the summary button
    summary_button = tk.Button(frame, text="View Summary", font=('Cambria', 15), bg='#ccc', width=40, height=1, command=show_summary)
    summary_button.grid(row=len(reference_list)+4, column=6, columnspan=3, pady=5, padx=50, sticky='ns')

    #update the scrollregion
    window.update()
    canvas.config(scrollregion=canvas.bbox('all'))

#generate pages
def generate_pages():
    label = tk.Label(window, text="How many pages do you want to generate?         ", font=('Cambria', 20), bg='red')
    label.grid(row=5, column=2, pady=15, sticky='ns')
    entry = tk.Entry(window, font=('Cambria', 20), bg='#ccc', width=15)
    entry.grid(row=6, column=2, pady=15, sticky='ns')
    button = tk.Button(window, text='Generate', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=lambda: generate_pages_to_file(entry.get()))
    button.grid(row=7, column=2, pady=15, sticky='ns')

    def generate_pages_to_file(number_pages):
        try:
            number_pages = int(number_pages)
            if number_pages >= 20:
                
                with open('input_replacement.txt', 'w') as f:

                    # Generate pages - random number between 0 and 9
                    pages = [random.randint(0, 9) for _ in range(number_pages)]
                    f.write(' '.join(map(str, pages)) + '\n')
                    #generate frame
                    frames = [random.randint(1, 5)]
                    f.write(' '.join(map(str, frames)) + '\n')  

                label = tk.Label(window, text="Pages generated!", font=('Cambria', 20), bg='red' )
                label.grid(row=8, column=2, pady=15, sticky='ns')
                window.after(2000, lambda: [widget.grid_forget() for widget in window.grid_slaves() if 5 <= int(widget.grid_info()["row"]) <= 8 and int(widget.grid_info()["column"]) == 2])

            else:
                label = tk.Label(window, text="Number of pages must be greater than 20!", font=('Cambria', 20), bg='red' )
                label.grid(row=8, column=2, pady=10, sticky='ns')
                label.after(2000, lambda: label.config(text=''))
        
        except Exception as e:
            label = tk.Label(window, text="Error generating pages!", font=('Cambria', 20), bg='red' )
            label.grid(row=8, column=2, pady=10, sticky='ns')
            print(e)
#stop the program
def stop_program():
    window.destroy()
    sys.exit()
    

#main program
def main():
    for widget in window.winfo_children():
        widget.destroy()
    #menu
    label = tk.Label(window, text="Choose an algorithm: ", font=('Cambria', 40), bg='red' )
    label.grid(row=0, column=2, pady=60, sticky='ns')
    button1=tk.Button(window, text='FCFS', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=FCFS_GUI)
    button1.grid(row=1, column=1, padx=80, sticky='ns')
    button2=tk.Button(window, text='SJF', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=SJF_GUI)
    button2.grid(row=1, column=2, padx=80, sticky='ns')
    button3=tk.Button(window, text='Priority FCFS', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=priority_FCFS_GUI)
    button3.grid(row=1, column=3, padx=80, sticky='ns')
    button4=tk.Button(window, text='Generate new processes to file', font=('Cambria', 15), bg='#ccc', width=30, height=2, command=generate_processes)
    button4.grid(row=3, column=2, padx=40, pady=60, sticky='ns')
    button5=tk.Button(window, text='FIFO', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=FIFO)
    button5.grid(row=4, column=1, padx=40, pady=5, sticky='ns')
    button5=tk.Button(window, text='OPT', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=OPT)
    button5.grid(row=5, column=1, padx=40, pady=40, sticky='ns')
    button6=tk.Button(window, text='LRU', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=LRU)
    button6.grid(row=4, column=3, padx=40, pady=5, sticky='ns')
    button7=tk.Button(window, text='LFU', font=('Cambria', 15), bg='#ccc', width=20, height=2, command=LFU)
    button7.grid(row=5, column=3, padx=40, pady=40, sticky='ns')
    button8=tk.Button(window, text='Generate new pages to file', font=('Cambria', 15), bg='#ccc', width=30, height=2, command=generate_pages)
    button8.grid(row=4, column=2, padx=40, pady=5, sticky='ns')
    stop_button=tk.Button(window, text='Stop', font=('Cambria', 15), bg='#ccc', width=10, height=1, command=stop_program)
    stop_button.place(relx=1.0, rely=0.0, anchor='ne')
    window.mainloop()

window = tk.Tk()
window.title('My Window')
window.geometry('800x700')
window.configure(background='red')
window.attributes('-fullscreen', True) #fullscreen
main()
