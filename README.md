# Index-book

Introduction

This project obtains data about a catalog of books from an XML file. Each book has a unique id and several attributes like author and title. I first build an inverted index and then use the index to facilitate the searching of books. There is a sample data stored in "books.xml" for testing my code.

(1) Creating Index
"index.py" is a Python script that takes two XML file names in command line. The first file stores book data and the second one is the output file name. The script takes the first file as the input and outputs the index in the second file.

For example: python index.py books.xml index.xml

(2) Searching
"search.py" takes the data file (e.g. books.xml), index file (e.g. index.xml) and a string of keywords, and outputs the search result in an XML file. which lists the documents having all the keywords in at least one of the attributes and also the complete content of the attributes.

For example,

python search.py books.xml index.xml "xml xslt" results.xml

will store the following results in a file called "results.xml":

<results>
	<book id="bk111">
		<description>The Microsoft MSXML3 parser is covered in detail, with
					attention to XML DOM interfaces, XSLT processing, SAX and
					more.</description>
	</book>
	<book id="xxx"> … </book>
	…
</results>

If nothing found, will return:

<results/>

