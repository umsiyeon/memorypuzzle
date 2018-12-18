FPS = 30 # 초당 프레임, 프로그램의 일반 속도
WINDOWWIDTH = 400 # 윈도우 가로
WINDOWHEIGHT = 300 # 윈도우 세로
REVEALSPEED = 7 # 상자가 보였다가 가려지는 속도
BOXSIZE = 40 # 상자의 가로, 세로사이즈
GAPSIZE = 10 # 상자사이의 간격
BOARDWIDTH = 4  # 상자의 가로 개수
BOARDHEIGHT = 3  # 상자의 세로 개수
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2) # 윈도우 가로 여백
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2) # 윈도우 세로 여백

# 색상 정의
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)

# 게임 기본 색상 셋팅
BGCOLOR = NAVYBLUE # 바탕화면색
LIGHTBGCOLOR = GRAY # 화면 깜빡일 때 사용할 색
BOXCOLOR = WHITE # 상자 색
HIGHLIGHTCOLOR = BLUE # 강조색

# 도형 변수 생성
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)