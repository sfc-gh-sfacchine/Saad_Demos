## Steps to Use


1. Clone this repo, and download files in data folder.
2. Go through 1.Load_Data locally using your IDE of choice. This will save the tables into the database and schema that you have set. I created a FEATURES database to put those tables in.
3. Upload 2.Train_Deploy into Snowflake Notebooks (there's a button next to the big + Notebook button in the UI)
4. Run that notebook in Snowflake, make changes depending on where your database and schema are. Use whichever virtual warehouse you desire.
5. Copy the contents of 3.Streamlit and paste it into a new Streamlit app within Snowflake. Make sure the model name and objects are the same from the Notebook. 
