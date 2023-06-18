import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard",page_icon="https://cdn-icons-png.flaticon.com/128/9032/9032033.png",layout='wide',initial_sidebar_state="expanded")
page_bg = """
    <style>
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    </style>
"""
@st.cache_resource(show_spinner="loading...")
def load_data():
    df = pd.read_csv("pages/Cleaned.csv")
    df = df.drop(columns=['Unnamed: 0','age_normalized','bmi_normalized','HbA1c_level_normalized','blood_glucose_level_normalized'])
    return df

df = load_data()

st.sidebar.subheader("DASHBOARD")
gender=st.sidebar.multiselect(
    "Select Gender",
    options=df['gender'].unique(),
    default=df["gender"].unique()
)

age_category=st.sidebar.multiselect(
    "Select the Age group",
    options=df['Age_category'].unique(),
    default=df['Age_category'].unique()
)

hypertension=st.sidebar.multiselect(
    "Select the Hypertension",
    options=df['hypertension'].unique(),
    default=df["hypertension"].unique()
)

heart_disease=st.sidebar.multiselect(
    "Select the Heart disease",
    options=df["heart_disease"].unique(),
    default=df["heart_disease"].unique()
)

smoking_history=st.sidebar.multiselect(
    "Select the Smoking history",
    options=df['smoking_history'].unique(),
    default=df['smoking_history'].unique()
)

diabetes=st.sidebar.multiselect(
    "Select the Diabetes Result",
    options=df['diabetes'].unique(),
    default=df['diabetes'].unique()[1]
)

Weight_Stage=st.sidebar.multiselect(
    "Select the BMI Stage",
    options=df['Weight_Stage'].unique(),
    default=df["Weight_Stage"].unique()
)

HbA1c_ranges=st.sidebar.multiselect(
    "Select the HbA1c level",
    options=df['HbA1c_ranges'].unique(),
    default=df["HbA1c_ranges"].unique()
)
df_selection=df.query(
"gender==@gender & Age_category==@age_category & hypertension==@hypertension & heart_disease==@heart_disease & smoking_history==@smoking_history & diabetes==@diabetes & Weight_Stage==@Weight_Stage & HbA1c_ranges==@HbA1c_ranges"
)
st.title("Dashboard")

def tabular():
    with st.expander("Dataframe"):
        show_data=st.multiselect("Filter :",df_selection.columns,default=[])
        st.write(df_selection[show_data])

    #Computations
    average_age = df_selection['age'].astype(float).mean()
    median_bmi = df_selection['bmi'].median()
    median_glucose = df_selection['blood_glucose_level'].median()
    median_hemoglobin = df_selection['HbA1c_level'].median()
    positive_cases = (df_selection['diabetes'] == "Yes").sum()

    col1, col2, col3, col4 , col5 = st.columns(5,gap="small")
    with col1:
        st.info("Average age",icon="🧑")
        st.metric("Mean Age",value=f"{average_age:,.0f}")

    with col2:
        st.info("BMI",icon="🔢")
        st.metric("Median BMI" , value=f"{median_bmi:,.2f}")
    
    with col3:
        st.info("Blood Glucose",icon="🩸")
        st.metric("Median",value=f"{median_glucose:,.2f}")

    with col4:
        st.info("HbA1c",icon="⚕️")
        st.metric("Median HbA1c",value=f"{median_hemoglobin:,.2f}")
    
    with col5:
        st.info("Positive result",icon="✅")
        st.metric("Counts of Result", value=f"{positive_cases}")

    st.markdown("""____""")

tabular()


def visulaizations():
    Glucose_by_age_category=df_selection.groupby(by=["Age_category",'diabetes'])['bmi'].mean().reset_index().sort_values(by="bmi",ascending=False)
    bar_chart=px.histogram(Glucose_by_age_category,x='Age_category',y='bmi',barmode='group',title="<b> Weight level by Age category </b>",template="plotly_dark")
    bar_chart.update_layout(plot_bgcolor="rgb(0,0,0,0)",paper_bgcolor="rgb(0,0,0,0)")
    bar_chart.update_xaxes(showgrid=False)
    bar_chart.update_yaxes(showgrid=False)
    bar_chart.update_xaxes(categoryorder="total descending")
    
    diabetes_by_bmi=px.histogram(df_selection,x='Weight_Stage',color="diabetes",barmode="group",title="<b> Diabetes by Weight </b>",template="plotly_dark")
    diabetes_by_bmi.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)")
    diabetes_by_bmi.update_xaxes(showgrid=False)
    diabetes_by_bmi.update_yaxes(showgrid=False)
    diabetes_by_bmi.update_xaxes(categoryorder="total descending")

    gender_counts=df_selection.loc[df_selection['diabetes']=="Yes",'gender'].value_counts()
    gender=px.pie(gender_counts,names=gender_counts.index,values=gender_counts.values,template='plotly_dark',hole=0.5)
    gender.update_layout(plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",title="<b> Result by Gender </b>")

    bar1,bar2,pie=st.columns([4,5,4],gap='large')
    bar1.plotly_chart(bar_chart,use_container_width=True)
    bar2.plotly_chart(diabetes_by_bmi,use_container_width=True)
    pie.plotly_chart(gender,use_container_width=True) 

    st.markdown("""___""")
visulaizations()
