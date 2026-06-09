import streamlit as st
import dashscope
from dashscope import MultiModalConversation
from PIL import Image
import os

# 1. API 配置
dashscope.api_key = st.secrets["DASHSCOPE_API_KEY"]

st.set_page_config(page_title="中高考阅卷台", layout="wide")
st.title("✍️ 中高考作文专业阅卷台")

uploaded_file = st.file_uploader("请上传作文原稿图片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.image(uploaded_file, caption="学生原稿", use_container_width=True)

    with col_right:
        if st.button("开始专业批改", type="primary"):
            with st.spinner("阅卷组长正在阅卷..."):
                temp_path = "temp.jpg"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 提示词：要求 AI 用【】进行强分隔
                prompt = """
                你是一位专业的中高考语文阅卷组长。请对作文进行分析。
                必须严格按照以下格式输出（不要输出任何开场白）：
                【分数统计】
                | 维度 | 得分 |
                |---|---|
                | 内容 | ... |
                | 表达 | ... |
                | 发展 | ... |
                【段落批注】
                1. 第一段：...
                2. 第二段：...
                【文章导图】
                (输出Mermaid代码)
                【总评与建议】
                ...
                """
                
                # 调用 API
                messages = [{'role': 'user', 'content': [{'image': os.path.abspath(temp_path)}, {'text': prompt}]}]
                response = MultiModalConversation.call(model='qwen-vl-max', messages=messages)
                
                if response.status_code == 200:
                    # 【核心修复】：在此定义 response_text 变量
                    response_text = response.output.choices[0].message.content
                    
                    # 开始切分与展示
                    sections = response_text.split("【")
                    
                    for sec in sections:
                        if "分数统计" in sec:
                            st.subheader("📊 分数统计")
                            st.markdown(sec.replace("分数统计】", "").strip())
                        elif "段落批注" in sec:
                            with st.expander("📝 逐段批注分析", expanded=True):
                                st.markdown(sec.replace("段落批注】", "").strip())
                        elif "文章导图" in sec:
                            with st.expander("🧠 文章逻辑思维导图"):
                                st.code(sec.replace("文章导图】", "").strip(), language="mermaid")
                        elif "总评与建议" in sec:
                            st.success("✅ 总评与建议")
                            st.markdown(sec.replace("总评与建议】", "").strip())
                else:
                    st.error(f"识别失败: {response.message}")
                
                if os.path.exists(temp_path): os.remove(temp_path)
