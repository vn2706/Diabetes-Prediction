import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie


st.set_page_config(page_title="Home Page", page_icon="https://cdn-icons-png.flaticon.com/128/9032/9032033.png",
                   layout='wide',initial_sidebar_state="collapsed")
@st.cache_data(show_spinner="loading...")
def home_page():
    @st.cache_resource
    def bg():
        bg="""
        <style>
        [data-testid="stHeader"]{
            background-color: rgba(0,0,0,0);
        }
        </style>
        """
        st.markdown(bg,unsafe_allow_html=True)
    bg()

    @st.cache_data(show_spinner="loading...")
    def load_data():
        df = pd.read_csv("https://raw.githubusercontent.com/Chan5ru222001/Streamlit_app/main/Cleaned.csv")
        df = df.drop(columns=['Unnamed: 0', 'age_normalized', 'bmi_normalized',
                    'HbA1c_level_normalized', 'blood_glucose_level_normalized'])
        return df
    df=load_data()

    @st.cache_resource(show_spinner="loading...")
    def load_lottie(url: str):
        r=requests.get(url)
        if r.status_code !=200:
            return None
        return r.json()

    st.title("Diabetes Prediction Using Machine Learning")
    col1, col2=st.columns([4,8])
    with col1:
        lottie=load_lottie("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
        st_lottie(lottie,speed=2,reverse=False,loop=True,quality="high",height=300, width=300)
    with col2:
        with st.container():
            st.info("Welcome to our Diabetes Prediction Web App! Using the powerful Decision Tree model, we can accurately predict the likelihood of diabetes with an impressive accuracy of **90.2%** . By analyzing features such as gender, heart disease, age, BMI, blood glucose level, and HbA1c level from the Diabetes dataset, our app provides valuable insights to help you assess your risk. Get instant results and take control of your health today.")
    
    st.markdown("""___""")
    st.subheader("Data")
    with st.expander("Click here"):
        st.dataframe(df)

home_page()


