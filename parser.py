import os, sys, requests, re
from bs4 import BeautifulSoup, Tag

parts = [
        'h1', 
        '#w-main'
        ]

tags = {
    'p'         :   '{}\n\n',
    'span'      :   '`{}`',
    'h1'        :   '\n# {}\n',
    'h2'        :   '\n## {}\n',
    'h3'        :   '\n### {}\n',
    'code'      :   '\n```{data-language}\n{}\n```\n',
    'a'         :   '[{}]({href})',
    'p.figsign' :   '*{}*\n\n',
    'img'       :   '![{alt}]({!src})',
    'li'        :   '- {}\n',
    'ul'        :   '{}\n',
    'w-example' :   '\n```html\n{}\n```\n',
    'p.exampleTitle' : '\n**{}**\n',
    'strong'    :   '\n**{}**\n\n',
    None        :   '{}'
}

def expandLink(link: str, baselink: str = '') -> str:
    base = re.search('(https{0,1}://[a-zA-Z0-9_\-\.]*\.[a-zA-Z0-9]{2,4})[\?]?', baselink).group(1)
    if not(re.search('(https{0,1}://[a-zA-Z0-9_\-\.]*\.[a-zA-Z0-9]{2,4})[\?]?', link)):
        tmp = ''
        if (link[0] != '/') and (base[-1] != '/'): tmp = '/'
        return(base + tmp + link)
    else: return(link)

def expandPattern(tag_: Tag, pattern: str) -> str:
    res = re.findall('{(\!{0,1}[a-zA-Z0-9_-]{1,20})}', pattern)
    for r in res:
        try: attr = tag_[r[1:] if r[0]=='!' else r]
        except: attr = ''
        if attr and r[0]=='!': attr = expandLink(attr, baseLink)
        pattern = re.sub('{'+r+'}', attr, pattern, count=1)
    return(pattern)

def findPattern(tag_: Tag) -> str:
    global tags
    patlist = []
    try: patlist.append(tag_.name + '#' + tag_.attrs['id'])
    except: pass
    try:
        for class_ in tag_.attrs['class']: patlist.append(tag_.name + '.' + class_)
    except: pass 
    patlist.append(tag_.name)
    
    for sign in patlist:
        if sign in tags.keys():
            return(tags[sign])

    return('{}')

def walk(dom: Tag) -> str:
    result = ''
    for child in dom.children:
        if child.name == None: result += child.text if (child.text != '' and child.text != '\n') else ''
        else:
            try: result += expandPattern(child, findPattern(child)).format(walk(child))
            except: result += walk(child)
    return(result)   
    

if __name__ == "__main__":
    global baseLink
    baseLink = sys.argv[1]
    soup = BeautifulSoup(requests.get(baseLink).content, 'lxml')
    soup = BeautifulSoup(   ''.join([str(soup.find(id=part[1:])) 
                            if part[0]=='#' else str(soup.find(part)) 
                            for part in parts]), 'lxml')
    # the following code needs to be rewritten 
    f = open('111.md', 'w', encoding='utf-8')
    
    f.write(walk(soup))
    f.close() 