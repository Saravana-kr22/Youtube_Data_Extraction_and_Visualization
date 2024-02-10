import mysql.connector as sql
from isodate import parse_duration
from scripts.mongodb import*

class Mysql(Mongodb):
    def __init__(self, channel):
        super().__init__()
        self.dbconnection = sql.connect( host = "mysqldb", user ="user",
                                          password = "password", database = "youtube")
        self.cursor = self.dbconnection.cursor()
        self.channel= channel

    def check_tables(self):
        query_check ="""SHOW TABLES"""
        self.cursor.execute(query_check)
        tables = self.cursor.fetchall()
        return (bool(tables))

    def create_table(self):
        query_tables =["""
                       CREATE TABLE Channel (
                        channel_id VARCHAR(255) PRIMARY KEY,
                        channel_name VARCHAR(255),
                        channel_subscription INT,
                        channel_views INT,
                        channel_description TEXT
                      );""",
                      """CREATE INDEX idx_channel_name ON Channel(channel_name); """,
                      """CREATE TABLE Playlist (
                        playlist_id VARCHAR(255) PRIMARY KEY,
                        channel_id VARCHAR(255),
                        channel_name VARCHAR(255),
                        FOREIGN KEY (channel_id) REFERENCES Channel(channel_id)
                      );""",
                      """CREATE TABLE Video (
                        video_id VARCHAR(255) PRIMARY KEY,
                        video_name VARCHAR(255),
                        video_description TEXT,
                        published_date VARCHAR(255),
                        view_count INT,
                        like_count INT,
                        comment_count INT,
                        duration INT,
                        channel_name VARCHAR(255),  
                        FOREIGN KEY (channel_name) REFERENCES Channel(channel_name)
                      );""",
                      """CREATE TABLE Comment (
                        comment_id VARCHAR(255) PRIMARY KEY,
                        video_id VARCHAR(255),
                        channel_id VARCHAR(255),
                        comment_text TEXT,
                        comment_author VARCHAR(255),
                        FOREIGN KEY (video_id) REFERENCES Video(video_id),
                        FOREIGN KEY (channel_id) REFERENCES Channel(channel_id)
                      );
                      """]
        
        for table in query_tables:
            self.cursor.execute(table)
        self.dbconnection.commit()  
        return()
    
        
    def channel_table(self):
        db = self.client["youtube_data_harversting"]
        collection = db[self.channel]
        data = []
        for i in collection.find({}, { 'channel_info': 1}):
            data.append(i['channel_info'])
        query_channel = """
            INSERT INTO Channel (
                channel_id,
                channel_name,
                Channel_subscription,
                channel_views,
                channel_description
                ) VALUES (%s, %s, %s, %s, %s)
                """
        channel_values = (data[0]['channel_id'],
                          data[0]['channel_name'],
                          data[0]['subscription_count'],
                          data[0]['channel_views'],
                          data[0]['channel_description']) 
        self.cursor.execute(query_channel, channel_values)
        self.dbconnection.commit()    

        return()
    
    def playlist_table(self):
        db = self.client["youtube_data_harversting"]
        collection = db[self.channel]
        data = []
        for i in collection.find({}, { 'playlist_info': 1}):
            data.append(i['playlist_info'])

        for playlist in data[0]:
            if playlist:
                query_playlist = """
                        INSERT INTO Playlist (
                            playlist_id,
                            channel_id,
                            channel_name
                            ) VALUES (%s, %s, %s)
                            """
                playlist_values = (playlist['PlaylistId'],
                                   playlist['ChannelId'],
                                   playlist['ChannelName'])
        
                self.cursor.execute(query_playlist, playlist_values)
                self.dbconnection.commit()    

        return()
    
    def video_table(self):
        db = self.client["youtube_data_harversting"]
        collection = db[self.channel]
        data = []
        for i in collection.find({}, { 'video_info': 1}):
            data.append(i['video_info'])

        for video in data[0]:
            query_video = """
                INSERT INTO Video (
                    video_id,
                    video_name,
                    video_description,
                    published_date,
                    view_count,
                    like_count,
                    comment_count,
                    duration,
                    channel_name
                    ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            video_values = (video['Video_Id'],
                            video['Title'],
                            video['Description'],
                            video['Published_Date'],
                            video['Views'],
                            video['Likes'],
                            video['Comments'],
                            self.duration(video['Duration']),
                            video['Channel_Name'])
            self.cursor.execute(query_video, video_values)
            
        self.dbconnection.commit()    

        return()
    
    def comment_table(self):
        db = self.client["youtube_data_harversting"]
        collection = db[self.channel]
        data = []
        for i in collection.find({}, { 'channel_info': 1}):
            channel_id = i['channel_info']["channel_id"]
        for i in collection.find({}, { 'comment_info': 1}):
            data.append(i['comment_info'])

        for comment in data[0]:
            if comment:
                for i in range(len(comment)):
                    query_Comment = """
                            INSERT INTO Comment (
                                comment_id,
                                video_id,
                                channel_id,
                                comment_text,
                                comment_author
                                )VALUES(%s,%s,%s,%s,%s)       
                        """
                    comment_values=(comment[i]['Comment_Id'],
                                    comment[i]['Video_Id'],
                                    channel_id,
                                    comment[i]['Comment_Text'],
                                    comment[i]['Comment_Author'])
                    self.cursor.execute(query_Comment, comment_values)
        self.dbconnection.commit()  
        return()  

        
    def duration(self,timestr):
        duration_obj = parse_duration(timestr)
        total = int(duration_obj.total_seconds())
        return (total)
    
    def  list_channel_names(self): 
        cursor = self.dbconnection.cursor()
        cursor.execute("SELECT channel_name,channel_subscription,channel_views from Channel")
        list_name = cursor.fetchall()
        return(list_name) 
    
    def migrate_sql(self):

        if not self.check_tables():
            self.create_table()

        try:
            self.channel_table()
        except sql.Error as er:
            print
            if er.errno == 1062:
                return(False)

        self.playlist_table()
        self.video_table()
        self.comment_table()
        self.dbconnection.close()
        return(True)

         