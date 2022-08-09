Jest to implementacja metody steganografii lingwistycznej bazujacej na substytucji synonimow.
Algorytm odczytuje z pliku text w ktrym ma zostac ukryta wiadomosc.
Dokonuje jego tokenizacji przy pomocy metody word_tokenize (biblioteka nltk).
Dla kazdego ze slow odczytanych z pliku wykonuje operacje:
- Usuwania przyrostka wykorzystujac w tym celu SnowballStemmer (biblioteka nltk).
- Part-of-speech tagging korzystajac z metody .pos_ (biblioteka spacy z zaladowanym modelem en_core_web_md)
Jesli slowo jest conajmniej 3 literowym czasownikiem lub rzeczownikiem:
- Wyszukuje liste jego synonimow w slowniku wordnet (biblioteka nltk)(Ograniczona do 3 najlepszych synonimow dla poprawienia jakosci substytucji).
- Dla kazdego z nich dokonuje oceny podobienstwa za pomoca funkcji .similarity() (biblioteka spacy).
Jesli znalezione zostaly conajmniej dwa synonimy:
- Na podstawie ocen podobienstwa generowane jest drzewo huffmana dla synonimow danego slowa
- Drzewo sprawdzene jest pod katem pokrycia kolejnych bitow sekretu a nastepnie dokonywana jest substytucja slow.

baza wiedzy:

concept - Synonymus Paraphrasing Using WordNet and Internet -book page 312-323 2004_Book_NaturalLanguageProcessingAndIn
	- A Practical and Effective Approach to Large-Scale Automated Linguistic Steganography -book page 156-165 2001_Book_InformationSecurity

English letter freq - https://en.wikipedia.org/wiki/Letter_frequency

huffman coding - http://stackoverflow.com/questions/11587044/how-can-i-create-a-tree-for-huffman-encoding-and-decoding

suffix removal - https://stackoverflow.com/questions/67126651/how-can-i-remove-suffix-using-the-nltk-package-in-python

POS tagging - https://stackabuse.com/python-for-nlp-parts-of-speech-tagging-and-named-entity-recognition/

t-lex - https://bitsofbinary.wordpress.com/2011/10/19/t-lex-system-with-huffman-coding/

nltk/worndet - https://www.nltk.org/howto/wordnet.html

spacy - https://spacy.io/usage/spacy-101#whats-spacy



pystempel - https://pypi.org/project/pystempel/

polish nlp - https://github.com/ksopyla/awesome-nlp-polish

spacy-pl - https://github.com/ipipan/spacy-pl

morfeusz - http://morfeusz.sgjp.pl/download/

pl-wordnet - https://github.com/maxadamski/plwordnet

gettingstarted - https://dziopa.com/blog/1-getting-started-nlp/

unimorph_inflect - https://github.com/antonisa/unimorph_inflect