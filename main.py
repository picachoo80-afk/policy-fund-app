import streamlit as st
from datetime import date
import csv, os

# =========================
# 기본 페이지(브랜딩)
# =========================
st.set_page_config(
    page_title="광명파트너스 | 정책자금 맞춤 도우미",
    page_icon="📊",
    layout="wide",
)

BRAND = "광명파트너스"
BLOG_URL = "https://blog.naver.com/kwangmyung80"
CONTACT_PHONE = "1877-2312"  # 대표번호

# =========================
# 스타일
# =========================
st.markdown("""
<style>
.block-container {padding-top: 1.25rem; padding-bottom: 2rem;}
.card {
  border: 1px solid #e6e6e6; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; background: #fff;
}
.result-card{
  border:1px solid #E5EAF2; border-radius:14px; padding:14px 16px; margin:10px 0; background:#F9FBFF;
}
.badge {display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; margin-left:6px;
  background:#EEF2FF; color:#334155; border:1px solid #E5E7EB;}
.small {font-size: 13px; color:#6b7280;}
hr.soft {border:none; border-top:1px dashed #e5e7eb; margin:10px 0;}
.sidebar-links a {display:block; margin:6px 0;}
</style>
""", unsafe_allow_html=True)

# =========================
# 사이드바
# =========================
with st.sidebar:
    st.markdown("### 🧭 사용 방법")
    st.markdown("- ① 기본정보 입력 → ② 추가 체크 → ③ **제출**")
    st.markdown("- 결과 하단의 **안내문구**와 **상담 신청**도 확인해 주세요.")
    st.markdown("---")
    st.markdown("### ☎ 상담/문의")
    st.markdown('<div class="sidebar-links">', unsafe_allow_html=True)
    st.markdown(f"- 대표번호: **{CONTACT_PHONE}**")
    st.markdown(f"- 블로그: [광명파트너스 네이버 블로그]({BLOG_URL})")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("👉 상담은 무료이며, 실제 신청은 고객님 명의로만 진행됩니다.")

# =========================
# 헤더
# =========================
st.markdown("## 📊 광명파트너스 – 정책자금 맞춤 도우미")
st.caption("정부 정책자금 진단 및 상담 연계 서비스")
st.markdown(f"📞 대표번호: **1877-2312**  ·  🔗 블로그: [바로가기]({BLOG_URL})")
st.markdown("---")

# =========================
# 유틸
# =========================
def years_between(d: date, ref: date | None = None) -> float:
    if ref is None: ref = date.today()
    return (ref - d).days / 365.25

def months_between(d: date, ref: date | None = None) -> float:
    if ref is None: ref = date.today()
    return (ref.year - d.year) * 12 + (ref.month - d.month) + (ref.day - d.day) / 30

def fmt_money(n: int) -> str:
    try:
        return f"{int(n):,}"
    except:
        return str(n)

def build_date_or_error(year: int, month: int, day: int, label: str):
    try:
        return date(year, month, day), None
    except Exception:
        return None, f"{label}: 올바르지 않은 날짜입니다."

# =========================
# 입력 폼
# =========================
with st.form("basic_form", clear_on_submit=False):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ① 기본정보")

    r1c1, r1c2 = st.columns([1,1])
    with r1c1:
        biz_type = st.radio("사업자 유형", ["개인사업자", "법인사업자"], index=0, horizontal=True)
    with r1c2:
        region = st.text_input("사업장 지역 (예: 경기도 안산시)", "경기도 안산시")

    st.markdown("**대표자 생년월일**")
    c_y, c_m, c_d = st.columns(3)
    with c_y:
        birth_year = st.number_input("연(Year)", 1900, 2025, 1980, step=1)
    with c_m:
        birth_month = st.number_input("월(Month)", 1, 12, 1, step=1)
    with c_d:
        birth_day = st.number_input("일(Day)", 1, 31, 1, step=1)

    st.markdown("**개업 연월일**")
    s_y, s_m, s_d = st.columns(3)
    with s_y:
        biz_year = st.number_input("연(Year)", 1900, 2025, 2024, step=1, key="biz_y")
    with s_m:
        biz_month = st.number_input("월(Month)", 1, 12, 1, step=1, key="biz_m")
    with s_d:
        biz_day = st.number_input("일(Day)", 1, 31, 1, step=1, key="biz_d")

    col1, col2 = st.columns(2)
    with col1:
        credit_nice = st.number_input("NICE 신용점수", 0, 1000, 700, step=1)
        sales = st.number_input("연 매출 (원)", 0, step=1_000_000, value=100_000_000)
        st.caption(f"입력값: {fmt_money(sales)} 원")
    with col2:
        credit_kcb  = st.number_input("KCB 신용점수", 0, 1000, 680, step=1)
        loan_amount = st.number_input("현재 대출 총액 (원)", 0, step=1_000_000, value=0)
        st.caption(f"입력값: {fmt_money(loan_amount)} 원")

    assets = st.number_input("자산 총액 (부동산·주식·자동차·임차보증금 등)", 0, step=1_000_000, value=0)
    st.caption(f"입력값: {fmt_money(assets)} 원")

    c3a, c3b, c3c = st.columns([1,1,1])
    with c3a:
        biz_sector = st.text_input("사업자등록증상 **업종** (예: 음식점업)", "음식점업")
    with c3b:
        biz_item   = st.text_input("사업자등록증상 **업태** (예: 한식)", "한식")
    with c3c:
        employees  = st.number_input("4대보험 직원 수", 0, step=1, value=0)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ② 추가 체크")

    st.markdown("**혁신성장촉진자금 - 혁신형 해당 여부**")
    colA1, colA2, colA3 = st.columns(3)
    with colA1:
        flag_export = st.checkbox("수출 실적 있음")
        flag_growth10 = st.checkbox("최근 2년 연속 매출 10%↑")
    with colA2:
        flag_smart_factory = st.checkbox("스마트공장 도입")
        flag_strong_local  = st.checkbox("강한소상공인/로컬크리에이터")
    with colA3:
        flag_postgrad = st.checkbox("졸업후보기업")

    st.markdown("**혁신성장촉진자금 - 일반형 해당 여부**")
    colB1, colB2, colB3, colB4 = st.columns(4)
    with colB1:
        flag_smart_tech = st.checkbox("스마트기술 활용")
    with colB2:
        flag_baeknyeon  = st.checkbox("백년소공인/백년가게")
    with colB3:
        flag_social     = st.checkbox("사회적경제기업")
    with colB4:
        flag_academy    = st.checkbox("신사업창업사관학교 수료(1년 이내)")

    st.markdown("**일시적 경영애로 사유**")
    flag_distress = st.checkbox("매출 10% 이상 감소(또는 예외사유 증빙)")

    submitted = st.form_submit_button("✅ ③ 제출하고 분석 결과 보기")

# =========================
# 제출 처리/분석
# =========================
if submitted:
    birth, err1 = build_date_or_error(int(birth_year), int(birth_month), int(birth_day), "대표자 생년월일")
    biz_start, err2 = build_date_or_error(int(biz_year), int(biz_month), int(biz_day), "개업 연월일")

    # 에러 표시
    if err1: st.error(err1)
    if err2: st.error(err2)

    if not (err1 or err2):
        # 입력 요약
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🧾 입력 요약")
        csum1, csum2, csum3 = st.columns([1,1,1])
        with csum1:
            st.write(f"- 사업자 유형: **{biz_type}**")
            st.write(f"- 지역: **{region}**")
            st.write(f"- 업종/업태: **{biz_sector} / {biz_item}**")
        with csum2:
            st.write(f"- 대표자 생년월일: **{birth.isoformat()}**")
            st.write(f"- 개업 연월일: **{biz_start.isoformat()}**")
            st.write(f"- 직원 수: **{employees}명**")
        with csum3:
            st.write(f"- NICE/KCB: **{credit_nice} / {credit_kcb}**")
            st.write(f"- 연 매출: **{fmt_money(sales)}원**")
            st.write(f"- 대출/자산: **{fmt_money(loan_amount)}원 / {fmt_money(assets)}원**")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 🔎 분석 결과")

        # 파생값
        age = int(years_between(birth))
        biz_months = months_between(biz_start)

        results = []

        # ---------------- 최소 게이트 ----------------
        # - 연 매출 1,000만원 미만 → 결과 없음
        # - 신용(NICE 515 이하 또는 KCB 454 이하) → 결과 없음
        # - 개업 3개월 미만 → 결과 없음
        if (sales >= 10_000_000) and (credit_nice > 515) and (credit_kcb > 454) and (biz_months >= 3):

            # 1) 일반경영안정자금 : 신용 기준만 반영
            if (credit_nice >= 665) and (credit_kcb >= 630):
                results.append({
                    "name": "일반경영안정자금",
                    "range": "2,000만원 ~ 7,000만원",
                    "rate": "연 3.28% (기준 2.68% +0.6%p)",
                    "notes": "은행 및 보증 조건에 따라 실금리는 달라질 수 있습니다.",
                    "link": "https://ols.sbiz.or.kr/"
                })

            # 2) 신용취약 소상공인자금 : 신용 구간 충족
            if (515 <= credit_nice <= 839) or (515 <= credit_kcb <= 839):
                results.append({
                    "name": "신용취약 소상공인자금",
                    "range": "최대 3,000만원 (연 1회)",
                    "rate": "연 4.28% (기준 2.68% +1.6%p)",
                    "notes": "신용관리교육 필수. 세부 한도/조건은 심사에 따라 달라집니다.",
                    "link": "https://ols.sbiz.or.kr/"
                })

            # 3) 청년 전용 자금(고용연계/창업 등) : 업력 조건 삭제(전역 게이트 3개월만 유지)
            if age <= 39 and (credit_nice >= 620 and credit_kcb >= 620):
                results.append({
                    "name": "청년 전용 자금(공고별)",
                    "range": "공고별 한도 (예: 1~2억원)",
                    "rate": "연 2.68% (기준 2.68% +0.0%p)",
                    "notes": "세부요건·금리는 공고마다 상이합니다.",
                    "link": "https://www.kosmes.or.kr/"
                })

            # 4) 혁신성장촉진자금 (혁신형/일반형)
            if any([flag_export, flag_growth10, flag_smart_factory, flag_strong_local, flag_postgrad,
                    flag_smart_tech, flag_baeknyeon, flag_social, flag_academy]):
                results.append({
                    "name": "혁신성장촉진자금",
                    "range": "운전 2억원 / 시설 10억원 (예시)",
                    "rate": "연 3.08% (기준 2.68% +0.4%p)",
                    "notes": "혁신형/일반형 증빙 필요. 금리는 유형·공고에 따라 달라질 수 있습니다.",
                    "link": "https://www.sbiz24.kr/"
                })

            # 5) 일시적 경영애로자금 : 사유 체크 시만 노출
            if flag_distress:
                results.append({
                    "name": "일시적 경영애로자금",
                    "range": "최대 7,000만원",
                    "rate": "연 2.68% (기준 2.68% +0.0%p)",
                    "notes": "매출감소 등 일시적 애로 사유가 필요합니다.",
                    "link": "https://ols.sbiz.or.kr/"
                })

        # ---------------- 결과 출력 ----------------
        if results:
            for r in results:
                st.markdown(f"""<div class="result-card">
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <div style='font-size:16px; font-weight:800;'>{r['name']}</div>
                        <span class="badge">분석</span>
                    </div>
                    <div class='small'>예상 한도: <b>{r['range']}</b></div>
                    <div class='small'>예상 금리: <b>{r['rate']}</b></div>
                    <hr class="soft" />
                    <div class='small'>{r['notes']}</div>
                    <div style='margin-top:6px;'>
                        👉 <a href="{r.get('link','')}" target="_blank">신청 안내 바로가기</a>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            # 게이트 미충족이거나 조건 미적합
            msg = []
            if sales < 10_000_000:
                msg.append("연 매출 1,000만원 미만")
            if credit_nice <= 515 or credit_kcb <= 454:
                msg.append("신용점수 낮음(NICE 515 이하 또는 KCB 454 이하)")
            if months_between(biz_start) < 3:
                msg.append("개업 3개월 미만")
            if msg:
                st.info("현재 조건에 맞는 자금을 찾지 못했습니다. " + " · ".join(msg))
            else:
                st.info("현재 조건에 맞는 자금을 찾지 못했습니다.")

        # ---------------- 안내(파란박스) ----------------
        st.markdown("""
<div style="
    border-left:6px solid #1f6feb;
    background:#eaf2ff;
    padding:14px 16px;
    border-radius:8px;
    margin: 12px 0 4px 0;">
  <b>안내</b><br/>
  💡 정책자금 승인 여부와 조건은 신용 점수나 매출뿐 아니라 <b>사업계획서·기술력·대표자 상황</b> 등에 따라 달라질 수 있습니다.
  또한 <b>복수 자금 활용</b>, <b>시차를 둔 추가 신청</b> 등 운용 방식에 따라 결과가 달라질 수 있습니다.<br/><br/>
  ※ 본 자료는 참고용이며, 실제 심사는 기관 정책 및 신청인 신용 상태에 따라 달라질 수 있습니다.
</div>
""", unsafe_allow_html=True)

        # ---------------- 상담 신청(연락처 수집 / CSV 저장) ----------------
        st.markdown("### 📞 상담 신청하기")
        st.caption("정확한 심사 가능 여부와 맞춤 전략은 상담을 통해 확인할 수 있습니다.")
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("이름")
            phone = st.text_input("연락처 (휴대폰 번호)")
            memo = st.text_area("추가 메모 (선택)")
            submit_contact = st.form_submit_button("📩 상담 신청하기")

        if submit_contact:
            if not name or not phone:
                st.error("이름과 연락처는 필수 입력입니다.")
            else:
                file_exists = os.path.isfile("contacts.csv")
                with open("contacts.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["이름", "연락처", "메모", "신청일"])
                    writer.writerow([name, phone, memo, date.today().isoformat()])
                st.success("✅ 상담 신청이 접수되었습니다. 곧 연락드리겠습니다.")

        # ---------------- 하단 상담/문의(간단 노출) ----------------
        st.markdown("---")
        st.subheader("📞 상담 및 문의 채널")
        st.markdown("- 대표번호: **1877-2312**")
        st.markdown("- 카카오채널: [바로 연결하기](https://open.kakao.com/o/shxgLPsh)")
        st.markdown("- 블로그: [광명파트너스 네이버 블로그](https://blog.naver.com/kwangmyung80)")


# 푸터
st.caption(f"ⓒ {date.today().year} {BRAND}")

