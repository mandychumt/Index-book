import sys
from lxml import etree

try:
    book_file = sys.argv[1:][0]
    output_file = sys.argv[1:][1]

    f = open(book_file)

except:
    print('Please enter valid file names\nand follow this format: books.xml index.xml')
    exit()

if book_file[-4:].lower() != '.xml' or output_file[-4:].lower() != '.xml' or len(book_file) < 5 or len(output_file) < 5 :
    print('Please enter valid file names\nand follow this format: books.xml index.xml')
    exit()

tree = etree.parse(f)

punctuations = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\n\r\t'
keyword_d = {} #{keyword1: {element1: [Id1, Id2 ,...], element2: [Id2, Id3, ...]}, keyword2:{...}, ... }

Id_ls = []
for Id in tree.xpath('//@id'): Id_ls.append(Id)

for element in ('author', 'title', 'genre', 'description'):

    keyword_ls = []
    word_ls = []

    for word in tree.xpath('//' + element):
        word = word.text.lower() #obtain text of the element of all books
        for punctuation in punctuations:
            word = word.replace(punctuation, ' ') #remove punctuation except for apostrophe
        word_ls.append(word)


    i = 0
    for Id in Id_ls: #deal with the text in each book
        words = word_ls[i].split(' ')
        for word in words:
            if len(word) == 0 : continue
            elif keyword_d.get(word,0) == 0: #check if a keyword exists in keyword_d
                keyword_d[word] = {element: [Id]} #create a new item of keyword_d if doesn't exist
            else: 
                if keyword_d[word].get(element,0) == 0 : #check if a element exists
                    keyword_d[word][element] = [Id] #create a new element:Id pair of the keyword's value if doesn't exist
                else:
                    if Id not in keyword_d[word][element]: keyword_d[word][element].append(Id) #add the Id to the Id list if the element exists
        i += 1

#store the index in the following structure:
#<keywords>
    #<keyword word="XXX">
        #<book element="XXX"> Id </book>
    #</keyword>
    #......
#</keywords>

root = etree.Element("keywords")

for key, value_d in list(keyword_d.items()):
    keyword = etree.SubElement(root, "keyword", word=key)
    for key,value in list(value_d.items()):
        book = etree.SubElement(keyword, "book", element=key)
        book.text = ','.join(value)

        
output_f = open(output_file, 'w')
output_f.write(etree.tostring(root, pretty_print=True).decode())
output_f.close()