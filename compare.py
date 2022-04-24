# Open File in Read Mode
file_1 = open('Datas\Pages\\ta2bss.com.new', 'r')
file_2 = open('Datas\Pages\\ta2bss.com.old', 'r')

print("Comparing files ", " new " + 'Datas\Pages\\ta2bss.com.new', " old " + 'Datas\Pages\\ta2bss.com.old', sep='\n')

file_1_line = file_1.readline()
file_2_line = file_2.readline()

# Use as a COunter
line_no = 1

print()

with open('Datas\Pages\\ta2bss.com.new') as file1:
    with open('Datas\Pages\\ta2bss.com.old') as file2:
        same = set(file1).intersection(file2)

print("Difference Lines in Both Files")
while file_1_line != '' or file_2_line != '':

    # Removing whitespaces
    file_1_line = file_1_line.rstrip()
    file_2_line = file_2_line.rstrip()

    # Compare the lines from both file
    if file_1_line != file_2_line:

        # otherwise output the line on file1 and use new sign
        if file_1_line == '':
            print("old", "Line-%d" % line_no, file_1_line)
        else:
            print("old-", "Line-%d" % line_no, file_1_line)

        # otherwise output the line on file2 and use # sign
        if file_2_line == '':
            print("new", "Line-%d" % line_no, file_2_line)
        else:
            print("new+", "Line-%d" % line_no, file_2_line)

        # Print a empty line
        print()

    # Read the next line from the file
    file_1_line = file_1.readline()
    file_2_line = file_2.readline()

    line_no += 1

file_1.close()
file_2.close()
