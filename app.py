... (기존 코드 생략)

# 관리자 카드 해석 등록
if st.session_state.user == "cotty79@naver.com":
    with st.expander("🛠 관리자 전용: 카드 해석 등록"):
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
                card_meanings[selected_card] = {
                    "정방향": 정,
                    "역방향": 역
                }
                st.success(f"'{selected_card}' 해석이 등록되었습니다.")
                st.rerun()

# 카드 표시 함수
...
