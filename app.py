import streamlit as st
import os
from paddleocr import PaddleOCR
from openai import OpenAI
from PIL import Image

# ==================== 安全检查与配置 ====================
# 请确保在 Streamlit Cloud 的 Settings -> Secrets 中配置了 DEEPSEEK_API_KEY
if "DEEPSEEK_API_KEY" not in st.secrets:
    st.error("未在 Secrets 中配置 DEEPSEEK_API_KEY，请检查设置。")
    st.stop()

# 1. 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

# 2. 初始化 PaddleOCR (首次加载时会自动下载模型)
# 使用缓存以提高速度
@st.cache_resource
def get_ocr_engine():
    return PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)

ocr = get_ocr_engine()

# ==================== 网页界面 ====================
st.set_page_config(page_title="智能作文批改助手", page_icon="✍️")
st.title("✍️ 专业级智能作文批改报告")
st.write("上传作文照片，AI 将为您提供专业的批改建议与结构化分析。")

# 文件上传
uploaded_file = st.file_uploader("选择作文照片 (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 3. 显示图片
    image = Image.open(uploaded_file)
    st.image(image, caption='已上传的作文图片', use_container_width=True)
    
    # 4. 识别文字
    if st.button("开始提取文字并批改"):
        with st.spinner("视觉引擎正在识别文字..."):
            # 保存临时文件供 OCR 读取
            temp_filename = "temp_input.jpg"
            image.save(temp_filename)
            
            # 执行 OCR
            ocr_result = ocr.ocr(temp_filename, cls=True)
            
            # 拼接识别结果
            original_text = ""
            if ocr_result and ocr_result[0]:
                for line in ocr_result[0]:
                    original_text += line[1][0] + " "
            
            # 清理临时文件
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        st.subheader("📝 识别出的文字内容")
        st.text_area("识别结果：", value=original_text, height=150)

        # 5. 调用 DeepSeek 进行专业批改
        with st.spinner("AI 老师正在撰写专业批改报告..."):
            try:
                prompt = f"""
                你是一位专业的语文老师。请根据学生提供的作文内容，撰写一份结构化的批改报告。
                
                作文内容：
                {original_text}
                
                请按照以下格式输出 Markdown 内容：
                # 📊 作文批改报告
                ## 🎯 总评
                (给出评分 0-100，总结优缺点)
                ## 🧠 逻辑结构分析
                (使用 Mermaid 语法绘制思维导图，总结文章脉络)
                ## 📝 详细点评
                - 错别字与标点：
                - 语句与病句：
                - 立意与修辞：
                ## ✅ 提升建议
                (给出 3 条具体的改进建议)
                """
                
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一位专业的语文批改专家。"},
                        {"role": "user", "content": prompt},
                    ],
                )
                
                # 展示结果
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"批改发生错误: {e}")

                st.error(f"发生异常: {e}")
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.remove(temp_path)

