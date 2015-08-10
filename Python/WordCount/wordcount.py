import sys

def printResult(filename, topN, case_sensitive):
    dict = getDictOfwords(filename, case_sensitive)
    topN = int(topN)

    if topN >= 1:
        words = sorted(dict, key=dict.get, reverse=True)
        for word in words[:topN]:
            print word, dict[word]
    else:
        words = sorted(dict.keys()) #return a list order by the key of the dictionary (the word)
        for word in words: #foreach item in the list
            print word, dict[word] # print the item and the value on the dictionay



def getDictOfwords(filename, case_sensitive):
    word_dict = {}
    input_file = open(filename, 'r')
    for line in input_file:
        words = line.split()
        for word in words:
            if not case_sensitive:
                word = word.lower()
            if not word in word_dict:
                word_dict[word] = 1
            else:
                word_dict[word] = word_dict[word] + 1
    input_file.close()
    return word_dict


def main():
    if len(sys.argv) <2:
        print 'Invalid number of arguments, please Inform:'
        print '  1) File name (mandatory)'
        print '  2) TopN words to return; Default 0: returns all words alphabetically'
        print '  3) Case Sensitive or not (default False, use "True" or "T" otherwise'
        sys.exit()

    filename = sys.argv[1]
    try:
        topN = int(sys.argv[2])
    except:
        topN = 0

    try:
        sensitive = sys.argv[3]
        if sensitive in ["TRUE", "true", "T", "t"]:
            sensitive = True
        else:
            sensitive = False
    except:
        sensitive = False

    printResult(filename, topN, sensitive)

if __name__ == '__main__':
  main()
