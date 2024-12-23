import pandas as pd  # 데이터 처리를 위한 라이브러리
from sklearn.model_selection import train_test_split  # 데이터 분할용
from sklearn.feature_extraction.text import CountVectorizer  # 텍스트 벡터화
from sklearn.naive_bayes import MultinomialNB  # 나이브 베이즈 분류기
from sklearn.metrics import accuracy_score, classification_report  # 평가 지표

# 1. 100개의 한글 가상 데이터 준비
titles = [
    '무료 아이폰 당첨!', '택배가 배송 중입니다', '축하합니다! 100만원에 당첨되셨습니다',
    '내일 회의 안건입니다', '계정 관련 중요 업데이트', '집에서 일하며 1000만원 벌기!',
    '청구서가 준비되었습니다', '저렴한 항공권을 지금 예약하세요!', '구독이 곧 만료됩니다',
    '무료 상품권을 받아가세요', '즉시 승인 대출 가능', '내일 저녁 시간 괜찮으신가요?',
    '배송이 예정되었습니다', '새 차를 받을 기회!', '오늘 모든 상품 50% 할인!',
    '긴급: 계정을 지금 확인하세요', '알림: 오전 10시 회의', '지금 바로 상품을 청구하세요!',
    '중요: 비밀번호 변경 필요', '특별 할인 혜택을 받아보세요', '신용 점수가 업데이트되었습니다',
    '웹 세미나 초대', '전자제품 독점 할인 제공', '한정 판매! 지금 쇼핑하세요',
    '구직 지원 상태 확인', '축하합니다! 귀하가 선택되었습니다', '은행 계좌 명세서',
    '긴급: 계정 보안 경고', '새로운 음성 메시지가 있습니다', '휴가 독점 할인 제공!',
    '회의 후속 조치', '무료 보고서를 지금 다운로드하세요', '마지막 기회! 최대 70% 할인',
    '팀 주간 뉴스레터', '환불이 처리되었습니다', '두 사람을 위한 무료 여행!',
    '새 친구 요청이 있습니다', '프리미엄 멤버십에 가입하세요', '현금 50만원 당첨!',
    '주문이 확인되었습니다', '지금 무료 샘플을 받아보세요', '웹 세미나가 2시간 후 시작됩니다',
    '추가 현금을 쉽게 벌 수 있습니다', '계정 잔액 업데이트', '오늘 밤 플래시 세일 종료',
    '축하합니다! 100만원 상품권 당첨', '구매해 주셔서 감사합니다', '꿈의 휴가를 획득하세요!',
    '행사에 대한 독점 초대', '결제 영수증', '당신을 위한 특별 보너스',
    '구독 업데이트 알림', '무료 전자책 지금 받아가기', '경품 행사 마지막 호출',
    '비행 일정', '내일 정오 회의 알림', '축하합니다! 특별 제안 획득',
    '보안 업데이트: 이메일 확인 요청', '최신 기기에 대한 큰 할인 혜택', '계정 인증 완료',
    '회원 전용 특별 보상', '뉴스레터에 가입해 주셔서 감사합니다', '긴급: 즉각 조치 필요',
    '1년치 무료 식료품 당첨!', '승인 요청이 승인되었습니다', '오늘 모든 주문 50% 할인',
    '무료 체험을 지금 시작하세요', '특별 선물 포함', '알림: 결제 마감일',
    '서비스 요청이 처리되었습니다', '한정 특가: 놓치지 마세요', '혜택 업데이트 알림',
    '럭셔리 여행 패키지 당첨!', '중요: 선호 설정 업데이트', '회의 요약 첨부',
    '프로필을 완료하고 상품 받기', '계정이 일시 정지되었습니다', '보상을 받을 마지막 날',
    '배송 업데이트', '재방문 고객을 위한 특별 제안', '선호 브랜드 대폭 할인',
    '지금 캐시백을 받아가세요!', '프로그램 가입 초대', 'VIP 액세스 독점 제공',
    '거래 영수증', '생산성 향상을 위한 무료 팁', '긴급: 주소 확인 요청',
    '독점 기회를 놓치지 마세요', '지원 상태 검토 중', '여행 패키지 대폭 할인',
    '보고서 다운로드 가능', '축하합니다! VIP 혜택 활성화', '결제가 거부되었습니다',
    '지금 자리 확보하세요', '오늘 흥미로운 상품 당첨!', '알림: 중요한 문서 보류 중',
    '오늘 최대 80% 할인', '고객님을 위한 독점 할인', '계정을 무료로 업그레이드'
]

# title 리스트와 같은 길이로 is_spam 생성
is_spam = [1 if i % 3 == 0 else 0 for i in range(len(titles))]  # 길이를 titles와 동일하게 설정

# DataFrame 생성
data = pd.DataFrame({
    'title': titles,
    'is_spam': is_spam
})


# 2. 데이터 전처리
X = data['title']  # 제목 데이터
y = data['is_spam']  # 레이블 데이터
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # 데이터를 훈련/테스트 세트로 분리

# 3. 텍스트 벡터화
vectorizer = CountVectorizer()  # 단어 기반 벡터화
X_train_vec = vectorizer.fit_transform(X_train)  # 훈련 데이터를 벡터화
X_test_vec = vectorizer.transform(X_test)  # 테스트 데이터를 벡터화

# 4. 모델 학습
model = MultinomialNB()  # 나이브 베이즈 분류기
model.fit(X_train_vec, y_train)  # 모델 훈련

# 5. 예측 및 평가
y_pred = model.predict(X_test_vec)  # 테스트 데이터 예측
accuracy = accuracy_score(y_test, y_pred)  # 정확도 계산
print(f'Accuracy: {accuracy}')  # 정확도를 출력
print(classification_report(y_test, y_pred))  # 분류 보고서 출력

# 6. 새로운 제목 예측 및 결과 출력
new_titles = ['축 당첨 현금을 받아가세요', '안녕하세요 저는 현숙입니다 저랑 만나실래요?']  # 새 이메일 제목
new_titles_vec = vectorizer.transform(new_titles)  # 벡터화
predictions = model.predict(new_titles_vec)  # 스팸 여부 예측

# 결과 출력
for title, prediction in zip(new_titles, predictions):  # 제목과 예측 결과를 순회
    if prediction == 1:  # 예측이 1(스팸)이면
        print(f'"{title}" -> 스팸메일')
    else:  # 예측이 0(정상)이면
        print(f'"{title}" -> 스팸메일이 아닙니다')
