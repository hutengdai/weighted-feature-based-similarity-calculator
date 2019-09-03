import pandas as pd
import csv

txt_file = r"lezgian-segment.txt"
csv_file = r"lezgian-segment.csv"

with open(txt_file, "r") as in_text:
    in_reader = csv.reader(in_text, delimiter='\t')
    with open(csv_file, "w") as out_csv:
        out_writer = csv.writer(out_csv)
        for row in in_reader:
            out_writer.writerow(row)
# with open(txt_file, "w") as my_output_file:
#     with open(csv_file, "r") as my_input_file:
#         [ my_output_file.write("\t".join(row)+'\n') for row in csv.reader(my_input_file)]
#     my_output_file.close()
    
    
# lezgian = pd.read_csv('lezgian.csv')

# print(lezgian)
