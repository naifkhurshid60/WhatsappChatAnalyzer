import  pandas as pd
from collections import Counter
from wordcloud import WordCloud # this lib is used to generate wordcloud
import emoji
from urlextract import  URLExtract #this lib is for extracting the url in our message
extract=URLExtract() # CREATING THE OBJECT OF IT
def fetch_statas(selected_user,df):# this function will fetch total messages and total words send by overall or individual
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    #1 we will fetch total number messsage
    num_messages=df.shape[0] # this will return total number of rows
    #2 we will etch total number  words
    words=[]
    for message in df['message']:
        words.extend(message.split()) #here we are splitting each message on the basis of space and adding it to our word list
    #3 We will fetch total number of media send by user or overall
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0] # this will return total number of rows of media messages

    #4 NOW WE WILL CTRACT THE URL FROM MESSGAES AND RETURN NUMBER OF URL IN MESSAGES
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message)) # it will add the url from message to links list

    return num_messages,len(words),num_media_messages,len(links)

# this funtion will take df as parameter and return the most active user
def most_busy_user(df):
    # here we are couting the value of each user in oor dataframe bt using value_count and head will return top 5 user only in decendong order
    x=df['user'].value_counts().head()
    #here we are counting the freqency of each user and converting the freqencu to percntage and the convering it to dataframe and change the column name
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'Percent'})
    return x,df
def create_wordcloud(selected_user,df):
    #we will open stop_hinglish file in read mode and initailize it stop_word variable
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    # now we will remove group notisfication,media ommited and stopword from our dataframe
    temp=df[df['user']!='group_notisfication']
    temp=df[df['message']!='<Media omitted>\n']
    # we will crete a function to remove stop words from string
    def remove_stop_words(message):
        y=[] # creting empty list
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        # we will return the list as a string
        return " ".join(y)
    # now we will crete a object of world cloud and pass the height witdth and font size of world cloud
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    # we will apply remove stop words function to message column
    temp['message']=temp['message'].apply(remove_stop_words)
    # generarte function will used to crete image of word cloud and we pass the column message and each message will be separated
    # with space so it will take each word in a word cloud
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return  df_wc
def most_common_word(selected_user,df):
    # we will open stop_hinglish file in read mode and initailize it stop_word variable
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    # now we will remove group notisfication,media ommited and stopword from our dataframe
    temp=df[df['user']!='group_notisfication']
    temp=df[df['message']!='<Media omitted>\n']
    # here we are removing stop words so we are iterating to each message in our dataframe and then itterating to
    #each word in df, if those word are not present in hinglish.txt then we append it to our list
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    # here we will crete a dataframe of most 20 commonwords in our words list and it will contain coloum
    # that count the frequency of each word
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
# analysis of emoji
def emoji_helper(selected_user,df):
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    # creating a empty list
    emojis = []
    for message in df['message']:
        #For each character (c) in the current message, it checks if the character is an emoji by verifying if it
        # exists in the set of English Unicode emojis (emoji.UNICODE_EMOJI['en']). If it is an emoji, it adds it to
        # the emojis list.
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    #Counter(emojis): Uses the Counter class from the collections module to count the occurrences of each emoji in
    # the emojis list. The result is a dictionary-like object where the keys are emojis, and the values are their respective
    # counts.
    #Retrieves the emojis and their counts in descending order, meaning the most frequently used emojis come first.
    Counter(emojis).most_common(len(Counter(emojis)))
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

#-> monthly timeline analysis fuction
def monthly_timeline(selected_user,df):
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    # here we will crete new dataframe grouping on basis of year,month and month_num and another column with count of message
    # reset index will crete a dataframe
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    # creating empty list
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    # adding it to our dataframe
    timeline['time']=time
    return timeline
#-> daily timeline analysis fuction
def daily_timeline(selected_user,df):
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user

    #applying groupby to df on only date and counting the message to another column and reting dataframe
    timeline=df.groupby('only_date').count()['message'].reset_index()
    #returning dataframe
    return timeline
#-> weekly map  function
def weekly_analysis_map(selected_user,df):
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    #returning the countof day_name
    return df['day_name'].value_counts()
#-> month map  function
def month_analysis_map(selected_user,df):
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    #returning the countof month name
    return df['month'].value_counts()

# creating heatmap
def activity_heatmap(selected_user,df):
    if(selected_user!='Overall'):# We will crete new user dataframe of that user only
        df=df[df['user']==selected_user] # create a new dataframe of selcted user
    # here creating pivot table with index day-name colums will be period  aggfunc is count and fillna is used to fill nan values with 0
    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap





















