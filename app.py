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
    .stApp {
        background: linear-gradient(135deg, #0d1421, #1a1a2e, #16213e);
        color: white;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 3px solid #ffd700 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        padding: 12px 15px !important;
    }
    
    .stRadio label, .stRadio p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8) !important;
    }
    
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
    
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 3px solid #ffd700 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 3px solid #ffd700 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-family: monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# 백초귀장술 데이터
def get_guijang_data():
    return [
        ['子日', '사살신', '합식', '기러기', '공망신', '약일충', '원진록', '해결신', '퇴식', '금조건', '백병주', '강일진', '천록'],
        ['丑日', '천록', '사살신', '합식', '기러기', '공망신', '약일충', '원진록', '해결신', '퇴식', '금조건', '백병주', '강일진'],
        ['寅日', '강일진', '천록', '사살신', '합식', '기러기', '공망신', '약일충', '원진록', '해결신', '퇴식', '금조건', '백병주'],
        ['卯日', '백병주', '강일진', '천록', '사살신', '합식', '기러기', '공망신', '약일충', '원진록', '해결신', '퇴식', '금조건'],
        ['辰日', '금조건', '백병주', '강일진', '천록', '사살신', '합식', '기러기', '공망신', '약일충', '원진록', '해결신', '퇴식'],
        ['巳日', '퇴식', '금조건', '백병주', '강일진', '천록', '사살신', '합식', '기러기', '공망신', '약일충', '원진록', '해결신'],
        ['午日', '해결신', '퇴식', '금조건', '백병주', '강일진', '천록', '사살신', '합식', '기러기', '공망신', '약일충', '원진록'],
        ['未日', '원진록', '해결신', '퇴식', '금조건', '백병주', '강일진', '천록', '사살신', '합식', '기러기', '공망신', '약일충'],
        ['申日', '약일충', '원진록', '해결신', '퇴식', '금조건', '백병주', '강일진', '천록', '사살신', '합식', '기러기', '공망신'],
        ['酉日', '공망신', '약일충', '원진록', '해결신', '퇴식', '금조건', '백병주', '강일진', '천록', '사살신', '합식', '기러기'],
        ['戌日', '기러기', '공망신', '약일충', '원진록', '해결신', '퇴식', '금조건', '백병주', '강일진', '천록', '사살신', '합식'],
        ['亥日', '합식', '기러기', '공망신', '약일충', '원진록', '해결신', '퇴식', '금조건', '백병주', '강일진', '천록', '사살신']
    ]

def get_guijang_interpretations():
    return {
        '퇴식': '자리에 있으니 관재구설과 여자를 조심해야 하며 매사가 하기 싫다. 질병을 얻게 되거나 하는 일마다 신통치가 않아 의욕도 없고 귀찮고 기분은 완전히 바닥이다. 이런 달에는 시험이나 취업을 하려하면 하는 일마다 잘 되지도 않는다. 억지스럽게 일을 성사시켰다면 후에 낭패를 보게 되고 여자가 끼어 있으면 더욱 불리한 달이니 조심해야 하는 달이다. 좋은 일보다 나쁜 일이 더 많은 달이니 조심해야 하는 달이다.',
        '금조건': '의 자리에 있으니 소득이 있는 달이다. 귀인이 도와서 일도 잘 풀리고 금전적 여유도 생기겠다. 장사하는 사람이라면 그동안 못 받았던 미수금이 있다면 이 달에 받을 수 있다.',
        '백병주': '의 자리이다. 힘든 달이 되겠다. 이달에는 건강까지 악화되어 병원 출입을 하게 된다. 지긋지긋하게 일이 꼬이고 시비구설을 조심해야 하고 중상모략이 있을 수 있는 매우 않 좋은 달이니 조심해야 하는 달이다.',
        '강일진': ' 달이다. 이달에는 기획했던 일이나 동업, 사업관계가 순조롭게 진행되는 달이다. 외향적으로 될 것도 같고 아닌 것도 같아 두 마음이다. 결정해야 될 문제가 있는 달이다. 하는 것이 더 유리하다. 운이 상승하는 달이다. 건강상태도 좋고 좋은 매물이나 물건도 나타나는 달이다. 새로운 일을 추진해도 괜찮은 달이다.',
        '천록': ' 자리다. 이달에는 희망이 상승하는 운이라서 마음만 바쁘고 새로운 일을 시작하고 싶은 충동 때문에 의욕 과다로 무조건 밀어 붙이게 된다. 시작은 좋은데 뒤에 스트레스 좀 받는다. 아랫사람의 하극상 입신사(立身事) 문제로 정신적인 괴로움이 발생해서 스트레스가 심한 달이 된다. 하지만 치고 빠지는 승부사는 결과가 좋다.',
        '사살신': ' 자리이다. 이 상담자 본인은 능력이 마비되어 하는 일마다 일이 꼬이고 시비 구설을 조심해야 하고 놀라고 의혹스런 일이나 돌발 사고가 발생할 수 있는 매우 않 좋은 달이니 조심해야 하는 달이다. 초상집에 갈 일이 생겨도 가지 말아야 한다.',
        '합식': '자리에 해당한다. 식구가 늘던가 문서가 들어오는 좋은 달이 된다. 이런 달에는 결혼하던가, 약혼, 맞선, 계약체결, 취임식, 약속, 이력서 제출, 문서 구입, 면접, 합의, 경조사 등을 행하면 아주 길(吉)하다.',
        '기러기': ' 달이다. 이동수가 있는 달이다. 지금 있는 자리에서 움직여야 된다. 이사를 하던지 여행을 떠날 수 있다. 하지만 일에 성과는 별로 없다. 모두 날아가 버릴 것이다.',
        '공망신': '의 달로 헛수고 하는 달이다. 계획한 일이 있다면 무산이 되고 바람을 맞게 된다. 만약에 이런 달에 약혼, 계약체결, 취임식, 이력서 제출, 문서 구입, 맞선, 면접, 경조사를 행하게 된다면 허사로 돌아갈 확률이 높고 만일 일이 성사 된다고 해도 반드시 뒷 탈이 생기게 되고 실망이 크게 된다. 노력해도 잘 안되는 달이다.',
        '약일충': '의 달로 좌불안석으로 마음이 붕 떠서 헤매는 달이다. 터 부정이 나서 이동, 변동할 일도 생기면 우왕좌왕 하면서 움직이는 때로 손재수가 생기는 달을 보내게 된다. 맥이 빠지는 달이다.',
        '원진록': '의 달이다. 매사 일이 성사되기 어렵고 방해자가 생겨서 일이 지체가 되고 주변 사람과 원수 관계가 되니 본인이 한발 물러서게 되고 일이 진행이 안되고 지체되는 달이다.',
        '해결신': '의 달이다. 지금까지 답답했던 일들이 해결되는 달이다. 본인이 이리저리 뛰어다니며 해결해야 하기 때문에 바쁜 달이다. 하지만 하고 싶은 일은 귀인이 나타나서 해결을 해주니 성과가 있어 기쁜 달이기도 한다.'
    }

def get_time_to_month():
    return {
        '寅': 1, '卯': 2, '辰': 3, '巳': 4, '午': 5, '未': 6,
        '申': 7, '酉': 8, '戌': 9, '亥': 10, '子': 11, '丑': 12
    }

def display_guijang_table():
    table_data = get_guijang_data()
    time_columns = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
    
    df_data = []
    for row in table_data:
        df_data.append(row)
    
    df = pd.DataFrame(df_data, columns=['날짜'] + time_columns)
    
    def color_cells(val):
        if val == '사살신':
            return 'background-color: #ffcdd2; color: #d32f2f; font-weight: bold; text-align: center;'
        elif val in ['합식', '강일진', '해결신', '금조건']:
            return 'background-color: #e1f5fe; color: #1976d2; font-weight: bold; text-align: center;'
        elif val in ['子日', '丑日', '寅日', '卯日', '辰日', '巳日', '午日', '未日', '申日', '酉日', '戌日', '亥日']:
            return 'background-color: #f5f5f5; color: #333; font-weight: bold; text-align: center;'
        else:
            return 'background-color: #fafafa; color: #666; text-align: center;'
    
    styled_df = df.style.applymap(color_cells).set_properties(**{
        'border': '1px solid #ddd',
        'font-size': '12px',
        'padding': '8px'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#ffd700'), ('color', '#333'), ('font-weight', 'bold'), ('text-align', 'center'), ('border', '1px solid #ddd')]},
        {'selector': 'td', 'props': [('border', '1px solid #ddd')]},
        {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]}
    ])
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

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

# 메인 페이지
if st.session_state.page == "main":
    st.markdown('<h1 class="main-title">🔮 타로세계</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.3rem; color: #ffd700; margin-bottom: 1rem;">원하는 카드를 선택하세요</p>
        <p style="color: #e0e0e0;">현재는 동양타로와 백초귀장술이 이용 가능합니다</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        if st.button("♈ 칼라타로", key="select_horoscope", use_container_width=True):
            st.error("🚧 준비중입니다")
    
    if st.button("🔮 백초귀장술", key="select_guijang", use_container_width=True):
        st.session_state.page = "guijang_login"
        st.rerun()

# 백초귀장술 로그인 페이지
elif st.session_state.page == "guijang_login":
    st.markdown('<h1 class="main-title">🔮 백초귀장술</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="max-width: 600px; margin: 0 auto; text-align: center; background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 20px; margin-bottom: 30px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 215, 0, 0.2);">
        <p style="font-size: 1.5rem; font-weight: bold; color: #ffd700; margin-bottom: 15px;">무조건 일진을 기준!!</p>
        <p style="font-size: 1.1rem; color: #e0e0e0;">동양의 오랜 지혜가 담긴 백초귀장술이 당신의 운명을 밝혀드립니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    input_id = st.text_input("✨ 아이디를 입력하세요", placeholder="등록된 아이디를 입력해주세요")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("입장하기"):
            if input_id:
                if input_id in ADMIN_IDS or input_id in USER_IDS:
                    st.session_state.login = input_id
                    st.session_state.page = "guijang_main"
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

# 백초귀장술 메인 페이지
elif st.session_state.page == "guijang_main":
    user_id = st.session_state.login
    is_admin = user_id in ADMIN_IDS
    is_user = user_id in USER_IDS
    
    st.markdown('<h1 style="text-align: center; color: #ffd700; font-size: 2.5rem; margin-bottom: 10px;">🔮 백초귀장술</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #c9b037; margin-bottom: 20px;">무조건 일진을 기준!!</p>', unsafe_allow_html=True)
    
    st.success(f"✨ {user_id}님 환영합니다. ✨")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 처음으로"):
            st.session_state.page = "main"
            st.session_state.login = ""
            st.rerun()
    
    with col2:
        if st.button("🔄 초기화"):
            if hasattr(st.session_state, 'show_guijang_result'):
                st.session_state.show_guijang_result = False
            st.rerun()
    
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
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <h3 style="color: #ffd700; margin-bottom: 10px;">📅 백초귀장술표</h3>
        <p style="color: #e0e0e0; font-size: 1.1rem;">아래 버튼을 클릭하여 표와 사용법을 확인하세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 📊 백초귀장술표 보기 & 사용법 (클릭하여 펼치기)", expanded=False):
        st.markdown("""
        ### 📖 백초귀장술표 사용법
        
        **🔍 표 읽는 방법:**
        - **세로축(행)**: 날짜 (子日, 丑日, 寅日... 亥日)
        - **가로축(열)**: 시간 (寅, 卯, 辰... 丑시)
        - **사용 예시**: 巳日(사일)의 寅시(인시) → 퇴식 → 음력 1월
        
        **🎨 색상 구분:**
        - 🔴 **빨간색**: 사살신 (흉한 일진)
        - 🔵 **파란색**: 합식, 강일진, 해결신, 금조건 (길한 일진)  
        - ⚫ **검정색**: 나머지 일진들
        """)
        
        st.markdown("---")
        st.markdown("### 📊 백초귀장술표")
        
        display_guijang_table()
    
    st.markdown("---")
    
    st.subheader("🎯 백초귀장술 상담")
    
    day_options = ['子日', '丑日', '寅日', '卯日', '辰日', '巳日', '午日', '未日', '申日', '酉日', '戌日', '亥日']
    selected_day = st.selectbox("📅 상담받을 날짜를 선택하세요", day_options, index=5)
    
    if st.button("🔮 백초귀장술 상담 결과 생성", use_container_width=True):
        st.session_state.guijang_day = selected_day
        st.session_state.show_guijang_result = True
    
    # 상담 결과 표시
    if hasattr(st.session_state, 'show_guijang_result') and st.session_state.show_guijang_result:
        selected_day = st.session_state.guijang_day
        
        st.markdown("---")
        st.subheader(f"📋 {selected_day} 백초귀장술 상담 결과")
        
        # 상담 정보 표시
        today = datetime.datetime.now()
        st.info(f"📅 **상담 일자**: {today.strftime('%Y년 %m월 %d일')} | 🔮 **해당 일진**: {selected_day}")
        
        # 테이블 데이터 가져오기
        table_data = get_guijang_data()
        interpretations = get_guijang_interpretations()
        time_to_month = get_time_to_month()
        
        # 선택된 날짜의 데이터 찾기
        day_row = None
        for row in table_data:
            if row[0] == selected_day:
                day_row = row
                break
        
        if day_row:
            time_columns = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
            
            # 월별 해석 표시
            for i, time in enumerate(time_columns):
                interpretation = day_row[i + 1]
                month = time_to_month[time]
                description = interpretations[interpretation]
                
                # 색상에 따른 이모지 결정
                if interpretation == '사살신':
                    emoji = "🔴"
                    alert_type = "error"
                elif interpretation in ['합식', '강일진', '해결신', '금조건']:
                    emoji = "🔵"
                    alert_type = "success"
                else:
                    emoji = "⚫"
                    alert_type = "info"
                
                # 각 월의 해석을 expander로 표시
                with st.expander(f"{emoji} **{month}월 - {interpretation}**", expanded=False):
                    st.write(f"**음력({month}月){interpretation}** {description}")
            
            st.markdown("---")
            
            # 결과 출력 버튼들
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📄 상담 결과 텍스트로 출력", use_container_width=True):
                    # 출력용 텍스트 생성
                    result_text = f"🔮 백초귀장술 상담 결과지\n"
                    result_text += f"상담 일자: {today.strftime('%Y년 %m월 %d일')}\n"
                    result_text += f"해당 일진: {selected_day}\n"
                    result_text += "=" * 50 + "\n\n"
                    
                    for i, time in enumerate(time_columns):
                        interpretation = day_row[i + 1]
                        month = time_to_month[time]
                        description = interpretations[interpretation]
                        result_text += f"【{month}월 - {interpretation}】\n"
                        result_text += f"음력({month}月){interpretation} {description}\n\n"
                    
                    result_text += "=" * 50 + "\n"
                    result_text += "※ 본 상담 결과는 참고용이며, 개인의 노력과 선택이 가장 중요합니다."
                    
                    st.text_area("📋 상담 결과 (복사해서 사용하세요)", result_text, height=400)
            
            with col2:
                if st.button("🔄 결과 초기화", use_container_width=True):
                    st.session_state.show_guijang_result = False
                    st.rerun()

# 동양타로 로그인 페이지
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

# 동양타로 메인
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
    
    st.markdown("---")
    st.subheader("🔮 카드 모드")
    
    mode = st.radio(
        "원하는 모드를 선택하세요", 
        ["3카드 보기", "원카드", "오늘의조언카드", "양자택일", "12개월운보기 (월별)"],
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
            
            for row in range(4):
                cols = st.columns(3)
                for col_idx in range(3):
                    card_idx = row * 3 + col_idx
                    if card_idx < 12:
                        file, direction = st.session_state.monthly_cards[card_idx]
                        month_num = month_sequence[card_idx]
                        
                        with cols[col_idx]:
                            st.markdown(f"**📅 {month_num}월**")
                            st.markdown(f"**{direction}**: {get_card_meaning(card_data, file, direction)}")
                            show_card(file, direction, width=180)
                            
                            if direction == "역방향":
                                if st.button("🔁 보조카드", key=f"monthly_subcard_{card_idx}"):
                                    exclude_files = [f for f, _ in st.session_state.monthly_cards]
                                    subcard = draw_cards(1, exclude=exclude_files)[0]
                                    st.session_state[f"monthly_sub_{card_idx}"] = subcard
                                    st.rerun()
                                
                                if f"monthly_sub_{card_idx}" in st.session_state:
                                    sub_file, sub_dir = st.session_state[f"monthly_sub_{card_idx}"]
                                    st.markdown("**🔁 보조카드:**")
                                    show_card(sub_file, sub_dir, width=120)
                                    st.markdown(f"**{sub_dir}**: {get_card_meaning(card_data, sub_file, sub_dir)}")
                
                if row < 3:
                    st.markdown("")

