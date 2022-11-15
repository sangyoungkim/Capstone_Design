from django.shortcuts import HttpResponse
from datetime import datetime
from Capstone_Design.get_stock_info import RT_search_text, keyword_stock_news_naver
# from Capstone_Design.test import a, b, c, rt
from Capstone_Design.prediction_stock_info import recommended_stock



index1 = 0
now = datetime.now()

rt = RT_search_text()
a, b, c = keyword_stock_news_naver(RT_search_text(),True,1,7)
recom = 'none'
rbf = 'none'
cross = 'none'
if len(a) == 0:
  a = ['none']
  b = [['none']]
  c = [[['none']]]

def index(request):
  return html(request, a[0])


def realtime_search():
  cont = ''
  for i in rt:
    cont += f'<li>{i}</li>'
  return cont

def select_rt(id_in):
  global index1
  cont = ''
  cnt = 0
  if a[0] == 'none':
    cont += f'<div class="none">현재 실시간 검색어와 연관된 주식이 없습니다<div>텅</div></div>'
    return cont
  cont += f'<div class="top box1"><select id="selextList" onchange="if(this.value) location.href=(this.value);">'
  for i in a:
    if i == id_in:
      index1 = cnt
      cont += f'<option value="/{i}" selected>{i}</option>'
    else:
      cont += f'<option value="/{i}">{i}</option>'
      cnt += 1
  cont += f'</select></div>'
  return cont

def stock_cont():
  global index1, recom, rbf, cross
  cont = ''
  cnt = 0
  if a[0] == 'none':
    return cont
  for i in b[index1]:
    recom, rbf, cross = recommended_stock(i,3)
    print("======================",rbf)
    cnt2 = 0
    cont += f'''<div class="stock_box">
      <div class="stock">#{i}</div>
      <div class="left">
        <div class="title"><span class="highlight">NEWS</span></div>'''
    for j in c[index1][cnt]:
      if '제목' in j and '링크' in j and '내용' in j:
        cont+=f'''<div class="box1 art2"><a href="{j['링크']}">
          <h2>{j['제목']}</h2>
          <div class="art2_cont" id="{i+str(cnt2)}">{j['내용']}</div>
          </a>
        </div>'''
      if '사진' in j:
        cont+= f'''<style>
          .stock_box .left #{i+str(cnt2)}:hover {{
            background-image: url('{j['사진']}');
            color: transparent;
            background-repeat: no-repeat;
            background-size: 100% 100%;
          }}
        </style>
        '''
      cnt2 += 1
    cont += f'''
      </div>
      <div class="right">
        <div class="title"><span class="highlight">GRAPH</span></div>'''
    if recom == 'none' and rbf == 'none' and cross == 'none':
      cont += f'''<div class="box1 none">해당 주식은 해외 주식으로 판단되며 데이터가 제공되지 않습니다.<br><a href="https://www.google.com/finance/quote/.IXIC:INDEXNASDAQ?hl=ko">해외 주식 보러가기</a></div>
      <div class="title"><span class="highlight">ANALYSIS</span></div>   
        <div class="box1 none">해당 주식은 해외 주식으로 판단되며 데이터가 제공되지 않습니다.<br><a href="https://www.google.com/finance/quote/.IXIC:INDEXNASDAQ?hl=ko">해외 주식 보러가기</a></div>
      </div>
    </div>'''
    else:
      cont+= f'''
        <div class="box1 graph" onclick='zoom(this)' style="background-image: url('static/images/{i}.png')">클릭 시 확대/축소</div><div class="graph_title hide">{i}</div>
        <div class="title"><span class="highlight">ANALYSIS</span></div>   
        <div class="box1 analysis">
          <div class="anl_cont">이동평균선 배열도 분석 결과 : <span>{recom}</span>(으)로 판단됩니다.<br>이동평균선 크로스 분석 결과 : <span>{cross}</span>(으)로 판단됩니다.<br>다음날 주가 예측(RBF) : <span>{rbf}</span>원</div>
        </div>
      </div>
    </div>'''
    cnt += 1
  return cont

def html(repuest, id):
  global index1, now
  html = f'''
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css" rel="stylesheet">
    <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square-neo.css" rel="stylesheet">
    <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square-round.css" rel="stylesheet">
    <link href="https://hangeul.pstatic.net/hangeul_static/css/NanumJungHagSaeng.css" rel="stylesheet">
    <link rel="stylesheet" href="../static/css/style.css">
    <title>공대 속 라이프</title>
  </head>
  <body>
    <header>
      <div class="wrap_header">
        <div class="left">
          <div class="title">공대  속 라이프</div>
          <div class="text">실시간 검색어와 연관된 주식 종목을 찾아 그래프 분석 및 머신 러닝을 사용하여 종목의 익일 주가 예측값을 제공하는 사이트입니다.   <br>모든 분석 결과는 100%의 정확도를 보장하지 않습니다. 또한 주가 예측 값은 어디까지나 단순 예측일 뿐이니 해당 주식의 매수 여부는 직접 판단해주시길 바랍니다. 주식을 처음 접하는 분들이나 개미투자자, 또는 실시간 주식 동향에 관심이 있는 투자자 분들께 도움이 되길 바랍니다.
            </div>
        </div>
        <div class="right">
            <div class="title">실시간 검색어</div>
            <ol>
              {realtime_search()}
            </ol>
            <div class="date">{now.strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
      </div>
    </header>
    <section>
      {select_rt(id)}
      {stock_cont()} 
      <script>
        function zoom(e) {{
          var elem1 = document.getElementsByClassName('graph_text');
          var elem2 = document.getElementsByClassName('graph_title');
          if (e.classList.contains('zoom_in')){{
            e.classList.remove('zoom_in');
            elem1[0].classList.add('hide');
            elem2[0].classList.add('hide');
          }} else {{
            e.classList.add('zoom_in');
            elem1[0].classList.remove('hide');
            elem2[0].classList.remove('hide');
          }}
        }}
      </script> 
    <div class="graph_text hide">
        <h2>이동평균선이란?</h2>
        일정 기간 동안 가격들의 평균을 연결한 선을 말합니다. 
        <small>(예 - 20일 이동평균선 = 20일간의 주가를 평균낸 값)</small>
        <ul>
          <li>단기 이동 평균선 : 5일, 10일, 20일 등 - 투자 심리를 파악하는데 용이함</li>
          <li>중기 이동 평균선 : 60일, 90일 - 시장의 수급 상황이나 추세릐 전환을 파악하는데 사용함</li>
          <li>장기 이동 평균선 : 120일, 180일, 240일 - 전반적인 경기 상황을 보여줌</li>
        </ul><br>
        <h2>이동평균선을 이용한 분석 방법</h2>
        <h4>크로스 분석</h4>
        <ul>
              <li>골든 크로스 : 단기 이동 평균선이 장기 이동평균선을 밑에서 위로 돌파하는 시점. 상승의 추세로 전환을 의미하기 때문에 매수 신호로 해석될 수 있음</li>
              <li>데드 크로스 : 골든 크로스와 반대. 단기 이동 평균선이 장기 이동 편균선을 위에서 아래로 관통하는 시점. 이는 하락 추세로의 전환을 의미하기 때문에 매도 신호로 해석될 수 있음</li>
              <small>※ 단기 : 5/20일선, 중기 : 20/60일선, 장기 : 60/120일선 비교</small>
        </ul>
        <h4>배열도 분석</h4>
        <ul>
              <li>정배열 : 단기 > 중기 > 장기 이동평균선 순서로 위에서 아래로 정 배열된 상태. 일반적으로 상승 추세로 전환을 뜻함</li>
              <li>역배열 : 장기 > 중기 > 단기 이동평균선 순서로 위에서 아래로 정 배열된 상태</li>
        </ul>
        <small>※ 모든 분석은 절대적이지 않은 점 알려드립니다.</small>
        <small class="ref"><b>출처 : <a href="https://www.nanumtrading.com/fx-%EB%B0%B0%EC%9A%B0%EA%B8%B0/%EA%B8%B0%EC%88%A0%EC%A0%81-%EB%B6%84%EC%84%9D/06-%EC%9D%B4%EB%8F%99-%ED%8F%89%EA%B7%A0%EC%84%A0/">nanumtrading</b></a></small>
      </div>
    </section>
    <footer>
      <div>COPYRIGHT Ⓒ 공대 속 라이프</div>
    </footer>
  </body>
  </html>'''
  return HttpResponse(html)


