import streamlit as st
import dashscope
from dashscope import MultiModalConversation
from PIL import Image
import os

# 1. 配置 API
dashscope.api_key = st.secrets["DASHSCOPE_API_KEY"]

# 2. 页面布局
st.set_page_config(page_title="智能作文批改", layout="wide")
st.title("✍️ 智能作文深度批改助手")

uploaded_file = st.file_uploader("上传手写作文图片...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 展示上传的图片
    image = Image.open(uploaded_file)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, caption="原卷", use_container_width=True)
    
    with col2:
        if st.button("开始专业批改"):
            with st.spinner("AI 正在深度阅卷，请稍候..."):
                # 保存临时文件
                temp_path = "temp_essay.jpg"
                image.save(temp_path)
                
                # 提示词：模仿你提供的专业报告结构
                prompt = """
                你是一位专业的中高考语文阅卷组组长。请详细分析这张作文图片，输出一份结构化报告：
                1. 识别并列出原文文本；
                2. 按维度打分 (内容/表达/发展，满分60)；
                3. 用 Mermaid 语法画出文章逻辑思维导图；
                4. 详细点评错别字、病句和立意；
                5. 给出具体的升格建议。
                """
                
                # 调用模型
                try:
                    messages = [{'role': 'user', 'content': [{'image': os.path.abspath(temp_path)}, {'text': prompt}]}]
                    response = MultiModalConversation.call(model='qwen-vl-max', messages=messages)
                    
                    if response.status_code == 200:
                        st.markdown(response.output.choices[0].message.content)
                    else:
                        st.error(f"分析失败: {response.message}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
