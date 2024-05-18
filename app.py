import streamlit as st
from PIL import Image
import requests
from io import BytesIO

home,user,library = st.tabs(["Home","Profile","Library"])

with home:
    st.title('Welcome to Recordix')
    rec1,rec2,rec3,rec4,rec5=st.columns(5)
    rec_list=[rec1,rec2,rec3,rec4,rec5]
    i=0
    while (i<5):
        with rec_list[i]:
            html_columns = """
            <style>
                
                .col-1 {
                    width:200px;
                }
                .col-1 .image-wrap{
                    width:100px;
                    height:200px;
                }
                 .col-1 .image-wrap img{
                    width:100%;
                    height:100%;
                    object-fit:contain;
                }
            </style>
            <div class="col-1">
                <h2>Playlist</h2>
                <div class="image-wrap">
                    <img src="https://lh3.googleusercontent.com/Ch_wVJF6ACcqbrMj0HHV1XwG4mt58cvSo2xJRoy4aa3_QAboM0deyEnoSYVW4JnultuibKk0ZLdwkvYO=w544-h544-l90-rj" class="playlist_image">
                </div>
            </div>
            """

            # Display the HTML in Streamlit
            st.markdown(html_columns, unsafe_allow_html=True)
        i+=1

with user:
    st.write("Hi, User")



