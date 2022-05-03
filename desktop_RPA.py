import pyautogui 

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
# pyautogui.scroll(ㅌ) #양수이면 위 방향을 x만큼 스크롤 음수인경우 아래로 스크롤 

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


