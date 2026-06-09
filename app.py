import streamlit as st
import dashscope
from dashscope import MultiModalConversation
from PIL import Image
import os

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
                # 调用模型，要求它明确返回不同板块的内容
                # 关键技巧：要求 AI 按【板块标题】进行分隔
                prompt = """
                你是一位中高考语文阅卷组长。请对作文进行深度批改，必须按以下格式返回，每一块内容用【标题】隔开：
                【分数统计】使用表格显示内容/表达/发展各分项。
                【段落批注】逐段分析，列出亮点与不足。
                【文章导图】仅输出Mermaid代码。
                【总评与建议】简短客观的总评及三条行动指南。
                不要输出任何开场白，直接输出各板块。
                """
                
                # ... (调用模型逻辑不变) ...
                # 这里假设得到 response_text
                
                # --- 【界面美化核心：强制切割】 ---
                sections = response_text.split("【")
                for sec in sections:
                    if "分数统计" in sec:
                        st.subheader("📊 分数统计")
                        st.markdown(sec.replace("分数统计】", ""))
                    elif "段落批注" in sec:
                        with st.expander("📝 逐段批注分析 (点击展开)", expanded=True):
                            st.markdown(sec.replace("段落批注】", ""))
                    elif "文章导图" in sec:
                        with st.expander("🧠 文章逻辑思维导图"):
                            st.code(sec.replace("文章导图】", ""), language="mermaid")
                    elif "总评与建议" in sec:
                        st.success("✅ 总评与建议")
                        st.markdown(sec.replace("总评与建议】", ""))
