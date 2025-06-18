import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
import os

class VocPdfGenerator:
    def __init__(self):
        # 한글 폰트 설정
        self.setup_korean_font()
        
        # 더미 데이터 정의
        self.requester_names = [
            "김철수", "이영희", "박민수", "최지연", "정성호", "한미영", "조대현", "신보라",
            "윤상철", "임수진", "강태우", "오혜원", "홍길동", "송미경", "전다영", "노태준"
        ]
        
        self.customer_companies = [
            "삼성전자 고객센터", "LG전자 AS센터", "현대자동차 콜센터", "SK텔레콤 고객상담실",
            "KB국민은행 고객센터", "신한은행 콜센터", "롯데마트 고객지원팀", "이마트 상담센터",
            "GS칼텍스 고객상담실", "포스코 고객센터", "한국전력 콜센터", "NH농협은행 상담실",
            "CJ제일제당 고객센터", "아모레퍼시픽 상담팀", "네이버 고객지원", "카카오 고객센터"
        ]
        
        self.group_companies = ["A회사", "B회사", "C회사", "D회사", "E회사"]
        
        self.voc_categories = ["고객사 귀책", "그룹사 귀책", "단순 문의"]
        
        self.processing_results = ["대응 완료", "대응 실패", "진행 중"]
        
        # VOC 내용과 대응 내용 템플릿
        self.voc_templates = {
            "음성인식": [
                "AI 상담사가 고객의 말을 제대로 인식하지 못하는 경우가 빈번하게 발생합니다.",
                "STT 변환 시 정확도가 떨어져 고객 불만이 증가하고 있습니다.",
                "소음이 있는 환경에서 음성 인식률이 현저히 떨어집니다."
            ],
            "응답속도": [
                "AI 상담사의 응답 시간이 너무 오래 걸려 고객들이 불편을 호소합니다.",
                "시스템 처리 속도가 느려 대기시간이 길어지고 있습니다.",
                "피크타임에 응답 지연이 심각한 수준입니다."
            ],
            "대화품질": [
                "AI 상담사의 답변이 부정확하거나 관련성이 떨어집니다.",
                "고객의 질문에 대한 맥락 이해도가 부족합니다.",
                "반복적인 질문에 대해 동일한 답변만 제공합니다."
            ],
            "시스템오류": [
                "AI 상담 시스템이 갑자기 종료되는 현상이 발생합니다.",
                "특정 키워드 입력 시 시스템 에러가 발생합니다.",
                "데이터베이스 연결 오류로 서비스 중단이 발생했습니다."
            ],
            "인터페이스": [
                "관리자 페이지의 UI가 직관적이지 않아 사용이 어렵습니다.",
                "모바일 환경에서 화면 표시에 문제가 있습니다.",
                "브라우저 호환성 문제로 일부 기능이 작동하지 않습니다."
            ]
        }
        
        self.response_templates = {
            "고객사 귀책": [
                "해당 이슈는 고객사의 네트워크 환경 설정 문제로 확인되었습니다. 네트워크 관리자와 협의하여 방화벽 설정을 조정해주시기 바랍니다.",
                "고객사에서 제공한 학습 데이터의 품질 문제로 인한 현상입니다. 추가 데이터 제공이 필요합니다.",
                "고객사의 하드웨어 사양이 권장 사양에 미치지 못하여 발생한 문제입니다. 시스템 업그레이드를 권장드립니다."
            ],
            "그룹사 귀책": [
                "저희 시스템의 버그로 확인되어 긴급 패치를 진행하였습니다. 현재 정상 작동하고 있습니다.",
                "AI 모델의 학습 데이터 부족으로 인한 문제였습니다. 추가 학습을 통해 성능을 개선하였습니다.",
                "서버 용량 부족으로 인한 지연 현상이었습니다. 서버 증설을 통해 해결하였습니다."
            ],
            "단순 문의": [
                "해당 기능은 다음 버전 업데이트에서 제공될 예정입니다. 정확한 일정은 별도 안내드리겠습니다.",
                "요청하신 기능은 현재 베타 테스트 중이며, 안정화 후 정식 서비스에 반영하겠습니다.",
                "문의하신 내용에 대해 상세한 매뉴얼을 첨부드립니다. 추가 문의사항이 있으시면 언제든 연락주세요."
            ]
        }

    def setup_korean_font(self):
        """한글 폰트 설정"""
        try:
            # Windows의 경우 맑은 고딕 폰트 사용
            font_path = "C:/Windows/Fonts/malgun.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('MalgunGothic', font_path))
                addMapping('MalgunGothic', 0, 0, 'MalgunGothic')  # normal
                self.korean_font = 'MalgunGothic'
                return
        except:
            pass
        
        try:
            # macOS의 경우 애플 고딕 폰트 사용
            font_path = "/System/Library/Fonts/AppleGothic.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('AppleGothic', font_path))
                addMapping('AppleGothic', 0, 0, 'AppleGothic')
                self.korean_font = 'AppleGothic'
                return
        except:
            pass
        
        try:
            # Linux의 경우 Noto Sans CJK 폰트 사용
            font_paths = [
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
            ]
            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('NotoSansCJK', font_path))
                    addMapping('NotoSansCJK', 0, 0, 'NotoSansCJK')
                    self.korean_font = 'NotoSansCJK'
                    return
        except:
            pass
        
        # 기본 폰트 (한글 지원 안됨)
        print("Warning: 한글 폰트를 찾을 수 없습니다. 영문으로 표시됩니다.")
        self.korean_font = 'Helvetica'

    def generate_voc_data(self):
        """VOC 데이터 생성"""
        requester = random.choice(self.requester_names)
        customer_company = random.choice(self.customer_companies)
        group_company = random.choice(self.group_companies)
        voc_category = random.choice(self.voc_categories)
        processing_result = random.choice(self.processing_results)
        
        # VOC 내용 생성
        voc_type = random.choice(list(self.voc_templates.keys()))
        voc_content = random.choice(self.voc_templates[voc_type])
        
        # 대응 내용 생성
        response_content = random.choice(self.response_templates[voc_category])
        
        # 처리 일자 생성 (최근 3개월 내)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        processing_date = start_date + timedelta(days=random.randint(0, 90))
        
        return {
            "요청자명": requester,
            "요청자_회사": customer_company,
            "VOC_내용": voc_content,
            "VOC_대응_내용": response_content,
            "VOC_대응_그룹사": group_company,
            "VOC_분류_카테고리": voc_category,
            "처리_결과": processing_result,
            "처리_일자": processing_date.strftime("%Y-%m-%d"),
            "문서_번호": f"VOC-{processing_date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        }

    def create_pdf(self, data, filename):
        """PDF 파일 생성"""
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # 제목
        c.setFont(self.korean_font, 16)
        c.drawString(50, height - 50, "AI 상담 서비스 VOC 대응 보고서")
        
        # 구분선
        c.line(50, height - 70, width - 50, height - 70)
        
        y_position = height - 100
        line_height = 25
        
        # 기본 정보 섹션
        c.setFont(self.korean_font, 12)
        c.drawString(50, y_position, "기본 정보")
        y_position -= line_height
        
        c.setFont(self.korean_font, 10)
        basic_info = [
            f"문서 번호: {data['문서_번호']}",
            f"처리 일자: {data['처리_일자']}",
            f"요청자명: {data['요청자명']}",
            f"요청자 회사: {data['요청자_회사']}",
            f"대응 그룹사: {data['VOC_대응_그룹사']}"
        ]
        
        for info in basic_info:
            c.drawString(70, y_position, info)
            y_position -= 20
        
        y_position -= 10
        
        # VOC 분류 정보
        c.setFont(self.korean_font, 12)
        c.drawString(50, y_position, "VOC 분류 정보")
        y_position -= line_height
        
        c.setFont(self.korean_font, 10)
        classification_info = [
            f"VOC 분류 카테고리: {data['VOC_분류_카테고리']}",
            f"처리 결과: {data['처리_결과']}"
        ]
        
        for info in classification_info:
            c.drawString(70, y_position, info)
            y_position -= 20
        
        y_position -= 20
        
        # VOC 내용
        c.setFont(self.korean_font, 12)
        c.drawString(50, y_position, "VOC 내용")
        y_position -= line_height
        
        c.setFont(self.korean_font, 10)
        # 긴 텍스트를 여러 줄로 나누기
        voc_content = data['VOC_내용']
        max_width = width - 140
        words = voc_content.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if c.stringWidth(test_line, self.korean_font, 10) < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        for line in lines:
            c.drawString(70, y_position, line)
            y_position -= 15
        
        y_position -= 20
        
        # VOC 대응 내용
        c.setFont(self.korean_font, 12)
        c.drawString(50, y_position, "VOC 대응 내용")
        y_position -= line_height
        
        c.setFont(self.korean_font, 10)
        # 대응 내용도 여러 줄로 나누기
        response_content = data['VOC_대응_내용']
        words = response_content.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if c.stringWidth(test_line, self.korean_font, 10) < max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        for line in lines:
            c.drawString(70, y_position, line)
            y_position -= 15
        
        # 푸터
        c.setFont(self.korean_font, 8)
        c.drawString(50, 50, f"생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(width - 200, 50, "AI 상담 서비스 운영팀")
        
        c.save()

    def generate_multiple_pdfs(self, count=50, output_folder="voc_reports"):
        """여러 개의 PDF 파일 생성"""
        # 출력 폴더 생성
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"폴더 '{output_folder}'가 생성되었습니다.")
        
        generated_files = []
        print(f"{count}개의 PDF 파일을 생성 중...")
        
        for i in range(count):
            # 데이터 생성
            data = self.generate_voc_data()
            
            # 파일 이름 생성 (번호 패딩)
            filename = f"voc_report_{i+1:03d}.pdf"
            filepath = os.path.join(output_folder, filename)
            
            # PDF 생성
            self.create_pdf(data, filepath)
            generated_files.append(filepath)
            
            # 진행상황 표시
            if (i + 1) % 10 == 0:
                print(f"{i + 1}/{count} 완료...")
        
        print(f"\n{count}개의 PDF 파일이 '{output_folder}' 폴더에 생성되었습니다.")
        return generated_files

    def generate_single_pdf(self, filename="voc_report_sample.pdf"):
        """단일 PDF 파일 생성"""
        data = self.generate_voc_data()
        self.create_pdf(data, filename)
        return data

# 사용 예시
if __name__ == "__main__":
    generator = VocPdfGenerator()
    
    # 50개의 PDF 파일 생성
    generated_files = generator.generate_multiple_pdfs(count=50, output_folder="voc_reports")
    
    print(f"\n생성된 파일 목록:")
    for i, file in enumerate(generated_files[:5]):  # 처음 5개만 표시
        print(f"  {file}")
    if len(generated_files) > 5:
        print(f"  ... 외 {len(generated_files) - 5}개 파일")
    
    print("\n필요한 라이브러리 설치:")
    print("pip install reportlab")