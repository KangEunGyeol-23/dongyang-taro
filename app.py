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

# 카드 데이터 불러오기
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

# 카드 이미지 표시
def show_card(file, direction, width=200):
    img_path = os.path.join(CARD_FOLDER, file)
    img = Image.open(img_path)
    if direction == "역방향":
        img = img.rotate(180)
    st.image(img, width=width)

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

# 로그인
if not st.session_state.login:
    st.set_page_config(page_title="동양타로", layout="centered")
    st.markdown("""
        <h1 style='text-align: center;'>🌓 동양타로</h1>
        <div style='padding: 10px; background-color: #f5f5f5; border-radius: 10px; text-align: center;'>
            <p style='font-size: 28px; font-weight: bold; color: #4a148c;'>오늘, 당신의 운명에 귀 기울이세요.</p>
            <p style='font-size: 18px;'>동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.</p>
            <p style='font-size: 18px;'>사랑, 직업, 재물 등 모든 고민에 대한 당신만의 길을 지금 바로 동양 타로에서 찾아보세요.</p>
            <p style='font-size: 18px;'>숨겨진 운명의 실타래를 풀어내고, 더 나은 내일을 위한 지혜를 얻을 시간입니다.</p>
        </div>
    """, unsafe_allow_html=True)
    input_id = st.text_input("아이디를 입력하세요")
    if input_id:
        st.session_state.login = input_id
        log_login(input_id)  # 로그인 로그 기록
        st.rerun()
    st.stop()

user_id = st.session_state.login
is_admin = user_id in ADMIN_IDS
is_user = user_id in USER_IDS

if not (is_admin or is_user):
    st.error("등록되지 않은 사용자입니다.")
    st.stop()

st.set_page_config(page_title="동양타로", layout="centered")
st.title("🌓 동양타로")
st.markdown("한 장의 카드가 내 마음을 말하다")
st.success(f"{user_id}님 환영합니다.")

if st.button("🏠 처음으로"):
    user_id_temp = user_id
    st.session_state.clear()
    st.session_state.login = user_id_temp
    st.rerun()

# --- 관리자 로그인 기록 확인 및 초기화 ---
if is_admin:
    st.markdown("---")
    st.subheader("📜 로그인 기록 관리 (관리자 전용)")
    if os.path.exists(LOGIN_LOG_FILE):
        df_log = pd.read_csv(LOGIN_LOG_FILE)
        st.dataframe(df_log.tail(20))
        if st.button("🗑️ 로그인 기록 초기화"):
            os.remove(LOGIN_LOG_FILE)
            st.success("로그인 기록이 초기화되었습니다.")
    else:
        st.info("아직 로그인 기록이 없습니다.")
