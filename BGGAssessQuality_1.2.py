'''
BGGAssessQuality.py

Display selected statistics for game specified by its ID.
'''

from bs4 import BeautifulSoup
import re
import StringIO
import sys
import Tkinter as Tk
import urllib2

URL = 'http://www.boardgamegeek.com/boardgame/%d/'

def getAssessment(id):
    url = URL % id
    doc = urllib2.urlopen(url).read()
    soup = BeautifulSoup(doc)
    b = StringIO.StringIO()
    print soup.prettify()
    fields = {
        u'AverageRating': float,
        u'AvgGameWeight': float,
        u'BoardGameRank': int,
        u'Fans': int,
        u'HasPartsForTrade': int,
        u'NumRatings': int,
        u'NumViews': int,
        u'PersonalComments': int,
        u'PlaysThisMonth': int,
        u'StandardDeviation': float,
        u'TotalPlays': int,
        u'UsersOwning': int,
        u'UsersTrading': int,
        u'UsersWanting': int,
        u'WantPartsInTrade': int,
        u'WarGameRank': int,
    }
    record = { }
    found = False
    title = soup.find('title').get_text('', strip=True)
    print >>b, title
    print >>b
    for table in soup.find_all('table', class_='geekitem_module'):
        link = table.find('a')
        name = link.get('name')
        if name == 'statistics':
            table2 = table.find('table')
            for tr in table.find_all('tr')[1:]:
                td = tr.find_all('td')
                if td and len(td) >= 2:
                    try:
                        t = td[0].get_text('', strip=True)
                        t = re.sub(r'[^A-Za-z0-9]', '', t)
                        if t in fields:
                            v = td[1].get_text('', strip=True)
                            v = re.sub(r'[^0-9.]', '', v)
                            record[t] = fields[t](v)
                    except:
                        if td:
                            print >>sys.stderr, 'Failed 1: ', td.prettify()

            for field in ['AverageRating', 'BoardGameRank', 'Fans',
                          'TotalPlays', 'UsersOwning', 'WarGameRank']:
                if field in record:
                    try:
                        value = record[field]
                        if type(value) == int:
                            print >>b, '%s: %d' % (field, value)
                        elif type(value) == float:
                            print >>b, '%s: %.2f' % (field, value)
                        else:
                            print >>b, '%s:' % (field), value
                        found = True
                    except:
                        if field:
                            print >>sys.stderr, 'Failed 2:', field
            if found: break
    if not found:
        print >>sys.stderr, 'Statistics Geek Module not found'
        sys.exit(1)

    text = b.getvalue()
    b.close()
    return text

    fancontrols = soup.find('div', id='fancontrols')
    link = fancontrols.find('a')
    fans = int(link.get_text('', strip=True))
    print 'fans:', fans

    for rank in soup.find_all('div', class_='mf nw b'):
        t = rank.get_text('', strip=True)
        m = re.compile('([^:]+):(.*)').match(t)
        if not m: continue
        rankname = m.group(1)
        rankvalue = int(m.group(2))
        print '%s: %d' %(rankname, rankvalue)

class App(Tk.Tk):
    def __init__(self, parent=None):
        Tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.label1 = Tk.Label(self, text='Game ID', anchor='e')
        self.label1.grid(row=0, column=0)
        
        self.gameid = Tk.Entry(self)
        self.gameid.grid(row=0, column=1, sticky='E')
        self.gameid.focus_set()
        self.gameid.bind('<Return>', self.gameid_action)

        self.text = Tk.Text(self)
        self.text.config(state=Tk.DISABLED)
        self.text.grid(row=1, column=0, columnspan=3, sticky='nsew')

        self.button = Tk.Button(self, text="QUIT", width=8, padx=5, pady=5,
                                command=self.destroy)
        self.button.grid(row=21, column=2, sticky='E')

        self.grid_columnconfigure(0, minsize=100,  weight=0)
        self.grid_columnconfigure(1, minsize=100,  weight=0)
        self.grid_columnconfigure(2, minsize=200,  weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def gameid_action(self, event):
        self.assess_action()

    def assess_action(self):
        try:
            id = int(self.gameid.get())
            t = getAssessment(id)
        except:
            t = 'Invalid game id'
        self.text.config(state=Tk.NORMAL)
        self.text.delete(1.0, Tk.END)
        self.text.insert(Tk.END, t)
        self.text.config(state=Tk.DISABLED)


if __name__ == '__main__':
    app = App()
    app.title('BGGAssessQuality')
    app.mainloop()
    sys.exit(0)

