import random, pygame, sys
from pygame.locals import *
from class_failscore.playerfailscore import *

print("원하는 난이도를 선택하세요 (E:easy, H:hard):")
mod = input()
if mod == 'E' or mod == 'e':
    from mod.mod_easy import *
elif mod == 'H' or mod == 'h':
    from mod.mod_hard import *
else:
    print("옳바르지 않은 입력입니다. 게임을 재실행하십시오")
    pygame.time.wait(3000)
    quit()

def main():
    global FPSCLOCK, DISPLAYSURF, BOARDWIDTH, BOARDHEIGHT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # 마우스 이벤트 발생시 x좌표
    mousey = 0 # 마우스 이벤트 발생시 y좌표
    pygame.display.set_caption('Memory Puzzle')

    mainBoard = getRandomizedBoard() # 게임판의 상태를 나타내는 데이터 구조 반환
    revealedBoxes = generateRevealedBoxesData(False) # 게임판 안의 어떤 상자가 닫혀 있는지 나태내는 데이터 구조 반환(2차원 리스트)

    firstSelection = None
    # 첫 번째 클릭일 경우, None에서 (x, y) 값 저장
    # 두 번째 클릭일 경우, (x, y) 값이 이미 저장
    # 이를 이용하여 첫 번째 클릭인지, 두번째 클릭인지 구분

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    # 게임 루프
    while True:
        mouseClicked = False # 클릭하면 True, 클릭안하면 False

        DISPLAYSURF.fill(BGCOLOR) # 게임바탕화면 색 칠하기
        drawBoard(mainBoard, revealedBoxes) # 현재의 게임판 상태 그리기

        # 이벤트 처리 루프
        for event in pygame.event.get():
            # QUIT 이벤트 또는 Esc키를 누루면 프로그램 종료
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # 마우스가 움직이면 mousex, mousey에 위치를 저장
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            # 마우스를 클릭하면 mousex, mousey에 위치를 저장하고, mouseClicked값 True
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        # 게임판에 어떤 상자를 클릭했는지 게임판의 좌표 나타냄
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        # 마우스 이벤트에 따른 처리
        if boxx != None and boxy != None:
            # 해당 위치의 상자를 연 적이 없을 때
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            # 해당 위치의 상자를 연 적이 없고, 마우스 클릭했을 때
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True # 상자가 보이도록 설정
                # 상자를 처음 클릭했을 경우
                if firstSelection == None:
                    firstSelection = (boxx, boxy)
                # 상자를 두 번째 클릭했을 경우
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    # 모양과 색 중 하나라도 다를 경우
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000) # 1초 대기
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)]) # 두 상자 닫기
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False # 첫 번째 상자 위치 값 False로 변경
                        revealedBoxes[boxx][boxy] = False # 두 번째 상자 위치 값 False로 변경
                        player.count(1)

                    # 플레이어가 이긴 경우
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000) # 2초 대기

                        # 게임판 재설정
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # 잠시 동안 게임판의 상자를 열어서 보여준다
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000) # 1초 대기

                        # 게임 재시작
                        startGameAnimation(mainBoard)
                    firstSelection = None # 첫 번째 클릭 값 재설정

        # 화면을 다시 그린 다음 시간 지연을 기다린다
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# 열린 상자에 대한 데이터 구조 만들기
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

# 모든 가능한 색에서 가능한 모양의 목록을 생성
def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # 아이콘 리스트의 순서를 랜덤으로 설정
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # 필요한 아이콘 수 계산
    icons = icons[:numIconsUsed] * 2 # 각각의 짝 만들기
    random.shuffle(icons)

    # 아이콘이 랜덤하게 그려진 상자 만들기
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board

# 리스트를 2차원 리스트로 만들기
def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

# 게임판의 좌표계를 픽셀좌표계로 변경
def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)

# 상자를 픽셀 좌표계에서 게임판 좌표계로 변환
def getBoxAtPixel(x, y): # x는 y는
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

# 아이콘 그리기
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # 1/4지점
    half =    int(BOXSIZE * 0.5)  # 1/2지점

    left, top = leftTopCoordsOfBox(boxx, boxy) # 보드의 좌표에서 픽셀의 좌표를 얻는다
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half),
                                                 (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

# 모양과 색상 값 불러오기
def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

# 열리거나 닫힌 상태의 상자 그리기
# 상자는 아이템 2개짜리 리스트이며, 상자의 x, y 위치를 가진다
def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # 닫힌상태면 덮개 그리기
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

# 상자가 열리는 애니메이션
def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

# 상자가 닫히는 애니메이션
def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

# 모든 상자 그리기
def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # 닫힌 상자 그리기
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # 열린 상자 그리기(아이콘 그리기)
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

# 닫힌 상자를 클릭했을 때, 파란색으로 클릭한 상자 표시
def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

# 게임시작할 때, 무작위로 상자 열어서 보여주는 애니메이션
def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(6, boxes)


    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

# 게임 종료되면 화면 깜빡이는 애니메이션
def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    BASICFONT = pygame.font.SysFont("malgungothic", 25, bold=True)
    gameOverSurf = BASICFONT.render(('clicked wrong boxes : ' + str(player.total()) + ' times'), True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT * 5 / 6)

    for i in range(13):
        color1, color2 = color2, color1 # 색 바꾸기
        DISPLAYSURF.fill(color1)
        DISPLAYSURF.blit(gameOverSurf, gameOverRect)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

# 모든 상자가 열린 경우, True 반환
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False # 모든 상자를 열지 못했으면 Fasle 반환
    return True


if __name__ == '__main__':
    main()