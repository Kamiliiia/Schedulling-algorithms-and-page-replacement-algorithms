def read_processes():
    #read input file and return list of processes
    try:
        with open('input.txt', 'r') as file:
            lines = file.readlines()
            if not lines:
                print("File is empty.")
                return []
            
            #split lines into lists
            arrival_times = list(map(int, lines[0].split()))
            execution_times = list(map(int, lines[1].split()))
            priority = list(map(int, lines[2].split()))
            quantum = int(lines[3])
            
           
            #create list for each process
            processes = []
            
            for i in range(len(arrival_times)):
              process = ['P'+ str(i), arrival_times[i], execution_times[i], priority[i], quantum]
              processes.append(process)

        return processes
    except FileNotFoundError:
        print("File not found.")
        return []
    except IOError:
        print("Error reading file.")
        return []
