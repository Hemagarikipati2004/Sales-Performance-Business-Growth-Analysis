from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "sales_clean.csv"

st.set_page_config(page_title="Sales Performance & Business Growth", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp {background: #0b1220; color: #e8eef9;}
[data-testid="stMetric"] {background:#151f32; border:1px solid #27364f; padding:16px; border-radius:12px;}
[data-testid="stMetricLabel"] {color:#a9b8ce;}
[data-testid="stMetricValue"] {color:#f4f7fc;}
section[data-testid="stSidebar"] {background:#111b2d;}
h1,h2,h3 {color:#f4f7fc;}
div[data-testid="stDataFrame"] {border:1px solid #27364f; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Sales Performance & Business Growth Analysis")
st.caption("Executive analytics | Revenue • Profitability • Customers • Products • Regions")

if not DATA.exists():
    st.error("Clean dataset not found. From the project folder, run: python src/clean_data.py")
    st.stop()

df = pd.read_csv(DATA, parse_dates=["order_date"])
min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()

with st.sidebar:
    st.header("Dashboard filters")
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df["region"].dropna().unique()), default=sorted(df["region"].dropna().unique()))
    categories = st.multiselect("Category", sorted(df["category"].dropna().unique()), default=sorted(df["category"].dropna().unique()))
    channels = st.multiselect("Sales channel", sorted(df["sales_channel"].dropna().unique()), default=sorted(df["sales_channel"].dropna().unique()))
    segments = st.multiselect("Customer segment", sorted(df["customer_segment"].dropna().unique()), default=sorted(df["customer_segment"].dropna().unique()))

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
else:
    start, end = pd.Timestamp(min_date), pd.Timestamp(max_date) + pd.Timedelta(days=1)

f = df[(df.order_date >= start) & (df.order_date < end) &
       df.region.isin(regions) & df.category.isin(categories) &
       df.sales_channel.isin(channels) & df.customer_segment.isin(segments)].copy()

if f.empty:
    st.warning("No records match the selected filters. Please widen your filter selection.")
    st.stop()

revenue = f.revenue.sum()
profit = f.profit.sum()
orders = f.order_id.nunique()
units = f.quantity.sum()
margin = profit / revenue * 100 if revenue else 0
aov = revenue / orders if orders else 0

# Previous period comparison based on equal-length date window, preserving non-date filters
days = max((end - start).days, 1)
prev_start, prev_end = start - pd.Timedelta(days=days), start
prev = df[(df.order_date >= prev_start) & (df.order_date < prev_end) &
          df.region.isin(regions) & df.category.isin(categories) &
          df.sales_channel.isin(channels) & df.customer_segment.isin(segments)]
prev_rev = prev.revenue.sum()
growth = ((revenue - prev_rev) / prev_rev * 100) if prev_rev else 0

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Total Revenue", f"₹{revenue:,.0f}", f"{growth:+.1f}% vs prior window")
c2.metric("Total Profit", f"₹{profit:,.0f}")
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("Total Orders", f"{orders:,}")
c5.metric("Units Sold", f"{units:,.0f}")
c6.metric("Average Order Value", f"₹{aov:,.0f}")

st.divider()
left,right = st.columns((1.6,1))
monthly = f.assign(month=f.order_date.dt.to_period("M").astype(str)).groupby("month",as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum"))
with left:
    st.subheader("Revenue & profit trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly.month,y=monthly.Revenue,mode="lines+markers",name="Revenue",line=dict(width=3)))
    fig.add_trace(go.Scatter(x=monthly.month,y=monthly.Profit,mode="lines+markers",name="Profit",line=dict(width=3)))
    fig.update_layout(template="plotly_dark",paper_bgcolor="#0b1220",plot_bgcolor="#0b1220",height=360,margin=dict(l=10,r=10,t=20,b=10),legend=dict(orientation="h"))
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Revenue by region")
    reg = f.groupby("region",as_index=False).revenue.sum().sort_values("revenue",ascending=True)
    fig = px.bar(reg,x="revenue",y="region",orientation="h",text_auto=".2s",template="plotly_dark")
    fig.update_layout(paper_bgcolor="#0b1220",plot_bgcolor="#0b1220",height=360,margin=dict(l=10,r=10,t=20,b=10),xaxis_title="Revenue (₹)",yaxis_title="")
    st.plotly_chart(fig,use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Category contribution")
    cat = f.groupby("category",as_index=False).revenue.sum()
    fig = px.pie(cat,values="revenue",names="category",hole=.55,template="plotly_dark")
    fig.update_layout(paper_bgcolor="#0b1220",height=350,margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Sales channel performance")
    ch = f.groupby("sales_channel",as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum"))
    fig = px.bar(ch,x="sales_channel",y=["Revenue","Profit"],barmode="group",template="plotly_dark")
    fig.update_layout(paper_bgcolor="#0b1220",plot_bgcolor="#0b1220",height=350,margin=dict(l=10,r=10,t=10,b=10),xaxis_title="",yaxis_title="Amount (₹)")
    st.plotly_chart(fig,use_container_width=True)

st.divider()
left,right = st.columns(2)
with left:
    st.subheader("Top 10 products by revenue")
    prod = f.groupby("product",as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum"),Units=("quantity","sum")).sort_values("Revenue",ascending=False).head(10)
    fig = px.bar(prod.sort_values("Revenue"),x="Revenue",y="product",orientation="h",text_auto=".2s",template="plotly_dark")
    fig.update_layout(paper_bgcolor="#0b1220",plot_bgcolor="#0b1220",height=400,margin=dict(l=10,r=10,t=10,b=10),xaxis_title="Revenue (₹)",yaxis_title="")
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Customer segment performance")
    seg = f.groupby("customer_segment",as_index=False).agg(Revenue=("revenue","sum"),Orders=("order_id","nunique"),Profit=("profit","sum"))
    fig = px.bar(seg,x="customer_segment",y="Revenue",color="customer_segment",text_auto=".2s",template="plotly_dark")
    fig.update_layout(showlegend=False,paper_bgcolor="#0b1220",plot_bgcolor="#0b1220",height=400,margin=dict(l=10,r=10,t=10,b=10),xaxis_title="",yaxis_title="Revenue (₹)")
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Detailed performance table")
detail = f.groupby(["region","category","product"],as_index=False).agg(Revenue=("revenue","sum"),Profit=("profit","sum"),Units=("quantity","sum"),Orders=("order_id","nunique"))
detail["Profit Margin %"] = (detail.Profit / detail.Revenue * 100).round(2)
st.dataframe(detail.sort_values("Revenue",ascending=False),use_container_width=True,hide_index=True)

st.subheader("Business insights")
best_region = f.groupby("region").revenue.sum().idxmax()
best_category = f.groupby("category").revenue.sum().idxmax()
best_product = f.groupby("product").profit.sum().idxmax()
cat_margin = f.groupby("category").agg(cat_profit=("profit","sum"), cat_revenue=("revenue","sum"))
cat_margin["margin_pct"] = cat_margin.cat_profit / cat_margin.cat_revenue.replace(0, pd.NA) * 100
low_margin = cat_margin.margin_pct.idxmin()
i1,i2 = st.columns(2)
i1.info(f"**Top revenue region:** {best_region}. Review its sales mix and replicate successful practices in lower-performing regions.")
i2.info(f"**Top revenue category:** {best_category}. Protect availability and monitor discount levels.")
i1.success(f"**Highest profit product:** {best_product}. Consider bundling or targeted campaigns while monitoring inventory.")
i2.warning(f"**Lowest-margin category:** {low_margin}. Review discounting, sourcing and operating costs before increasing promotion.")

st.download_button("Download filtered sales data",f.to_csv(index=False).encode("utf-8"),"filtered_sales_data.csv","text/csv")
st.caption("Demo dataset: synthetic records generated for portfolio and learning use. Revenue and profit are illustrative.")
