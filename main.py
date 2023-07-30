from InsClawer import InsClawer
import streamlit as st
import pandas as pd
from PIL import Image
from instagrapi.exceptions import ChallengeRequired
import time

# user_name       = "amy.quach.ngoc"
# password        = "Ngoc2002"


ins = InsClawer()

st.set_page_config(page_title="AI Growth Tools", 
                    page_icon="assets/logo.ico",
                    layout="wide")



#---- MAIN PAGE -----#
left, right= st.columns([1,6], gap="small")
image = Image.open('assets/logo.png')

left.image(image, width=100)

right.write("")
right.write("")

right.title("AI GROWTH CO.")
st.markdown("---")

col1,col2,col3,col4 = st.columns([2,1,1,1])

col1.subheader("Hello, there 👋👋\nPlease Login to your IG Account to be able to run the Exactor")
username = col2.text_input('Username', placeholder="Enter username:")
password = col3.text_input('Password', type="password",placeholder="Enter password:")


col4.write("")
col4.write("")
login_btn_clicked = col4.button('Login', help="Click to log in")

# login
if login_btn_clicked:
    user_name = username 
    time.sleep(10)
    
user_name = username.replace(".","")
file_path       = f"data/data_{user_name}.csv"

try:
    df = pd.read_csv(file_path)
    
except FileNotFoundError or pd.errors.EmptyDataError:
    data = {
        "PK":           [],
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

st.sidebar.divider()

# Multi checkbox displaying data
is_pressed = False
# Expander
with st.sidebar.expander("Please select display elements:"):
    pk_ckBox = st.checkbox('PK')
    username_ckBox = st.checkbox('Username')
    fullname_ckBox = st.checkbox('Full name')
    email_ckBox = st.checkbox('Email')
    phone_ckBox = st.checkbox('Phone number')
    followers_ckBox = st.checkbox('Followers')
    bio_ckBox = st.checkbox('Biography')
    lang_ckBox = st.checkbox('Language')
    city_ckBox = st.checkbox('City')
    hashtag_ckBox = st.checkbox('Hashtags')
    select_all = st.checkbox('All', value=True)

# List of selected columns
selected_columns = []

# Add selected columns to the list
if pk_ckBox:
    selected_columns.append('PK')
    
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
    
if select_all:
    if "PK" not in selected_columns:
        selected_columns.append('PK')
    if "Username" not in selected_columns:
        selected_columns.append('Username')
    if "Full name" not in selected_columns:
        selected_columns.append('Full name')
    if "Email" not in selected_columns:
        selected_columns.append('Email')
    if "Phone" not in selected_columns:
        selected_columns.append('Phone')
    if "Followers" not in selected_columns:
        selected_columns.append('Followers')
    if "Biography" not in selected_columns:
        selected_columns.append('Biography')
    if "Language" not in selected_columns:
        selected_columns.append('Language')
    if "City" not in selected_columns:
        selected_columns.append('City')
    if "Hashtags" not in selected_columns:
        selected_columns.append('Hashtags')
        
    selected_columns.pop()

# Lọc dữ liệu theo location_name và language và các checkbox
df_selection = df[(df["City"].isin(location_name)) & (df["Language"].isin(language))]
df_selection = df_selection[selected_columns]


# tổng người dùng đã lấy được dữ liệu
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
amount = int(right_column.slider('Number of users:', 0, 100))

start_btn_clicked = right_column.button("Start")

# khi bấm nút start sẽ bắt đầu lấy dữ liệu
if start_btn_clicked and amount > 0:
    # Instagram user login
    ins.clientLogin(username, password)
    
    # set proxy
    ins.client.set_proxy("http://zC1vghLnwV4jgu4u:wifi;de;;;@proxy.soax.com:9000")
    ins.client.set_locale('de_DE')
    ins.client.set_timezone_offset(-60)
    ins.client.get_settings()
    
    # set delay range 
    ins.client.delay_range = [1,3]
    
    user_input = user_input.replace(" ", "").lower()
    ins.getMediasTopData(user_input, amount = amount)
    ins.getUserData()
    ins.createCSV(file_path=file_path)
    ins.remove_duplicates_csv(file_path=file_path, columns_to_check= ["Username", "Full name"])


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

   


    
    
    