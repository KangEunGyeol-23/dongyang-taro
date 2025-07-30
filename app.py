<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>타로세계</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #0d1421, #1a1a2e, #16213e);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        
        /* 배경 별들 */
        .stars-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .star {
            position: absolute;
            width: 2px;
            height: 2px;
            background: #ffd700;
            border-radius: 50%;
            animation: twinkle 3s infinite alternate;
        }
        
        @keyframes twinkle {
            0% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        
        /* 메인 컨테이너 */
        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }
        
        /* 헤더 */
        .main-title {
            font-size: 3rem;
            background: linear-gradient(45deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
            margin-bottom: 3rem;
        }
        
        /* 카드 그리드 */
        .cards-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 20px;
            max-width: 700px;
            margin: 0 auto;
        }
        
        /* 카드 스타일 */
        .card-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid rgba(255, 215, 0, 0.3);
            backdrop-filter: blur(10px);
        }
        
        .card-item:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 15px 30px rgba(255, 215, 0, 0.4);
            border-color: #ffd700;
        }
        
        .card-image {
            width: 100%;
            height: 160px;
            border-radius: 10px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            color: white;
            position: relative;
        }
        
        .card-title {
            font-size: 1.1rem;
            font-weight: bold;
            color: #ffd700;
            text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
        }
        
        /* 각 카드별 배경색 */
        .oriental-bg {
            background: linear-gradient(135deg, #2d1b69, #11052c);
            border: 2px solid #7209b7;
        }
        
        .universal-bg {
            background: linear-gradient(135deg, #1a0033, #4a0080);
            border: 2px solid #9d4edd;
        }
        
        .saju-bg {
            background: linear-gradient(135deg, #0f3460, #16537e);
            border: 2px solid #00a8cc;
        }
        
        .horoscope-bg {
            background: linear-gradient(135deg, #7c2d12, #ea580c);
            border: 2px solid #f97316;
        }
        
        .complex-bg {
            background: linear-gradient(135deg, #064e3b, #059669);
            border: 2px solid #10b981;
        }
        
        /* 준비중 모달 */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
        }
        
        .modal-content {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            margin: 15% auto;
            padding: 30px;
            border-radius: 20px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            border: 2px solid #ffa500;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        }
        
        .modal h3 {
            color: #ffa500;
            font-size: 1.5rem;
            margin-bottom: 15px;
        }
        
        .modal p {
            color: #e0e0e0;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .close-btn {
            background: linear-gradient(45deg, #ffd700, #c9b037);
            color: #1a1a2e;
            border: none;
            border-radius: 25px;
            padding: 10px 25px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .close-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);
        }
        
        /* 로그인 화면 */
        .login-screen {
            display: none;
            max-width: 400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 215, 0, 0.3);
        }
        
        .login-title {
            color: #ffd700;
            font-size: 1.8rem;
            margin-bottom: 20px;
        }
        
        .login-input {
            width: 100%;
            padding: 15px;
            font-size: 1.1rem;
            border: 3px solid #ffd700;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.95);
            color: #000000;
            margin-bottom: 20px;
            font-weight: bold;
        }
        
        .login-input:focus {
            outline: none;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
        }
        
        .login-btn {
            width: 100%;
            background: linear-gradient(45deg, #ffd700, #c9b037);
            color: #1a1a2e;
            border: none;
            border-radius: 25px;
            padding: 15px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 15px;
        }
        
        .back-btn {
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            color: #ffd700;
            border: 2px solid #ffd700;
            border-radius: 25px;
            padding: 12px;
            font-size: 1rem;
            cursor: pointer;
        }
        
        /* 반응형 */
        @media (max-width: 600px) {
            .main-title {
                font-size: 2rem;
            }
            
            .cards-container {
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }
            
            .card-image {
                height: 120px;
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>
    <!-- 배경 별들 -->
    <div class="stars-bg">
        <div class="star" style="top: 10%; left: 20%; animation-delay: 0s;"></div>
        <div class="star" style="top: 20%; left: 80%; animation-delay: 1s;"></div>
        <div class="star" style="top: 70%; left: 10%; animation-delay: 2s;"></div>
        <div class="star" style="top: 80%; left: 90%; animation-delay: 0.5s;"></div>
        <div class="star" style="top: 40%; left: 70%; animation-delay: 1.5s;"></div>
        <div class="star" style="top: 60%; left: 30%; animation-delay: 2.5s;"></div>
    </div>
    
    <div class="container">
        <!-- 메인 화면 -->
        <div id="mainScreen">
            <h1 class="main-title">🔮 타로세계</h1>
            
            <div class="cards-container">
                <!-- 동양타로 -->
                <div class="card-item" onclick="selectCard('oriental', '동양타로')">
                    <div class="card-image oriental-bg">☯️</div>
                    <div class="card-title">동양타로</div>
                </div>
                
                <!-- 유니버셜타로 -->
                <div class="card-item" onclick="showComingSoon('유니버셜타로')">
                    <div class="card-image universal-bg">🌟</div>
                    <div class="card-title">유니버셜타로</div>
                </div>
                
                <!-- 사주오라클카드 -->
                <div class="card-item" onclick="showComingSoon('사주오라클카드')">
                    <div class="card-image saju-bg">🏮</div>
                    <div class="card-title">사주오라클카드</div>
                </div>
                
                <!-- 호로스코프카드 -->
                <div class="card-item" onclick="showComingSoon('호로스코프카드')">
                    <div class="card-image horoscope-bg">♈</div>
                    <div class="card-title">호로스코프카드</div>
                </div>
                
                <!-- 복합카드 -->
                <div class="card-item" onclick="showComingSoon('복합카드')">
                    <div class="card-image complex-bg">🔮</div>
                    <div class="card-title">복합카드</div>
                </div>
            </div>
        </div>
        
        <!-- 로그인 화면 -->
        <div id="loginScreen" class="login-screen">
            <h2 class="login-title">🌓 동양타로</h2>
            <p style="color: #e0e0e0; margin-bottom: 25px; text-align: center;">
                오늘, 당신의 운명에 귀 기울이세요
            </p>
            <input type="text" id="loginInput" class="login-input" placeholder="아이디를 입력하세요" />
            <button class="login-btn" onclick="login()">입장하기</button>
            <button class="back-btn" onclick="goBack()">뒤로 가기</button>
        </div>
    </div>
    
    <!-- 준비중 모달 -->
    <div id="comingSoonModal" class="modal">
        <div class="modal-content">
            <h3>🚧 준비중입니다</h3>
            <p id="modalCardName"></p>
            <p>빠른 시일 내에 서비스를 제공할 예정이니<br>조금만 기다려주세요.</p>
            <p style="color: #ffd700; font-weight: bold;">현재는 동양타로만 이용 가능합니다.</p>
            <button class="close-btn" onclick="closeModal()">확인</button>
        </div>
    </div>

    <script>
        // 사용자 ID 목록
        const ADMIN_IDS = ["cotty23"];
        const USER_IDS = ["cotty00", "teleecho", "37nim", "ckss12"];
        
        function selectCard(cardType, cardName) {
            if (cardType === 'oriental') {
                // 동양타로 선택 시 로그인 화면으로
                document.getElementById('mainScreen').style.display = 'none';
                document.getElementById('loginScreen').style.display = 'block';
            }
        }
        
        function showComingSoon(cardName) {
            document.getElementById('modalCardName').textContent = cardName + '는 현재 준비중입니다.';
            document.getElementById('comingSoonModal').style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('comingSoonModal').style.display = 'none';
        }
        
        function login() {
            const userId = document.getElementById('loginInput').value.trim();
            
            if (!userId) {
                alert('아이디를 입력해주세요.');
                return;
            }
            
            if (ADMIN_IDS.includes(userId) || USER_IDS.includes(userId)) {
                alert('동양타로에 입장합니다!');
                // Streamlit 앱으로 이동 (로컬 서버)
                window.location.href = `http://localhost:8501?user=${userId}`;
            } else {
                alert('등록되지 않은 사용자입니다.');
            }
        }
        
        function goBack() {
            document.getElementById('mainScreen').style.display = 'block';
            document.getElementById('loginScreen').style.display = 'none';
            document.getElementById('loginInput').value = '';
        }
        
        // 엔터키 로그인
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('loginInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    login();
                }
            });
        });
        
        // 모달 외부 클릭시 닫기
        window.onclick = function(event) {
            const modal = document.getElementById('comingSoonModal');
            if (event.target == modal) {
                closeModal();
            }
        }
    </script>
</body>
</html>
