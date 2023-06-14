from InsClawer import InsClawer
import streamlit as st
import pandas as pd

# user_name       = "amyquach48"
# password        = "amyquach2002"
file_path       = "data.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    data = {
        'pk': [],
        'username': [],
        'full_name': [],
        'profile_pic_url': [],
        'caption': [],
        'hashtags': [],
        'location_name': []
    }

    df = pd.DataFrame(data)
    
ins = InsClawer()

def DataExaction(ins, user_input, amount): 
    ins.getMediasTopData(user_input, amount= amount)
    ins.getUserData()
    ins.createCSV(file_path=file_path)



st.set_page_config(page_title="Instagram CSV", 
                    page_icon="favicon.ico",
                    layout="wide")



#---- MAIN PAGE -----#
st.title("🖥️🖥️ Dashboard")
st.markdown("##")
st.markdown("---")

col1,col2,col3,col4 = st.columns([2,1,1,1])

col1.subheader("Hello, there 👋👋\nPlease Login to your IG Account to run the Exactor")
username = col2.text_input('Username', placeholder="Enter username:")
password = col3.text_input('Password', type="password",placeholder="Enter password:")

col4.write("")
col4.write("")
login_btn_clicked = col4.button('Login', help="Click to log in")

# login
if login_btn_clicked:
    ins.clientLogin(username, password)
#---- SIDEBAR -----#
st.sidebar.empty()
st.sidebar.header("Please filter here:")
location_name = st.sidebar.multiselect(
    "Select Location Name:",
    options= sorted([str(x) for x in df["location_name"].unique()] + ["All"]),
    default=["All"],
    key="location_multiselect",
)

if "All" in location_name:
    # If "All" is selected, set location_name to all unique options
    location_name = list(df["location_name"].unique())

df_selection = df[df["location_name"].isin(location_name)]
total_data = len(df_selection)

st.write("")
st.write("")
left_col, right_col = st.columns(2)
left_col.subheader(f"Total: {total_data} 👤")
right_col.subheader(f"Logged as: {username}")
st.markdown("---")

left_column, right_column = st.columns([2,1])
left_column.dataframe(df_selection)

# Exact data
right_column.subheader("Data Exactor")
user_input = right_column.text_input("Keywords Input:")
amount = int(right_column.slider('Amount users', 0, 100))
start_btn_clicked = right_column.button("Start")

# khi bấm nút start sẽ bắt đầu lấy dữ liệu
if start_btn_clicked and amount > 0:
    DataExaction(ins, user_input, amount)
    
right_column.text("Download the filtered data 👇")
# Tải bản csv đã filter về máy
download_file_btn = right_column.download_button(
    label="Download data as CSV",
    data = df_selection.to_csv().encode('utf-8'),
    file_name='data.csv',
    mime='text/csv'
)



   


    
    
    