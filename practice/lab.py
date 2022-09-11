# 코드 테스트 및 실험 파일

lt = []
def delete_List(): #함수구현
  key = input('Input Data :')
  i = 0
  while(i < len(lt)):
    if(lt[i] == key):
      del lt[i]
    else:
      i = i +1
    
def append_List(): #함수구현
  key = input('Input Data :')
  lt.append(key)
def print_List(): #함수구현
  print(lt)
  pass
	
while True:
  print('1. Append List')
  print('2. Print List')
  print('3. delete List')
  print('4. Exit')

  key = input('Select Number [1~4] :')
  if key == '1':
    append_List()
  elif key == '2':
    print_List()
  elif key == '3':
    delete_List()
  else:
    break

print('\nThanks.')