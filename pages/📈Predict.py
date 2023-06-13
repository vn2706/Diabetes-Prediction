import pandas as pd
import streamlit as st
import pickle

st.set_page_config(page_title="Prediction of Diabetes", page_icon="https://cdn-icons-png.flaticon.com/128/9032/9032033.png",
                   layout='centered', initial_sidebar_state="expanded")
def details():
    smoking_history={'never': 0,
        'No Info': 1,
        'current': 2,
        'former': 3,
        'ever': 4,
        'not current': 5}
    gender={0:"Female",1:"Male"}
    heart_disease={0:"No",1:"Yes"}
    hypertension={0:"No",1:"Yes"}
    info={"Smoking History":smoking_history,"Gender":gender,"Heart Disease":heart_disease,"Hypertension":hypertension}
    return info

with st.expander("Please review this information:"):
    st.write(details()) 

@st.cache_data()
def vedio():
    video_html = """
            <style>
            [data-testid="stHeader"]{
                background-color: rgba(0,0,0,0);
            }

            [id="predict-the-result"]{
                background-color: rgba(0,0,0,0);
                text-align: center;
                margin-right: 150px;
                margin-left: 80px;
            }
            """
    st.markdown(video_html,unsafe_allow_html=True)

vedio()

@st.cache_data
def data():
    df_pred = pd.read_csv("D:\VS Code\Pandas\Streamlit\Diabetes_data.csv")
    df_pred.drop(columns=['Unnamed: 0'], inplace=True)
    return df_pred

@st.cache_resource(show_spinner="loading...")
def pickle_data():
        with open('D:\VS Code\Pandas\Streamlit\model.pkl', 'rb') as file:
            loaded_model = pickle.load(file)
        return loaded_model

loaded_model=pickle_data()
df_pred=data()

st.title("Predict the Result!")

col1, col2, col3 = st.columns([4, 4, 4], gap='large')

with col1:
    f1 = st.selectbox("Select Gender", options=df_pred['gender'].unique())
    f2 = st.selectbox("Select Hypertension",
                      options=df_pred['hypertension'].unique())
    f3 = st.number_input("Enter HbA1c level", min_value=3.5, max_value=9.0)

with col2:
    f4 = st.selectbox("Select Heart Disease",
                      options=df_pred['heart_disease'].unique())
    f5 = st.number_input("Enter Body Mass Index",
                         min_value=10.00, max_value=95.00)
    f6 = st.number_input("Enter the Age", min_value=7, max_value=80)

with col3:
    f7 = st.selectbox("Select Smoking History",
                      options=df_pred['smoking_history'].unique())
    f8 = st.number_input("Enter Blood Glucose Level",
                         min_value=80, max_value=300)


st.markdown("""___""")

def predict():
    p1, p2, p3 = st.columns([5, 2, 5])
    result = ""
    with p2:
        button = st.button("Predict")
        if button:
            features = [[int(f1), int(f6), int(f2), int(
                f4), int(f7), float(f5), float(f3), float(f8)]]
            result = loaded_model.predict(features)
            if result == 0:
                return "The prediction indicates that the individual does not have diabetes"
            else:
                return "The individual is predicted to have diabetes."
    return result

st.success(predict())
