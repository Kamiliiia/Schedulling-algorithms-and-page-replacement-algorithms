def read_file():
    with open('input_replacement.txt', 'r') as f:
        lines = f.readlines()
        reference_string=lines[0].strip()
        num_frames=int(lines[1])
        print(reference_string)
        print(num_frames)

    return reference_string, num_frames