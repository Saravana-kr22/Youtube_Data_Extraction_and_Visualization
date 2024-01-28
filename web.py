import streamlit as st
from scripts.youtube_extraction import *
from scripts.mongodb import *
from scripts.mysql import *
from scripts.sql_query import *
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd


class Website:
    def __init__(self) :
        st.set_page_config(layout="wide", page_title="Youtube Data Extraction and Harvesting", page_icon="src/youtube.svg")
        self.website()

    def home(self):
                
        st.markdown("## :blue[Overview] : Retrieving the Youtube channels data from the Google API, storing it in a MongoDB as data lake, migrating and transforming data into a SQL database, then querying the data and displaying it in the Streamlit app.")
        st.markdown("## :blue[Technologies used] :")
        st.markdown("<ol><li> Python</li><li> Youtube Data API</li><li> MongoDB</li><li> MySql</li><li> Streamlit</li><li> matplotlib</li></ol>",
                    unsafe_allow_html= True)
    

    #data extraction webpage
    def data_extraction(self):
        Input_column , Display_column = st.columns(2, gap="large")
        with Input_column:
            #Input for the channel id
            st.header("Data Extraction")
            channel_id_input = st.text_input("Enter the Channel_ID",placeholder="Channel_ID", key = "channelid", 
                            help="Channel_id can be obtain from the share channel button in the channel details")
            channel_ids = channel_id_input.split(",")
            extract = st.button("Extract")
            if extract:
                Mongodb().delete_temp_data()
                for channel_id in channel_ids:
                    channel_id.replace(" ","")
                    info ={}
                    info = Youtube().channel_info(channel_id)
                    if info:                        
                        Mongodb().store_temp_info(info)        
                        st.success(f"Channel information has been extracted for {info['channel_name']}", icon="✅")
                          
                    else:
                        if channel_id:
                            st.error(f"Channel id {channel_id} is invalid, Please Enter a valid Channel id",  icon="🚨")
                        else:
                            st.warning( "Please Enter a Channel id for extract", icon="⚠️")
                st.info("Move to the Manage dataBase to store the data", icon = "⬅️")
               
        with Display_column:
            collections = Mongodb().collection_list("youtube_temp_data")
            if collections:
                st.header("Extracted Data")
                for colletion in collections:
                    st.write(colletion)

    #Function to manage the database
    def manage_database(self):
        mongodb_column , sql_column = st.columns(2, gap="large")
        with mongodb_column:
            collections = Mongodb().collection_list("youtube_temp_data")
            if collections:
                st.title("MongoDB")
                channels = st.multiselect("Select the channel to Store in MongoDB" , collections)
                if st.button("Store channel details to MongoDB", disabled= not channels):
                    for channel in channels:
                        existing_channels = Mongodb().collection_list("youtube_data_harversting")
                        if channel in existing_channels:
                            Mongodb().delete_document(channel)
                        channel_info = Mongodb().read_collection(channel)
                        playlist_info = Youtube().playlist_info(channel_info['channel_id'])
                        videos = Youtube().video_list(channel_info['channel_id'])
                        video_info = []
                        comment_info = []
                        for video in videos:
                            video_info.append(Youtube().video_info(video))
                            comment_info.append(Youtube().comment_info(video))

                        data = {'channel_info': channel_info,
                                'playlist_info': playlist_info,
                                'video_info': video_info,
                                'comment_info':comment_info}
                        
                        Mongodb().add_document(data)

                        st.success(f"{ data['channel_info']['channel_name']} has been stored successfully", icon="✅")
                        
            else:
                st.error(f"Channel Details is Not Extracted Yet",  icon="🚨")
                st.warning("Please Extract the channel details in the Data Extraction Page before store it in MongoDB",
                            icon = "⬅️")


        with sql_column:
            st.title("MySQL")
            availble_channels = Mongodb().collection_list("youtube_data_harversting")
            if availble_channels: 
                channel = st.selectbox("select the channel to Migrate to MySQL", availble_channels)
                if st.button("Migrate to MySQL", disabled= not channel):
                    if Mysql(channel).migrate_sql():
                        st.success(f"{ channel} has been successfully Migrated to MySQL", icon="✅")
                    else:
                        st.warning (f"{channel} data is availble in the Database",  icon="⚠️")
            else:
                st.warning("No Channel is found to migrate to MySQL", icon="⚠️")
                st.info("Store the data to the MongoDB to the Migrate to MySQL", icon = "⬅️")

    #function to view the data
    def data_visualization(self):
        analysis_column, visualization_column = st.columns(2, gap="large")
        a = 0
        with analysis_column:
            st.title("Data Analysis")
            channel_data = Mysql(0).list_channel_names()
            if channel_data:
                questions = ["What are the names of all the videos and their corresponding channels?", 
                            "Which channels have the most number of videos, and how many videos do they have?", 
                            "What are the top 10 most viewed videos and their respective channels?", 
                            "How many comments were made on each video, and what are their corresponding video names?", 
                            "Which videos have the highest number of likes, and what are their corresponding channel names?" ,
                            "What is the total number of likes and dislikes for each video, and what are their corresponding video names?" , 
                            "What is the total number of views for each channel, and what are their corresponding channel names?", 
                            "What are the names of all the channels that have published videos in the year 2022?", 
                            "What is the average duration of all videos in each channel, and what are their corresponding channel names?" ,
                            "Which videos have the highest number of comments, and what are their corresponding channel names?"]
                
                question = st.selectbox("Select a Quection below", questions)
                if question ==questions[0]:
                    st.dataframe(Sql().q1())
                    a = 0
                elif question == questions[1]:
                    st.dataframe(Sql().q2())
                    a = 1
                elif question == questions[2]:
                    st.dataframe(Sql().q3())
                    a = 2
                elif question == questions[3]:
                    st.dataframe(Sql().q4())
                    a = 3
                elif question == questions[4]:
                    st.dataframe(Sql().q5())
                    a = 4
                elif question == questions[5]:
                    st.dataframe(Sql().q6())
                    a = 5
                elif question == questions[6]:
                    st.dataframe(Sql().q7())
                    a = 6

                elif question == questions[7]:
                    st.dataframe(Sql().q8())
                    a = 7

                elif question == questions[8]:
                    st.dataframe(Sql().q9())
                    a = 8

                elif question == questions[9]:
                    st.dataframe(Sql().q10())
                    a = 9

            else:
                st.warning("No data found in MySQL Database", icon="⚠️")

        with visualization_column:
            st.title("Data Visualization")
            if a == 0:
                df = Sql().q1()
                channel_count = df['Channel Name'].value_counts()
                fig, ax = plt.subplots()
                ax.pie(channel_count, labels=channel_count.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  
                st.pyplot(fig)

            elif a == 1:
                df = Sql().q2()
                fig, ax = plt.subplots()
                ax.bar(df['Channel Name'], df['Video Count'])
                ax.set_ylabel('Video Count')
                ax.set_xlabel('Channel Name')
                st.pyplot(fig)

            elif a ==2:
                df = Sql().q3()
                fig,ax = plt.subplots()
                ax.pie(df['Views'], labels= df["Video Name"], autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

            elif a == 3:
                df = Sql().q4()
                fig, ax = plt.subplots()
                ax.bar(df['Video Name'], df['Comment Count'])
                ax.set_ylabel('Comment Count')
                ax.set_xlabel('Video Name')
                st.pyplot(fig)

            elif a == 4:
                df = Sql().q5()
                fig,ax = plt.subplots()
                ax.pie(df['Like Count'], labels= df["Video Name"], autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

            elif a == 5:
                df = Sql().q6()
                fig,ax = plt.subplots()
                ax.pie(df['Like Count'], labels= df["Video Name"], autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

            elif a == 6:
                df = Sql().q7()
                fig, ax = plt.subplots()
                ax.bar(df['Channel Name'], df['Views Count'])
                ax.set_ylabel('Views Count')
                ax.set_xlabel('Channel Name')
                st.pyplot(fig)

            elif a == 7:
                df = Sql().q8()
                video_count = df['Channel Name'].value_counts()
                fig, ax = plt.subplots()
                ax.pie(video_count, labels=video_count.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  
                st.pyplot(fig)

            elif a == 8:
                df = Sql().q9()
                fig, ax = plt.subplots()
                ax.bar(df['Channel Name'], df['Avg.Duration'])
                ax.set_ylabel('Avg.Duration')
                ax.set_xlabel('Channel Name')
                st.pyplot(fig)

            elif a == 9:
                df = Sql().q10()
                fig,ax = plt.subplots()
                ax.pie(df['Comment Count'], labels= df["Video Name"], autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)


    #Function for the whole website
    def website(self):
        # Creating a two column for navigation and content
        hide_default_format = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
        st.markdown(hide_default_format, unsafe_allow_html=True)
        st.column_config.TextColumn('nav', )
        st.markdown("<h1 style='text-align: center;'>Youtube Data Extraction and Harvesting</h1>" ,unsafe_allow_html=True)
        with st.sidebar:
            st.image("src/youtube.svg", width= 75, use_column_width= True)
            st.markdown("<h1 style='text-align: center;'>Navigation &darr;</h1>" ,unsafe_allow_html=True)

            page =  option_menu(menu_title="Pages", options= ["Home","Data Extraction", "Manage Database","Data Visualization"], 
                                icons=["house", "database-add","database-fill-check" , "pencil-square"])

        if page == "Home":
            self.home()
            
        if page == "Data Extraction":
            self.data_extraction()

        if page == "Manage Database":
            self.manage_database()

        if page == "Data Visualization":
            self.data_visualization()
                

if __name__ == "__main__":
     # To increase the wide of the webpage
    Website()
