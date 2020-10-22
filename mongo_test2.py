import pymongo

conn = pymongo.MongoClient("localhost", 27017)
db = conn.test
collection = db.members

# rs = collection.find({"이름": "고길동"})

#################### 데이터 수정 ############################
# 아래처럼 이름을 고말똥으로 수정하는 경우 이름 필드외에 나머지 필드는 모두 삭제됨.
# 데이터를 날릴 수 있음.
# collection.update({"이름":"강길동"}, {"이름":"고말똥"})

# $set 을 이용하면 나머지 필드는 모두 존재함 
# collection.update({"이름":"김말똥"},{"$set":{"이름":"손흥민"}})

# 고길동 레코드(doc)가 여러개 있었지만 하나의 첫번째 레코드만 수정됨. multi= False(기본값)
# collection.update({"이름":"고길동"}, {"$set":{"이름":"손흥민"}})

# 여러개의 document를 동시에 수정
# collection.update({"이름":"고길동"}, {"$set":{"이름":"손흥민"}}, multi=True)

# collection.update({"이름":"손흥민"}, {"$set":{"별명":"축구짱"}})

# 이름 박지성이 없기 때문에 아무 변화가 없다.
# collection.update({"이름":"박지성"}, {"$set":{"별명":"박짱"}})

# 업데이트 대상이 존재하지 않을 경우 삽입, 존재하는 경우 수정하라는 옵션(upsert = True, update + insert)
# collection.update({"이름":"박지성"}, {"$set":{"별명":"박짱"}}, upsert = True)

####################### 데이터 삭제 #################################
# collection.remove({"이름": "박지성"})

# collection의 데이터가 모두 날아감. 잘못쓰면 망함
# collection.remove({})

# collection.delete_one({"이름": "손흥민"})
collection.delete_many({"이름": "손흥민"})
 




# for r in rs:
#     print(r)

