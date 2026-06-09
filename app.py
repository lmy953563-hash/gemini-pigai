import streamlit as st
import dashscope
from dashscope import MultiModalConversation
from PIL import Image
import os

# 1. 配置 API Key (请确保在 Streamlit Secrets 中配置了 DASHSCOPE_API_KEY)
# 如果本地测试，可以在这里临时写死：dashscope.api_key = "你的sk-..."
try:
    dashscope.api_key = st.secrets["DASHSCOPE_API_KEY"]
except:
    st.error("请在 Settings -> Secrets 中配置 DASHSCOPE_API_KEY")
    st.stop()

st.set_page_config(page_title="作文批改助手", page_icon="✍️")
st.title("✍️ 智能作文视觉批改")
st.write("上传作文照片，AI 将为您提供专业的批改建议。")

# 2. 文件上传
uploaded_file = st.file_uploader("请上传作文图片", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='上传的作文', use_container_width=True)

    # 3. 批改逻辑
    if st.button("开始智能批改"):
        with st.spinner("AI 老师正在通过视觉识别读取手写内容..."):
            # 保存临时文件供 API 读取
            temp_path = "temp_作文.jpg"
            image.save(temp_path)
            
            try:
                # 调用通义千问视觉模型 qwen-vl-max
                messages = [{
                    'role': 'user',
                    'content': [
                        {'image': os.path.abspath(temp_path)},
                        {'text': '你是一位经验丰富的语文老师。请识别图片中的文字内容，并从错别字、病句、立意、修辞四个维度进行深入点评，最后给出评分和修改建议。'}
                    ]
                }]
                
                response = MultiModalConversation.call(model='qwen-vl-max', messages=messages)
                
                if response.status_code == 200:
                    st.markdown("---")
                    st.markdown("### 📝 批改报告")
                    st.write(response.output.choices[0].message.content)
                else:
                    st.error(f"识别出错: {response.message}")
            
            except Exception as e:
                st.error(f"发生异常: {e}")
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.remove(temp_path)

