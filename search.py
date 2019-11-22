import sys
from lxml import etree

try:
    book_file = sys.argv[1:][0]
    index_file = sys.argv[1:][1]
    keywords = sys.argv[1:][2]
    result_file = sys.argv[1:][3]
    f = open(index_file)

except:
    print('Please enter valid file names\nand follow this format: books.xml index.xml "a string of keywords" results.xml')
    exit()

if book_file[-4:].lower() != '.xml' or index_file[-4:].lower() != '.xml' or result_file[-4:].lower() != '.xml' or len(book_file) < 5 or len(index_file) < 5 or len(result_file) < 5:
    print('Please enter valid file names\nand follow this format: books.xml index.xml')
    exit()

punctuations = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\n\r\t'
for punctuation in punctuations: #remove punctuations except for apostrophe
    keywords = keywords.replace(punctuation, ' ')


tree = etree.parse(f)
index_word_ls = []
# obtain a list of keywords in XML file stored index information
for word in tree.xpath('//@word'):
    index_word_ls.append(word)

#create a dictionary to store found (Id,element) for all valid words, structure: {(Id,element):word, ...}
word_d = {}
#create a dictionary to store required results found, structure: {Id:element, ...}
result_d = {} 

if len(keywords) != 0 and keywords != ' ':
    keyword_ls = keywords.lower().split(' ')
    while '' in keyword_ls: keyword_ls.remove('')
    for word in keyword_ls:
        if word not in index_word_ls:
            break
        #find the elements of books that contain input keywords
        for element in tree.xpath("//keyword[@word = \"" + word + "\"]/book/@element"): 
            #for each element, get the Ids of books
            for Id in tree.xpath("//keyword[@word = \"" + word + "\"]/book[@element='" + element + "']/text()")[0].split(','):
                if (Id,element) in word_d: word_d[(Id,element)].append(word)
                else: word_d[(Id,element)] = [word]

for pair,words in list(word_d.items()):
    if len(words) == len(keyword_ls): #if all words occur in at least one element, store in result_d
        if pair[0] not in result_d: result_d[pair[0]] = [pair[1]]
        else: result_d[pair[0]].append(pair[1])

#output serach results in an XML file
try: 
    f = open(book_file)
except: 
    print('Please enter valid file names\nand follow this format: books.xml index.xml')
    exit()

tree = etree.parse(f)
root = etree.Element("results")
for (Id,elements) in list(result_d.items()):
    book = etree.SubElement(root, "book", id=Id)
    for element in elements:
        child = etree.SubElement(book, element)
        child.text = tree.xpath("//book[@id='" + Id + "']/" + element + "/text()")[0]
output_f = open(result_file, 'w')
output_f.write(etree.tostring(root, pretty_print=True).decode())
output_f.close()