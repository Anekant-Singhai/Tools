import sys

def append_words(input_file, output_file, word):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for i, line in enumerate(lines):
            file.write(line)
            # Insert the word after every n lines
            if i % 2 == 0 and i != len(lines)-1 :  # Replace n with the desired number of lines
                file.write(word + '\n')

    # Remove the last line if it contains the same word
    with open(output_file, "r+") as file:
        lines = file.readlines()
        if lines[-1].strip() == word:
            file.seek(0)  # Move the file pointer to the beginning of the file
            file.writelines(lines[:-1])  # Write all lines except the last line

    print(f"Word '{word}' appended to alternate lines in '{output_file}'.")

if len(sys.argv) >= 4:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    word = sys.argv[3]

    append_words(input_file, output_file, word)
else:
    print("Usage: python script.py <input_file> <output_file> <word>")
