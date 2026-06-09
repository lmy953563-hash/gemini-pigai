import streamlit as st
import dashscope
from dashscope import MultiModalConversation
from PIL import Image
import os

# 1. 配置
dashscope.api_key = st.secrets["DASHSCOPE_API_KEY"]

st.set_page_config(page_title="中高考专业阅卷台", layout="wide")
st.title("✍️ 中高考作文专业阅卷台")

uploaded_file = st.file_uploader("请上传作文原稿图片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 布局：左侧原稿，右侧批改报告
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("🖼️ 原稿展示")
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

    with col2:
        if st.button("开始专业批改", type="primary"):
            with st.spinner("阅卷组长正在阅卷中..."):
                temp_path = "temp_essay.jpg"
                image.save(temp_path)
                
                # 精准指令：强制分开输出批注与总评
                prompt = """
                你是一位中高考语文阅卷组长。请分析这张图片中的作文，请严格按以下 JSON 结构输出，以便我进行排版：
                {
                    "comments": "在每段文字旁的具体批注，直接引用原文并给出评价",
                    "structure_map": "Mermaid思维导图代码",
                    "score_table": "Markdown表格（内容/表达/发展得分）",
                    "summary": "专业总评文字",
                    "advice": "3-5条具体的写作提升建议"
                }
                输出格式：只需输出上述内容的 Markdown 整合版本，标题分明，使用表格和列表，不要混在一起。
                """
                
                try:
                    messages = [{'role': 'user', 'content': [{'image': os.path.abspath(temp_path)}, {'text': prompt}]}]
                    response = MultiModalConversation.call(model='qwen-vl-max', messages=messages)
                    
                    if response.status_code == 200:
                        content = response.output.choices[0].message.content
                        st.markdown(content)
                    else:
                        st.error("识别失败，请检查图片清晰度")
                finally:
                    if os.path.exists(temp_path): os.remove(temp_path)

