def SJF_algorithm():
    from read_file_processes import read_processes

    #read processes from file
    processes = read_processes()

    print("Processes: ", processes) 
    sorted_processes = sorted(processes, key=lambda x: x[1]) #sort by arrival time
    print("Sorted processes: ", sorted_processes)
    # read processes from file
    #processes = read_processes()

    print("Processes: ", processes)

    t=0 #time
    gantt_chart = [] #gantt chart
    completed = {} #dictionary of completed processes
    process_list = sorted_processes.copy() #list of processes

    while process_list != []: #while there are processes in the list
        available_processes = [] #list of available processes
        for process in process_list: #for each process in the list
            if process[1] <= t: #if the arrival time is less than or equal to the time
                available_processes.append(process) #add the process to the list of available processes

        #no processes available
        if available_processes == []:
            gantt_chart.append("Idle") #add idle to the gantt chart
            t += 1 #increment time by 1
            continue #continue to the next iteration of the loop
        else: #processes available
            available_processes.sort(key=lambda x: x[2])    #sort by execution time
            process = available_processes[0]
            execution_time = process[2] 
            process_id = process[0]
            arrival_time = process[1]
            t += execution_time
            gantt_chart.append(process_id)
            #calculate completion time
            completion_time = t 
            #calculate turnaround time
            turnaround_time = completion_time - arrival_time
            #calculate waiting time
            waiting_time = turnaround_time - execution_time

            process_list.remove(process) #remove the process from the list of processes
            completed[process_id] = [process_id, arrival_time, execution_time, completion_time, turnaround_time, waiting_time]  #add the process to the dictionary of completed processes
        print("Gantt chart: ", gantt_chart)
        print("Completed: ", completed)

    #calculate average turnaround time
    total_turnaround_time = 0
    for process in completed:
        total_turnaround_time += completed[process][3] #add the turnaround time of each process to the total turnaround time
    average_turnaround_time = total_turnaround_time / len(completed)


    #calculate average waiting time
    total_waiting_time = 0
    for process in completed:
        total_waiting_time += completed[process][4]
    average_waiting_time = total_waiting_time / len(completed)

    print("Average turnaround time: ", average_turnaround_time)
    print("Average waiting time: ", average_waiting_time)

    return gantt_chart, completed, average_turnaround_time, average_waiting_time  #return values to GUI.py

SJF_algorithm()

