# On the listing for a day, films information is at depth 6 and below. 
# Title: in <h6> element, hyperlinked to further description.

from wwwclient import browse, scrape

urls_seen = {
    # url: True, ...
    }
movies = {
    # title: {url: ..., ... }, ... 
    }
for day in range(17,27):
    print day
    session = browse.Session('http://www.worldfilmbkk.com/theprograms_sections.php?showdate=%s.11.12'%day)
    page = session.page()
    tree = scrape.HTML.tree(page)
    subtree = tree.cut(below=5).filter(accept = lambda n:n.name.lower() == 'h6')
    links = scrape.HTML.links(subtree)
    for a,url in links:
        if not urls_seen.has_key(url):
            urls_seen[url] = True
            session = browse.Session(url)
            page = session.page()
            tree = scrape.HTML.tree(page)
            st = tree.cut(below=5)
            # The film title is in the first H3 element
            title = st.find(lambda n:n.name=='h3')[0].text()
            if not movies.has_key(title):
                movies[title] = {'url': url}
                print title
                info_ul = st.find(lambda n:n.name=='ul')[0]
                for i in info_ul.children:
                    print i.text()
                    text = i.text().strip()
                    if text:
                        if ':' in text:
                            key, value = text.split(':', 1)
                            key = key.strip()
                            if movies[title].has_key(key):
                                value = '\n'.join([movies[title][key], value])
                        else:
                            key = 'origin'
                            value = text
                        print 'key', key, 'value', value, 
                        movies[title][key] = value
                synopsis = ''
                for i in st.find(lambda n:n.name=='p')[0].children:
                    if 'mso-' in i.text():
                        # Some descriptions have MS Office bumf in them.
                        pass
                    else:
                        synopsis += i.text()
                movies[title]['synopsis'] = synopsis

# In case you want to restart from here:
# import pickle
# pickle.dump(open('movies.pickle', 'w'))

# Create a calendar
from icalendar import Calendar, Event, LocalTimezone
cal = Calendar()
from datetime import datetime
cal.add('prodid', '-//Scraped from website//...//')
cal.add('version', '1.0')
import pytz
import re

tz = pytz.timezone('Asia/Bangkok')
# tz = LocalTimezone()
dt_re = re.compile('(?P<day>\d\d)\.(?P<month>\d\d)\.(?P<year>\d\d) \((?P<hour>\d\d):(?P<minute>\d\d)\)')

for title in movies:
    details = movies[title]
    screening = details.get('Screening Date')
    if not screening:
        continue
    times = dt_re.findall(screening)
    for d,m,y,H,M in times:
        event = Event()
        description = ''
        for k,v in details.items():
            if not isinstance(v, unicode):
                v = unicode(v, encoding='utf-8')
                v = ' '.join(v.splitlines())
            description += '   %s: %s' % (k,v)
        event.add('summary', title.replace(',','\,').replace(';','\;'))
        event.add('description', description.replace(',','\,').replace(';','\;'))
        event.add('dtstart', datetime(int('20'+y),int(m),int(d),int(H),int(M),0,tzinfo=tz))
        event.add('dtend', datetime(int('20'+y),int(m),int(d),int(H)+1,int(M),0,tzinfo=tz))
        cal.add_component(event)

f = open('movies.ics', 'wb')
f.write(cal.to_ical())
f.close()

