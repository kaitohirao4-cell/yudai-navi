import streamlit as st
import time
import random
import urllib.parse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from streamlit_geolocation import streamlit_geolocation


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="YUDAI NAVI",
    layout="centered"
)


# ============================================================
# SETTINGS
# ============================================================

# 雄大の家はStreamlit Secretsから取得
YUDAI_HOME_ADDRESS = st.secrets["YUDAI_HOME_ADDRESS"]

# 学習院大学 目白キャンパス
GAKUSHUIN_NAME = "学習院大学"
GAKUSHUIN_ADDRESS = "東京都豊島区目白1丁目5-1"


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
<style>

.block-container {
    max-width: 820px;
    padding-top: 3rem;
    padding-bottom: 5rem;
}

.main-title {
    font-size: 44px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 2px;
}

.main-subtitle {
    color: #777;
    font-size: 15px;
    margin-bottom: 32px;
}

.section-label {
    font-size: 13px;
    color: #777;
    letter-spacing: 1.2px;
    margin-top: 20px;
    margin-bottom: 5px;
}

.analysis-box {
    border: 1px solid #dedede;
    border-radius: 15px;
    padding: 20px;
    margin-top: 15px;
    margin-bottom: 15px;
}

.final-box {
    border: 2px solid #222;
    border-radius: 18px;
    padding: 28px 20px;
    margin-top: 25px;
    margin-bottom: 20px;
    text-align: center;
}

.final-caption {
    color: #777;
    font-size: 12px;
    letter-spacing: 1px;
}

.final-answer {
    font-weight: 800;
    font-size: 31px;
    margin-top: 8px;
}

.system-box {
    border-left: 4px solid #333;
    padding: 13px 16px;
    background: #f7f7f7;
    margin-top: 18px;
    margin-bottom: 18px;
}

.micro {
    font-size: 12px;
    color: #888;
}

div[data-testid="stMetric"] {
    border: 1px solid #e5e5e5;
    padding: 14px;
    border-radius: 12px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="main-title">
YUDAI NAVI
</div>

<div class="main-subtitle">
人生に迷ったとき、行き先だけは迷わせない。
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# GEOCODING
# ============================================================

@st.cache_data(show_spinner=False)
def geocode_address(address):

    try:

        geolocator = Nominatim(
            user_agent="yudai_navi_v3"
        )

        location = geolocator.geocode(
            address,
            timeout=10
        )

        if location:

            return (
                location.latitude,
                location.longitude
            )

    except Exception:
        pass

    return None, None


YUDAI_LAT, YUDAI_LON = geocode_address(
    YUDAI_HOME_ADDRESS
)

GAKUSHUIN_LAT, GAKUSHUIN_LON = geocode_address(
    GAKUSHUIN_ADDRESS
)

# 学習院のジオコーディング失敗時用
if GAKUSHUIN_LAT is None:
    GAKUSHUIN_LAT = 35.7180
    GAKUSHUIN_LON = 139.7060


# ============================================================
# GOOGLE MAPS
# ============================================================

def google_maps_route(address, mode="transit"):

    destination = urllib.parse.quote(address)

    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&destination={destination}"
        f"&travelmode={mode}"
    )


# ============================================================
# TEXT ANALYSIS
# ============================================================

CATEGORY_KEYWORDS = {

    "仕事・労働": [
        "仕事",
        "会社",
        "上司",
        "部下",
        "客先",
        "出社",
        "残業",
        "転職",
        "辞めたい",
        "退職",
        "会議",
        "働きたくない",
        "行きたくない"
    ],

    "恋愛・人間関係": [
        "彼女",
        "彼氏",
        "好き",
        "恋愛",
        "別れ",
        "振ら",
        "既読",
        "未読",
        "デート",
        "喧嘩",
        "友達",
        "嫌われ",
        "返信"
    ],

    "食事": [
        "腹減",
        "お腹",
        "ご飯",
        "飯",
        "食べたい",
        "ラーメン",
        "寿司",
        "焼肉",
        "飲みたい"
    ],

    "疲労・睡眠": [
        "眠い",
        "寝たい",
        "疲れ",
        "だるい",
        "しんどい",
        "休みたい",
        "眠れない"
    ],

    "金銭・投資": [
        "株",
        "投資",
        "NISA",
        "配当",
        "含み損",
        "含み益",
        "お金",
        "金",
        "貯金",
        "仮想通貨",
        "ビットコイン"
    ],

    "学業・知性": [
        "大学",
        "学校",
        "勉強",
        "試験",
        "テスト",
        "レポート",
        "課題",
        "頭良く",
        "学習院"
    ],

    "暇": [
        "暇",
        "ひま",
        "退屈",
        "やることない",
        "何しよう"
    ],

    "人生・将来": [
        "人生",
        "将来",
        "不安",
        "どうしよう",
        "悩み",
        "迷って",
        "生き方"
    ],

    "移動・外出": [
        "どこ行く",
        "どこいく",
        "遊び",
        "出かけ",
        "暇だから",
        "場所"
    ]
}


def detect_category(text):

    result = {}

    for category, keywords in CATEGORY_KEYWORDS.items():

        score = sum(
            1
            for keyword in keywords
            if keyword in text
        )

        result[category] = score

    best = max(
        result,
        key=result.get
    )

    if result[best] == 0:
        return "分類不能・高度な相談"

    return best


# ============================================================
# SPECIAL INPUT DETECTION
# ============================================================

def detect_special_case(text):

    if (
        "雄大の家に行きたくない" in text
        or "雄大の家はいかない" in text
        or "雄大の家は行かない" in text
        or "雄大に会いたくない" in text
    ):
        return "refusal"

    if (
        "本当に" in text
        or "ほんとに" in text
        or "マジ" in text
        or "まじ" in text
    ):
        return "doubt"

    if (
        "他" in text
        and (
            "方法" in text
            or "選択肢" in text
            or "場所" in text
        )
    ):
        return "alternative"

    if "なぜ" in text or "なんで" in text:
        return "why"

    if "雄大" in text:
        return "yudai"

    return None


# ============================================================
# NORMAL ADVICE
# ============================================================

def get_normal_advice(category):

    answers = {

        "仕事・労働":
        "一般的には、問題を仕事内容、人間関係、疲労、待遇に分け、"
        "今日中に大きな結論を出さず整理するのが妥当です。",

        "恋愛・人間関係":
        "感情が大きく動いている場合は、すぐ追加連絡をせず、"
        "自分が何を求めているのかを整理するのが一般的です。",

        "食事":
        "空腹時は集中力や判断力が落ちることがあります。"
        "一般的にはまず食事を取るのが合理的です。",

        "疲労・睡眠":
        "疲れている状態では重要な判断を避け、"
        "睡眠や休息を優先するのが一般的です。",

        "金銭・投資":
        "一般的には、期待リターンだけでなくリスク、期間、"
        "資金余力を分けて考える必要があります。",

        "学業・知性":
        "問題を小さな作業に分け、優先順位を付けて"
        "一つずつ進めるのが一般的です。",

        "暇":
        "運動、散歩、友人との予定、新しい場所への外出などが"
        "一般的な選択肢になります。",

        "人生・将来":
        "今日変えられることと長期的に考えることを分けて、"
        "一つずつ整理するのが一般的です。",

        "移動・外出":
        "目的、予算、移動時間、天候などを比較して"
        "行き先を決めるのが一般的です。",

        "分類不能・高度な相談":
        "追加情報を集め、まず問題そのものを具体化するのが一般的です。"
    }

    return answers[category]


# ============================================================
# YUDAI REASON
# ============================================================

def get_yudai_reason(category):

    options = {

        "仕事・労働": [
            "退職、休暇、転職、上司への相談を比較しました。いずれも雄大の家へ行った後でも実行できます。",
            "勤務先に問題がある可能性があります。しかし現在地が雄大の家ではないことも重要な観測結果です。",
            "仕事上の問題と認識しましたが、YUDAI NAVIは職場より雄大へのアクセスを優先しました。"
        ],

        "恋愛・人間関係": [
            "追加メッセージを送る前に移動してください。現在もっとも不足している変数は雄大です。",
            "人間関係の問題を検出しました。第三者として雄大を投入すると状況がさらに複雑になる可能性があります。",
            "恋愛問題の原因は特定できませんでしたが、雄大の家にいないことだけは確認できました。"
        ],

        "食事": [
            "冷蔵庫の中身は確認できません。しかし雄大の家に何か存在する可能性を採択しました。",
            "一般的には飲食店を検索しますが、本システムでは雄大宅が検索結果を独占しています。",
            "栄養学的根拠は確認できませんでしたが、目的地として雄大の家が残りました。"
        ],

        "疲労・睡眠": [
            "疲労時は複雑な意思決定を避けるべきです。そのため目的地を一つに絞りました。",
            "自宅へ帰るという強力な候補も検証しましたが、YUDAI NAVI審査部門が却下しました。",
            "判断能力低下の可能性があります。本システムが代わりに目的地を決定しました。"
        ],

        "金銭・投資": [
            "期待リターン、リスク、流動性を比較しましたが、なぜか雄大の家だけ残りました。",
            "投資判断には慎重さが必要です。一方、雄大宅への移動判断にはそこまで必要ありません。",
            "資産ポートフォリオより先に、現在地ポートフォリオの修正が必要と判定されました。"
        ],

        "学業・知性": [
            "知的問題のため学習院大学を有力候補として検証しましたが、最終目的地には選定されませんでした。",
            "学習院大学経由案も評価しました。しかし雄大本人へのアクセスがより重要と仮定されました。",
            "学術的には学習院大学、YUDAI NAVI的には雄大の家という結果です。"
        ],

        "暇": [
            "暇であるという事実は、雄大宅へ移動する時間が存在することを意味します。",
            "予定がない状態は、雄大訪問アルゴリズムにおいて非常に高く評価されます。",
            "暇という問題は解決可能です。雄大が在宅しているかどうかは本システムの管轄外です。"
        ],

        "人生・将来": [
            "人生全体を最適化することは困難ですが、次の目的地だけなら決定できます。",
            "長期的な答えは算出できませんでした。しかし短期的な目的地は特定されました。",
            "人生の方向性は不明ですが、移動方向だけは確定しました。"
        ],

        "移動・外出": [
            "外出先を比較する問題として非常に相性の良い入力です。そして比較は一瞬で終了しました。",
            "複数地点を候補に追加しましたが、雄大の家以外は内部ランキングから消失しました。",
            "目的地選定エンジンが正常に作動しています。結果は予想通りです。"
        ],

        "分類不能・高度な相談": [
            "入力内容の完全な理解には失敗しました。しかし目的地計算モジュールは正常です。",
            "解析不能な要素が存在します。安全策として雄大の家が採択されました。",
            "内容理解の信頼度は低いですが、目的地判定の自信だけは異常に高い状態です。"
        ]
    }

    return random.choice(
        options[category]
    )


# ============================================================
# DISTANCE COMMENT
# ============================================================

def distance_comment(distance):

    if distance < 0.2:

        return (
            "ほぼ到着しています。"
            "ここまで来て目的地を変更する合理性は確認できません。"
        )

    elif distance < 1:

        return (
            "雄大圏内です。"
            "徒歩での最終接近フェーズに移行できます。"
        )

    elif distance < 3:

        return (
