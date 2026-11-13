import re,json,pathlib
p=pathlib.Path('Bakups/13del11del20261030amnew.sql'); s=p.read_text(encoding='utf-8',errors='replace')
# Remove SQL comments only for parsing structural declarations, retain source for DDL/objects.
def split_top(src):
 out=[]; start=0; depth=0; quote=None; esc=False
 for i,c in enumerate(src):
  if quote:
   if esc: esc=False
   elif c=='\\': esc=True
   elif c==quote:
    if i+1<len(src) and src[i+1]==quote: continue
    quote=None
  elif c in "'\"`": quote=c
  elif c=='(': depth+=1
  elif c==')': depth-=1
  elif c==',' and depth==0: out.append(src[start:i].strip()); start=i+1
 out.append(src[start:].strip()); return out
# CREATE TABLE definitions terminate at matching close paren preceding engine clause
T={}
for m in re.finditer(r'CREATE\s+TABLE\s+`([^`]+)`\s*\(',s,re.I):
 name=m.group(1); j=m.end(); depth=1; q=None; esc=False
 while j<len(s) and depth:
  c=s[j]
  if q:
   if esc: esc=False
   elif c=='\\': esc=True
   elif c==q: q=None
  elif c in "'\"`": q=c
  elif c=='(': depth+=1
  elif c==')': depth-=1
  j+=1
 body=s[m.end():j-1]; ddl=s[m.start():j]+(re.search(r'\s*ENGINE=.*?;',s[j:],re.S|re.I).group(0) if re.search(r'\s*ENGINE=.*?;',s[j:],re.S|re.I) else ';')
 cols=[]; keys=[]
 for part in split_top(body):
  cm=re.match(r'^`([^`]+)`\s+(.+)$',part,re.S)
  if cm:
   cn,rest=cm.groups(); typ=re.match(r'(.+?)(?=\s+(?:NOT\s+NULL|NULL\b|DEFAULT\b|AUTO_INCREMENT\b|ON\s+UPDATE\b|COMMENT\b|GENERATED\b)|$)',rest,re.I|re.S)
   cols.append({'name':cn,'type':typ.group(1).strip(),'nullable':not bool(re.search(r'\bNOT\s+NULL\b',rest,re.I)),'default':(re.search(r'\bDEFAULT\s+((?:\'[^\']*\')|(?:b\'[^\']*\')|(?:[^\s,]+))',rest,re.I).group(1) if re.search(r'\bDEFAULT\s+((?:\'[^\']*\')|(?:b\'[^\']*\')|(?:[^\s,]+))',rest,re.I) else None),'auto':bool(re.search(r'AUTO_INCREMENT',rest,re.I)),'onUpdate':(re.search(r'ON\s+UPDATE\s+[^,]+',rest,re.I).group(0) if re.search(r'ON\s+UPDATE\s+[^,]+',rest,re.I) else None),'raw':part})
  elif part: keys.append(part)
 T[name]={'columns':cols,'constraints':keys,'ddl':ddl.strip()}
# Count row tuples in INSERT ... VALUES, with quote-aware top-level tuple scanner
counts={k:0 for k in T}
for m in re.finditer(r'INSERT\s+INTO\s+`([^`]+)`[^;]*?\bVALUES\s*',s,re.I|re.S):
 name=m.group(1); i=m.end(); n=0; quote=None; esc=False; depth=0
 while i<len(s):
  c=s[i]
  if quote:
   if esc: esc=False
   elif c=='\\': esc=True
   elif c==quote:
    if i+1<len(s) and s[i+1]==quote: i+=1
    else: quote=None
  elif c in "'\"`": quote=c
  elif c=='(': depth+=1; 
  elif c==')':
   depth-=1
   if depth==0: n+=1
  elif c==';' and depth==0: break
  i+=1
 counts[name]=counts.get(name,0)+n
for name,x in T.items():
 x['rows']=counts.get(name,0)
 x['pk']=[]; x['fks']=[]; x['indexes']=[]; x['unique']=[]; x['checks']=[]
 for k in x['constraints']:
  if re.match(r'PRIMARY KEY',k,re.I): x['pk']+=re.findall(r'`([^`]+)`',k.split('(',1)[1].split(')',1)[0])
  fk=re.search(r'CONSTRAINT\s+`([^`]+)`\s+FOREIGN KEY\s*\((.*?)\)\s+REFERENCES\s+`([^`]+)`\s*\((.*?)\)',k,re.I|re.S)
  if fk: x['fks'].append({'name':fk.group(1),'columns':re.findall(r'`([^`]+)`',fk.group(2)),'table':fk.group(3),'refColumns':re.findall(r'`([^`]+)`',fk.group(4)),'raw':k})
  if re.match(r'(?:KEY|INDEX)\b',k,re.I): x['indexes'].append(k)
  if re.match(r'UNIQUE',k,re.I): x['unique'].append(k)
  if re.match(r'CONSTRAINT.*CHECK|CHECK',k,re.I): x['checks'].append(k)
 for col in x['columns']:
  col['pk']=col['name'] in x['pk']; col['fks']=[f for f in x['fks'] if col['name'] in f['columns']]; col['uk']=any(re.search(r'\(`'+re.escape(col['name'])+r'`\)',u) for u in x['unique'])
triggers=[]
for m in re.finditer(r'\bTRIGGER\s+`([^`]+)`\s+(BEFORE|AFTER)\s+(INSERT|UPDATE|DELETE)\s+ON\s+`([^`]+)`',s,re.I):
 if any(z['name']==m.group(1) for z in triggers): continue
 triggers.append({'name':m.group(1),'timing':m.group(2),'event':m.group(3),'table':m.group(4),'sql':''})
objects={k:[] for k in ['views','functions','procedures','events']}
for kind,pat in [('views',r'\bVIEW\s+`([^`]+)`\s+AS'),('functions',r'\bFUNCTION\s+`([^`]+)`'),('procedures',r'\bPROCEDURE\s+`([^`]+)`'),('events',r'\bEVENT\s+`([^`]+)`')]:
 for m in re.finditer(pat,s,re.I):
  if not any(o['name']==m.group(1) for o in objects[kind]): objects[kind].append({'name':m.group(1),'sql':''})
objects['triggers']=triggers
# Keep complete view SQL fragments and routine bodies available to the UI.
for v in objects['views']:
 m=re.search(r'\bVIEW\s+`'+re.escape(v['name'])+r'`\s+AS(.*?)(?:\*/)',s,re.I|re.S)
 v['sql']=('CREATE VIEW `'+v['name']+'` AS '+m.group(1).strip()) if m else ''
for kind,word in [('functions','FUNCTION'),('procedures','PROCEDURE'),('events','EVENT')]:
 for o in objects[kind]:
  m=re.search(r'CREATE\s+(?:DEFINER=`[^`]+`@`[^`]+`\s+)?'+word+r'\s+`'+re.escape(o['name'])+r'`.*?(?:END\s*;|\*/)',s,re.I|re.S)
  o['sql']=m.group(0) if m else ''
for t in triggers:
 m=re.search(r'\bTRIGGER\s+`'+re.escape(t['name'])+r'`.*?END\s*\*/',s,re.I|re.S)
 t['sql']=m.group(0) if m else ''
out={'database':'db_test','source':str(p),'tables':T,'objects':objects,'totalRows':sum(counts.values()),'totalFks':sum(len(t['fks']) for t in T.values())}
pathlib.Path('datos_bd.js').write_text('window.DB_DATA = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps({'tables':len(T),'counts':counts,'totalRows':out['totalRows'],'fks':out['totalFks'],'objects':{k:len(v) for k,v in objects.items()}},ensure_ascii=False,indent=2))
