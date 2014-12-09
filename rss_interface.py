import Tkinter as tk
import re
import feedparser
from future import Future
import webbrowser

rss_top = ["http://feeds.reuters.com/reuters/topNews","http://feeds.bbci.co.uk/news/rss.xml","http://rss.cnn.com/rss/edition.rss"]
rss_business = ["http://feeds.reuters.com/reuters/businessNews","http://feeds.bbci.co.uk/news/business/rss.xml","http://rss.cnn.com/rss/edition_business.rss"]
rss_tech = ["http://feeds.reuters.com/reuters/technologyNews","http://feeds.bbci.co.uk/news/technology/rss.xml","http://rss.cnn.com/rss/edition_technology.rss"]
rss_science = ["http://feeds.reuters.com/reuters/scienceNews","http://feeds.bbci.co.uk/news/science_and_environment/rss.xml","http://rss.cnn.com/rss/edition_space.rss"]
rss_entertainment = ["http://feeds.reuters.com/reuters/entertainment","http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml","http://rss.cnn.com/rss/edition_entertainment.rss"]
entries = []
searchedentries = []

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        global lb,keyword

        frame1 = tk.Frame(self)
        frame1.pack(fill=tk.X, expand=True)
        
        

        b1 = tk.Button(frame1,text="Top Story",command=self.ClickTop,bg="red")
        b2 = tk.Button(frame1,text="Business",command=self.ClickBus)
        b3 = tk.Button(frame1,text="Technology",command=self.ClickTech)
        b4 = tk.Button(frame1,text="Science",command=self.ClickSci)
        b5 = tk.Button(frame1,text="Entertainment",command=self.ClickEnt)
        b1.pack(side=tk.LEFT,padx=30,pady=5)
        b2.pack(side=tk.LEFT,padx=30)
        b3.pack(side=tk.LEFT,padx=30)
        b4.pack(side=tk.LEFT,padx=30)
        b5.pack(side=tk.LEFT,padx=30)

        searchframe = tk.Frame(self)
        searchframe.pack(fill=tk.X, expand=True)
        searchbutton = tk.Button(searchframe,text="Search",command=self.ClickSearch)
        keyword = tk.StringVar()
        txt = tk.Entry(searchframe,textvariable=keyword,width=100)
        txt.pack(side=tk.LEFT,padx=10,pady=5)
        searchbutton.pack(side=tk.LEFT,padx=10,pady=5)

        frame3 = tk.Frame(self)
        frame3.pack(fill=tk.X, expand=True)
        sb = tk.Scrollbar(frame3,orient=tk.VERTICAL)
        lb = tk.Listbox(frame3,yscrollcommand=sb.set,height=20)
        sb.configure(command=lb.yview)

        sb.pack(side=tk.RIGHT,fill=tk.Y)
        lb.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.X, expand=True)
        b6 = tk.Button(frame2,text="Read",command=self.ClickRead)
        b6.pack(side=tk.LEFT,padx = 10)
        b7 = tk.Button(frame2,text="Link", command=self.OpenUrl)
        b7.pack(side=tk.LEFT,padx = 10)

        frame4 = tk.Frame(self)
        frame4.pack(fill=tk.X, expand=True)
        self.titleVariable = tk.StringVar()
        lbltitle = tk.Label(frame4,font = ('bold'),textvariable=self.titleVariable)
        lbltitle.pack(side=tk.LEFT,pady=5)

        frame5 = tk.Frame(self)
        frame5.pack(fill=tk.X, expand=True)
        self.summaryVariable = tk.StringVar()
        lblsummary = tk.Label(frame5,textvariable = self.summaryVariable,wraplength=700,justify=tk.LEFT)
        lblsummary.pack(side=tk.LEFT)
    

    def ClickTop(self):
        del searchedentries[:]
        self.GetFeed(rss_top)
        self.setSelect()

    def ClickBus(self):
        del searchedentries[:]
        self.GetFeed(rss_business)
        self.setSelect()

    def ClickTech(self):
        del searchedentries[:]
        self.GetFeed(rss_tech)
        self.setSelect()

    def ClickSci(self):
        del searchedentries[:]
        self.GetFeed(rss_science)
        self.setSelect()        

    def ClickEnt(self):
        del searchedentries[:]
        self.GetFeed(rss_entertainment)
        self.setSelect()            

    def GetFeed(self,cat):
        del entries[:]
        future_calls = [Future(feedparser.parse,rss_url) for rss_url in cat]
        rss_feeds = [future_obj() for future_obj in future_calls]
        for feed in rss_feeds:
            entries.extend( feed[ "items" ] )

    def setSelect(self):
        lb.delete(0,tk.END)
        for entry in entries:
            lb.insert(tk.END,entry.title)

    def setSearchedSelect(self):
        lb.delete(0,tk.END)
        for entry in searchedentries:
            lb.insert(tk.END,entry.title)

    def ClickRead(self):
        if (searchedentries):
            self.titleVariable.set(searchedentries[self.whichSelected()].title)
            s = re.sub('<[^>]+>', '', searchedentries[self.whichSelected()].description)
        else:
            self.titleVariable.set(entries[self.whichSelected()].title)
            s = re.sub('<[^>]+>', '', entries[self.whichSelected()].description)
            
        self.summaryVariable.set(s)

    def ClickSearch(self):
        del searchedentries[:]
        for entry in entries:
            s = re.sub('<[^>]+>', '', entry.description)
            if(keyword.get().lower() in entry.title.lower()) or (keyword.get().lower() in s.lower()):
                searchedentries.append(entry)
        self.setSearchedSelect()
        

    def whichSelected(self):
        return int(lb.curselection()[0])

    def OpenUrl(self):
        if (searchedentries):
            webbrowser.open_new(searchedentries[self.whichSelected()].link)
        else :
            webbrowser.open_new(entries[self.whichSelected()].link)

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Online Article Searching Tool")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("700x550")
    root.mainloop()
