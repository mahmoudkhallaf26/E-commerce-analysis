import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
st.set_page_config(layout='wide')
df = pd.read_csv("shopping_trends.csv")
df["total_Profit"] = df["Purchase Amount (USD)"] * df["Previous Purchases"]
def age(x):
    if x in range(18,24):
        return "Youth"
    elif x in range(25,34):
        return"Young adults"
    elif x in range(35,44):
        return "Early middle"
    elif x in range(45,54):
        return "Late middle"
    elif x in range(55,60):
        return "Pre-retirement"
    else:
        return "Old age"
df["Age group"] = df["Age"].apply(age)        
def page1():
    tab1,tab2,tab3 = st.tabs(['Category',"Item Purchased","user"])
    with tab1:
        col1,col2 = st.columns(2)
        season = st.sidebar.multiselect("Select Seasons",df["Season"].unique(),default=df["Season"].unique())
        gender = st.sidebar.multiselect("Select gender",df["Gender"].unique(),default=df["Gender"].unique())
        mask = df["Season"].isin(season)
        mask1 = df["Gender"].isin(gender)
        df_filter = df[mask&mask1]
        with col1:
            st.plotly_chart(px.pie(data_frame=df_filter,names="Category",facet_col="Gender",hole=0.4,title="Product purchase percentage for each category by gender"))
            st.plotly_chart(px.histogram(data_frame=df_filter,x="Category",color="Age group",barmode="group",title="Product purchase rate for each category by age group"))
        with col2:    
            st.plotly_chart(px.histogram(data_frame=df_filter,x="Category",y="total_Profit",color="Season",barmode="group",title="Total profit distribution by category and season"))
            st.plotly_chart(px.histogram(data_frame=df_filter,x="Category",color="Discount Applied",barmode="group",title="Distribution of Categories by Discount Applied"))
    with tab2:
        col1,col2,col3 = st.columns(3)
        with col1:
            st.markdown("<p>TOP 10 Item have high rate</p>", unsafe_allow_html=True)
            st.dataframe(pd.pivot_table(data=df_filter,index="Item Purchased",values="Review Rating").sort_values(by="Review Rating",ascending=False).head(10))
            
        with col2:
            st.markdown("<p>TOP 10 Item have high Profit</p>", unsafe_allow_html=True)
            st.dataframe(pd.pivot_table(data=df_filter,index="Item Purchased",values="total_Profit").sort_values(by="total_Profit",ascending=False).head(10))
            
        with col3:
            st.plotly_chart(px.histogram(data_frame=df_filter["Item Purchased"].value_counts().sort_values(ascending=False).to_frame().reset_index().head(10),x="Item Purchased",y="count",title="TOP 10 Best Selling Products"))
            
        
        st.plotly_chart(px.treemap(data_frame=df_filter,path=["Item Purchased","Age group"],color_continuous_scale='Viridis',title="Map showing the most purchased product for each Age group"))
            
    with tab3:
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<p>Top 10 Location make order and Shipping Type use</p>",unsafe_allow_html=True)
            st.dataframe(pd.pivot_table(data=df_filter,columns="Shipping Type",index="Location",values="Customer ID",aggfunc="count",margins=True).sort_values(by="All",ascending=False)[1:].head(10))
            st.plotly_chart( px.pie(data_frame=df,names="Payment Method",title="Percentage of each payment method"))
        with col2:
            st.plotly_chart(px.histogram(data_frame=df,x="Frequency of Purchases",color="Subscription Status",barmode="group",title="Distribution of purchase frequency by subscription status"))
            st.plotly_chart(px.histogram(data_frame=df_filter,x="Shipping Type",color="Subscription Status" , barmode="group",title="Shipping companies users from subscribers and non-subscribers"))
            st.plotly_chart(px.treemap(data_frame=df,path=["Age group","Subscription Status"],title="Tree map showing subscription status within age groups"))
def page2():
    st.markdown("<h2>summary</h2>",unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style='display: flex; align-items: center; font-family: Arial, sans-serif; font-size: 14px;'>
        <span style="font-weight: bold; margin-right: 10px;">Most requested category:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {pd.pivot_table(data=df,index="Category",aggfunc="count",values="Customer ID").reset_index().sort_values(by="Customer ID",ascending=False)["Category"].iloc[0]}
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style='display: flex; align-items: center; font-family: Arial, sans-serif; font-size: 14px;'>
        <span style="font-weight: bold; margin-right: 10px;">Most requested item:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {pd.pivot_table(data=df,index="Item Purchased",aggfunc="count",values="Customer ID").reset_index().sort_values(by="Customer ID",ascending=False)["Item Purchased"].iloc[0]}
        </div>
        </div>
        """, unsafe_allow_html=True)
        Category = st.selectbox("select category",df["Category"].unique())
        mask = df["Category"] == Category
        df_filter1 = df[mask]
        st.markdown(f"""
        <div style='font-family: Arial, sans-serif; font-size: 16px; display: flex; align-items: center; gap: 10px;margin-top: 20px;'>
        <span style="font-weight: bold;">category Profit:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {df[df["Category"] ==Category ]["total_Profit"].sum()}
        </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='display: flex; align-items: center; font-family: Arial, sans-serif; font-size: 14px;'>
        <span style="font-weight: bold; margin-right: 10px;">Total Profit:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {df["total_Profit"].sum()}
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style='display: flex; align-items: center; font-family: Arial, sans-serif; font-size: 14px;'>
        <span style="font-weight: bold; margin-right: 10px;">Total Subscription:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {pd.pivot_table(data=df,index="Subscription Status",aggfunc="count",values="Customer ID").reset_index()["Customer ID"][1]}
        </div>
        </div>
        """, unsafe_allow_html=True)
        Item=st.selectbox("Select Item",df_filter1["Item Purchased"].unique())
    with col3:
        st.markdown(f"""
        <div style='display: flex; align-items: center; font-family: Arial, sans-serif; font-size: 14px;'>
        <span style="font-weight: bold; margin-right: 10px;">Highest Profit Category:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {pd.pivot_table(data=df,index="Category",values="total_Profit").sort_values(by="total_Profit", ascending=False).reset_index()["Category"][0]}
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style='display: flex; align-items: center; font-family: Arial, sans-serif; font-size: 14px;'>
        <span style="font-weight: bold; margin-right: 10px;">Highest Profit item:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {pd.pivot_table(data=df,index="Item Purchased",values="total_Profit").sort_values(by="total_Profit", ascending=False).reset_index()["Item Purchased"][0]}
        </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style='font-family: Arial, sans-serif; font-size: 16px; display: flex; align-items: center; gap: 10px;margin-top: 20px;'>
        <span style="font-weight: bold;">Item Profit:</span>
        <div style='padding: 10px 20px; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 5px; background-color: rgba(0, 0, 0, 0.05);'>
        {df[df["Item Purchased"] ==Item ]["total_Profit"].sum()}
        </div>
        </div>
        """, unsafe_allow_html=True)

        
pages = {
    'analysis' : page1,
    'summary' : page2
}
pg = st.sidebar.radio('Navigate between pages' , pages.keys())

pages[pg]()
