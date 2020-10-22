# from web_project import app
# from web_project import request, redirect, url
# from web_project import login_required

from web_project import *
from flask import Blueprint
from flask import send_from_directory

bp = Blueprint("board", __name__, url_prefix="/board")
# 플라스크의 Blueprint 객체는 라우트를 구조적으로
# 관리할 수 있도록 하는 클래스
# Blueprint( "이름", __name__, url_prefix='/')

@bp.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = "{}.jpg".format(rand_generator())
            savefilepath = os.path.join(app.config["BOARD_IMAGE_PATH"], filename)
            file.save(savefilepath)
            return url_for("board.board_images", filename = filename)

@bp.route("/images/<filename>")
def board_images(filename):
    return send_from_directory(app.config["BOARD_IMAGE_PATH"], filename)

@bp.route("/list")
def list():

    # 페이지 값
    # page 매개변수가 없을 경우 기본값을 1로 설정, 그자료형은 int형
    page = request.args.get("page", default=1, type=int)

    # 한페이지당 몇개의 게시글을 출력할지를 받아옴.(인자로 받아와서 처리함)
    limit = request.args.get("limit", 7, type=int)

    # search 변수의 기본값을 -1로 설정
    search = request.args.get("search", -1, type=int)

    # 기본값 없이 문자열로 받아옴.
    keyword = request.args.get("keyword", "", type=str)

    # 최종 쿼리를 완성해서 보내는 객체
    query = { }

    # 검색어를 추가할 리스트 객체
    # $regex => SQL의 like연산자 기능, 검색어 '길' => 홍길동, 갓길, 김영길...
    # 길이 포함된 문자열을 모두 검색
    search_list = []

    if search == 0:
        search_list.append({"title":{"$regex": keyword}})
    elif search == 1:
        search_list.append({"contents":{"$regex": keyword}})
    elif search == 2:
        search_list.append({"title":{"$regex": keyword}})
        search_list.append({"contents":{"$regex": keyword}})
    elif search == 3:
        search_list.append({"name":{"$regex": keyword}})

    if len(search_list) > 0 :
        query = {"$or": search_list }

    '''
        {
            "$or" :[
                {"title":{"$regex": "손흥민"}},
                {"title":{"$regex": "김말똥"}},
                {"title":{"$regex": "홍길동"}},
            ]
        }
        {
            "$and" :[
                {"title":{"$regex": "손흥민"}},
                {"title":{"$regex": "김말똥"}},
                {"title":{"$regex": "홍길동"}},
            ]
        }
    '''

    print(query)

    board = mongo.db.board
    # docs = board.find({}).skip((page-1)*limit).limit(limit)
    docs = board.find(query).skip((page-1)*limit).limit(limit).sort("regdate", -1)

    ########################## 페이징 처리를 위한 변수 설정 ######################
    # 리스트의 전체 갯수
    # tot_count = board.find({}).count()
    tot_count = board.find(query).count()

    # 마지막 페이지의 수를 구하기
    last_page_num = math.ceil(tot_count / limit)

    # 페이지 블럭을 5개씩 표현
    block_size = 5

    # 현재 블럭의 위치 : 0, 1
    block_num = int((page - 1) / block_size)

    # 블럭의 시작값 : 첫번째 블럭일 경우에는 시작값 : 1, 두번째 블럭의 시작값 : 6
    block_start = int((block_size * block_num) + 1)

    # 블럭의 마지막 값 : 첫번째 블럭의 마지막값 : 5
    # 블럭의 마지막 값 : 두번째 블럭의 마지막값 : 10

    block_last = block_start + (block_size - 1)


    # docs = board.find({})
    return render_template("bbs/list.html", docs = docs,
                                        limit = limit,
                                        page = page,
                                        block_start = block_start,
                                        block_last = block_last,
                                        last_page_num = last_page_num,
                                        search = search,
                                        keyword=keyword,
                                        title="리스트")


##############################
# @app.route("/view")
# def board_view():
    # idx = request.args.get("idx")

# fancy url, clean url 표기 방식(보안적인 측면 고려, 사용편의성 고려한 표기 방식)
@bp.route("/view/<idx>")
@login_required
def board_view(idx):
    # if session.get("id") is None:
    #     return redirect(url_for("member_login"))

    # get 방식으로 전달되는 값을 받아오기
    page = request.args.get("page")
    search = request.args.get("search")
    keyword = request.args.get("keyword")

    if idx is not None:
        board = mongo.db.board

        # data = board.find_one({"_id":ObjectId(idx)})
        # return_documet=False는 조회수가 업데이트 된 후(보고난후)에 변수에 할당
        # return_documet=True는 볼때 바로 변수에 바로 할당됨.
        data = board.find_one_and_update({"_id":ObjectId(idx)}, {"$inc":{"hit":1}}, return_document=False)
        
        if data is not None:
            result = {
                "id" : data.get("_id"),
                "name" : data.get("name"),
                "title" : data.get("title"),
                "contents" : data.get("contents"),
                "regdate" : data.get("regdate"),
                "hit":data.get("hit"),
                "writer_id":data.get("writer_id", "")
            }

            return render_template("bbs/view.html", result = result, page=page, search=search, keyword=keyword, title="글 상세보기" )
    return abort(404) # 500 : Internal Server Error

@bp.route('/write', methods=["GET", "POST"])
@login_required
def board_write():
    if request.method == "POST":
        filename = None
        if "attachFile" in request.files:
            file = request.files["attachFile"]
            if file and allowed_file(file.filename):
                filename = check_filename(file.filename)
                file.save(os.path.join(app.config["BOARD_ATTACH_PATH"], filename))

                
        name = request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")

        #print(name, title, contents)

        # UTC는 국제 표준시(참고: GMT(Greenwich Mean Time) - 그리니치 평균시, 세계 협정시 )
        # UTC와 GMT는 혼용되어 사용됨, 시간차가 거의 없음.(소수점의 차이)

        # UTC Time은 밀리세컨드(millisecond: 1000분의 1초)로 표현되기 때문 * 1000을 해주고 
        # 소수점이 나오는 걸 방지하기 위해 round로 반올림 해준다.
        current_utc_time = round(datetime.utcnow().timestamp()*1000)

        # board 컬렉션 생성해서 board라는 이름으로 받음
        board = mongo.db.board

        post_data = {
            "name":name,
            "title": title,
            "contents":contents, 
            "regdate": current_utc_time,
            #글수정, 삭제시 본인의 글인지 확인하기 위한 용도
            "writer_id":session.get("id"), 
            "hit" : 0          
        }

        doc = board.insert_one(post_data)
        print(doc.inserted_id)

        # 렌더링을 할 경우에는 insered_id는 Object(객체)이므로 문자열로 형변환 해야 한다.        
        # return str(doc.inserted_id)

        return redirect(url_for("board.board_view", idx=doc.inserted_id))

    else:    
        return render_template("bbs/write.html",title="글쓰기")

@bp.route("/modify/<idx>", methods=["GET", "POST"])
def modify(idx):
    if request.method == "GET":
        board  = mongo.db.board
        data = board.find_one({"_id": ObjectId(idx)})

        if data is None:
            flash("게시물이 존재하지 않습니다.")
            return redirect(url_for("board.list"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template("bbs/modify.html", data=data, title="글수정")
            else:
                flash("글수정 권한이 없습니다.")
                return render_template("bbs/modify.html", data=data, title="글수정")
    else:
        print("POST")
        title = request.form.get("title")
        contents = request.form.get("contents")
        delOlFile = request.form.get("delOldFile", "")

        board = mongo.db.board
        data = board.find_one({"_id":ObjectId(idx)})

        if session.get("id") == data.get("writer_id"):
            filename = None
            if "attachFile" in request.files:
                file = request.file["attachFile"]
                if file and allowed_file(file.filename):
                    filename = check_filename(file.filename)
                    file.save(os.path.join(app.config["BOARD_ATTACH_FILE_PATH"], filename))

                    if data.get("attachFile"):
                        board_delete_attach_file(data.get("attachFile"))
            else:
                if delOlFile == "on":
                    filename = None
                    if data.get("attachFile"):
                        board_delete_attach_file(data.get("attachFile"))
                    else:
                        filename = data.get("attachFile")

            board.update_one({"_id":ObjectId(idx)}, {"$set":{
                                    "title":title, 
                                    "contents":contents,
                                    "attachFile":filename
                                    }
                                })
            flash("수정되었습니다!!!")
            return redirect(url_for("board.board_view", idx = idx))
        else:
            flash("글수정 권한이 없습니다.")
            return redirect(url_for("board.list"))

@bp.route("/delete/<idx>")
def delete(idx):
    board = mongo.db.board
    data = board.find_one({"_id":ObjectId(idx)})
    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id":ObjectId(idx)})
        flash("삭제되었습니다.")

    else:
        flash("삭제권한이 없습니다!!!")
    return redirect(url_for("board.list"))
