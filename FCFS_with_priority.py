def FCFS_with_priority(): #function to calculate FCFS with priority
    #read processes from file
    from read_file_processes import read_processes
    priority_processes = read_processes()
   
    #Initialize variables
    completed_processes = []
    arrival_times = []
    execution_times = []
    number_processes = []
    priority_times = []
    waiting_times = []
    turnaround_times = []
    exit_times = []

    #append to lists 
    for process in priority_processes:
        #print(f"Process: {process}")
        number_processes.append(process[0])
        arrival_times.append(process[1])
        execution_times.append(process[2])
        priority_times.append(process[3])
        quantum = process[4]

    #create queue which is copy of priority_processes
    queue=priority_processes.copy()

    process_dict = {process[0]: list(process) for process in queue}
    t=0 #current time

    #available processes
    available_processes = [process for process in queue if process[1] <= t]
    available_processes.sort(key=lambda x: (x[3],x[1])) #sort by priority and by arrival time
    #print(f"queue at time: {t}")

    while queue: #while there are processes in the queue
        available_processes = [process for process in queue if process[1] <= t] #available processes are processes with arrival time less than or equal to current time
        available_processes.sort(key=lambda x: (x[3],x[1])) #sort by priority and by arrival time
        #print(f"queue at time: {t}")
        for i, process in enumerate(available_processes):
            waiting_time = t - process[1] #current time - arrival time
            #print(f"number: {process[0]}, arriving {process[1]}, execution time: {process[2]}, waiting time: {waiting_time}, priority: {process[3]} ")
            #aging priority
            if waiting_time >= quantum:
                process[3] = process[3] - (waiting_time // quantum)
                if process[3] < 0:
                    process[3] = 0
        #if there are available processes
        if available_processes:
            current_process = min(available_processes, key=lambda x:x[3]) #current process is the process with the lowest priority
            if current_process in queue:
                queue.remove(current_process) #remove the current process from the queue
            else:
                print("")
            #print(f"Currently executing process: {available_processes[0][0]}") 
            original_process = process_dict[current_process[0]] #get the original process from the dictionary
            waiting_time = t - process[1] #current time - arrival time
            waiting_times.append(waiting_time)
            current_process.append(waiting_time)
            original_process.append(waiting_time)
            original_process.append(original_process[3])
            
            if waiting_time >= quantum:
                original_process[3] = original_process[3] - (waiting_time // quantum)
                if original_process[3] < 0:
                    original_process[3] = 0
            
            t += available_processes[0][2] #current time = current time + executing time
            turnaround_time = t - available_processes[0][1] #current time - arrival time
            turnaround_times.append(turnaround_time)
            current_process.append(turnaround_time)
            original_process.append(turnaround_time)
            exit_times.append(t)
            current_process.append(t) #add exit time to current process
            original_process.append(t) #add exit time to original process
            #completed_processes.append(current_process) #add the current process to the list of completed processes

            completed_processes.append(original_process) #add the original process to the list of completed processes
        else: #if there are no available processes
            t +=1
    average_waiting_time = sum(waiting_times)/len(waiting_times)
    average_turnaround_time = sum(turnaround_times)/len(turnaround_times)
    print(f"Average waiting time: {average_waiting_time}")
    print(f"Average turnaround time: {average_turnaround_time}")
    print(f"Completed processes: {completed_processes}")

    return completed_processes, exit_times, turnaround_times, waiting_times, average_turnaround_time, average_waiting_time #return values to GUI.py

#FCFS_with_priority() #call function
