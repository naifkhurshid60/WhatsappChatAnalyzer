import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'# here we are using regular expression so we will crete 2 cols 1 for date and time and another for msg and user name
    messages = re.split(pattern, data)[1:] # here we are making them split in a 2 cols order and storing the messages and user name in messages with help of regular expression

    dates=re.findall(pattern,data)
    #here we are converting messages and date into dataframe with 2 cols user-message and message date
    a = {'user_messages': messages, 'message_date': dates}

    df = pd.DataFrame.from_dict(a, orient='index')
    # changing the rows to cols and cols to rows
    df=df.transpose()

    #renaming colums
    df.rename(columns={'message_date': 'date'}, inplace=True)
    # changing the format of date
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M - ')
    users=[]
    messages=[]
    for message in df['user_messages']:
        # using regex split to split the text into user and message and adding then into diif list
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            #if it following pattern exist it means that send a msg so will split them add them into user and messges list
            users.append(entry[1])
            messages.append(entry[2])
        else:
            # if condition dose not follows then it means that it is group notisfication so we will add string group notisfication
            #in user list and messgae list be null
            users.append('group_notification')
            messages.append(entry[0])
    # now we adding this to our dataframe and after that removing our user_message column
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_messages'],inplace=True)
    # Now we are breaking the column date into year month coloumns
    #first we will extract year and add it to our dataframe
    df['year']=df['date'].dt.year
    # now we will remove nan vaues from it to convert it to int
    df.dropna(subset=['year'],axis=0,inplace=True)
    #extraccting date from the df and adding it to column
    df['only_date']=df['date'].dt.date
    #now we will extract month number and add it yo our dataframe
    df['month_num']=df['date'].dt.month
    # now we will extract month and add it to datframe
    df['month']=df['date'].dt.month_name()
    #now we will extract date
    df['day']=df['date'].dt.day
    # extrating days and adding it to dataframe sunday to saturday
    df['day_name']=df['date'].dt.day_name()
    # now we extract hours and minute
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    #adding period that is extracting the gour suppose 17:00 hr and we will converr it to 17-18 ans 23 to 23-0
    # creating empty list
    period=[]
    #traversing each hour on basis of day_name and hour and adding it to list in a perticular format
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+'-'+str(00))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    # adding the list to dataframe
    df['period']=period



    # now return the dataframe
    return df
