# The calculator of phonemic similarity 
This is a calculator of phonemic similarity I programmed for my project on gradient symbolic representation. 
- Make sure you installed python 3.
- Make sure you put 'yourfeaturefile.txt' inside of the master folder
- The basic usage is: 
  1. Make your own featurefile 'yourfeaturefile.txt' as what I did in "lezgian.txt". 
    - [UCLA Pheatures Spreadsheet]  (https://linguistics.ucla.edu/people/hayes/120a/Pheatures/) is a nice tool. 
    - Choose segments in UCLA Pheatures Spreadsheet, obtain all features and copy+paste all to a Excel/Numbers/any spreadsheets. 
    - Export the spreadsheet to a nice, tab-delimited table in .txt file.
  2. Choose your directory: Type following code in your Command Line tools (Windows) or Terminal (Mac), add your own directory after cd.
```bash
cd [your directory]
```
3. Run the python program: Type following code in your Command Line tools or Terminal. 
```bash
python3 similarity.py yourfeaturefile.txt
``` 

