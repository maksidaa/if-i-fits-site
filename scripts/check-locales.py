#!/usr/bin/env python3
"""Language-only page checks. Run after build-locales.py."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess
root=Path(__file__).resolve().parent.parent
locales=['en','es','pt-BR','ja','ko','zh-Hans']
class Page(HTMLParser):
 def __init__(self):super().__init__();self.lang=None;self.links=[];self.nav=False;self.choices=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html':self.lang=a.get('lang')
  if tag=='nav' and a.get('class')=='languages':self.nav=True
  if tag=='a' and self.nav:self.choices+=1
  if tag in ['a','img','link']:
   u=a.get('src',a.get('href',''))
   if u and not u.startswith(('http:','https:','#','mailto:')):self.links.append(u)
 def handle_endtag(self,tag):
  if tag=='nav':self.nav=False
for locale in locales:
 catalog=json.loads((root/'locales'/f'{locale}.json').read_text())
 assert set(catalog)==set(json.loads((root/'locales/en.json').read_text())),locale
 for name in ['index.html','support.html','privacy.html']:
  f=root/name if locale=='en' else root/locale/name
  p=Page();p.feed(f.read_text());assert p.lang==locale,(f,'language');assert p.choices==6,(f,'language choices')
  for link in p.links:assert (f.parent/link).exists(),(f,link)
for name in ['index.html','support.html','privacy.html']:
 original=subprocess.check_output(['git','show',f'HEAD:{name}'],cwd=root).decode()
 strip=lambda s:re.sub(r'\n?<!-- language-(?:head|nav):start -->.*?<!-- language-(?:head|nav):end -->','',s,flags=re.S).replace('\n\n</head>','\n</head>')
 assert strip((root/name).read_text())==strip(original),(name,'unrelated English change')
assert not subprocess.check_output(['git','diff','--name-only','--','ota/'],cwd=root).strip(),'ota files changed'
print('PASS: all 18 pages, 6 language choices each, local links/assets, matching catalogs, original English, no OTA changes.')
