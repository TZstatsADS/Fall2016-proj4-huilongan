# Project: Words 4 Music

### [Project Description](doc/Project4_desc.md)

![image](http://cdn.newsapi.com.au/image/v1/f7131c018870330120dbe4b73bb7695c?width=650)

Term: Fall 2016

+ [Data link](https://courseworks2.columbia.edu/courses/11849/files/folder/Project_Files?preview=763391)-(**courseworks login required**)
+ [Data description](doc/readme.html)
+ Contributor's name: Huilong An
+ Projec title: Lyric detection based on Recommendation Algorithm
+ Project summary: 
	What make my project different from others? 
	Based on User-based Collaborative filtering theory, I made some some modification to my project:
	1. Randomly sampled a baseline: As the music features are almost all vectors or matrices, I chose the longest 		vectors,and used their size to make sampling. 
	2. Calculated Pearson correlation coefficient amaong each feature between the provided song and the baseline, which is 	       to quantify each song into a vector.
	3. Calculated Pearson correlation coefficient as the similarity between new song and provided song.
	4. Ranked the similar provided song compared to the new song and to rank the word.
	Potential problem:
	The whole procedure decides it is very hard to rank all the word. In order to make the computation quick, I actually 
	just used a part of similar songs(based on their rank).
	Programming language:
	To extract features from HDF5 -> Python
	To get the final result -> R
	Data:
	similarity matrix
	final result -> both in csv format

	
Following [suggestions](http://nicercode.github.io/blog/2013-04-05-projects/) by [RICH FITZJOHN](http://nicercode.github.io/about/#Team) (@richfitz). This folder is orgarnized as follows.

```
proj/
├── lib/
├── data/
├── doc/
├── figs/
└── output/
```

Please see each subfolder for a README file.
