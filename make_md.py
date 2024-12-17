import sys, re, os, requests
from bs4 import BeautifulSoup


def argsAnalize(args):
    lvl = 0
    lnk = ''
    for i in range(len(args)):
        if args[i] == '-l':
            try: lvl = int(args[i+1])
            except: lvl = 0
        else:
            try: res = re.search(r'https*://.*', args[i]).group(0)
            except: res = ''
            if res: lnk = args[i]
    return(lvl, lnk)

def usage():
    print('Not actual parameters.\nUsage: {} [-l 0..6] <URL>'.format(sys.argv[0]))

def tagUL(ul):
    tmp = ''
    for i in ul.children: 
        if i.name == 'li': 
            tmp += ('* ' + i.text + '\n')
    return(tmp+'\n')
    
def tagTR(tr):
    tmp = ''
    th = ''
    for i in tr.children:
        if i.name == 'td':
            tmp += '|' + i.text.replace('\n', '').strip().replace('<', '\<').replace('>', '\>')
        elif i.name == 'th':
            tmp += '|**' + i.text + '**'
            th += '|-'
    tmp += '|\n'
    if th: th += '|\n'
    return(tmp + th)

def tagTRHead(tr):
    #print('> call: tagTRHead()')
    tmp = ''
    th = ''
    for i in tr.children:
        if i.name == 'td':
            #print('> tagTRHead() child is {}'.format(type(i.span)))
            if i.text:
                tmp += '|**' + i.text + '**'
            else:
                tmp += '|**' + i.span['title'] + '**'
            th += '|-'
    tmp += '|\n'
    if th: th += '|\n'
    return(tmp + th)

def tagTable(table):
    tmp = ''
    for i in table.children:
        if i.name == 'caption':
            tmp += '\n**' + table.caption.text + '**\n'
        elif i.name == 'tr':
            #print("> tagTable()->i.name=='tr'")
            #print("> tagTable()->i.class is '{}'".format(i['class']))
            try:
                cls = i['class']
            except:
                cls = None

            if  cls and 'br' in cls:
                #print("> tagTable()->tr.class is 'br'")
                tmp += tagTRHead(i)
            else:
                #print("> tagTable()->tr.class is empty")
                tmp += tagTR(i) 
    tmp += '\n'
    return(tmp)
    
def tagP(P, href):
    tmp = ''
    for child in P.children:
        if child.name == 'span' or child.name == 'code' or child.name == 'pre':
            tmp += '`' + child.text + '`'
        elif child.name == 'a':
            tmp += '[{}]({})'.format(child.text, href.split('/')[0] + '//' + href.split('/')[2] + child['href'])
        else:
            tmp += child.text
    return(tmp.strip().replace('\n', '')+'\n\n')

def savePage(name, page):
    f = open(name, 'w', encoding='utf-8')
    for l in page: f.write(l)
    f.close()

def getHead(lvl, correct):
    return('#'*(lvl+correct) + ' ')

def processPage(url, correction):
    path = os.path.dirname(os.path.realpath(__file__))+'\\'
    name = url.split('/')[-1]
    cont = []

    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml') # html.parser
    soup.prettify()
    cont.append(getHead(1, correction) + soup.h1.text + '\n\n')
    content = soup.find(id='w-main')
    
    href = url.split('/')[0] + '//' + url.split('/')[2]

    for child in content.children:
        if child.name == 'p':
            try: cls = child['class']
            except: cls = None
            if cls and ('fig' in cls):
                cont.append('\n![' + child.img['alt'] + '](' + href + child.img['src'] + ')\n\n')
            elif cls and 'figsign' in cls:
                cont.append('*' + child.text.strip().replace('\n', '') + '*' + '\n\n')
            elif cls and 'exampleTitle' in cls:
                cont.append('**' + child.text + '**\n')
            elif cls and 'example' in cls:
                cont.append('```\n' + child.text + '\n```\n\n')
            else:
                cont.append(tagP(child, url))
        elif child.name == 'h2':
            cont.append(getHead(2, correction) + child.text + '\n\n') 
        elif child.name == 'h3':
            cont.append(getHead(3, correction) + child.text + '\n\n') 
        elif child.name == 'h4':
            cont.append(getHead(4, correction) + child.text + '\n\n') 
        elif child.name == 'h5':
            cont.append(getHead(5, correction) + child.text + '\n\n') 
        elif child.name == 'h6':
            cont.append(getHead(6, correction) + child.text + '\n\n') 
        elif child.name == 'w-example':
            cont.append('```html\n' + child.text + '\n```\n\n')
        elif child.name == 'pre':
            cont.append('```' + child.code['data-language'] + '\n' + child.code.text + '\n```\n\n')
        elif child.name == 'ul':
            cont.append(tagUL(child))
        elif child.name == 'table':
            cont.append(tagTable(child))
        elif child.name == 'strong':
            cont.append('**' + child.text + '**\n\n')

    savePage(path + name + '.md', cont)

if __name__ == "__main__":
    level, url = argsAnalize(sys.argv)
    if not(url): 
        usage()
        exit(1)
    
    print('Page URL: {}'.format(url))
    print('Start headers level set to: {}'.format(level if level else 'NOT CORRECTION'))

    processPage(url, level)