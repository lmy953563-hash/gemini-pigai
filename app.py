import streamlit as st
from openai import OpenAI

# 1. 配置 DeepSeek API
client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

st.title("✍️ DeepSeek 作文批改助手")

text = st.text_area("请直接输入作文内容进行批改：")

if st.button("开始智能批改"):
    with st.spinner("AI 老师正在批改中..."):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一位专业的语文老师，请对作文进行点评、评分和修改建议。"},
                    {"role": "user", "content": text},
                ],
            )
            st.markdown("### 📝 批改报告")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"发生错误: {e}")


