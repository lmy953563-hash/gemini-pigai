import streamlit as st
import dashscope
from dashscope import MultiModalConversation
from PIL import Image
import os

# 配置 API
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
                
                prompt = """
                你是一位专业的中高考语文阅卷组长。请对作文进行分析。
                必须严格按照以下格式输出，每一项前面加上【】作为标记：
                【分数统计】(输出表格)
                【段落批注】(输出分析)
                【文章导图】(输出Mermaid代码)
                【总评与建议】(输出点评)
                """
                
                try:
                    messages = [{'role': 'user', 'content': [{'image': os.path.abspath(temp_path)}, {'text': prompt}]}]
                    response = MultiModalConversation.call(model='qwen-vl-max', messages=messages)
                    
                    if response.status_code == 200:
                        response_text = response.output.choices[0].message.content
                        
                        # 【核心修正】：增加安全判断
                        if "【" in response_text:
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
                            # 如果 AI 没有按格式输出，直接显示所有内容，避免报错
                            st.warning("⚠️ AI 返回格式略有不同，已为您完整显示：")
                            st.markdown(response_text)
                    else:
                        st.error(f"识别失败: {response.message}")
                except Exception as e:
                    st.error(f"发生错误: {str(e)}")
                finally:
                    if os.path.exists(temp_path): os.remove(temp_path)
