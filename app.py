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

user_id = st.session_state.login
if not user_id:
    st.set_page_config(page_title="동양타로", layout="centered")
    st.title("🌓 동양타로")
    st.markdown("""
    "오늘, 당신의 운명에 귀 기울이세요."

    동양의 오랜 지혜가 담긴 타로가 당신의 삶에 깊은 통찰과 명쾌한 해답을 선사합니다.

    사랑, 직업, 재물 등 모든 고민에 대한 당신만의 길을 지금 바로 동양 타로에서 찾아보세요.

    숨겨진 운명의 실타래를 풀어내고, 더 나은 내일을 위한 지혜를 얻을 시간입니다.
    """)
    user_id = st.text_input("아이디를 입력하세요")
    st.session_state.login = user_id
    st.stop()

is_admin = user_id in ADMIN_IDS
is_user = user_id in USER_IDS

if not (is_admin or is_user):
    st.error("등록되지 않은 사용자입니다.")
    st.stop()

st.set_page_config(page_title="동양타로", layout="centered")
st.title("🌓 동양타로")
st.markdown("\"한 장의 카드가 내 마음을 말하다\"")
st.success(f"{user_id}님 환영합니다.")

if st.button("🏠 처음으로"):
    user_id_temp = user_id
    st.session_state.clear()
    st.session_state.login = user_id_temp
    st.rerun()

if is_admin:
    st.subheader("🛠️ 관리자 전용: 카드 해석 등록 및 관리")
    card_data = load_card_data()
    all_files = os.listdir(CARD_FOLDER)
    registered_files = card_data["filename"].tolist()
    unregistered_files = [f for f in all_files if f not in registered_files]

    selected_file = st.selectbox("📋 해석이 등록되지 않은 카드 선택", unregistered_files)
    upright = st.text_area("✅ 정방향 해석 입력")
    reversed_ = st.text_area("⛔ 역방향 해석 입력")

    if st.button("💾 해석 저장"):
        card_data = card_data.append({
            "filename": selected_file,
            "upright": upright,
            "reversed": reversed_
        }, ignore_index=True)
        save_card_data(card_data)
        st.success("해석이 저장되었습니다.")

    if st.button("🗂 전체 카드 해석 CSV 다운로드"):
        csv = card_data.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 다운로드", data=csv, file_name="card_data.csv", mime="text/csv")

else:
    st.subheader("🔮 타로 뽑기")
    previous_mode = st.session_state.get("selected_mode")
    mode = st.radio("모드 선택", ["3카드 보기", "원카드", "조언카드", "양자택일"])

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

    if mode in ["3카드 보기", "원카드", "조언카드"]:
        st.session_state.question = st.text_input("질문을 입력하세요", value=st.session_state.question)
    elif mode == "양자택일":
        st.session_state.q1 = st.text_input("선택1 질문 입력", value=st.session_state.q1)
        st.session_state.q2 = st.text_input("선택2 질문 입력", value=st.session_state.q2)

    if mode == "3카드 보기" and st.session_state.question.strip():
        if st.button("🔮 3장 뽑기"):
            st.session_state.cards = draw_cards(3)
            st.session_state.subcards = {}
            st.session_state.subcard_used = {}

    if "cards" in st.session_state:
        cols = st.columns(3)
        used_files = [f for f, _ in st.session_state.cards]
        for i, (file, direction) in enumerate(st.session_state.cards):
            with cols[i]:
                show_card(file, direction)
                st.markdown(get_card_meaning(card_data, file, direction))

                if direction == "역방향" and file not in st.session_state.subcard_used:
                    if st.button(f"🔁 보조카드 보기 ({i+1})"):
                        subcard = draw_cards(1, exclude=used_files + list(st.session_state.subcards.keys()))[0]
                        st.session_state.subcards[file] = subcard
                        st.session_state.subcard_used[file] = True

                if file in st.session_state.subcards:
                    sub_file, sub_dir = st.session_state.subcards[file]
                    show_card(sub_file, sub_dir, width=150)
                    st.markdown(get_card_meaning(card_data, sub_file, sub_dir))

    if mode == "원카드" and st.session_state.question.strip():
        if st.button("✨ 한 장 뽑기"):
            st.session_state.card = draw_cards(1)[0]
            st.session_state.subcards = {}
            st.session_state.subcard_used = {}

    if "card" in st.session_state:
        file, direction = st.session_state.card
        show_card(file, direction, width=300)
        st.markdown(get_card_meaning(card_data, file, direction))

        if direction == "역방향" and file not in st.session_state.subcard_used:
            if st.button("🔁 보조카드 보기"):
                subcard = draw_cards(1, exclude=[file])[0]
                st.session_state.subcards[file] = subcard
                st.session_state.subcard_used[file] = True

        if file in st.session_state.subcards:
            sub_file, sub_dir = st.session_state.subcards[file]
            show_card(sub_file, sub_dir, width=200)
            st.markdown(get_card_meaning(card_data, sub_file, sub_dir))

    if mode == "조언카드" and st.session_state.question.strip():
        if st.button("🌿 오늘의 조언카드"):
            st.session_state.adv_card = draw_cards(1)[0]
            st.session_state.subcards = {}
            st.session_state.subcard_used = {}

    if "adv_card" in st.session_state:
        file, direction = st.session_state.adv_card
        show_card(file, direction, width=300)
        st.markdown(get_card_meaning(card_data, file, direction))

        if direction == "역방향" and file not in st.session_state.subcard_used:
            if st.button("🔁 보조카드 보기"):
                subcard = draw_cards(1, exclude=[file])[0]
                st.session_state.subcards[file] = subcard
                st.session_state.subcard_used[file] = True

        if file in st.session_state.subcards:
            sub_file, sub_dir = st.session_state.subcards[file]
            show_card(sub_file, sub_dir, width=200)
            st.markdown(get_card_meaning(card_data, sub_file, sub_dir))

    if mode == "양자택일" and st.session_state.q1.strip() and st.session_state.q2.strip():
        if st.button("🔍 선택별 카드 뽑기"):
            st.session_state.choice_cards = draw_cards(2)
            st.session_state.final_choice_card = None

    if "choice_cards" in st.session_state:
        used_files = [f for f, _ in st.session_state.choice_cards]
        cols = st.columns(2)
        for i, (file, direction) in enumerate(st.session_state.choice_cards):
            with cols[i]:
                show_card(file, direction, width=200)
                st.markdown(f"**선택{i+1}**")
                st.markdown(f"질문: {st.session_state.q1 if i == 0 else st.session_state.q2}")
                st.markdown(get_card_meaning(card_data, file, direction))

    if st.session_state.q1.strip() and st.session_state.q2.strip():
        if st.button("🧭 최종 결론 카드 보기"):
            exclude_files = [f for f, _ in st.session_state.choice_cards] if "choice_cards" in st.session_state else []
            st.session_state.final_choice_card = draw_cards(1, exclude=exclude_files)[0]

    if "final_choice_card" in st.session_state and st.session_state.final_choice_card:
        file, direction = st.session_state.final_choice_card
        st.markdown("---")
        st.markdown(f"### 🏁 최종 결론 카드")
        show_card(file, direction, width=300)
        st.markdown(get_card_meaning(card_data, file, direction))
