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

# 초기 세션 상태 설정
if "subcards" not in st.session_state:
    st.session_state.subcards = {}
if "subcard_used" not in st.session_state:
    st.session_state.subcard_used = {}
if "question" not in st.session_state:
    st.session_state.question = ""
if "q1" not in st.session_state:
    st.session_state.q1 = ""
if "q2" not in st.session_state:
    st.session_state.q2 = ""
if "login" not in st.session_state:
    st.session_state.login = ""
if "cards" not in st.session_state:
    st.session_state.cards = []
if "adv_card" not in st.session_state:
    st.session_state.adv_card = None
if "card" not in st.session_state:
    st.session_state.card = None

# 로그인 로직
if not st.session_state.login:
    st.set_page_config(page_title="동양타로", layout="centered")
    st.title("🌓 동양타로")
    st.markdown("""
    "오늘, 당신의 운명에 귀 기울이세요."

    동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.

    사랑, 직업, 재물 등 모든 고민에 대한 당신만의 길을 지금 바로 동양 타로에서 찾아보세요.

    숨겨진 운명의 실타래를 풀어내고, 더 나은 내일을 위한 지혜를 얻을 시간입니다.
    """)
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
mode = st.radio("모드 선택", ["3카드 보기", "원카드", "조언카드", "양자택일"])
card_data = load_card_data()

# 보조카드 표시 함수
def handle_subcard(file, exclude):
    if file in st.session_state.subcards:
        sub_file, sub_dir = st.session_state.subcards[file]
        show_card(sub_file, sub_dir, width=150)
        st.markdown(get_card_meaning(card_data, sub_file, sub_dir))
    elif st.button("🔁 보조카드 보기", key=f"sub_{file}"):
        subcard = draw_cards(1, exclude=exclude)[0]
        st.session_state.subcards[file] = subcard
        st.session_state.subcard_used[file] = True
        sub_file, sub_dir = subcard
        show_card(sub_file, sub_dir, width=150)
        st.markdown(get_card_meaning(card_data, sub_file, sub_dir))

# 모드별 실행
if mode == "3카드 보기":
    st.session_state.question = st.text_input("질문을 입력하세요")
    if st.session_state.question and st.button("🔮 카드 뽑기"):
        st.session_state.cards = draw_cards(3)
        st.session_state.subcards = {}
        st.session_state.subcard_used = {}

    if st.session_state.cards:
        exclude = [f for f, _ in st.session_state.cards]
        cols = st.columns(3)
        for i, (file, direction) in enumerate(st.session_state.cards):
            with cols[i]:
                show_card(file, direction)
                st.markdown(get_card_meaning(card_data, file, direction))
                if direction == "역방향" and file not in st.session_state.subcard_used:
                    handle_subcard(file, exclude)

elif mode == "원카드":
    st.session_state.question = st.text_input("질문을 입력하세요")
    if st.session_state.question and st.button("🔮 카드 뽑기"):
        st.session_state.card = draw_cards(1)[0]
        st.session_state.subcards = {}
        st.session_state.subcard_used = {}

    if st.session_state.card:
        file, direction = st.session_state.card
        show_card(file, direction)
        st.markdown(get_card_meaning(card_data, file, direction))
        if direction == "역방향" and file not in st.session_state.subcard_used:
            handle_subcard(file, [file])

elif mode == "조언카드":
    st.session_state.question = st.text_input("질문을 입력하세요")
    if st.session_state.question and st.button("🔮 카드 뽑기"):
        st.session_state.adv_card = draw_cards(1)[0]
        st.session_state.subcards = {}
        st.session_state.subcard_used = {}

    if st.session_state.adv_card:
        file, direction = st.session_state.adv_card
        show_card(file, direction)
        st.markdown(get_card_meaning(card_data, file, direction))
        if direction == "역방향" and file not in st.session_state.subcard_used:
            handle_subcard(file, [file])

elif mode == "양자택일":
    st.session_state.q1 = st.text_input("선택1 질문 입력")
    st.session_state.q2 = st.text_input("선택2 질문 입력")

    if st.session_state.q1 and st.session_state.q2:
        if st.button("🔍 선택별 카드 뽑기"):
            st.session_state.choice_cards = draw_cards(2)
            st.session_state.final_choice_card = None

        if "choice_cards" in st.session_state:
            exclude = [f for f, _ in st.session_state.choice_cards]
            cols = st.columns(2)
            for i, (file, direction) in enumerate(st.session_state.choice_cards):
                with cols[i]:
                    st.markdown(f"질문: {st.session_state.q1 if i == 0 else st.session_state.q2}")
                    show_card(file, direction)
                    st.markdown(get_card_meaning(card_data, file, direction))

        if st.button("🧭 최종 결론 카드 보기"):
            final = draw_cards(1, exclude=exclude)[0]
            file, direction = final
            show_card(file, direction, width=250)
            st.markdown(get_card_meaning(card_data, file, direction))
