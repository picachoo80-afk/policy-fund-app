import streamlit as st
from datetime import date

# ============= App Meta & Style ======================
st.set_page_config(page_title="정책자금 맞춤 도우미", page_icon="💰", layout="wide")

# Minimal CSS for cards, badges, spacing
st.markdown("""
<style>
/* tighter overall */
.block-container {padding-top: 1.25rem; padding-bottom: 2rem;}
/* section card */
.card {
  border: 1px solid #e6e6e6; border-radius: 12px; padding: 16px 18px; margin-bottom: 14px; background: #fff;
}
.card h4 {margin: 0 0 10px 0; font-weight: 700;}
/* result card */
.result-card{
  border:1px solid #E5EAF2; border-radius:14px; padding:14px 16px; margin:10px 0; background:#F9FBFF;
}
.badge {
  display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; font-weight:600; margin-left:6px; background:#EEF2FF; color:#334155; border:1px solid #E5E7EB;
}
.kicker {color:#64748B; font-size:13px;}
.small {font-size: 13px; color:#6b7280;}
hr.soft {border:none; border-top:1px dashed #e5e7eb; margin:10px 0;}
/* subtle label */
label[data-baseweb="checkbox"] p, label p {font-size: 14px;}
/* fix link button spacing in sidebar */
.sidebar-links a {display:block; margin:6px 0;}
</style>
""", unsafe_allow_html=True)

# ============= Sidebar ===============================
with st.sidebar:
    st.markdown("### 🧭 빠른 안내")
    st.markdown(
        "- ① 기본정보 입력 → ② 추가 체크 → ③ **제출**\n"
        "- 결과 하단의 **안내 문구**와 **상담 링크** 확인"
    )
    st.markdown("---")
    st.markdown("### ☎ 상담/문의", help="텍스트 링크만 노출 (요청 반영)")
    st.markdown('<div class="sidebar-links">', unsafe_allow_html=True)
    st.markdown("- 대표번호: **1877-2312**")
    st.markdown("- 카카오채널: [바로 연결하기](https://open.kakao.com/o/shxgLPsh)")
    st.markdown("- 블로그: [광명파트너스 블로그](https://blog.naver.com/kwangmyung80)")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("👉 상담은 무료이며, 실제 신청은 고객님 명의로만 진행됩니다.")

# ============= Header ================================
st.markdown("## 💰 정책자금 맞춤 도우미")
st.markdown(
    '<span class="kicker">고객 기본정보를 바탕으로 조건에 맞는 정책자금을 간단 추천합니다.</span>',
    unsafe_allow_html=True
)

# progress-like step hint
c1, c2, c3 = st.columns([1,1,1])
with c1: st.markdown("**① 기본정보**")
with c2: st.markdown("**② 추가체크**")
with c3: st.markdown("**③ 제출 & 결과**")

st.markdown("")

# ============= Utils ================================
def years_between(d: date, ref: date | None = None) -> float:
    if ref is None: ref = date.today()
    return (ref - d).days / 365.25

def months_between(d: date, ref: date | None = None) -> float:
    if ref is None: ref = date.today()
    return (ref.year - d.year) * 12 + (ref.month - d.month) + (ref.day - d.day) / 30

def fmt_money(n: int) -> str:
    return f"{n:,}"

def build_date_or_error(year: int, month: int, day: int, label: str):
    try:
        return date(year, month, day), None
    except Exception:
        return None, f"{label}: 올바르지 않은 날짜입니다."

# ============= Form ================================
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
        birth_year = st.number_input("연(Year)", min_value=1900, max_value=2025, value=1980, step=1)
    with c_m:
        birth_month = st.number_input("월(Month)", min_value=1, max_value=12, value=1, step=1)
    with c_d:
        birth_day = st.number_input("일(Day)", min_value=1, max_value=31, value=1, step=1)

    st.markdown("**개업 연월일**")
    s_y, s_m, s_d = st.columns(3)
    with s_y:
        biz_year = st.number_input("연(Year) ", min_value=1900, max_value=2025, value=2024, step=1, key="biz_y")
    with s_m:
        biz_month = st.number_input("월(Month) ", min_value=1, max_value=12, value=1, step=1, key="biz_m")
    with s_d:
        biz_day = st.number_input("일(Day) ", min_value=1, max_value=31, value=1, step=1, key="biz_d")

    st.markdown('<hr class="soft">', unsafe_allow_html=True)

    c2a, c2b = st.columns(2)
    with c2a:
        credit_nice = st.number_input("NICE 신용점수", min_value=0, max_value=1000, value=700, step=1)
        sales = st.number_input("연 매출 (원)", min_value=0, step=1_000_000, value=100_000_000)
        st.caption(f"입력값: {fmt_money(sales)} 원")
    with c2b:
        credit_kcb  = st.number_input("KCB 신용점수",  min_value=0, max_value=1000, value=680, step=1)
        loan_amount = st.number_input("현재 대출 총액 (원)", min_value=0, step=1_000_000, value=0)
        st.caption(f"입력값: {fmt_money(loan_amount)} 원")

    assets = st.number_input("자산 총액 (부동산·주식·자동차·임차보증금 등)", min_value=0, step=1_000_000, value=0)
    st.caption(f"입력값: {fmt_money(assets)} 원")

    st.markdown('<hr class="soft">', unsafe_allow_html=True)

    c3a, c3b, c3c = st.columns([1,1,1])
    with c3a:
        biz_sector = st.text_input("사업자등록증상 **업종** (예: 음식점업)", "음식점업")
    with c3b:
        biz_item   = st.text_input("사업자등록증상 **업태** (예: 한식)", "한식")
    with c3c:
        employees  = st.number_input("4대보험 직원 수", min_value=0, step=1, value=0)

    st.markdown('</div>', unsafe_allow_html=True)

    # ----- 추가 체크 (혁신/일반/애로) -----
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

    st.markdown('<hr class="soft">', unsafe_allow_html=True)

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

    st.markdown('<hr class="soft">', unsafe_allow_html=True)

    st.markdown("**일시적 경영애로 사유**")
    flag_distress = st.checkbox("매출 10% 이상 감소(또는 예외사유 증빙)")

    st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("✅ ③ 제출하고 결과 보기")

# ============= Submit Handling ======================
if submitted:
    birth, err1 = build_date_or_error(int(birth_year), int(birth_month), int(birth_day), "대표자 생년월일")
    biz_start, err2 = build_date_or_error(int(biz_year), int(biz_month), int(biz_day), "개업 연월일")

    if err1: st.error(err1)
    if err2: st.error(err2)

    if not err1 and not err2:
        # Summary
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

        st.markdown("### ✅ 간단 추천 결과")

        # Derived
        age = int(years_between(birth))
        biz_years = years_between(biz_start)
        biz_months = months_between(biz_start)
        sales_억 = sales / 100_000_000

        results = []

        # ---- Gate: 최소 조건 ----
        if (sales >= 10_000_000) and (credit_nice > 515) and (credit_kcb > 454) and (biz_months >= 3):
            # 1) 일반경영안정자금 (간접/대리대출)
            if (biz_years >= 1 and sales_억 <= 5 and credit_nice >= 665 and credit_kcb >= 630):
                results.append({
                    "name": "소상공인진흥공단 일반경영안정자금",
                    "why": "업력 1년↑ · 매출 5억원↓ · 신용(NICE 665↑, KCB 630↑)",
                    "limit": "2,000만~7,000만원",
                    "docs": ["사업자등록증명(홈택스)", "부가세과세표준증명", "임대차계약서"],
                    "link": "https://ols.sbiz.or.kr/"
                })

            # 2) 신용취약 소상공인자금 (직접)
            if (sales_억 <= 3 and ((515 < credit_nice <= 839) or (454 < credit_kcb <= 839))):
                results.append({
                    "name": "신용취약 소상공인자금",
                    "why": "매출 3억원↓ · 신용(NICE/KCB 515~839 구간)",
                    "limit": "최대 3,000만원",
                    "docs": ["사업자등록증명", "소득금액증명", "부가세과세표준증명"],
                    "link": "https://ols.sbiz.or.kr/"
                })

            # 3) 중진공 청년전용 창업자금 (간접)
            if (age <= 39 and biz_years < 1 and credit_nice >= 620 and credit_kcb >= 620):
                results.append({
                    "name": "중진공 청년전용 창업자금",
                    "why": "만 39세↓ · 업력 1년↓ · 신용(NICE/KCB 각 620↑)",
                    "limit": "최대 7,000만원(심사 별도)",
                    "docs": ["사업계획서", "주민등록등본", "사업자등록증명"],
                    "link": "https://www.kosmes.or.kr/"
                })

            # 4) 법인 운전자금 (간접/보증·협약)
            if (biz_type == "법인사업자" and sales_억 >= 1):
                results.append({
                    "name": "법인 운전자금(보증부/협약)",
                    "why": "법인 · 매출 1억원↑",
                    "limit": "3,000만원~",
                    "docs": ["법인등기부등본", "법인인감증명서", "재무제표"],
                    "link": "https://www.kodit.co.kr/"
                })

            # 5) 혁신성장촉진자금 - 혁신형 (간접/운전자금)
            if any([flag_export, flag_growth10, flag_smart_factory, flag_strong_local, flag_postgrad]):
                results.append({
                    "name": "혁신성장촉진자금(혁신형·운전자금)",
                    "why": "혁신형 요건(수출/매출성장/스마트공장/강한소상공인·로컬/졸업후보기업 중 1개↑)",
                    "limit": "운전자금 최대 2억원(예시)",
                    "docs": ["사업계획서", "혁신형 증빙"],
                    "link": "https://www.sbiz24.kr/"
                })

            # 6) 혁신성장촉진자금 - 일반형 (간접/운전자금)
            if any([flag_smart_tech, flag_baeknyeon, flag_social, flag_academy]):
                results.append({
                    "name": "혁신성장촉진자금(일반형·운전자금)",
                    "why": "일반형 요건(스마트기술/백년소·가게/사회적경제/사관학교 수료 중 1개↑)",
                    "limit": "운전자금 최대 1억원(예시)",
                    "docs": ["사업계획서", "일반형 증빙"],
                    "link": "https://www.sbiz24.kr/"
                })

            # 7) 일시적경영애로자금 (직접/운전자금)
            if (sales_억 < 1.04 and biz_years < 7 and flag_distress):
                results.append({
                    "name": "일시적경영애로자금(직접·운전자금)",
                    "why": "연매출 1억 400만원↓ · 업력 7년↓ · 경영애로",
                    "limit": "최대 7,000만원(예시)",
                    "docs": ["사업자등록증명", "매출 감소 증빙"],
                    "link": "https://ols.sbiz.or.kr/"
                })

        # ---- Render results (cards) ----
        if results:
            for r in results:
                with st.container():
                    st.markdown(f"""<div class="result-card">
                    <div style='display:flex;justify-content:space-between;align-items:center;'>
                        <div style='font-size:16px; font-weight:800;'>{r['name']}</div>
                        <span class="badge">추천</span>
                    </div>
                    <div class='small'>사유: {r['why']}</div>
                    <hr class="soft" />
                    <div><b>예상 가능 금액:</b> {r['limit']}</div>
                    <div style='margin-top:6px;'><b>필요 서류</b></div>
                    <ul style='margin-top:4px;'>
                        {''.join([f"<li class='small'>{d}</li>" for d in r['docs']])}
                    </ul>
                    <a href="{r['link']}" target="_blank">신청/안내 바로가기</a>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("현재 입력 조건에 맞는 자금을 찾지 못했습니다. 조건을 조정하거나 상담을 권장드립니다.")

        # ---- 파란 박스 안내 (상담 안내 위) ----
        st.info(
            "💡 정책자금 승인 여부와 조건은 단순 점수나 매출뿐 아니라 "
            "사업계획서·기술력·대표자 상황 등에 따라 달라질 수 있습니다. "
            "또한 복수 자금 활용, 시차를 둔 추가 신청 등 운용 방식에 따라 결과가 달라질 수 있습니다.\n\n"
            "※ 본 자료는 참고용이며, 실제 심사는 기관 정책 및 신청인 신용 상태에 따라 달라질 수 있습니다."
        )

        # ---- 상담/문의 (텍스트 링크) ----
        st.markdown("---")
        st.subheader("📞 상담 및 문의 채널")
        st.markdown("- 대표번호: **1877-2312**")
        st.markdown("- 카카오채널: [바로 연결하기](https://open.kakao.com/o/shxgLPsh)")
        st.markdown("- 블로그: [광명파트너스 블로그](https://blog.naver.com/kwangmyung80)")
        st.caption("👉 상담은 무료이며, 실제 신청은 고객님 명의로만 진행됩니다.")
