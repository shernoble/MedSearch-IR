MEDICAL INFORMATION RETRIEVAL SYSTEM

I OVERVIEW
This project is an Information Retrieval (IR) system for medical information using Whoosh, a fast, featureful full-text indexing and searching library implemented in pure Python. The system is built on Flask, a lightweight web framework.

II GETTING STARTED

PREREQUISITES
* Python 3.x
* Flask
* Whoosh
PROJECT STRUCTURE
* app.py : the main flask application file
*templates/index.html: html pages for rendering the pages
*output_files_whoosh_main: whoosh index directory

INSTALLATION, SETUP
1.unzip the project file and open the codes folder in your editor of choice.
2. Install the above dependencies using pip install
a. pip install flask
b. pip install whoosh 
3. Then run the command:
a. python app.py
4. you will see the following in your terminal: 
	 * Running on http://127.0.0.1:5000
5. open your web browser and type http://127.0.0.1:5000, click enter
6. the web application will open and now you can enter your search query 
7. the top 10 results will be displayed
8. you are allowed to mark each output as relevant or non-relevant and submit the feedback which will be used to re-rank the documents.
9. The assessment components like precision @ k and MAP are used to assess the IR model.
FEATURES
* Fuzzy search: Fuzzy search capability for medical information.
* Retrieval of relevant documents based on user queries.
* Feedback mechanism to update scores for documents.

OTHER FILES

*whoosh-indexing.py: file that consistes of code used to create whoosh index for over 60k documents
*example-webscrapper.py : code used for webscrapping to get content from webpages (i.e. get documents)
*example-websitelinks.py: code used to get links of websites and also deep crawling those websites to get further links
*unique_urls2.txt: example of links we retrieved from crawling

![image](https://github.com/user-attachments/assets/a5be079a-bb66-4732-a8bd-108d58a9ebce)

