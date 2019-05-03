
import schedule
import praw
import feedparser
from requests import get
from bs4 import BeautifulSoup
import time
import lxml

urlRSS = [
            ("Online Khabar", "https://www.onlinekhabar.com/feed"),
            ("Himalayan Times", "https://thehimalayantimes.com/feed/"),
            ("Ratopati", "http://ratopati.com/rss/"),
            ("Nepali Times", "https://www.nepalitimes.com/feed/"),
            ("Lokantaar", "http://lokaantar.com/rss/"), #useless
            ("Pahilo Post", "http://www.pahilopost.com/rss"),
            ("Thaha Khabar", "http://thahakhabar.com/rss/"),
            ("Ujyalo Online", "http://ujyaaloonline.com/rss/"),
            ("Setopati", "https://setopati.com/feed"),
         ]

selftext = """News sites:\n 
1. **[Online Khabar](https://www.onlinekhabar.com/)**
2. **[Himalayan Times](https://thehimalayantimes.com/)**
3. **[Ratopati](https://ratopati.com/)**
4. **[Nepali Times](https://www.nepalitimes.com/feed/)**
4. **[Lokantaar](https://lokaantar.com/)**
5. **[Pahilo Post](http://www.pahilopost.com/)**
6. **[Thaha Khabar](http://thahakhabar.com/)**
7. **[Ujyalo Online](https://ujyaaloonline.com/)**
8. **[Setopati](https://setopati.com/)**"""

def getTitle(): #GUILTY OF THIS scraping
    html = get("https://www.hamropatro.com/date-converter").text
    soup = BeautifulSoup(html, "html.parser")
    date = soup.find("span", {"class": "nep"}).text[1:-1]
    time = soup.find("div", {"class": "time"}).text[1:-1].split("\n")[0][1:]

    title = date+ " : "+ time
    return title

##    
def comment_submission(submission, replyText):
    start = 0
    while True:
        try:
            commentMain = submission.reply(replyText)
            break
        except:
            start = start + 1
            print(". ", end="")
            time.sleep(5)
            if start == 5: 
                return None
    return commentMain

            
def comment_reply(comment, replyText):
    start = 0
    while True:
        try:
            retTemp = comment.reply(replyText)
            break
        except:
            start = start + 1
            print(". ", end="")
            time.sleep(5)
            if start == 5: 
                return None
    return retTemp

def main(): #to make post in reddit and comment
    print("START \n")
    reddit = praw.Reddit(username = "",
                     password = "",
                    client_id = "",
                    client_secret = "",
                    user_agent = "NepalNews by /u/Gaumatri")
    
    AllFeed = []
    for _ in urlRSS:
        feed = feedparser.parse(_[1])
        AllFeed.append((_[0], feed))
        
    subreddit = reddit.subreddit('NewsNepal')
    post = subreddit.submit(getTitle(), selftext=selftext)
    print("POST CREATED")
    
    Thread = []
    comment = ""
    commentTree = """{}
* [Link]({})

* Summary: {}

* Description: {}"""

    for feed in AllFeed:
        comment = "# {}\n\n\n".format(feed[0])
        for news in feed[1]["entries"]:
            comment = comment + "* {}\n".format(news["title"])

        submission = reddit.submission(post.id)
        # submission = reddit.submission("bje0or")
    
        commentMain = comment_submission(submission, comment)
        if commentMain == None:
            return None
            print("STOPPED DUE TO TOO FREQUENT COMMENTING")
#         commentMain = submission.reply(comment)
        
        print("URL: {}".format(submission.shortlink))
        print("    COMMENT MADE")
        comment = reddit.comment(id= commentMain.id)

        for news in feed[1]["entries"]:
            time.sleep(10)

            # tmptext = news.get("content", None)
            # if tmptext != None:
            #     text = news["content"][0].get("value", "VIEW SOURCE")
            #     cleantext = BeautifulSoup(text, "lxml").text.replace("\n", "\n\n")
            # else:
            #     cleantext = "[VIEW SOURCE]({})".format(news["link"])

            cleantext = "[VIEW SOURCE]({})".format(news["link"])
            replyText = commentTree.format(news["title"], news["link"], news["summary"], cleantext)
            
            check  = comment_reply(comment, replyText[:9500])  
            if check == None:
                return None
                print("STOPPED DUE TO TOO FREQUENT COMMENTING")
                
            print("        REPLIED TO COMMENT")



# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
# schedule.every().day.at('22:30').do(job_that_executes_once)



#THE TIME SHOULD BE INPUT AT 0 timezone
schedule.every().day.at("00:15").do(main)
schedule.every().day.at("06:15").do(main)
schedule.every().day.at("12:15").do(main)


print("OK my watch starts")
time.sleep(60)
while True:
    print(". ", end="")
    use = schedule.run_pending()
    time.sleep(10)
