import streamlit as st
import random
import os
import pandas as pd
from PIL import Image

# --- 설정 ---
ADMIN_IDS = ["cotty23"]
USER_IDS = ["cotty00", "teleecho", "ckss12", 37nim]

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
st.title("🌓 동양타로")
st.markdown("\"한 장의 카드가 내 마음을 말하다\"")

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

    if st.button("🏠 처음으로"):
        user_id_temp = user_id
        st.session_state.clear()
        st.session_state.login = user_id_temp
        st.rerun()

    # --- 관리자 모드 ---
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

    # --- 일반 사용자 모드 ---
    else:
        st.subheader("🔮 타로 뽑기")
        mode = st.radio("모드 선택", ["3카드 보기", "원카드", "조언카드", "양자택일"])
        card_data = load_card_data()

        def show_card(file, direction, width=200):
            img_path = os.path.join(CARD_FOLDER, file)
            img = Image.open(img_path)
            if direction == "역방향":
                img = img.rotate(180)
            st.image(img, width=width)

        if mode == "3카드 보기":
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

        elif mode == "원카드":
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

        elif mode == "조언카드":
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

        elif mode == "양자택일":
            q1 = st.text_input("선택1 질문 입력", key="q1")
            q2 = st.text_input("선택2 질문 입력", key="q2")

            if q1 and q2:
                if st.button("🔍 선택별 카드 뽑기"):
                    st.session_state.choice_cards = draw_cards(2)
                    st.session_state.final_choice_card = None

            if "choice_cards" in st.session_state:
                cols = st.columns(2)
                used_files = [f for f, _ in st.session_state.choice_cards]
                for i, (file, direction) in enumerate(st.session_state.choice_cards):
                    with cols[i]:
                        show_card(file, direction, width=200)
                        st.markdown(f"**선택{i+1}**")
                        st.markdown(f"질문: {q1 if i == 0 else q2}")
                        st.markdown(get_card_meaning(card_data, file, direction))

            if q1 and q2:
                if st.button("🧭 최종 결론 카드 보기"):
                    used_files = [f for f, _ in st.session_state.choice_cards] if "choice_cards" in st.session_state else []
                    st.session_state.final_choice_card = draw_cards(1, exclude=used_files)[0]

            if "final_choice_card" in st.session_state and st.session_state.final_choice_card:
                file, direction = st.session_state.final_choice_card
                st.markdown("---")
                st.markdown(f"### 🏁 최종 결론 카드")
                show_card(file, direction, width=300)
                st.markdown(get_card_meaning(card_data, file, direction))
