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

# 보조카드 관련 처리 상태 저장용
if "subcards" not in st.session_state:
    st.session_state.subcards = {}

if "subcard_used" not in st.session_state:
    st.session_state.subcard_used = {}

# 로그인
st.title("\ud83c\udf03 \ub3d9\uc591\ud0c0\ub85c")
st.markdown("\"\ud55c \uc7a5\uc758 \uce74\ub4dc\uac00 \ub0b4 \ub9c8\uc74c\uc744 \ub9d0\ud55c\ub2e4\"")

if "login" not in st.session_state:
    st.session_state.login = ""

user_id = st.text_input("아이디를 입력하세요", value=st.session_state.login)
st.session_state.login = user_id

if user_id:
    is_admin = user_id in ADMIN_IDS
    is_user = user_id in USER_IDS

    if not (is_admin or is_user):
        st.error("등록되지 않은 사용자입니다.")
        st.stop()

    st.success(f"{user_id}님 환영합니다.")

    if st.button("\ud83c\udfe0 \ucc98\uc74c\uc73c\ub85c"):
        user_id_temp = user_id
        st.session_state.clear()
        st.session_state.login = user_id_temp
        st.rerun()

    # --- 관리자 모드 ---
    if is_admin:
        st.subheader("\ud83d\udee0\ufe0f \uad00\ub9ac\uc790 \uc804\uc6a9: \uce74\ub4dc \ud574\uc11d \ub4f1\ub85d \ubc0f \uad00\ub9ac")

        card_data = load_card_data()
        all_files = os.listdir(CARD_FOLDER)
        registered_files = card_data["filename"].tolist()
        unregistered_files = [f for f in all_files if f not in registered_files]

        selected_file = st.selectbox("\ud83d\udccb \ud574\uc11d\uc774 \ub4f1\ub85d\ub418\uc9c0 \uc54a\uc740 \uce74\ub4dc \uc120\ud0dd", unregistered_files)

        upright = st.text_area("\u2705 \uc815\ubc29\ud654 \ud574\uc11d \uc785\ub825")
        reversed_ = st.text_area("\u26d4 \uc5ed\ubc29\ud654 \ud574\uc11d \uc785\ub825")

        if st.button("\ud83d\udcce \ud574\uc11d \uc800\uc7a5"):
            card_data = card_data.append({
                "filename": selected_file,
                "upright": upright,
                "reversed": reversed_
            }, ignore_index=True)
            save_card_data(card_data)
            st.success("해석이 저장되었습니다.")

        if st.button("\ud83d\udcc2 \uc804\uccb4 \uce74\ub4dc \ud574\uc11d CSV \ub2e4\uc6b4\ub85c\ub4dc"):
            csv = card_data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("\ud83d\udcc5 \ub2e4\uc6b4\ub85c\ub4dc", data=csv, file_name="card_data.csv", mime="text/csv")

    # --- 일반 사용자 모드 ---
    else:
        st.subheader("\ud83d\udd2e \ud0c0\ub85c \ubd2c\uae30")
        previous_mode = st.session_state.get("selected_mode")
        mode = st.radio("모드 선택", ["3카드 보기", "원카드", "조언카드", "양자택일"])

        # 모드 변경 시 질문 초기화
        if previous_mode != mode:
            st.session_state.question = ""
            st.session_state.q1 = ""
            st.session_state.q2 = ""
            st.session_state.selected_mode = mode

        card_data = load_card_data()

        def show_card(file, direction, width=200):
            img_path = os.path.join(CARD_FOLDER, file)
            img = Image.open(img_path)
            if direction == "역방향":
                img = img.rotate(180)
            st.image(img, width=width)

        # 공통 질문 입력
        if mode in ["3카드 보기", "원카드", "조언카드"]:
            st.session_state.question = st.text_input("질문을 입력하세요", value=st.session_state.get("question", ""))
        elif mode == "양자택일":
            st.session_state.q1 = st.text_input("선택1 질문 입력", key="q1", value=st.session_state.get("q1", ""))
            st.session_state.q2 = st.text_input("선택2 질문 입력", key="q2", value=st.session_state.get("q2", ""))

        # 각 모드별로 질문 입력이 완료되었을 때만 뽑기 버튼 노출
        if mode == "3카드 보기" and st.session_state.question.strip():
            if st.button("\ud83d\udd2e 3\uc7a5 \ubd2c\uae30"):
                st.session_state.cards = draw_cards(3)
                st.session_state.subcards = {}
                st.session_state.subcard_used = {}

        if mode == "원카드" and st.session_state.question.strip():
            if st.button("\u2728 \ud55c \uc7a5 \ubd2c\uae30"):
                st.session_state.card = draw_cards(1)[0]
                st.session_state.subcards = {}
                st.session_state.subcard_used = {}

        if mode == "조언카드" and st.session_state.question.strip():
            if st.button("\ud83c\udf3f \uc624\ub298\uc758 \uc870\uc5b8\uce74\ub4dc"):
                st.session_state.adv_card = draw_cards(1)[0]
                st.session_state.subcards = {}
                st.session_state.subcard_used = {}

        if mode == "양자택일" and st.session_state.q1.strip() and st.session_state.q2.strip():
            if st.button("\ud83d\udd0d \uc120\ud0dd\ubcc4 \uce74\ub4dc \ubd2c\uae30"):
                st.session_state.choice_cards = draw_cards(2)
                st.session_state.final_choice_card = None
