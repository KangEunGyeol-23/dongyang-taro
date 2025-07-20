import streamlit as st
from PIL import Image
import os
import random
import pandas as pd
import json
from datetime import datetime

# ✅ 허용된 이메일 목록
ALLOWED_USERS = ["cotty79@naver.com", "teleecho@naver.com"]

# ✅ 카드 해석 딕셔너리 (초기값)
card_meanings = {}

# ✅ JSON 불러오기 기능
if os.path.exists("card_meanings.json"):
    with open("card_meanings.json", "r", encoding="utf-8") as f:
        card_meanings = json.load(f)

# ✅ 로그인 처리
if "user" not in st.session_state:
    st.markdown("## 🔐 로그인")
    email = st.text_input("이메일을 입력하세요")
    if st.button("로그인"):
        if email in ALLOWED_USERS:
            st.session_state.user = email
            st.success(f"{email} 님 환영합니다.")
            st.rerun()
        else:
            st.error("접근 권한이 없습니다.")
    st.stop()

# 세션 초기화
for key in ["mode", "cards", "reversed", "extra_cards", "advice_card", "question_yes", "question_no", "history"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["cards", "reversed", "extra_cards", "history"] else ""

img_folder = "카드이미지"

# 카드 불러오기
def load_cards():
    if not os.path.exists(img_folder):
        st.error(f"이미지 폴더가 없습니다: {img_folder}")
        return []
    return [f for f in os.listdir(img_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

def draw_cards(n):
    card_pool = load_cards()
    if len(card_pool) < n:
        return []
    cards = random.sample(card_pool, n)
    directions = [random.choice(['정방향', '역방향']) for _ in range(n)]
    return list(zip(cards, directions))

def show_card(card, direction, width=200):
    img = Image.open(os.path.join(img_folder, card))
    if direction == "역방향":
        img = img.rotate(180)
    st.image(img, caption=f"{card} ({direction})", width=width)

def interpret_result(card_name, direction):
    return card_meanings.get(card_name, {}).get(direction, "💬 이 카드에 대한 해석이 준비 중입니다.")

def save_result(title, card_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"시간": timestamp, "타입": title, "카드 정보": card_data}
    st.session_state.history.append(entry)

def download_history():
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 결과 다운로드 (CSV)", data=csv, file_name="타로_기록.csv", mime="text/csv")

# ✅ 관리자 모드
if st.session_state.user == "cotty79@naver.com":
    with st.expander("🛠 관리자 전용: 카드 해석 등록 및 관리"):
        def get_unregistered_cards():
            return [fname for fname in load_cards() if fname not in card_meanings]

        unregistered = get_unregistered_cards()
        if not unregistered:
            st.success("✅ 모든 카드에 해석이 등록되어 있습니다.")
        else:
            selected_card = st.selectbox("🃏 해석이 등록되지 않은 카드 선택", unregistered)
            정 = st.text_area("✅ 정방향 해석 입력")
            역 = st.text_area("⛔ 역방향 해석 입력")
            if st.button("💾 해석 저장"):
                card_meanings[selected_card] = {"정방향": 정, "역방향": 역}
                with open("card_meanings.json", "w", encoding="utf-8") as f:
                    json.dump(card_meanings, f, ensure_ascii=False, indent=2)
                st.success(f"'{selected_card}' 해석이 저장되었습니다.")
                st.rerun()

        df = pd.DataFrame([
            {"카드": k, "정방향": v.get("정방향", ""), "역방향": v.get("역방향", "")}
            for k, v in card_meanings.items()
        ])
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📄 전체 카드 해석 CSV 다운로드", data=csv, file_name="card_meanings.csv", mime="text/csv")

# 🔮 앱 본문 시작
# (기존 카드 모드: 3카드, 원카드, 양자택일 등은 이전 구조 그대로 유지)
# 각 카드 출력 후 interpret_result(card, direction) 함수로 해석 출력
