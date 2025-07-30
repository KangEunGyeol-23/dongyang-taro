import streamlit as st
import random
import os
import pandas as pd
import datetime
from PIL import Image

# --- 설정 ---
ADMIN_IDS = ["cotty23"]
USER_IDS = ["cotty00", "teleecho", "37nim", "ckss12"]

CARD_FOLDER = "cards"
CARD_DATA_FILE = "card_data.csv"
LOGIN_LOG_FILE = "login_log.csv"

# 페이지 설정을 가장 먼저
st.set_page_config(
    page_title="🌓 동양타로", 
    page_icon="🌓", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 적용
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #0d1421, #1a1a2e, #16213e);
        color: white;
    }
    
    /* 메인 헤더 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 텍스트 입력 스타일 - 검정색 글씨 버전 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 3px solid #ffd700 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        backdrop-filter: blur(5px);
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 12px 15px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffed4e !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8) !important;
        background: rgba(255, 255, 255, 1) !important;
        color: #000000 !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.6) !important;
        opacity: 1 !important;
        font-weight: normal !important;
    }
    
    /* 라디오 버튼 텍스트만 선명하게 */
    .stRadio label {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8) !important;
    }
    
    .stRadio p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(45deg, #ffd700, #c9b037);
        color: #1a1a2e;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
        background: linear-gradient(45deg, #ffed4e, #ffd700);
    }
    
    /* 배경 별들 효과 */
    .stars-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .star {
        position: absolute;
        width: 2px;
        height: 2px;
        background: #ffd700;
        border-radius: 50%;
        animation: twinkle 3s infinite alternate;
    }
    
    @keyframes twinkle {
        0% { opacity: 0.3; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# 배경 별들 생성
st.markdown("""
<div class="stars-background">
    <div class="star" style="top: 10%; left: 20%; animation-delay: 0s;"></div>
    <div class="star" style="top: 20%; left: 80%; animation-delay: 1s;"></div>
    <div class="star" style="top: 70%; left: 10%; animation-delay: 2s;"></div>
    <div class="star" style="top: 80%; left: 90%; animation-delay: 0.5s;"></div>
    <div class="star" style="top: 40%; left: 70%; animation-delay: 1.5s;"></div>
    <div class="star" style="top: 60%; left: 30%; animation-delay: 2.5s;"></div>
    <div class="star" style="top: 30%; left: 50%; animation-delay: 0.8s;"></div>
    <div class="star" style="top: 90%; left: 60%; animation-delay: 1.8s;"></div>
    <div class="star" style="top: 15%; left: 40%; animation-delay: 2.2s;"></div>
    <div class="star" style="top: 85%; left: 25%; animation-delay: 1.2s;"></div>
</div>
""", unsafe_allow_html=True)

# 카드 데이터 불러오기
@st.cache_data
def load_card_data():
    if os.path.exists(CARD_DATA_FILE):
        return pd.read_csv(CARD_DATA_FILE)
    else:
        return pd.DataFrame(columns=["filename", "upright", "reversed"])

# 카드 데이터 저장하기
def save_card_data(df):
    df.to_csv(CARD_DATA_FILE, index=False)

# 로그인 로그 저장
def log_login(user_id):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[user_id, now]], columns=["user_id", "login_time"])
    if os.path.exists(LOGIN_LOG_FILE):
        existing = pd.read_csv(LOGIN_LOG_FILE)
        updated = pd.concat([existing, new_entry], ignore_index=True)
    else:
        updated = new_entry
    updated.to_csv(LOGIN_LOG_FILE, index=False)

# 카드 뽑기 함수 (중복 제외)
def draw_cards(n=1, exclude=None):
    files = os.listdir(CARD_FOLDER)
    if exclude:
        files = [f for f in files if f not in exclude]
    selected = random.sample(files, min(n, len(files)))
    cards = [(file, random.choice(["정방향", "역방향"])) for file in selected]
    return cards

# 카드 해석 가져오기
def get_card_meaning(df, filename, direction):
    row = df[df["filename"] == filename]
    if not row.empty:
        if direction == "정방향":
            return row.iloc[0]["upright"]
        else:
            return row.iloc[0]["reversed"]
    return "등록된 해석이 없습니다."

# 카드 이미지 표시 (개선된 버전)
def show_card(file, direction, width=200):
    img_path = os.path.join(CARD_FOLDER, file)
    if os.path.exists(img_path):
        img = Image.open(img_path)
        if direction == "역방향":
            img = img.rotate(180)
        st.image(img, width=width)
    else:
        # 카드 이미지가 없을 때 별자리 패턴 표시
        st.markdown(f"""
        <div style="
            width: {width}px; 
            height: {int(width*1.5)}px; 
            background: linear-gradient(45deg, #0d1421, #1a1a2e); 
            border: 3px solid #ffd700; 
            border-radius: 15px; 
            position: relative;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: #ffd700;
            box-shadow: 0 10px 30px rgba(255, 215, 0, 0.2);
        ">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🌟</div>
                <div>{file}</div>
                <div style="font-size: 0.9rem; margin-top: 5px;">{direction}</div>
            </div>
            <div style="position: absolute; top: 20%; left: 15%; width: 3px; height: 3px; background: #ffd700; border-radius: 50%; animation: twinkle 2s infinite alternate;"></div>
            <div style="position: absolute; top: 30%; right: 20%; width: 2px; height: 2px; background: #ffd700; border-radius: 50%; animation: twinkle 2s infinite alternate 0.5s;"></div>
            <div style="position: absolute; bottom: 30%; left: 25%; width: 2px; height: 2px; background: #ffd700; border-radius: 50%; animation: twinkle 2s infinite alternate 1s;"></div>
            <div style="position: absolute; bottom: 20%; right: 15%; width: 3px; height: 3px; background: #ffd700; border-radius: 50%; animation: twinkle 2s infinite alternate 1.5s;"></div>
        </div>
        """, unsafe_allow_html=True)

# 월 리스트 순환 함수
def get_month_sequence(start_month):
    return [(i % 12) + 1 for i in range(start_month - 1, start_month + 11)]

# 초기 세션 상태 설정
for key in ["subcards", "subcard_used", "cards", "adv_card", "card", "advice_for_three_cards", "monthly_cards", "choice_cards"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key.endswith("cards") else None
if "login" not in st.session_state:
    st.session_state.login = ""
if "show_advice_card" not in st.session_state:
    st.session_state.show_advice_card = False
if "final_choice_card" not in st.session_state:
    st.session_state.final_choice_card = None

# 로그인 화면
if not st.session_state.login:
    st.markdown('<h1 style="text-align: center; color: #ffd700; font-size: 3rem; margin-bottom: 2rem;">🌓 동양타로</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="max-width: 600px; margin: 0 auto; text-align: center; background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 20px; margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 215, 0, 0.2);">
        <p style="font-size: 1.5rem; font-weight: bold; color: #ffd700; margin-bottom: 15px; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);">오늘, 당신의 운명에 귀 기울이세요.</p>
        <p style="font-size: 1.1rem; margin-bottom: 10px; color: #e0e0e0;">동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.</p>
        <p style="font-size: 1.1rem; margin-bottom: 10px; color: #e0e0e0;">사랑, 직업, 재물 등 모든 고민에 대한 당신만의 길을 지금 바로 동양 타로에서 찾아보세요.</p>
        <p style="font-size: 1.1rem; color: #e0e0e0;">숨겨진 운명의 실타래를 풀어내고, 더 나은 내일을 위한 지혜를 얻을 시간입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    input_id = st.text_input("✨ 아이디를 입력하세요", placeholder="등록된 아이디를 입력해주세요")
    
    if input_id:
        st.session_state.login = input_id
        log_login(input_id)
        st.rerun()
    st.stop()

user_id = st.session_state.login
is_admin = user_id in ADMIN_IDS
is_user = user_id in USER_IDS

if not (is_admin or is_user):
    st.error("🚫 등록되지 않은 사용자입니다.")
    st.stop()

# 메인 화면
st.markdown('<h1 style="text-align: center; color: #ffd700; font-size: 2.5rem; margin-bottom: 10px;">🌓 동양타로</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #c9b037; margin-bottom: 20px;">한 장의 카드가 내 마음을 말하다</p>', unsafe_allow_html=True)

st.success(f"✨ {user_id}님 환영합니다. ✨")

if st.button("🏠 처음으로", key="home_button"):
    user_id_temp = user_id
    st.session_state.clear()
    st.session_state.login = user_id_temp
    st.rerun()

# 관리자 로그인 기록 확인
if is_admin:
    st.markdown("---")
    st.subheader("📜 로그인 기록 관리 (관리자 전용)")
    if os.path.exists(LOGIN_LOG_FILE):
        df_log = pd.read_csv(LOGIN_LOG_FILE)
        st.dataframe(df_log.tail(20), use_container_width=True)
        if st.button("🗑️ 로그인 기록 초기화"):
            os.remove(LOGIN_LOG_FILE)
            st.success("✅ 로그인 기록이 초기화되었습니다.")
    else:
        st.info("📝 아직 로그인 기록이 없습니다.")

# 공통 카드 기능 모드
if is_user or is_admin:
    st.markdown("---")
    st.subheader("🔮 카드 모드")
    
    mode = st.radio(
        "원하는 모드를 선택하세요", 
        ["3카드 보기", "원카드", "오늘의조언카드", "양자택일", "12개월운보기 (월별)"],
        horizontal=True
    )
    
    card_data = load_card_data()

    # 보조카드 표시 함수
    def handle_subcard(file, exclude):
        if file in st.session_state.subcards:
            sub_file, sub_dir = st.session_state.subcards[file]
            st.markdown("### 🔁 보조카드")
            show_card(sub_file, sub_dir, width=150)
            st.markdown(f"**{sub_dir}**: {get_card_meaning(card_data, sub_file, sub_dir)}")
        else:
            if st.button("🔁 보조카드 보기", key=f"subcard_btn_{file}"):
                subcard = draw_cards(1, exclude=exclude + list(st.session_state.subcards.keys()))[0]
                st.session_state.subcards[file] = subcard
                st.rerun()

    # 안내 메시지
    if not any([st.session_state.cards, st.session_state.card, st.session_state.adv_card, st.session_state.choice_cards, st.session_state.monthly_cards]):
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.05); border-radius: 20px; border: 1px solid rgba(255, 215, 0, 0.2);">
            <p style="color: #ffd700; font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">💫 질문을 마음속으로 떠올려보세요</p>
            <p style="color: #e0e0e0; font-size: 1.1rem; margin-bottom: 1.5rem;">궁금한 것을 생각하며 카드를 뽑아보세요</p>
            <div style="font-size: 2rem; opacity: 0.4;">🌟✨🔮✨🌟</div>
        </div>
        """, unsafe_allow_html=True)

    if mode == "3카드 보기":
        if st.button("🔮 3장 뽑기", key="draw_three"):
            st.session_state.cards = draw_cards(3)
            st.session_state.subcards = {}
            st.session_state.advice_for_three_cards = None

        if st.session_state.cards:
            cols = st.columns(3)
            selected_files = [f for f, _ in st.session_state.cards]
            for i, (file, direction) in enumerate(st.session_state.cards):
                with cols[i]:
                    show_card(file, direction)
                    st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")
                    if direction == "역방향":
                        handle_subcard(file, exclude=selected_files)

            if st.button("🌟 조언카드 보기"):
                st.session_state.advice_for_three_cards = draw_cards(1, exclude=selected_files)[0]
                st.rerun()

            if st.session_state.advice_for_three_cards:
                st.markdown("---")
                st.markdown("### 🧭 3카드에 대한 조언")
                file, direction = st.session_state.advice_for_three_cards
                show_card(file, direction, width=300)
                st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")

    elif mode == "원카드":
        if st.button("✨ 한 장 뽑기", key="draw_one"):
            st.session_state.card = draw_cards(1)[0]
            st.session_state.subcards = {}

        if st.session_state.card:
            file, direction = st.session_state.card
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                show_card(file, direction, width=300)
                st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")
                if direction == "역방향":
                    handle_subcard(file, exclude=[file])

    elif mode == "오늘의조언카드":
        if st.button("🌿 오늘의 조언카드", key="draw_advice"):
            st.session_state.adv_card = draw_cards(1)[0]
            st.session_state.subcards = {}

        if st.session_state.adv_card:
            file, direction = st.session_state.adv_card
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                show_card(file, direction, width=300)
                st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")
                if direction == "역방향":
                    handle_subcard(file, exclude=[file])

    elif mode == "양자택일":
        col1, col2 = st.columns(2)
        with col1:
            q1 = st.text_input("선택1 질문 입력", key="q1", placeholder="첫 번째 선택지를 입력하세요")
        with col2:
            q2 = st.text_input("선택2 질문 입력", key="q2", placeholder="두 번째 선택지를 입력하세요")

        if q1 and q2:
            if st.button("🔍 선택별 카드 뽑기"):
                st.session_state.choice_cards = draw_cards(2)

        if st.session_state.choice_cards:
            cols = st.columns(2)
            selected_files = [f for f, _ in st.session_state.choice_cards]
            for i, (file, direction) in enumerate(st.session_state.choice_cards):
                with cols[i]:
                    st.markdown(f"**선택{i+1}**: {q1 if i == 0 else q2}")
                    show_card(file, direction, width=200)
                    st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")

        if q1 and q2:
            if st.button("🧭 최종 결론 카드 보기"):
                used = [f for f, _ in st.session_state.choice_cards] if st.session_state.choice_cards else []
                st.session_state.final_choice_card = draw_cards(1, exclude=used)[0]
                st.rerun()

        if st.session_state.final_choice_card:
            file, direction = st.session_state.final_choice_card
            st.markdown("---")
            st.markdown("### 🏁 최종 결론 카드")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                show_card(file, direction, width=300)
                st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")

    elif mode == "12개월운보기 (월별)":
        selected_month = st.selectbox("현재 월을 선택하세요", list(range(1, 13)), index=datetime.datetime.now().month-1)
        if st.button("🗓️ 12개월 운세 보기"):
            st.session_state.monthly_cards = draw_cards(12)

        if st.session_state.monthly_cards:
            month_sequence = get_month_sequence(selected_month)
            cols = st.columns(3)
            for i, (file, direction) in enumerate(st.session_state.monthly_cards):
                col = cols[i % 3]
                with col:
                    st.markdown(f"**📅 {month_sequence[i]}월**")
                    show_card(file, direction, width=180)
                    st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")
                    if direction == "역방향":
                        handle_subcard(file, exclude=[f for f, _ in st.session_state.monthly_cards])
                
                if (i + 1) % 3 == 0:
                    st.markdown("<br>", unsafe_allow_html=True)
