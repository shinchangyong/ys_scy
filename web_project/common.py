from functools import wraps
from web_project import session, redirect, request, url_for, ALLOWED_EXTENSIONS
from string import digits, ascii_lowercase, ascii_uppercase
import random

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("id") is None or session.get("id") == "":
            # request.url은 현재 url을 의미함.
            return redirect(url_for("member.member_login", next_url=request.url))
        return f(*args, **kwargs)
    return decorated_func

# 파일이 유효한지 체크하는 함수
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

# 파일명을 random하게 생성해주는 함수
def rand_generator(length=8):
    char = ascii_lowercase + ascii_uppercase + digits
    return "".join(random.sample(char, length))