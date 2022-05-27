import pyautogui
import pyperclip 
#
# =======================마우스의 이동  모든 함수에서 duration 사용 가능 
# size = pyautogui.size() #현재 윈도우 창 사이즈를 배열로 반환 받음 0번째 가로 1번째 높이
# pyautogui.moveTo(100,100)#마우스를 해당 좌표로 이동시킴 왼쪽위가 x 0, y 0임
# pyautogui.moveTo(500,500,duration=2) # 마우스가 이동하는 과정을 보여줌 duration 에 들어간 숫자(초)동안 이동함
# pyautogui.move(100,100) #현재마우스가 있는 위치에서 x,y만큼 이동함 (상대좌표)
# pyautogui.position() #현재 마우스 위치를 리턴받음.

# #========================마우스 액션  모든 함수에서 duration 사용 가능 
# pyautogui.sleep(3) #3초동안 마우스 대기
# pyautogui.click(100,100) # 해당위치를 클릭함 duration 사용 가능 cilck = down + up
# pyautogui.mouseDown(x,y) # 마우스 누른상태 안에 좌표값 넣을 수 있음
# pyautogui.mouseUp(x,y) #마우스 누른거 뗀 상태 마우스 좌표 값 넣을 수 있음
# pyautogui.clickDouble() # 더블 클릭  pyautogui.clicks(click = n ) n번 클릭하라는 소리
# pyautogui.rightClick() #오른쪽 클릭  pyautogui.middleClick() 마우스 휠 클릭 
# pyautogui.drag(x,y) #현재 기준으로 xy로 드래그하는거임 To 붙이면 절대좌표 기준으로 이동 
# pyautogui.scroll(x) #양수이면 위 방향을 x만큼 스크롤 음수인경우 아래로 스크롤 

# #=========================마우스정보 
# pyautogui.mouseInfo() #해당 마우스 위치를 따라가면서 해당 마우스 좌표정보와 색상정보등 실시간으로 시각화 해줌
# #프로그램 동작중 멈추고 싶으면 마우스를 화면 끝으로 가져가면 프로그램 강제 중단 
# pyautogui.FAILSAFE() #마우스가 화면 끝으로 가져가도 프로램 중단되지 않음
# pyautogui.PAUSE = x #모든 동작에 x초 씩 slee()을 걸음

# #============================스크린 (픽셀값으로 해당 사진과 동일한 부분을 찾는거임)
# img = pyautogui.screenshot() 
# img.save("sca.png") # img 변수에 현재화면 스크린샷 찍고 sca.png 파일로 저장
# pyautogui.pixel(x,y) # 해당하는 좌표에 픽셀을 가져와서 리턴해줌 (해당픽셀에 RGB값을 줌)
# pyautogui.pixelMatchColor(x,y(r,g,b)) # 해당 좌표가 입력된 rgb값이 맞는지 판단 하여 boolean값 리턴

# #============================이미지 처리
# pyautogui.locateOnScreen("name.png") # name사진하고 동일한 화면부분을 찾아서 반환해줌 위치 가로넓이 세로넓이 이미지 없거나 미발견시 None 값 반환
# pyautogui.Click(pyautogui.locateOnScreen("name.png")) # 위 구문으로 찾고 바로 클릭가능
# pyautogui.locateAllOnScreen("name.png") #해당 사진하고 동일안 화면부분 찾아서 배열형태로 반환


# #============================이미지처리 속도개선
# pyautogui.locateOnScreen("name.png",grayscale = True)#다 흑백처리하고 하는거라 속도 30퍼 정도향상 정확도 조금 하락
# pyautogui.locateOnScreen("name.png",region=(x,y,h,w)) # 탐색 범위를 지정
# pyautogui.locateOnScreen("name.png",confidence = 0.9) #90퍼정도 비슷하면 찾아라 정확도 조정하는 구문 confidence

# #==============================윈도우 다루기
# fw = pyautogui.getActiveWindow() # 현재활성화된 창의 정보를 가져옴 리턴받음
# print(fw.title) #창의 제목정보를 프린트
# print(fw.size) #창의 사이즈를 프린트
# print(fw.left,fw.top.fw.right.fw.bottom) #창의 좌표정보를 프린트받음
# for i in pyautogui.getAllWindows():
#     i  # i값에 떠있는 창에 정보 전부 가져옴 배열 형태
# for i in pyautogui.getActiveWindowTitle("name"):
#     i # name이라는 이름을 갖는 창만 가져옴 
# fw.activate() # fw창을 앞으로 가져와서 활성화 시킴
# if fw.isMaximized : 
#       fw.maximize() # 현재 최대화 처리 되지 않았다면 maximize는 boolean값으로 리턴받음
# fw.close() # 창을 닫음

# #===============================키보드 다루기
# pyautogui.write("12345",intertval =1 ) #12345를 씀 interval 안에 들어간 숫자 달레이 초 
# pyautogui.write(["left","right","enter"]) #방향키 왼쪽 오른쪽하고 엔터 누름
# pyautogui.keyDown("shift") # 쉬프트 키 누름
# pyautogui.press("4") # 4 누름
# pyautogui.keyUp("shift") #쉬프트 키 뗌
# pyautogui.hotkey("shift","4") # 쉬프트 누른채로 4누르고 쉬프트 떼고 4뗌 추가해서 계속 연속적인 사용가능

# pip install pyperclip # 이거 설치해야 한글입력 가능
# import pyperclip
# pyperclip.copy("하이루")#하이루 복사한거  복사했으니깐 이거 붙여넣기해서 한글을 쓸 수 있음 pyautogui.hotkey("ctrl","v") 이용

# # ===================================메세지 박스
# pyautogui.countdown(3) #3초간 카운트 해줌 print 해줌
# pyautogui.alert("메세지","제목") #제목 이란 메세지 박스에 메세지란 팝업 창 띄움 
# pyautogui.confirm("계속 진행 하겠습니까?","제목") # OK Cancel 값으로 리턴받음
# pyautogui.prompt("파일명은?","입력") # 사용자로 부터 값을 입력받음 취소시 None 값을 받음
# pyautogui.password("비밀번호 입력","제목") # 입력하는 값 실시간으로 모자이크 처리 

#========================파일시스템1 (파일을 다루는 시스템)

# import os
# prinmt(os.getcwd())# 현재 작업 공간을 가져와서 프린트
# os.chdir("폴더 경로 이름 ") # 현재 작업공간을 바꾸는거임
# os.chdir("..") # 현재 작업공간에서 상위폴더로 이동하는것 ../.. 은 조부모 폴더로 가는것


#========================퀴즈
# 1. 그림판 실행 (단축키 :win + r, 입력값 : mspaint ) 하고 최대화
# 2. 텍스트 기능으로 텍스는 입력
# 3. 5초 대기후 종료 저장안함

pyautogui.hotkey("win","r")
pyautogui.write("mspaint")
pyautogui.press("Enter")
pyautogui.sleep(1)
paint = pyautogui.getActiveWindow()
print("이름",paint.title)
if paint.isMaximized == False:
    paint.maximize()


#pyautogui.mouseInfo()
pyautogui.click(397,86)
pyautogui.moveTo(300,300,duration=0.1)
pyautogui.click()
pyperclip.copy("5초후 프로그램 종료")
pyautogui.hotkey("ctrl","v")

pyautogui.sleep(3)
paint.close()
pyautogui.press("n")


