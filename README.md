# The weighted feature-based calculator of phonological similarity 
This is a  weighted feature-based calculator of phonological similarity.
- Make sure you installed python 3.

- Make sure you put 'yourfeaturefile.txt' inside of the master folder

- The basic usage is: 
1. Make your own featurefile 'yourfeaturefile.txt' as what I did in "lezgian.txt". [UCLA Pheatures Spreadsheet](https://linguistics.ucla.edu/people/hayes/120a/Pheatures/) is a nice tool. 
    - Choose segmental inventory in UCLA Pheatures Spreadsheet, obtain all features and copy+paste all to a Excel/Numbers/any spreadsheets. 
    - Export the spreadsheet to a tab-delimited table in .txt file.
2. Choose your directory: Type following code in your Command Line tools (Windows) or Terminal (Mac), add your own directory after cd.
```bash
cd [your directory]
```

3. Run the python program: Type following code in your Command Line tools or Terminal. 
```bash
python3 similarity.py yourfeaturefile.txt
``` 
4. The output will be a similarity-matrix.csv file with all the computed similarities.

5. The easiest way to change the weights of features in the dlist of similarity.py.   

- If you want to commit to this program, only similarity.py matters. Other files are kept for my other research purpose.

- If you use this program in your work, please cite: Dai, H. (2021). Gradient Similarity in Lezgian Laryngeal Harmony: Representation and Computation. In 38th West Coast Conference on Formal Linguistics (pp. 147-157). Cascadilla Proceedings Project.

@inproceedings{dai_gradient_2021,
	title = {Gradient similarity in {Lezgian} laryngeal harmony: representation and computation},
	url = {https://hutengdai.com/files/Lezgian_paper_WCCFL.pdf},
	booktitle = {Proceedings of the 38th {West} {Coast} {Conference} on {Formal} {Linguistics}},
	publisher = {Cascadilla Press},
	author = {Dai, Huteng},
	year = {2021},
}

- Feel free to contact me (hutengdai[*]gmail.com) if you have any questions!


