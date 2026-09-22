import streamlit as st
import random
import time

st.set_page_config(
    page_title="YUDAI NAVI",
    page_icon="🏠",
    layout="centered"
)

# =========================
# 設定
# =========================

# Googleマップで「雄大の家」を開いて
# 「共有」→「リンクをコピー」
# そのURLをここに貼る
YUDAI_MAP_URL = "https://www.google.co.jp/maps/place/雄大の家/@35.6676062,139.6617396,17z/data=!3m1!4b1!4m6!3m5!1s0x6018f30023fb14a9:0x939d10be96b9e5ed!8m2!3d35.6676019!4d139.6643145!16s%2Fg%2F11xgkb4_ml?entry=ttu&g_ep=EgoyMDI2MDkxNi4wIKXMDSoASAFQAw%3D%3D"

# =========================
# デザイン
# =========================

st.markdown("""
<style>
    .block-container {
        max-width: 700px;
        padding-top: 2rem;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .sub-title {
        text-align: center;
        color: #888;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #ddd;
        text-align: center;
        margin-top: 15px;
    }

    .big-result {
        font-size: 32px;
        font-weight: 800;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# タイトル
# =========================

st.markdown(
    '<div class="main-title">🏠 YUDAI NAVI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">あなたの悩みをAIが分析し、最適な行動を提案します。</div>',
    unsafe_allow_html=True
)


# =========================
# セッション
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# 過去メッセージ
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# AI回答生成
# =========================

def generate_answer(question):

    question_lower = question.lower()

    # 入力内容によって多少返答を変える
    if any(word in question for word in ["仕事", "会社", "上司", "残業"]):

        reason = """
仕事上のストレスが蓄積している可能性があります。

こういう場合は一度環境を変えて、
信頼できる場所で状況を整理することが重要です。
"""

    elif any(word in question for word in ["腹減", "お腹", "ご飯", "飯"]):

        reason = """
エネルギー不足が意思決定能力に影響している可能性があります。

まずは安心できる場所へ移動し、
今後の行動を考える必要があります。
"""

    elif any(word in question for word in ["彼女", "彼氏", "恋愛", "喧嘩"]):

        reason = """
感情が強く動いている状態では、
冷静な判断が難しくなることがあります。

一度別の環境へ移動して、
落ち着いて状況を整理するのが良いでしょう。
"""

    elif any(word in question for word in ["眠", "疲れ", "だる"]):

        reason = """
現在の状態では休息が必要な可能性があります。

安全で落ち着ける場所への移動を優先してください。
"""

    elif any(word in question for word in ["暇", "ひま"]):

        reason = """
現在、明確な予定がない状態と判断しました。

時間を有効活用するため、
新しい場所へ移動することを推奨します。
"""

    else:

        reason = random.choice([
            """
状況を総合的に分析しました。

複数の解決策を比較しましたが、
環境を変えることが最も効果的と判断しました。
""",
            """
かなり複雑な問題ですね。

しかし、現在の状況・心理状態・行動可能性を分析した結果、
取るべき行動は明確です。
""",
            """
あなたの入力内容を分析しました。

問題そのものを直接解決するよりも、
まず場所を変えることが重要だと判断しました。
"""
        ])

    return reason


# =========================
# 入力
# =========================

question = st.chat_input(
    "今困っていることを入力してください"
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)


    with st.chat_message("assistant"):

        st.write("状況を分析しています…")

        progress = st.progress(0)

        for percent in [10, 27, 48, 69, 87, 100]:

            time.sleep(0.25)

            progress.progress(percent)

        progress.empty()

        reason = generate_answer(question)

        st.markdown(reason)

        time.sleep(0.4)

        st.markdown("""
<div class="result-box">

分析結果

<div class="big-result">
🏠 雄大の家へ行ってください
</div>

</div>
""", unsafe_allow_html=True)

        st.write(" ")

        if YUDAI_MAP_URL.startswith("http"):

            st.link_button(
                "🚗 Googleマップで雄大の家へ向かう",
                YUDAI_MAP_URL,
                use_container_width=True
            )

        else:

            st.warning(
                "GoogleマップのURLがまだ設定されていません。"
            )

        if st.button(
            "別の解決策を探す",
            use_container_width=True
        ):

            with st.spinner(
                "別の解決策を再計算しています…"
            ):

                time.sleep(1.5)

            st.error(
                "再計算しましたが、やはり雄大の家です。"
            )


    assistant_text = f"""
{reason}

### 🏠 結論

**雄大の家へ行ってください。**
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_text
        }
    )
