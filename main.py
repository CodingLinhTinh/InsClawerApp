from InsClawer import InsClawer
import streamlit as st
import pandas as pd
from PIL import Image
from instagrapi.exceptions import ChallengeRequired
import time

# user_name       = "amy.quach.ngoc"
# password        = "Ngoc2002"
# keyword         = "lustige katzen"
# '''
# Just to give you a better overview: 
# () is always an opinion:

# Leads finder parameters: 
# Username|Full Name| E-Mail| Phone | Biography | City | Followers
# (I also like the hashtag parameter currently this can be kept in process)
# (if there is any possibility to get Engagement Rate as Parameter it would be awesome)

# Scraping: 
# Follower Slider for Audience Quality Check | 
# Language Filtering (German, English)| 
# CSV Export (if possible also as TXT additional, if not no worries)

# Scraper Cache Clearing to reset the scraped Data's for better Overview
# Logo Branding and Favicon DONE

# And maybe more pertinent login process, so it gets a smoother flow
# a list of the csv which have been created and with and with checkbox they can choose which csv they want to combine into a file if possible would be really efficient

# '''
file_path       = "data.csv"

try:
    df = pd.read_csv(file_path)
    
except FileNotFoundError or pd.errors.EmptyDataError:
    data = {
        "Username":     [],
        "Full name":    [],
        "Email":        [],
        "Phone":        [],
        "Biography":    [],
        "City":         [],
        "Followers":    [],
        "Hashtags":     [],
        "Language":     []
    }

    df = pd.DataFrame(data)

ins = InsClawer()

st.set_page_config(page_title="Instagram CSV", 
                    page_icon="logo.ico",
                    layout="wide")



#---- MAIN PAGE -----#
left, right= st.columns([1,6], gap="small")
image = Image.open('logo.png')

left.image(image, width=100)

right.write("")
right.write("")

right.title("AI GROWTH CO.")

st.markdown("##")
st.markdown("---")

col1,col2,col3,col4 = st.columns([2,1,1,1])

col1.subheader("Hello, there 👋👋\nPlease Login to your IG Account to be able to run the Exactor")
username = col2.text_input('Username', placeholder="Enter username:")
password = col3.text_input('Password', type="password",placeholder="Enter password:")

user_name = username

col4.write("")
col4.write("")
login_btn_clicked = col4.button('Login', help="Click to log in")

# login
if login_btn_clicked:
    user_name = user_name + "✅"
    
    
#---- SIDEBAR -----#
st.sidebar.empty()
st.sidebar.header("Please filter here:")

location_name = st.sidebar.multiselect(
    "Select City Name:",
    options= sorted([str(x) for x in df["City"].unique()] + ["All"]),
    default=["All"],
    key="location_multiselect",
)

language = st.sidebar.multiselect(
    "Select Language Audience:",
    options= sorted([str(x) for x in df["Language"].unique()] + ["All"]),
    default=["All"],
    key="language_multiselect",
)

if "All" in location_name:
    # If "All" is selected, set location_name to all unique options
    location_name = list(df["City"].unique())

if "All" in language:
    # If "All" is selected, set location_name to all unique options
    language = list(df["Language"].unique())



# Multi checkbox displaying data
st.sidebar.header("Please select display elements:")

username_ckBox = st.sidebar.checkbox('Username')
fullname_ckBox = st.sidebar.checkbox('Full name')
email_ckBox = st.sidebar.checkbox('Email')
phone_ckBox = st.sidebar.checkbox('Phone number')
followers_ckBox = st.sidebar.checkbox('Followers')
bio_ckBox = st.sidebar.checkbox('Biography')
lang_ckBox = st.sidebar.checkbox('Language')
city_ckBox = st.sidebar.checkbox('City')
hashtag_ckBox = st.sidebar.checkbox('Hashtags')

# List of selected columns
selected_columns = []

# Add selected columns to the list
if username_ckBox:
    selected_columns.append('Username')

if fullname_ckBox:
    selected_columns.append('Full name')

if email_ckBox:
    selected_columns.append('Email')

if phone_ckBox:
    selected_columns.append('Phone')

if followers_ckBox:
    selected_columns.append('Followers')

if bio_ckBox:
    selected_columns.append('Biography')

if lang_ckBox:
    selected_columns.append('Language')

if city_ckBox:
    selected_columns.append('City')
    
if hashtag_ckBox:
    selected_columns.append('Hashtags')
    

# Lọc dữ liệu theo location_name và language
df_selection = df[(df["City"].isin(location_name)) & (df["Language"].isin(language))]

df_selection = df_selection[selected_columns]


total_data = len(df_selection)

st.write("")
st.write("")
left_col, right_col = st.columns(2)
left_col.subheader(f"Total: {total_data} 👤")
right_col.subheader(f"Logged as: {user_name}")
st.markdown("---")

left_column, right_column = st.columns([2,1])
left_column.dataframe(df_selection)


# Exact data
right_column.subheader("Data Exactor")
user_input = right_column.text_input("Keywords Input:")
amount = int(right_column.slider('Amount users:', 0, 100))
start_btn_clicked = right_column.button("Start")

# khi bấm nút start sẽ bắt đầu lấy dữ liệu
if start_btn_clicked and amount > 0:
    ins.clientLogin(username, password)
    try:
        progress_text = "Operation in progress. Please wait..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(amount + 1):
            time.sleep(0.1)
            progress_value = round(percent_complete / amount, 2)
            if percent_complete == amount:  # Kiểm tra vòng lặp cuối cùng
                progress_value = 1.0
            my_bar.progress( progress_value  , text=f"{progress_text} ({progress_value*100}%)")
            try:
                user_input = user_input.replace(" ", "").lower()
                ins.getMediasTopData(user_input, amount = 100)
                # append vào Output
                ins.getUserData()
            except Exception as e:
                if "feedback_required" in str(e):
                    st.error("Instagram requires feedback. Stopping for 5 mins then refresh the page", icon="🚨")
                    time.sleep(5*60)
            

            
        ins.createCSV(file_path=file_path)
        ins.remove_duplicates_csv(file_path=file_path, columns_to_check= ["Username", "Full name"])
    except ChallengeRequired:
        pass


# Download the data
st.write("")
st.text("Download the filtered data 👇")

# Filter DataFrame based on selected columns
df_export = df_selection

# Remove columns not selected (unchecked)

unchecked_columns = set(df.columns) - set(selected_columns)
try:
    df_export.drop(columns=unchecked_columns, inplace=True)
except KeyError as e:
    pass

# Tải bản csv đã filter về máy
download_file_btn = st.download_button(
    label="Download data as CSV",
    data = df_export.to_csv().encode('utf-8'),
    file_name='data.csv',
    mime='text/csv'
)



   


    
    
    