def split_file(input_file, chunk_size):
    with open(input_file, 'r',encoding="utf-8") as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lines[i]="\"" + lines[i].strip() + "\"\n"

    num_chunks = (len(lines) + chunk_size - 1) // chunk_size  

    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = min((i + 1) * chunk_size, len(lines))
        chunk = lines[start_index:end_index]
        chunk[-1] = chunk[-1].strip()

        output_file = f"{input_file[:-4]}_{i + 1:02d}.txt"  
        with open(output_file, 'w',encoding="utf-8") as out:
            out.writelines(chunk)

if __name__ == "__main__":
    input_file = "image_data.txt"
    chunk_size = int(input("Enter the number of lines for each chunk: "))
    split_file(input_file, chunk_size)
    print("Files split successfully.")

