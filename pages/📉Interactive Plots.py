import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Interactive Plots",page_icon="https://cdn-icons-png.flaticon.com/128/9032/9032033.png",layout='centered',initial_sidebar_state="collapsed")

@st.cache_data(show_spinner="Loading")
def load_data():
    df = pd.read_csv("D:\VS Code\Pandas\Streamlit\Cleaned.csv")
    df = df.drop(columns=['Unnamed: 0', 'age_normalized', 'bmi_normalized',
                 'HbA1c_level_normalized', 'blood_glucose_level_normalized'])
    return df


@st.cache_data(show_spinner="Loading")
def plot_box(df, x_axis):
    plot = px.box(df, x=x_axis)
    return plot


@st.cache_data(show_spinner="Loading")
def plot_countplot(df, x_axis, y_axis,user_input):
    plot = px.histogram(df, x=x_axis, color=y_axis, barmode='group',animation_frame=user_input)
    return plot


def Interactive_plot(df):
    st.header("Distribution of Numerical Features")
    x_axis = st.selectbox("Select the Columns", options=df.select_dtypes(
        include=[int, float, np.number]).columns)
    button = st.button("Plot Boxplot")
    if button:
        plot = plot_box(df, x_axis)
        st.plotly_chart(plot)

    st.markdown("""___""")

    st.header("Category frequency plot")
    op1,op2=st.columns([5,5],gap='large')
    with op1:
        x_axis = st.selectbox("Select the columns for x-axis",
                            options=df.select_dtypes(include=[object]).columns)
    with op2:
        y_axis = st.selectbox("Select the column for y-axis",
                            options=df.select_dtypes(include=[object]).columns)
    

        
    user_input=st.selectbox("KeyFrame",options=df.select_dtypes(include=[object]).columns)
    button = st.button("Plot Countplot")
    if button:
        plot = plot_countplot(df, x_axis, y_axis,df[user_input])
        plot.update_yaxes(showgrid=False)
        st.plotly_chart(plot)

df = load_data()

Interactive_plot(df)
