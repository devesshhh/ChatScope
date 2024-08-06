# Libraries Imported
# streamlit run app.py
import streamlit as st
import time
import io
import csv
import sys
import os

from custom_modules import func_use_extract_data as func
from custom_modules import func_analysis as analysis

# to disable warning by file_uploader going to convert into io.TextIOWrapper
st.set_option('deprecation.showfileUploaderEncoding', False)

# ------------------------------------------------

# Sidebar and main screen text and title.
st.title("❤️ ChatScope: Your WhatsApp Conversation Analyzer ❤️")
st.markdown(
    "This app is designed to analyze your WhatsApp chat using the exported text file 😎"
)
st.sidebar.image("./assets/images/logo.jpg", use_column_width=True)
st.sidebar.title("Analysis:")
st.sidebar.markdown(
    "This tool allows you to examine your WhatsApp conversation by importing the exported text file 😎"
)


st.sidebar.markdown('<b>Devesh Amlesh Rai</b>\
                <a href = "https://github.com/devesshhh" ><img src="https://img.shields.io/badge/Author-@devesshhh-gray.svg?colorA=gray&colorB=dodgerblue&logo=github"/>\
                <a/>', unsafe_allow_html=True)
st.sidebar.markdown('<b>Anant Manish Singh</b>\
                <a href="https://github.com/AnantSingh0121"><img src="https://img.shields.io/badge/Author-@AnantSingh0121-gray.svg?colorA=gray&colorB=dodgerblue&logo=github"/></a>',
                unsafe_allow_html=True)

st.sidebar.markdown('**Unlock the magic of exporting your chat history!**')
st.sidebar.text('Follow these steps 👇:')
st.sidebar.text('1) Access the individual or group chat.')
st.sidebar.text('2) Click on options > More > Export chat.')
st.sidebar.text('3) Select the option to export without media.')

st.sidebar.markdown("*Voilà! You're now ready to embark on your journey 😃*")
# -------------------------------------------------

# Unleash the power of uploading text files and select the enchanting date format {Method 1}
st.sidebar.markdown('**Summon your chat text file into the realm:**')
date_format = st.sidebar.selectbox('Choose the date format:',
                                   ('mm/dd/yyyy', 'mm/dd/yy',
                                    'dd/mm/yyyy', 'dd/mm/yy',
                                    'yyyy/mm/dd', 'yy/mm/dd'), key='0')
filename = st.sidebar.file_uploader("Choose your text file and upload here: ", type=["txt"])
st.sidebar.markdown("**Worry not, for your data remains ephemeral!**")
st.sidebar.markdown("**Feel the magic and use it to your heart's content 😊**")


# =========================================================

# Select feature for txt file {Way 2}

# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.sidebar.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)

# filename = file_selector()
# st.sidebar.markdown('You selected {}'.format(filename))

# Check file format
# if not filename.endswith('.txt'):
#     st.error("Please upload only text file!")
#     st.sidebar.error("Please upload only text file!")
# else:

# ===========================================================
if filename is not None:

    # Loading files into data as a DataFrame
    # filename = ("./Chat.txt")
    # @st.cache(persist=True, allow_output_mutation=True) # https://docs.streamlit.io/library/advanced-features/caching#:~:text=st.cache_data%C2%A0is%20the%20recommended%20way%20to%20cache%20computations%20that%20return%20data%3A%20loading%20a%20DataFrame%20from%20CSV%2C
    @st.cache_data
    def load_data(date_format=date_format):

        file_contents = []

        if filename is not None:
            content = filename.read().decode('utf-8')

            # Use StringIO object to create a file-like object
            with io.StringIO(content) as f:
                reader = csv.reader(f, delimiter='\n')
                for each in reader:
                    if len(each) > 0:
                        file_contents.append(each[0])
                    else:
                        file_contents.append('')
        else:
            st.error("Please upload the WhatsApp chat dataset!")

        return func.read_data(file_contents, date_format)

    try:
        data = load_data()

        if data.empty:
            st.error("Please upload the WhatsApp chat dataset!")

        if st.sidebar.checkbox("Show raw data", True):
            st.write(data)
        # ------------------------------------------------

        # Members name involve in Chart
        st.sidebar.markdown("### To Analyze select")
        names = analysis.authors_name(data)
        names.append('All')
        member = st.sidebar.selectbox("Member Name", names, key='1')

        if not st.sidebar.checkbox("Hide", True):
            try:
                if member == "All":
                    st.markdown(
                        "### Analyze {} members together:".format(member))
                    st.markdown(analysis.stats(data), unsafe_allow_html=True)

                    st.write("**Top 10 frequent use emoji:**")
                    emoji = analysis.popular_emoji(data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(data))

                    st.markdown('**Word Cloud:**')
                    st.text(
                        "This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**Most active date:**')
                    st.pyplot(analysis.active_date(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**Most active time for chat:**')
                    st.pyplot(analysis.active_time(data))
                    # st.pyplot()

                    st.write(
                        '**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(data))

                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(data))

                    st.write('**Chatter:**')
                    st.plotly_chart(analysis.chatter(data))

                else:
                    member_data = data[data['Author'] == member]
                    st.markdown("### Analyze {} chat:".format(member))
                    st.markdown(analysis.stats(member_data),
                                unsafe_allow_html=False)

                    st.write("**Top 10 Popular emoji:**")
                    emoji = analysis.popular_emoji(member_data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.write('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(member_data))

                    st.markdown('**Word Cloud:**')
                    st.text(
                        "This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(member_data))

                    time.sleep(0.2)

                    st.write(
                        '**Most active date of {} on WhatsApp:**'.format(member))
                    st.pyplot(analysis.active_date(member_data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.write('**When {} is active for chat:**'.format(member))
                    st.pyplot(analysis.active_time(member_data))
                    # st.pyplot()

                    st.write(
                        '**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(member_data))

                    st.write('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(member_data))

            except:
                e = sys.exc_info()[0]
                st.error("It seems that something is wrong! Try Again. Error Type: {}".format(
                    e.__name__))

        # --------------------------------------------------

    except:
        e = sys.exc_info()
        st.error("Something is wrong in loading the data! Please select the correct date format or Try again. Error Type: {}.\n \n **For Detail Error Info: {}**".format(e[0].__name__, e[1]))
        # Debugging
        # e = sys.exc_info()
        # st.error("Something is wrong! Try Again. Error Type: {}".format(e))


st.sidebar.markdown(
    "[![Approved by mom :) ](https://forthebadge.com/images/badges/approved-by-my-mom.png)](https://www.linkedin.com/in/devesh-rai-544437230/)")
st.sidebar.markdown(
    "[![Built with Love](https://forthebadge.com/images/badges/built-with-love.svg)](https://www.linkedin.com/in/anantsingh1302/)")