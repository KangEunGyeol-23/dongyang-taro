import streamlit as st
import random
import os
import pandas as pd
from PIL import Image

# --- 설정 ---
ADMIN_IDS = ["cotty23"]
USER_IDS = ["cotty00", "teleecho", "37nim", "ckss12"]

CARD_FOLDER = "cards"
CARD_DATA_FILE = "card_data.csv"

# 카드 데이터 불러오기
def load_card_data():
    if os.path.exists(CARD_DATA_FILE):
        return pd.read_csv(CARD_DATA_FILE)
    else:
        return pd.DataFrame(columns=["filename", "upright", "reversed"])

# 카드 데이터 저장하기
def save_card_data(df):
    df.to_csv(CARD_DATA_FILE, index=False)

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
if "subcards" not in st.session_state:
    st.session_state.subcards = {}
if "subcard_used" not in st.session_state:
    st.session_state.subcard_used = {}
if "login" not in st.session_state:
    st.session_state.login = ""
if "cards" not in st.session_state:
    st.session_state.cards = []
if "adv_card" not in st.session_state:
    st.session_state.adv_card = None
if "card" not in st.session_state:
    st.session_state.card = None
if "advice_for_three_cards" not in st.session_state:
    st.session_state.advice_for_three_cards = None
if "show_advice_card" not in st.session_state:
    st.session_state.show_advice_card = False
if "monthly_cards" not in st.session_state:
    st.session_state.monthly_cards = []
if "choice_cards" not in st.session_state:
    st.session_state.choice_cards = []
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

# --- 카드 기능 모드 ---
st.subheader("🔮 타로 뽑기")
mode = st.radio("모드 선택", ["3카드 보기", "원카드", "오늘의조언카드", "양자택일", "12개월운보기 (월별)"])
card_data = load_card_data()

# 보조카드 표시 함수
def handle_subcard(file, exclude):
    if file in st.session_state.subcards:
        sub_file, sub_dir = st.session_state.subcards[file]
        show_card(sub_file, sub_dir, width=150)
        st.markdown(get_card_meaning(card_data, sub_file, sub_dir))
    else:
        if st.button("🔁 보조카드 보기", key=f"subcard_btn_{file}"):
            subcard = draw_cards(1, exclude=exclude + list(st.session_state.subcards.keys()))[0]
            st.session_state.subcards[file] = subcard
            sub_file, sub_dir = subcard
            show_card(sub_file, sub_dir, width=150)
            st.markdown(get_card_meaning(card_data, sub_file, sub_dir))

if mode == "3카드 보기":
    if st.button("🔮 3장 뽑기"):
        st.session_state.cards = draw_cards(3)
        st.session_state.subcards = {}

    if st.session_state.cards:
        cols = st.columns(3)
        selected_files = [f for f, _ in st.session_state.cards]
        for i, (file, direction) in enumerate(st.session_state.cards):
            with cols[i]:
                show_card(file, direction)
                st.markdown(get_card_meaning(card_data, file, direction))
                if direction == "역방향":
                    handle_subcard(file, exclude=selected_files)

elif mode == "원카드":
    if st.button("✨ 한 장 뽑기"):
        st.session_state.card = draw_cards(1)[0]
        st.session_state.subcards = {}

    if st.session_state.card:
        file, direction = st.session_state.card
        show_card(file, direction, width=300)
        st.markdown(get_card_meaning(card_data, file, direction))
        if direction == "역방향":
            handle_subcard(file, exclude=[file])

elif mode == "오늘의조언카드":
    if st.button("🌿 오늘의 조언카드"):
        st.session_state.adv_card = draw_cards(1)[0]
        st.session_state.subcards = {}

    if st.session_state.adv_card:
        file, direction = st.session_state.adv_card
        show_card(file, direction, width=300)
        st.markdown(get_card_meaning(card_data, file, direction))
        if direction == "역방향":
            handle_subcard(file, exclude=[file])

elif mode == "양자택일":
    q1 = st.text_input("선택1 질문 입력", key="q1")
    q2 = st.text_input("선택2 질문 입력", key="q2")

    if q1 and q2:
        if st.button("🔍 선택별 카드 뽑기"):
            st.session_state.choice_cards = draw_cards(2)

    if st.session_state.choice_cards:
        cols = st.columns(2)
        selected_files = [f for f, _ in st.session_state.choice_cards]
        for i, (file, direction) in enumerate(st.session_state.choice_cards):
            with cols[i]:
                show_card(file, direction, width=200)
                st.markdown(f"**선택{i+1}**")
                st.markdown(f"질문: {q1 if i == 0 else q2}")
                st.markdown(get_card_meaning(card_data, file, direction))

        if st.button("🧭 최종 결론 카드 보기"):
            used = [f for f, _ in st.session_state.choice_cards]
            st.session_state.final_choice_card = draw_cards(1, exclude=used)[0]

    if st.session_state.final_choice_card:
        file, direction = st.session_state.final_choice_card
        st.markdown("---")
        st.markdown(f"### 🏁 최종 결론 카드")
        show_card(file, direction, width=300)
        st.markdown(get_card_meaning(card_data, file, direction))

elif mode == "12개월운보기 (월별)":
    selected_month = st.selectbox("현재 월을 선택하세요", list(range(1, 13)))
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
                st.markdown(get_card_meaning(card_data, file, direction))
                if direction == "역방향":
                    handle_subcard(file, exclude=[f for f, _ in st.session_state.monthly_cards])
