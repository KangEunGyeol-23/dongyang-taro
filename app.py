import streamlit as st
import random
import os
import pandas as pd
from PIL import Image

# --- 설정 ---
ADMIN_IDS = ["cotty23"]
USER_IDS = ["cotty00", "teleecho"]

CARD_FOLDER = "cards"
CARD_DATA_FILE = "card_data.csv"

# 카드 데이터 불러오기
def load_card_data():
    if os.path.exists(CARD_DATA_FILE):
        return pd.read_csv(CARD_DATA_FILE)
    else:
        return pd.DataFrame(columns=["filename", "image_desc", "summary", "upright", "reversed", "advice"])

# 카드 데이터 저장하기
def save_card_data(df):
    df.to_csv(CARD_DATA_FILE, index=False)

# 카드 뽑기 함수 (정/역방향 랜덤 포함)
def draw_cards(n=1):
    files = os.listdir(CARD_FOLDER)
    selected = random.sample(files, n)
    cards = [(file, random.choice(["정방향", "역방향"])) for file in selected]
    return cards

# 카드 해석 가져오기
def get_card_meaning(df, filename, direction):
    row = df[df["filename"] == filename]
    if not row.empty:
        meaning = []
        meaning.append(f"🖼️ 이미지 설명: {row.iloc[0]['image_desc']}")
        meaning.append(f"🧭 카드 요약: {row.iloc[0]['summary']}")
        if direction == "정방향":
            meaning.append(f"🟢 정방향 해석: {row.iloc[0]['upright']}")
        else:
            meaning.append(f"🔴 역방향 해석: {row.iloc[0]['reversed']}")
        meaning.append(f"📝 조언: {row.iloc[0]['advice']}")
        return "\n\n".join(meaning)
    return "등록된 해석이 없습니다."

if "subcards" not in st.session_state:
    st.session_state.subcards = {}

if "subcard_used" not in st.session_state:
    st.session_state.subcard_used = {}

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

        tab1, tab2 = st.tabs(["카드 등록", "등록된 카드 관리"])

        with tab1:
            selected_file = st.selectbox("📋 해석이 등록되지 않은 카드 선택", unregistered_files)
            image_desc = st.text_area("🖼️ 이미지 설명 입력")
            summary = st.text_area("🧭 카드 요약 입력")
            upright = st.text_area("✅ 정방향 해석 입력")
            reversed_ = st.text_area("⛔ 역방향 해석 입력")
            advice = st.text_area("📝 조언 입력")

            if st.button("💾 해석 저장"):
                card_data = card_data.append({
                    "filename": selected_file,
                    "image_desc": image_desc,
                    "summary": summary,
                    "upright": upright,
                    "reversed": reversed_,
                    "advice": advice
                }, ignore_index=True)
                save_card_data(card_data)
                st.success("해석이 저장되었습니다.")

        with tab2:
            edit_file = st.selectbox("✏️ 등록된 카드 선택", registered_files)
            row = card_data[card_data["filename"] == edit_file].iloc[0]
            image_desc = st.text_area("🖼️ 이미지 설명 입력", row['image_desc'])
            summary = st.text_area("🧭 카드 요약 입력", row['summary'])
            upright = st.text_area("✅ 정방향 해석 입력", row['upright'])
            reversed_ = st.text_area("⛔ 역방향 해석 입력", row['reversed'])
            advice = st.text_area("📝 조언 입력", row['advice'])

            if st.button("💾 수정 저장"):
                card_data.loc[card_data["filename"] == edit_file, ["image_desc", "summary", "upright", "reversed", "advice"]] = \
                    image_desc, summary, upright, reversed_, advice
                save_card_data(card_data)
                st.success("수정이 저장되었습니다.")

            if st.button("🗑️ 카드 삭제"):
                card_data = card_data[card_data["filename"] != edit_file]
                save_card_data(card_data)
                st.success("카드 해석이 삭제되었습니다.")

        if st.button("🗂 전체 카드 해석 CSV 다운로드"):
            csv = card_data.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 다운로드", data=csv, file_name="card_data.csv", mime="text/csv")
