from django.db import models


class User(models.Model):
    # 사용자 id, pw
    user_id = models.CharField("아이디", unique=True, max_length=20)
    user_pw = models.CharField("비밀번호", max_length=20)
    
    class Meta:
        db_table = 'user'  # 테이블 이름을 설정합니다.

class Board(models.Model):
    # 글의 제목, 내용, 작성일, 마지막 수정일
    
    # delete=models.CASCADE : 관련 User 인스턴스가 삭제되면 해당 Board 인스턴스도 함께 삭제
    # related_name="boards" : uSER 모델에서 boards 모델에 역참조할 때 사용(boards <-(역참조)-- user)
    # null=True : 이건 이유를 잘 모르겠음
    # verbose_name : 레이블의 이름을 설정
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards", null=True, verbose_name="아이디")
    title = models.CharField("제목", max_length=50, null=False)
    content = models.TextField("내용", null=False)
    # dt_created = models.DateTimeField("작성일", auto_now_add=True, null=False)
    # dt_modified = models.DateTimeField("수정일", auto_now=True, null=False)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    # user를 User 클래스의 foreingnKey로 지정
    # 일대다의 경우 다 모델에 foreignkey를 설정해야 됨
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment", verbose_name="아이디")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comment", null=True, verbose_name="게시물")
    content = models.TextField("내용", blank=True)