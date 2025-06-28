import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
from wordcloud import WordCloud
import os
print("Current Working Directory:", os.getcwd())

st.title("Đồ án tốt nghiệp DS-ML - CSC 304")
st.subheader("Chào mừng các bạn đến với đồ án tốt nghiệp DS-ML - CSC 304")
st.write("### Có 2 chủ đề trong khóa học:")

# Đọc dữ liệu đã xử lý (giả sử bạn đã lưu ra file csv từ notebook)
df = pd.read_csv('Processed_reviews.csv')

st.title("Phân tích đánh giá công ty - Data Science Project 1")

# Hiển thị bảng dữ liệu
st.subheader("Dữ liệu đánh giá mẫu")
st.dataframe(df.head())

# Biểu đồ phân bố cảm xúc
st.subheader("Phân bố cảm xúc")
sentiment_counts = df['sentiment'].value_counts()
st.bar_chart(sentiment_counts)

# WordCloud từ đánh giá tích cực
st.subheader("WordCloud từ đánh giá tích cực")
pos_text = " ".join(df[df['sentiment'] == 'positive']['liked_clean'].dropna())
if pos_text:
    wc = WordCloud(width=800, height=400, background_color="white").generate(pos_text)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# WordCloud từ đánh giá tiêu cực
st.subheader("WordCloud từ đánh giá tiêu cực")
neg_text = " ".join(df[df['sentiment'] == 'negative']['suggestion_clean'].dropna())
if neg_text:
    wc = WordCloud(width=800, height=400, background_color="white").generate(neg_text)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# Biểu đồ cụm (cluster)
st.subheader("Phân cụm đánh giá (KMeans)")
if 'x' in df.columns and 'y' in df.columns and 'cluster' in df.columns:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="x", y="y", hue="cluster", palette="Set2", ax=ax)
    st.pyplot(fig)

# Thống kê theo công ty
st.subheader("Phân tích theo công ty")
company_list = df["Company Name"].dropna().unique()
company = st.selectbox("Chọn công ty", company_list)
company_df = df[df["Company Name"] == company]
st.write(f"Số lượt đánh giá: {len(company_df)}")
st.write(f"Điểm trung bình: {company_df['Rating'].mean():.2f}")

# Hiển thị nhận xét tích cực/tiêu cực nổi bật
st.write("**Nhận xét tích cực nổi bật:**")
st.write(company_df[company_df["sentiment"] == "positive"]["What I liked"].head(3).tolist())
st.write("**Nhận xét tiêu cực nổi bật:**")
st.write(company_df[company_df["sentiment"] == "negative"]["Suggestions for improvement"].head(3).tolist())
