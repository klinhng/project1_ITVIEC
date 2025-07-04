
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(layout="wide")
st.title("ITViec Company Review Dashboard")

# Đọc dữ liệu
df = pd.read_excel('Processed_reviews.xlsx')

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Tìm review theo từ khóa", "🏢 Phân tích cảm xúc", "🔗 Phân nhóm kết quả", "🆕 Review mới"])

with tab1:
    st.header("1. Tìm công ty theo từ khóa nổi bật")
    keyword = st.text_input("Nhập từ khóa bạn quan tâm:")
    if keyword:
        temp_df = df.copy()
        mask = (
            temp_df["What I liked"].fillna("").str.contains(keyword, case=False, na=False) |
            temp_df["Suggestions for improvement"].fillna("").str.contains(keyword, case=False, na=False)
        )
        filtered = temp_df.loc[mask, ["Company Name", "What I liked", "Suggestions for improvement", "sentiment"]].dropna(how='all').head(10)
        if not filtered.empty:
            st.dataframe(filtered.rename(columns={
                "Company Name": "Công ty",
                "What I liked": "Review tích cực",
                "Suggestions for improvement": "Review tiêu cực",
                "sentiment": "Cảm xúc"
            }))
        else:
            st.info("Không tìm thấy công ty có review phù hợp với từ khóa.")

with tab2:
    st.header("2. Phân tích cảm xúc công ty")
    company2 = st.selectbox("Chọn công ty", df["Company Name"].dropna().unique(), key="company2")
    company_df = df[df["Company Name"] == company2]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔄 Số lượt đánh giá", len(company_df))
        st.metric("⭐ Điểm trung bình", f"{company_df['Rating'].mean():.2f}")
        st.write("### 📊 Biểu đồ phân bố cảm xúc")
        sentiment_counts = company_df['sentiment'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

        st.write("### 👍 Nhận xét tích cực tiêu biểu")
        for review in company_df[company_df["sentiment"] == "positive"]["What I liked"].dropna().head(3):
            st.success(review)

        st.write("### 👎 Nhận xét tiêu cực tiêu biểu")
        for review in company_df[company_df["sentiment"] == "negative"]["Suggestions for improvement"].dropna().head(3):
            st.error(review)

    with col2:
        st.write("### ☁️ WordCloud tích cực")
        pos_text = " ".join(company_df[company_df['sentiment'] == 'positive']['liked_clean'].dropna())
        if pos_text:
            wc = WordCloud(width=400, height=200, background_color="white").generate(pos_text)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

        st.write("### ☁️ WordCloud tiêu cực")
        neg_text = " ".join(company_df[company_df['sentiment'] == 'negative']['suggestion_clean'].dropna())
        if neg_text:
            wc = WordCloud(width=400, height=200, background_color="white").generate(neg_text)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

with tab3:
    st.header("3. Phân nhóm kết quả đánh giá (Clustering)")
    if {'x', 'y', 'cluster', 'Company Name'}.issubset(df.columns):
        selected_cluster = st.selectbox("Chọn công ty để hiển thị cụm", df["Company Name"].dropna().unique(), key="cluster_company")
        subset = df[df["Company Name"] == selected_cluster]

        if not subset.empty:
            st.write("### 📍 Biểu đồ phân cụm đánh giá bằng KMeans")
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.scatterplot(data=subset, x="x", y="y", hue="cluster", palette="Set2", ax=ax)
            ax.set_title("Phân cụm đánh giá công ty")
            st.pyplot(fig)
        else:
            st.warning("Không tìm thấy dữ liệu phân cụm cho công ty này.")
    else:
        st.info("Dữ liệu chưa có thông tin phân cụm (x, y, cluster).")

with tab4:
    st.header("4. Phân tích review mới")
    review_mode = st.radio("Chọn cách nhập review:", ["Nhập tay", "Tải lên file (.xlsx)"])
    new_df = None

    if review_mode == "Nhập tay":
        new_company = st.text_input("Tên công ty")
        new_liked = st.text_area("Nội dung tích cực (What I liked)")
        new_suggest = st.text_area("Nội dung tiêu cực (Suggestions for improvement)")

        if st.button("Phân tích"):
            if new_company and (new_liked or new_suggest):
                sentiment = "positive" if "good" in new_liked.lower() else "negative"
                new_df = pd.DataFrame([{
                    "Company Name": new_company,
                    "What I liked": new_liked,
                    "Suggestions for improvement": new_suggest,
                    "sentiment": sentiment
                }])
            else:
                st.warning("Vui lòng nhập đầy đủ thông tin tối thiểu.")

    else:
        uploaded_file = st.file_uploader("Tải file .xlsx có các review mới", type=["xlsx"])
        if uploaded_file:
            new_df = pd.read_excel(uploaded_file)
            st.success("Đã tải thành công!")
            st.write("📄 Dữ liệu preview:", new_df.head())

    if new_df is not None and not new_df.empty:
        st.subheader("📊 Kết quả phân tích cảm xúc (giả lập)")
        st.write(new_df[["Company Name", "What I liked", "Suggestions for improvement", "sentiment"]])

        if "liked_clean" not in new_df.columns:
            new_df["liked_clean"] = new_df["What I liked"].fillna("")
        if "suggestion_clean" not in new_df.columns:
            new_df["suggestion_clean"] = new_df["Suggestions for improvement"].fillna("")

        st.subheader("☁️ WordCloud từ review mới")
        pos_text = " ".join(new_df[new_df['sentiment'] == 'positive']['liked_clean'].dropna())
        if pos_text:
            wc = WordCloud(width=400, height=200, background_color="white").generate(pos_text)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

        neg_text = " ".join(new_df[new_df['sentiment'] == 'negative']['suggestion_clean'].dropna())
        if neg_text:
            wc = WordCloud(width=400, height=200, background_color="white").generate(neg_text)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
