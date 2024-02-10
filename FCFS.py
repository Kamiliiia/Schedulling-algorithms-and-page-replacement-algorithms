def FCFS_algorithm():
    from read_file_processes import read_processes
    #read processes from file
    processes = read_processes()

    print("Processes: ", processes) 
    sorted_processes = sorted(processes, key=lambda x: x[1]) #sort by arrival time
    print("Sorted processes: ", sorted_processes)

    #Initialize variables
    number_processes = []
    exit_time = sorted_processes[0][1]
    exit_times = []
    turnaround_times = []
    waiting_times = []
    arriving_times = []
    execution_times = []

    for process in sorted_processes:
      print("Process: ", process)
      #create a list of process numbers
      number_processes.append(process[0])
      #create a list of arrival times
      arriving_times.append(process[1])
      print("Arriving times: ", arriving_times)
      #create a list of execution times
      execution_times.append(process[2])
      print("Execution times: ", execution_times)
      #calculate exit time - exit time plus execution time
      if process[1] > exit_time:
        exit_time = process[1]
      #add execution time to exit time
      exit_time += process[2]
      exit_times.append(exit_time)
      print("Exit time: ", exit_time)
      #calculate turnaround time - exit time minus arrival time
      turnaround_time = exit_time - process[1]
      turnaround_times.append(turnaround_time)
      print("Turnaround time: ", turnaround_time)
      #calculate waiting time - turnaround time minus execution time
      waiting_time = turnaround_time - process[2]
      waiting_times.append(waiting_time)
      print("Waiting time: ", waiting_time)


    #calculate average turnaround time
    average_turnaround_time = sum(turnaround_times)/len(turnaround_times)
    print("Average turnaround time: ", average_turnaround_time)

    #calculate average waiting time
    average_waiting_time = sum(waiting_times)/len(waiting_times)
    print("Average waiting time: ", average_waiting_time) 

    return number_processes, arriving_times, execution_times, exit_times, turnaround_times, waiting_times, average_turnaround_time, average_waiting_time  #return values to GUI.py