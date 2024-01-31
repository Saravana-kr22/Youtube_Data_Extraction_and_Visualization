# Youtube_Data_Extraction_and_Visualization 
Youtube Data Extraction and Visualization is a project that intends to provide users with the ability to access and analyse data from numerous YouTube channels. SQL, MongoDB, and Streamlit are used in the project to develop a user-friendly application that allows users to retrieve, save, and query YouTube channel and video data.

## Table of Contents
- [LIBRARIES USED](#libraries-used)
- [Installation](#installation)
- [USAGE](#usage)
- [FEATURES](#features)
- [CONTRIBUTING](#contributing)
- [LICENSE](#license)
- [CONTACT](#contact)

## LIBRARIES USED
this project requires the following components:

1. [STREAMLIT](#streamlit)
2. [GOOGLE API CLIENT](#google-api-client)
3. [MONGODB ATLAS](#mongodb-atlas)
4. [MySQL](#mysql)
5. [PANDAS](#pandas)
6. [MATPLOTLIB](#matplotlib)


### STREAMLIT:

Streamlit library was used to create a user-friendly UI that enables users to interact with the programme and carry out data retrieval and analysis operations.


### GOOGLE API CLIENT:

The googleapiclient library in Python facilitates the communication with different Google APIs. Its primary purpose in this project is to interact with YouTube's Data API v3, allowing the retrieval of essential information like channel details, video specifics, and comments. By utilizing googleapiclient, developers can easily access and manipulate YouTube's extensive data resources through code.

### MONGODB ATLAS:

MongoDB Atlas is a comprehensive cloud-based database service designed specifically for MongoDB. In this project, MongoDB Atlas is utilized to store the data obtained from YouTube's Data API v3. By leveraging MongoDB Atlas, developers can benefit from a fully managed and hassle-free database solution that ensures the reliable and scalable storage and retrieval of data, thereby facilitating efficient data management.


### MySQL:

MySQL is an open-source relational database management system (RDBMS) that is widely used for managing and organizing data. It is known for its reliability, scalability, and ease of use. MySQL uses a client-server model and is compatible with various programming languages, making it a popular choice for web applications.

### PANDAS

Matplotlib is a 2D plotting library for creating static, animated, and interactive visualizations in Python. It provides a wide variety of plotting options and customization features, making it a powerful tool for data visualization. Matplotlib is often used for creating charts, graphs, histograms, and other types of plots.

### MATPLOTLIB

Matplotlib is a 2D plotting library for creating static, animated, and interactive visualizations in Python. It provides a wide variety of plotting options and customization features, making it a powerful tool for data visualization. Matplotlib is often used for creating charts, graphs, histograms, and other types of plots.


## Installation

To run this project, you need the following:
```Python3, 
Google API Key, 
MongoDB ATLAS URL,
MySQL
```
To install all the requried lib for python `pip install -r requirements.txt`

## USAGE

To run this project, follow these steps:

1. Clone the repository: git clone https://github.com/Saravana-kr22/Youtube_Data_Extraction_and_Visualization.git
2. Install the required packages: `pip install -r requirements.txt'
3. Run the Streamlit app: streamlit run web.py
4. Access the app in your browser at http://localhost:8501

## FEATURES:

### The following functions are available in the Youtube Data Extraction and Visualization:

1. Retrieval of channel and video data from YouTube using the YouTube API.

Enter the channel_id in the textbox with the , as a sperator and then press *Extract* button  to extract the channel details

![Data Extraction!](/src/data_extraction.png "Data Extraction")

After successfull Extraction you can see the channel names in the Extracted Data column

2. Storage of data in a MongoDB database as a data lake.

After extracting the channel details move to *Manage DataBase* tab and select the channel names to be Stored in the MongoDB under *Mongo"DB* column and press *Store to MongoDb button* to store data in MongoDB

![MongoDB!](/src/mongodb.png "MongoDB")


3. Migration of data from the data lake to a SQL database.

After Storing the data in MongoDB to Migrate tha to SQL select the channel names in the selecbox under the *MySQL* tab and then press the *Migrate to MySQL* button to migrtae it to SQL Tables

![MySQL!](/src/mysql.png "MySQL")S

*Note:* Before this step you need to create a table in the database schema in Mysql.please refer [mysql.py](/scripts/mysql.py) for the table structure

4. Search and retrieval of data from the SQL database using different search options.

After Migrating the data to SQL move to *Data Visualization* choose the one of the question in the selectbox to analyzis and visualization of the data

![Data Visualization!](/src/data_visualization.png "Data Visualization")

## CONTRIBUTING

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit a issue or pull request.

## LICENSE

This project is licensed under the MIT License. Please review the LICENSE file for more details.

## CONTACT

📧 Email: mailto:smartsaravana002@gmail.com 

For any further questions or inquiries, feel free to reach out. 
