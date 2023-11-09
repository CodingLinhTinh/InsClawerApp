from InsClawer import InsClawer
from Automation import Automation
import streamlit as st
import pandas as pd
from PIL import Image
from instagrapi.exceptions import ChallengeRequired
import time 
from io import BytesIO
import re
import os

user_file_path = "data/users.csv"

ins = InsClawer()
automation =  Automation()

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

col1,col2,col3,col4 = st.columns([2,2,2,1])

col1.subheader("Hello, there 👋👋\nPlease Login to your Account to be able to run the Exactor")
username = col2.text_input('Username', placeholder="Enter username:")
password = col3.text_input('Password', type="password",placeholder="Enter password:")


col4.write("")
col4.write("")
login_btn_clicked = col4.button('Login', help="Click to log in", use_container_width=True)

# login
if login_btn_clicked:
    
    # Lấy giá trị từ users.csv
    user_df = pd.read_csv(user_file_path)
        
    if user_df["Username"].item() != username or str(user_df["Password"].item()) != password:
        col4.error("Username or Password is incorrect! Refresh and try again.")
    else:
        col4.success(f"{username.replace('_','')} Logged In.")
    
    time.sleep(5)
    
    # Saving clawing data
    user_name = username.replace("_","")
    data_file_path       = f"data/data_{user_name}.csv"

# Saving clawing data
user_name = username.replace("_","")
data_file_path       = f"data/data_{user_name}.csv"

try:
    df = pd.read_csv(data_file_path)
    
except FileNotFoundError or pd.errors.EmptyDataError :
    data = {
        "PK":               [],
        "Username":         [],
        "Full name":        [],
        "Email":            [],
        "Phone":            [],
        "Followers":        [],
        "Following Count":  [],
        "City":             [],
        "Language":         [],
        "Is Private?":      [],
        "Is Verified?":     [],
        "Is Bussiness?":    [],
        "Media Count":      [],
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
    pk_ckBox                = st.checkbox('PK')
    username_ckBox          = st.checkbox('Username')
    fullname_ckBox          = st.checkbox('Full name')
    email_ckBox             = st.checkbox('Email')
    phone_ckBox             = st.checkbox('Phone number')
    followers_ckBox         = st.checkbox('Followers')
    lang_ckBox              = st.checkbox('Language')
    city_ckBox              = st.checkbox('City')
    media_count_ckBox       = st.checkbox('Media Count')
    following_count_ckBox   = st.checkbox('Following Count')
    select_all              = st.checkbox('All', value=True)

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

if lang_ckBox:
    selected_columns.append('Language')

if city_ckBox:
    selected_columns.append('City')
 

if media_count_ckBox:
    selected_columns.append('Media Count') 

if following_count_ckBox:
    selected_columns.append('Following Count') 


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
    if "Language" not in selected_columns:
        selected_columns.append('Language')
    if "City" not in selected_columns:
        selected_columns.append('City') 
    if "Media Count" not in selected_columns:
        selected_columns.append('Media Count')  
    if "Following Count" not in selected_columns:
        selected_columns.append('Following Count') 

    selected_columns.pop()

# Lọc dữ liệu theo location_name và language và các checkbox
df_selection = df[(df["City"].isin(location_name)) & (df["Language"].isin(language))]


#---------#

# tổng người dùng đã lấy được dữ liệu
total_data = len(df_selection)

st.write("")
st.write("")
left_col, right_col = st.columns(2)
left_col.subheader(f"Total: {total_data} 👤")
right_col.subheader(f"Welcome {user_name} 🌸")
st.markdown("---")

left_column, right_column = st.columns([2,1])
left_column.write("## All User's Data")
left_column.dataframe(df_selection)


###-----------IG LOGIN-------------------
# Bot Login
right_column.subheader("Instagram Login")
bot_name = right_column.text_input("IG username:",placeholder="Enter IG username:")
bot_pass = right_column.text_input('Password:', type="password",placeholder="Enter password:")

right_column.markdown("---")
###------------------------------

###-----------DATA EXACTORS-------------------
# Exact data
right_column.subheader("Data Exactor")
user_input = right_column.text_input("Keywords Input 🔍:")
amount = int(right_column.slider('Number of data retrievals ⏳:', 0, 20))

start_btn_clicked = right_column.button("Start", use_container_width=True)

# khi bấm nút start sẽ bắt đầu lấy dữ liệu
if start_btn_clicked and amount > 0:
    # set proxy
    # ins.client.set_proxy("")
    # ins.client.set_locale('de_DE')
    # ins.client.set_timezone_offset(-60)
    # ins.client.get_settings()
    
    # set delay range 
    ins.client.delay_range = [1,3]
    
    
    progress_text = "Operation in progress. Please wait..."
    my_bar = left_column.progress(0, text=progress_text)

 
    for percent_complete in range(amount + 1):
        time.sleep(0.1)
        progress_value = round( (percent_complete) / amount, 2)
        if percent_complete == amount:  # Kiểm tra vòng lặp cuối cùng
            progress_value = 1.0
            
        # hiển thị %
        my_bar.progress( progress_value  , text=f"{progress_text} ({progress_value*100}%)")
        
        user_input = user_input.replace(" ", "").lower()
        
        # Instagram user login
        try:
            ins.clientLogin(bot_name, bot_pass)
            time.sleep(3)
        except Exception as e:
            print(e)
            
        ins.getMediasTopData(user_input, amount = amount)
        time.sleep(3)
        ins.getUserData()
        time.sleep(3)
            
        if len( ins.output ) > 0:
            ins.createCSV(file_path=data_file_path)
            ins.remove_duplicates_csv(file_path=data_file_path, columns_to_check= ["Username", "Full name"])

###------------------------------
st.markdown("---")
###-----------FILTERS-------------------
st.write(f"## Filters")

## Filter Data
l1,l2,m,r1,r2 = st.columns([2,2,1,1,1])

option_followers = l1.selectbox(
        'Filter Followers',
        ('Followers > 1000', 'Followers < 1000', 'No Followers')
    )

option_media = l2.selectbox(
        'Filter Media Count',
        ('Media Count > 1000', 'Media < 1000', 'No Media')
    )
m.write("")
m.write("")
isPrivate_ckBox = m.checkbox("Is Private?", key="1")

r1.write("")
r1.write("")
isVerified_ckBox = r1.checkbox("Is Verified?", key="2")

r2.write("")
r2.write("")
isBussiness_ckBox = r2.checkbox("Is Bussiness?", key="3")

if isPrivate_ckBox:
    selected_columns.append('Is Private?')  
if isVerified_ckBox:
    selected_columns.append('Is Verified?') 
if isBussiness_ckBox:
    selected_columns.append('Is Bussiness?')

if "Is Private?" not in selected_columns:
    selected_columns.append('Is Private?')  
if "Is Verified?" not in selected_columns:
    selected_columns.append('Is Verified?')    
if "Is Bussiness?" not in selected_columns:
    selected_columns.append('Is Bussiness?') 

## Dữ liệu hiển thị đã được chọn trong selection box
df_selection = df_selection[selected_columns]

condition1 = (df['Followers'] >= 1000)
condition2 = (df['Media Count'] >= 1000)

if option_followers == "Followers < 1000":
    condition1 = (df['Followers'] < 1000)
if option_followers == "No Followers":
    condition1 = (df['Followers'] == 0)
    
if option_media == "Media < 1000":
    condition2 = (df['Media Count'] < 1000)
if option_media == "No Media":
    condition2 = (df['Media Count'] == 0)

# Lọc và hiển thị dữ liệu dựa trên điều kiện và checknbox
filtered_data = df_selection[condition1 & condition2]

# Display the filtered data only if the checkbox or condition is met
if isPrivate_ckBox or isVerified_ckBox or isBussiness_ckBox or (option_followers == "Followers >= 1000") or (option_media == "Media Count >= 1000"):
    st.dataframe(filtered_data.head(10))
    
###------------------------------

###-----------DOWNLOAD BTN-------------------
# Download the data
l1.write("")
l1.text("Download CSV 👍")

# Filter DataFrame based on selected columns
df_export = filtered_data

# Remove columns not selected (unchecked)
unchecked_columns = set(df.columns) - set(selected_columns)
try:
    df_export.drop(columns=unchecked_columns, inplace=True)
except KeyError as e:
    pass

# Tải bản csv đã filter về máy
download_csv_btn = l1.download_button(
    label="Download data as CSV",
    data = df_export.to_csv().encode('utf-8'),
    file_name='data.csv',
    mime='text/csv'
)

### Tải về dang txt
# Tạo dữ liệu văn bản từ dữ liệu đã được lọc (df_export)
text_data = df_export.to_csv(index=False)  # Chuyển dữ liệu DataFrame thành văn bản CSV

# Lưu dữ liệu văn bản vào buffer
txt_buffer = BytesIO()
txt_buffer.write(text_data.encode())

# Hiển thị nút tải dữ liệu văn bản
l2.write("")
l2.text("Download TXT 👇")
l2.download_button(label="Download as Text", data=txt_buffer, key="txt_download", file_name="data.txt", mime="text/plain")

###------------------------------
st.markdown("---")
###-----------AUTOMATION-------------------
st.markdown("# Automation")
l,mid,r = st.columns(3)
l.markdown("## Interaction to Media")

left_1,right_1 = l.columns([2,1])
media_url = left_1.text_input("Media Url:", placeholder="Enter Media URL:")

right_1.write("")
right_1.write("")
submit_btn = right_1.button("Submit", type="primary", use_container_width=True)

l1,l2,m = l.columns(3)
like_btn = l1.button("Like", use_container_width=True)
archive_btn = l2.button("Archive", use_container_width=True)
view_btn = m.button("View", use_container_width=True)

r1,r2,m = l.columns(3)
unlike_btn = r1.button("UnLike", use_container_width=True)
unarchive_btn = r2.button("UnArchive", use_container_width=True)
info_btn = m.button("Info", use_container_width=True)

if submit_btn:
    time.sleep(3)
    ## Login
    if automation.clientLogin(bot_name, bot_pass) == True:
        st.toast('Logged in!', icon='💖')
        st.toast('Got the Media!', icon='📷')
    else:
        err = l.error("Please Login with IG.")
        time.sleep(2)
        err.empty()
        
# https://www.instagram.com/reel/CwFTbV5J5qo/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA==
if like_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        media_pk = automation.getMediaPkfromUrl(media_url)
        automation.likeAMedia(media_pk)
        st.toast('Liked!', icon='👍')

if unlike_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        media_pk = automation.getMediaPkfromUrl(media_url)
        automation.unlikeAMedia(media_pk)
        st.toast('Unliked!', icon='👎')

if archive_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        media_pk = automation.getMediaPkfromUrl(media_url)
        automation.archiveMedia(media_pk)
        st.toast('Archive!', icon='📝')
        
if unarchive_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        media_pk = automation.getMediaPkfromUrl(media_url)
        automation.unarchiveMedia(media_pk)
        st.toast('Unarchive!', icon='📝')

if view_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        media_pk = automation.getMediaPkfromUrl(media_url)
        automation.viewAMedia(media_pk)
        st.toast('Viewed!', icon='👁️')

if info_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        media_pk = automation.getMediaPkfromUrl(media_url)
        data = automation.infoAMedia(media_pk)
        l.markdown(f'''
        **Video Information:**

        - **Title:** {data['title']}
        - **Caption Text:** {data['caption_text']}
        - **Video Duration:** {data['video_duration']}
        - **View Count:** {data['view_count']}
        - **Like Count:** {data['like_count']}
        - **Comment Count:** {data['comment_count']}

        **User Information:**

        - **Username:** {data['username']}
        - **Full Name:** {data['full_name']}
        - **Location:** {data['location']}
        - **Time:** {data['time']}
        ''')

##---------------------------------

##--------------View all User's Media--------------------
l.markdown("---")
l.markdown("## View all User's Media")
left_1,right_1 = l.columns([2,1])
username_to_view = left_1.text_input("Ussers to View:", placeholder="Enter Username:")

right_1.write("")
right_1.write("")
view_all_btn = right_1.button("View All", type="primary", use_container_width=True)


col1, col2 = l.columns(2)
follow_btn = col1.button("Follow", use_container_width=True)
unfollow_btn = col2.button("Unfollow", use_container_width=True)

if view_all_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        user_id = automation.getUserInfoByUsername(username_to_view)
        amount = 20
        automation.getUserMedias(user_id, amount)
        st.toast('Viewed All!', icon='👁️')
        
if follow_btn:
    if automation.clientLogin(bot_name, bot_pass) == True:
        user_id = automation.getUserInfoByUsername(username_to_view)
        if automation.FollowUser(user_id):
            st.toast('Followed!', icon='✅')

if unfollow_btn: 
    if automation.clientLogin(bot_name, bot_pass) == True:
        user_id = automation.getUserInfoByUsername(username_to_view)
        if automation.UnFollowUser(user_id):
            st.toast('UnFollowed!', icon='🚩')
 
##---------------------------------- 

##--------------UPLOAD PHOTOS-------------------
mid.markdown("## Upload Photos")
caption = mid.text_area("Caption:", placeholder="Enter Caption:")

col_1, col_2 = mid.columns(2)
like_and_view_counts_disabled_ckbox = col_1.checkbox("Like and View counts disabled?")
disable_comments_ckbox = col_2.checkbox("Disable comments?")

hashtag_generate_btn = mid.button("Generate Hashtags", type="primary",use_container_width=True)
def generate_hashtags(caption):
    # Phân tách từng từ trong caption
    words = re.findall(r'\w+', caption)

    # Tạo 10 hashtag từ các từ trong caption
    hashtags = ['#' + word for word in words[:10]]

    # Kết hợp các hashtag thành một chuỗi
    generated_hashtags = ' '.join(hashtags)

    return generated_hashtags

if hashtag_generate_btn:
    generated_hashtags = generate_hashtags(caption)
    hashtag_generation = mid.text_area("Genearation Hashtag:", value=generated_hashtags)

    
uploaded_file = mid.file_uploader("Upload File:", type=['png', 'jpg'],help="Uploading only png or jpg")
if uploaded_file is not None:
     # Đọc nội dung của tệp
    file_content = uploaded_file.read()

    # Tạo một đường dẫn tệp trên hệ thống của bạn
    file_path = os.path.join('./assets/', uploaded_file.name)

    # Kiểm tra và tạo thư mục nếu nó không tồn tại
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Lưu nội dung của tệp vào đường dẫn đã chọn
    with open(file_path, 'wb') as file:
        file.write(file_content)
        
    image = Image.open(file_path)
    mid.image(image, caption=caption)
        

upload_btn = mid.button("Upload", type="primary",use_container_width=True)

extra_data = {
    "like_and_view_counts_disabled": int(like_and_view_counts_disabled_ckbox),
    "disable_comments": int(disable_comments_ckbox)
}

if upload_btn:
    print(file_path)
    if automation.clientLogin(bot_name, bot_pass) == True:
        automation.PhotoUpload(path=file_path, caption=caption, extra_data=extra_data)
        st.toast('Uploaded!', icon='🖼️')

r.markdown("## Upload Videos, Reels")




    
    
    