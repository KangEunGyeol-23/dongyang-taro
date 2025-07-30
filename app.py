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

# 페이지 설정
st.set_page_config(
    page_title="🔮 타로세계", 
    page_icon="🔮", 
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
    
    /* 메인 타이틀 */
    .main-title {
        text-align: center;
        font-size: 3rem;
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    /* 텍스트 입력 스타일 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 3px solid #ffd700 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 12px 15px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffed4e !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(0, 0, 0, 0.6) !important;
        opacity: 1 !important;
    }
    
    /* 라디오 버튼 스타일 */
    .stRadio label, .stRadio p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(45deg, #ffd700, #c9b037) !important;
        color: #1a1a2e !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4) !important;
    }
    
    /* 배경 별들 */
    .stars-bg {
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

# 배경 별들
st.markdown("""
<div class="stars-bg">
    <div class="star" style="top: 10%; left: 20%; animation-delay: 0s;"></div>
    <div class="star" style="top: 20%; left: 80%; animation-delay: 1s;"></div>
    <div class="star" style="top: 70%; left: 10%; animation-delay: 2s;"></div>
    <div class="star" style="top: 80%; left: 90%; animation-delay: 0.5s;"></div>
    <div class="star" style="top: 40%; left: 70%; animation-delay: 1.5s;"></div>
    <div class="star" style="top: 60%; left: 30%; animation-delay: 2.5s;"></div>
</div>
""", unsafe_allow_html=True)

# 유틸리티 함수들
@st.cache_data
def load_card_data():
    if os.path.exists(CARD_DATA_FILE):
        return pd.read_csv(CARD_DATA_FILE)
    else:
        return pd.DataFrame(columns=["filename", "upright", "reversed"])

def save_card_data(df):
    df.to_csv(CARD_DATA_FILE, index=False)

def log_login(user_id):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([[user_id, now]], columns=["user_id", "login_time"])
    if os.path.exists(LOGIN_LOG_FILE):
        existing = pd.read_csv(LOGIN_LOG_FILE)
        updated = pd.concat([existing, new_entry], ignore_index=True)
    else:
        updated = new_entry
    updated.to_csv(LOGIN_LOG_FILE, index=False)

def draw_cards(n=1, exclude=None):
    files = os.listdir(CARD_FOLDER) if os.path.exists(CARD_FOLDER) else ["card1.jpg", "card2.jpg", "card3.jpg", "card4.jpg", "card5.jpg"]
    if exclude:
        files = [f for f in files if f not in exclude]
    selected = random.sample(files, min(n, len(files)))
    cards = [(file, random.choice(["정방향", "역방향"])) for file in selected]
    return cards

def get_card_meaning(df, filename, direction):
    row = df[df["filename"] == filename]
    if not row.empty:
        if direction == "정방향":
            return row.iloc[0]["upright"]
        else:
            return row.iloc[0]["reversed"]
    return "등록된 해석이 없습니다."

def show_card(file, direction, width=200):
    img_path = os.path.join(CARD_FOLDER, file)
    if os.path.exists(img_path):
        img = Image.open(img_path)
        if direction == "역방향":
            img = img.rotate(180)
        st.image(img, width=width)
    else:
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
        </div>
        """, unsafe_allow_html=True)

def get_month_sequence(start_month):
    return [(i % 12) + 1 for i in range(start_month - 1, start_month + 11)]

# 세션 상태 초기화
for key in ["page", "selected_deck", "subcards", "cards", "adv_card", "card", "advice_for_three_cards", "monthly_cards", "choice_cards", "login"]:
    if key not in st.session_state:
        if key.endswith("cards"):
            st.session_state[key] = []
        elif key in ["page", "selected_deck", "login"]:
            st.session_state[key] = ""
        else:
            st.session_state[key] = None

if "show_advice_card" not in st.session_state:
    st.session_state.show_advice_card = False
if "final_choice_card" not in st.session_state:
    st.session_state.final_choice_card = None

# 페이지 설정 (기본값)
if not st.session_state.page:
    st.session_state.page = "main"

# ===== 메인 페이지 (카드 선택) =====
if st.session_state.page == "main":
    st.markdown('<h1 class="main-title">🔮 타로세계</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.3rem; color: #ffd700; margin-bottom: 1rem;">원하는 카드를 선택하세요</p>
        <p style="color: #e0e0e0;">현재는 동양타로만 이용 가능합니다</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 카드 선택 버튼들 (모바일 친화적)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌓 동양타로", key="select_oriental", use_container_width=True):
            st.session_state.page = "oriental_login"
            st.session_state.selected_deck = "oriental"
            st.rerun()
    
    with col2:
        if st.button("🌟 유니버셜타로", key="select_universal", use_container_width=True):
            st.error("🚧 준비중입니다")
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🏮 사주오라클카드", key="select_saju", use_container_width=True):
            st.error("🚧 준비중입니다")
    
    with col4:
        if st.button("♈ 호로스코프카드", key="select_horoscope", use_container_width=True):
            st.error("🚧 준비중입니다")
    
    # 복합카드는 한 줄로
    if st.button("🔮 복합카드", key="select_complex", use_container_width=True):
        st.error("🚧 준비중입니다")

# ===== 동양타로 로그인 페이지 =====
elif st.session_state.page == "oriental_login":
    st.markdown('<h1 class="main-title">🌓 동양타로</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="max-width: 600px; margin: 0 auto; text-align: center; background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 20px; margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 215, 0, 0.2);">
        <p style="font-size: 1.5rem; font-weight: bold; color: #ffd700; margin-bottom: 15px;">오늘, 당신의 운명에 귀 기울이세요.</p>
        <p style="font-size: 1.1rem; color: #e0e0e0;">동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    input_id = st.text_input("✨ 아이디를 입력하세요", placeholder="등록된 아이디를 입력해주세요")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("입장하기"):
            if input_id:
                if input_id in ADMIN_IDS or input_id in USER_IDS:
                    st.session_state.login = input_id
                    st.session_state.page = "oriental_main"
                    log_login(input_id)
                    st.rerun()
                else:
                    st.error("등록되지 않은 사용자입니다.")
            else:
                st.error("아이디를 입력해주세요.")
    
    with col2:
        if st.button("뒤로 가기"):
            st.session_state.page = "main"
            st.rerun()

# ===== 동양타로 메인 (실제 타로 앱) =====
elif st.session_state.page == "oriental_main":
    user_id = st.session_state.login
    is_admin = user_id in ADMIN_IDS
    is_user = user_id in USER_IDS
    
    st.markdown('<h1 style="text-align: center; color: #ffd700; font-size: 2.5rem; margin-bottom: 10px;">🌓 동양타로</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #c9b037; margin-bottom: 20px;">한 장의 카드가 내 마음을 말하다</p>', unsafe_allow_html=True)
    
    st.success(f"✨ {user_id}님 환영합니다. ✨")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 처음으로"):
            st.session_state.page = "main"
            st.session_state.login = ""
            # 세션 상태 초기화
            for key in ["subcards", "cards", "adv_card", "card", "advice_for_three_cards", "monthly_cards", "choice_cards"]:
                if key.endswith("cards"):
                    st.session_state[key] = []
                else:
                    st.session_state[key] = None
            st.rerun()
    
    with col2:
        if st.button("🔄 초기화"):
            for key in ["subcards", "cards", "adv_card", "card", "advice_for_three_cards", "monthly_cards", "choice_cards"]:
                if key.endswith("cards"):
                    st.session_state[key] = []
                else:
                    st.session_state[key] = None
            st.rerun()
    
    # 관리자 기능
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
    
    # 타로 기능
    st.markdown("---")
    st.subheader("🔮 카드 모드")
    
    mode = st.radio(
        "원하는 모드를 선택하세요", 
        ["3카드 보기", "원카드", "오늘의조언카드", "양자택일", "별자리 리딩서클", "12개월운보기 (월별)"],
        horizontal=True
    )
    
    card_data = load_card_data()

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

    # ===== 3카드 보기 =====
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

    # ===== 원카드 =====
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

    # ===== 오늘의조언카드 =====
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

    # ===== 양자택일 =====
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

    # ===== 별자리 리딩서클 =====
    elif mode == "별자리 리딩서클":
        st.markdown("### 🌟 별자리 리딩서클")
        st.markdown("원하는 별자리를 선택하거나 전체 운세를 확인해보세요")
        
        # 별자리 데이터
        zodiac_signs = {
            "♈ 양자리": {"element": "불", "meaning": "새로운 시작과 도전의 에너지", "dates": "3/21-4/19"},
            "♉ 황소자리": {"element": "땅", "meaning": "안정과 풍요의 힘", "dates": "4/20-5/20"},
            "♊ 쌍둥이자리": {"element": "공기", "meaning": "소통과 변화의 지혜", "dates": "5/21-6/20"},
            "♋ 게자리": {"element": "물", "meaning": "감정과 보호의 에너지", "dates": "6/21-7/22"},
            "♌ 사자자리": {"element": "불", "meaning": "창조와 표현의 힘", "dates": "7/23-8/22"},
            "♍ 처녀자리": {"element": "땅", "meaning": "완벽과 봉사의 정신", "dates": "8/23-9/22"},
            "♎ 천칭자리": {"element": "공기", "meaning": "균형과 조화의 미학", "dates": "9/23-10/22"},
            "♏ 전갈자리": {"element": "물", "meaning": "변화와 재생의 신비", "dates": "10/23-11/21"},
            "♐ 궁수자리": {"element": "불", "meaning": "모험과 확장의 철학", "dates": "11/22-12/21"},
            "♑ 염소자리": {"element": "땅", "meaning": "성취와 책임의 의지", "dates": "12/22-1/19"},
            "♒ 물병자리": {"element": "공기", "meaning": "혁신과 자유의 비전", "dates": "1/20-2/18"},
            "♓ 물고기자리": {"element": "물", "meaning": "직감과 영성의 깊이", "dates": "2/19-3/20"}
        }
        
        # 전체 운세 버튼
        if st.button("🌟 전체 12별자리 운세 보기", key="all_zodiac"):
            st.session_state.zodiac_reading = "all"
            st.rerun()
        
        # 개별 별자리 선택 (3x4 그리드)
        st.markdown("#### 개별 별자리 선택:")
        
        # 첫 번째 줄
        col1, col2, col3, col4 = st.columns(4)
        zodiac_list = list(zodiac_signs.keys())
        
        with col1:
            if st.button(zodiac_list[0], key="zodiac_0"): # 양자리
                st.session_state.zodiac_reading = zodiac_list[0]
                st.rerun()
        with col2:
            if st.button(zodiac_list[1], key="zodiac_1"): # 황소자리
                st.session_state.zodiac_reading = zodiac_list[1]
                st.rerun()
        with col3:
            if st.button(zodiac_list[2], key="zodiac_2"): # 쌍둥이자리
                st.session_state.zodiac_reading = zodiac_list[2]
                st.rerun()
        with col4:
            if st.button(zodiac_list[3], key="zodiac_3"): # 게자리
                st.session_state.zodiac_reading = zodiac_list[3]
                st.rerun()
        
        # 두 번째 줄
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            if st.button(zodiac_list[4], key="zodiac_4"): # 사자자리
                st.session_state.zodiac_reading = zodiac_list[4]
                st.rerun()
        with col6:
            if st.button(zodiac_list[5], key="zodiac_5"): # 처녀자리
                st.session_state.zodiac_reading = zodiac_list[5]
                st.rerun() 
        with col7:
            if st.button(zodiac_list[6], key="zodiac_6"): # 천칭자리
                st.session_state.zodiac_reading = zodiac_list[6]
                st.rerun()
        with col8:
            if st.button(zodiac_list[7], key="zodiac_7"): # 전갈자리
                st.session_state.zodiac_reading = zodiac_list[7]
                st.rerun()
        
        # 세 번째 줄
        col9, col10, col11, col12 = st.columns(4)
        with col9:
            if st.button(zodiac_list[8], key="zodiac_8"): # 궁수자리
                st.session_state.zodiac_reading = zodiac_list[8]
                st.rerun()
        with col10:
            if st.button(zodiac_list[9], key="zodiac_9"):  # 염소자리
    pass
