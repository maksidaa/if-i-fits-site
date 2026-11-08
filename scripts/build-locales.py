#!/usr/bin/env python3
"""Translate the existing English pages, preserving content/layout. Never publishes or touches ota/."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import json, re
root=Path(__file__).resolve().parent.parent
languages={'en':'English','es':'Español','pt-BR':'Português (Brasil)','ja':'日本語','ko':'한국어','zh-Hans':'简体中文'}
pages=['index.html','support.html','privacy.html']
base='https://maksidaa.github.io/if-i-fits-site/'

def without_links(source):
    return re.sub(r'\n?<!-- language-(?:head|nav):start -->.*?<!-- language-(?:head|nav):end -->', '', source, flags=re.S)

class Translate(HTMLParser):
    def __init__(self, locale, dictionary):
        super().__init__(convert_charrefs=True)
        self.locale=locale;self.dictionary=dictionary;self.out=[];self.skip=0
    def t(self, value):
        key=' '.join(value.split())
        if not key:return value
        if key not in self.dictionary:raise ValueError(f'{self.locale}: missing translation: {key}')
        leading=value[:len(value)-len(value.lstrip())];trailing=value[len(value.rstrip()):]
        return leading+escape(self.dictionary[key])+trailing
    def handle_starttag(self, tag, attrs):
        raw=self.get_starttag_text()
        values=dict(attrs)
        def replace(match):
            name,quote,value=match.group(1),match.group(2),match.group(3)
            if tag=='html' and name=='lang':value=self.locale
            elif name in ['src','href'] and (value.startswith('images/') or value=='style.css'):value='../'+value
            elif name in ['alt','aria-label','title'] and value:value=self.t(value)
            elif tag=='meta' and name=='content' and (values.get('name')=='description' or values.get('property') in ['og:title','og:description']):value=self.t(value)
            else:return match.group(0)
            return name+'='+quote+value+quote
        raw=re.sub(r'\b(lang|src|href|alt|aria-label|title|content)=("|\')(.*?)\2',replace,raw)
        self.out.append(raw)
        if tag in ['style','script']:self.skip+=1
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):
        if tag in ['style','script']:self.skip-=1
        self.out.append('</'+tag+'>')
    def handle_data(self,data):self.out.append(data if self.skip else self.t(data))
    def handle_comment(self,data):self.out.append('<!--'+data+'-->')
    def handle_decl(self,data):self.out.append('<!'+data+'>')

for page in pages:
    source=without_links((root/page).read_text())
    for locale in languages:
        dictionary=json.loads((root/'locales'/f'{locale}.json').read_text())
        if locale=='en':output=source
        else:
            parser=Translate(locale,dictionary);parser.feed(source);output=''.join(parser.out)
        def path(loc):return ('' if loc=='en' else loc+'/')+page
        alternates='\n<!-- language-head:start -->\n'+''.join('<link rel="alternate" hreflang="'+loc+'" href="'+base+path(loc)+'">\n' for loc in languages)+'<link rel="alternate" hreflang="x-default" href="'+base+page+'">\n<!-- language-head:end -->'
        prefix='' if locale=='en' else '../'
        nav='\n<!-- language-nav:start -->\n<nav class="languages" aria-label="'+escape(dictionary['Choose language'])+'">'+''.join('<a lang="'+loc+'" href="'+prefix+path(loc)+'"'+(' aria-current="page"' if loc==locale else '')+'>'+label+'</a>' for loc,label in languages.items())+'</nav>\n<!-- language-nav:end -->'
        output=output.replace('\n</head>',alternates+'\n</head>').replace('</header>','</header>'+nav)
        directory=root if locale=='en' else root/locale;directory.mkdir(exist_ok=True)
        (directory/page).write_text(output)
print('Built 15 translations and language navigation. Original English content retained; ota/ unchanged.')
