import streamlit as st
import google.generativeai as genai
from PIL import Image

# 配置 Gemini
genai.configure(api_key=st.secrets["AQ.Ab8RN6IKDfolU0XqfVG9CWqdIPpXZXsOqiz7QHZ-VmcfCmVgWw"])
model = genai.GenerativeModel('gemini-1.5-flash') # 用 flash 模型速度更快且免费额度大

st.title("📸 作文拍照批改助手")

# 1. 用户拍照或上传
uploaded_file = st.file_uploader("请拍摄或上传作文照片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 显示图片
    image = Image.open(uploaded_file)
    st.image(image, caption='上传的作文', use_column_width=True)
    
    if st.button("开始智能批改"):
        with st.spinner("AI 正在识别字迹并批改中..."):
            # 2. 将图片传给 AI 进行分析 (Gemini 多模态能力可以直接看图)
            prompt = """
            这是一篇学生作文的照片。请完成以下工作：
            1. 识别图片中的文字内容。
            2. 批改作文，指出错别字、语病，并对文章进行点评。
            3. 给出一个分数，并说明扣分理由。
            4. 提供具体的优化建议。
            """
            response = model.generate_content([prompt, image])
            
            # 3. 显示结果
            st.markdown("### 📝 批改报告")
            st.write(response.text)
