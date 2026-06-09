import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. 配置 API Key
# 首先尝试从 Streamlit Secrets 读取
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("未找到有效的 API Key，请在 Secrets 中配置 GOOGLE_API_KEY")
    st.stop()

# 2. 设置 AI 模型
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 网页界面
st.set_page_config(page_title="作文批改助手", page_icon="✍️")
st.title("✍️ 智能作文批改助手")
st.write("上传作文照片，让 AI 为你精准批改。")

# 4. 上传文件功能
uploaded_file = st.file_uploader("选择作文照片 (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 展示图片
    image = Image.open(uploaded_file)
    st.image(image, caption='你的作文', use_column_width=True)
    
    # 5. 批改逻辑
    if st.button("开始智能批改"):
        with st.spinner("AI 老师正在认真阅读中..."):
            try:
                prompt = """
                你是一位专业的语文老师。请完成以下任务：
                1. 识别并提取图片中的作文文字。
                2. 检查错别字、标点错误和病句。
                3. 从立意、结构、修辞角度进行点评。
                4. 给出一个 0-100 的评分，并详细说明扣分原因。
                5. 提供具体的优化建议。
                """
                
                # 调用 Gemini 模型
                response = model.generate_content([prompt, image])
                
                # 展示结果
                st.markdown("---")
                st.markdown("### 📝 批改报告")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"批改发生错误，请检查 API Key 权限或网络连接: {e}")

