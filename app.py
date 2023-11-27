import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns # importing this for activity heatmap
st.sidebar.title("Whatsapp Chat Analyzer") # this will add sidebar and add the following text
st.sidebar.text('Developed by Naif Khurshid')
st.sidebar.divider()
st.sidebar.caption('Export the chat between user or group from whatsapp in 24 hrs format ')

# now we are adding upload file option in sidebar
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    #here we convet bytes data to strig
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    #this is going to show the data in our app of the file which we uploaded
    #st.text(data)
    # now we will call def preprocess from preprocessor and pass the data which will going to return the datafrmae
    df=preprocessor.preprocess(data)
    # we will display our dataframe in our app
    #st.dataframe(df)

    #now we will fetch the uniqe user from dataframe and save it to a list
    user_list=df['user'].unique().tolist();
    #we will remove the group notisfication from our list
    user_list.remove('group_notification')
    #now we will sort the list in ascending order
    user_list.sort()
    # we will add overall option to our list
    user_list.insert(0,"Overall")
    # we will add this user list in a sidebar as a dropdown
    selected_user=st.sidebar.selectbox("Show Analysis of wrt",user_list) # this will return the user which we selectd
    #-> HERE WE WILL DO ANALYSIS TO FIND THE TOTAL NUMBER OF MESSAGE SEND WORDS SEND MEDIA SEND AND LINK SEND BY USERS OR OVERALL
    #now we will add button and pass it to if which means if someone click then it will go inside if block
    if st.sidebar.button("Show Analyis"):
        #we will fetch the details of the user from fetch_stats funvtion in helper
        num_messages, words,num_media_messages,num_links=helper.fetch_statas(selected_user,df)
        st.title('Top Statistics')
        #now we will crete 4 coloms
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages") # this is going to create a column header of col1
            st.title(num_messages) # this will show the tot message under tot msg col
        with col2:
            st.header("Total Words") # this is going to create a column header of col2
            st.title(words) # this will show the tot words title under tot msg col
        with col3:
            st.header("Media Send") # this is going to create a column header of col3
            st.title(num_media_messages) # this will show the tot media send by user or overall  title under media shared column
        with col4:
            st.header("Links Send") # this is going to create a column header of col3
            st.title(num_links) # this will show the tot media send by user or overall  title under media shared column

        #->monthly timeline analysis
        # we will our monthly_timeline fuction which will return the df
        st.title('Monthly Timeline')
        #calling function
        timeline=helper.monthly_timeline(selected_user,df)
        #creating subplots
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        # rotating x axis index vertically
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #-> daily timeline analysis

        # we will our daily_timeline fuction which will return the df
        st.title('Daily Timeline')
        #calling function
        daily_timeline=helper.daily_timeline(selected_user,df)
        #creating subplots
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='red')
        # rotating x axis index vertically
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #-> weekly analysis day wise sunday to saturday
        st.title('Activity Map')
        # creating 2 columns
        col1,col2=st.columns(2)
        with col1:
            st.header('Most Busy Day')
            # calling our function which will return the df
            busy_day=helper.weekly_analysis_map(selected_user,df)
            # creating subplot
            fig,ax=plt.subplots()
            # creating bar plot
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            # calling our function which will return the df
            busy_month=helper.month_analysis_map(selected_user,df)
            # creating subplot
            fig,ax=plt.subplots()
            # creating bar plot
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #-> creating heatmap to display heatmap activity at different time period
        st.title('Weekly Activity Heatmap')
        # calling the function
        user_heatmap=helper.activity_heatmap(selected_user,df)
        #creating subplot
        fig,ax=plt.subplots()
        # initializing ax with seaborn heatmap and passing the pivot table
        ax=sns.heatmap(user_heatmap)
        # dsipaly it
        st.pyplot(fig)








        #-> We will find the most active user in a group
        if selected_user=='Overall':
            #here we will crete a title that is most active user and it will have two columns
            st.title('Most Active Users')
            #calling our most busy function it will return a  name of users with as a df and another df which will contain the name of users and there activity percentage
            x,new_df=helper.most_busy_user(df)
            #This line creates a new figure and axis using Matplotlib. The fig variable represents the
            # entire figure, and ax represents the axis or subplot within that figure.
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                # This line creates a bar plot using Matplotlib's bar function.
                # It uses the index of the DataFrame x for the x-axis values and the values of the DataFrame x for the
                # y-axis values. The bars are colored red.
                ax.bar(x.index, x.values,color='red')
                # This line rotates the x-axis labels vertically for better readability.
                plt.xticks(rotation='vertical')
                #This line displays the Matplotlib figure (fig) using Streamlit's pyplot function.
                st.pyplot(fig)

            with col2:
                #here we will display our new_df which will contain the name of users and there activity percentage
                st.dataframe(new_df)

        #-> now we will create word cloud and call our function which will return the image object
        st.title('Word Cloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        # first we will crete subplot
        fig,ax=plt.subplots()
        #then we will display cloud word cloud image in the axis of plot
        ax.imshow(df_wc)
        #then we will display our whole figure
        st.pyplot(fig)

        #->analysis most common word used
        # here we will call our function most common word which will return a dataframe
        most_common_df=helper.most_common_word(selected_user,df)

        # now we will display our dataframe
        # we will convert it to bar graph
        fig,ax=plt.subplots()
        # we will usr horizontal bar
        ax.barh(most_common_df[0],most_common_df[1])
        #ritating the x index
        plt.xticks(rotation='vertical')
        st.title('Most Common Words Used')
        st.pyplot(fig)
        #st.title('Most Common Words Used')
        #st.dataframe(most_common_df)

        #-> Analysis of emoji
        #calling emoji function which will return emoji df
        st.title('Emoji Analysis')
        emoji_df=helper.emoji_helper(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            #the firts parameter is the value and then we ars passing the lables we areusing head to display only 5 emoji
            #autopct wlll show the percentage
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)










