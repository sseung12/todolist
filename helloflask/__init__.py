from flask import Flask,render_template,request,redirect,url_for
import sqlite3
app =Flask(__name__)
app.debug=True



@app.route("/")
def main():
  return render_template("index.html")

# 완료한 내역 넘기기
@app.route("/done")
def done():
  page = request.args.get('page',type=int,default=1)
  conn = sqlite3.connect("./static/db/todolistdb.db")
  perpage=10
  page_indexing=3
  total=""
  with conn:
    cursor = conn.cursor()
    sql = "select count(*) from list where done =1"
    cursor.execute(sql)
    total = cursor.fetchone()
    data=(perpage,(page-1)*perpage)
    sql  = "select * from list where done = 1 limit ? offset ?"
    result = cursor.execute(sql,data)
  total = list(total)
  total = total[0]

  page_count =total //perpage 
  if total % perpage >=1:
    page_count= page_count+1
  
  # index 숫자 처리
  if page%page_indexing==0:
    first_index =page-page_indexing
    last_index=page
  else:
    first_index=page-(page%page_indexing)
    last_index= page+(page_indexing-(page%page_indexing))

  if page_count<=last_index:
    last_index =page_count
  
  
  # prev_index = 0 if condition == 0 else (prev_index = first_index-3)
  if first_index-perpage <0:
    prev_index=1
  else:
    prev_index=first_index-perpage
  if last_index + perpage >page_count:
    next_index=page_count
  else:
    next_index=last_index+1
  # view에 넘길 데이터
  paging_itmes ={"page" :page,
                "total_page" :total ,
                "page_count":page_count,
                "first_index":first_index,
                "last_index":last_index,
                "prev_index":prev_index,
                "next_index":next_index
                }


  return render_template("done.html",result=result,paging_items=paging_itmes)

@app.route("/doing")
def doing():
  page =request.args.get('page',type=int, default=1)

  conn = sqlite3.connect("./static/db/todolistdb.db")
  perpage = 10
  page_indexing=3
  
  total=""
  with conn:
    cursor = conn.cursor()
    sql= "select count(id) from list where done =0"
    cursor.execute(sql)
    total =cursor.fetchone()
    data=(perpage,(page-1)*perpage)
    sql = "select * from list where done =0 limit ? offset ?"
    result = cursor.execute(sql,data)

  total = list(total)
  total = total[0]
  # page 갯수
  page_count =total //perpage 
  if total % perpage >=1:
    page_count= page_count+1
  
  # index 숫자 처리
  if page%page_indexing==0:
    first_index =page-page_indexing
    last_index=page
  else:
    first_index=page-(page%page_indexing)
    last_index= page+(page_indexing-(page%page_indexing))

  if page_count<=last_index:
    last_index =page_count
  
  
  # prev_index = 0 if condition == 0 else (prev_index = first_index-3)
  if first_index-perpage <0:
    prev_index=1
  else:
    prev_index=first_index-perpage
  if last_index + perpage >page_count:
    next_index=page_count
  else:
    next_index=last_index+1
  # view에 넘길 데이터
  paging_items ={"page" :page,
                "total_page" :total ,
                "page_count":page_count,
                "first_index":first_index,
                "last_index":last_index,
                "prev_index":prev_index,
                "next_index":next_index
                }

  return render_template("doing.html",result=result,paging_items=paging_items)


@app.route("/ajax",methods=['POST'])
def ajax():
  print("함수 들어옴")
  
  result = request.form["id"]

  conn = sqlite3.connect("./static/db/todolistdb.db")

  with conn:
    cur = conn.cursor()
    sql ="update list set done = 1 where id ="+result
    cur.execute(sql)
    conn.commit

  return result  

if __name__ == '__main__':
  app.run()