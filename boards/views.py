from .models import User, Board, Comment
from .serializers import BoardSerializer, UserSerializer, CommentSerializer
from rest_framework import generics, mixins
from django.shortcuts import render # user id, pw 입력 칸 만들기
from rest_framework.views import APIView
from rest_framework.response import Response

class UserAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer, operation_id="유저 생성")
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDeleteAPIView(APIView):
    @swagger_auto_schema(operation_id="사용자 삭제")
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "유저가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"message": "해당 유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

class BoardAPIView(APIView):
    @swagger_auto_schema(request_body=BoardSerializer, operation_id="게시글 조회")
    def get(self, request):
        # 게시글 객체 전부 가져옴(orm)
        boards = Board.objects.all()
        # boards 객체들 직렬화
        # many=True : 여러 개의 객체를 직렬화하는 경우 사용
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
        
    @swagger_auto_schema(request_body=BoardSerializer, operation_id="게시글 작성")
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        # BoardSerializer에 전달된 데이터가 유효한지를 검사
        if serializer.is_valid():
            # 입력받은 내용들 중 user_id 추출
            author_id = serializer.validated_data.get('author').id
            # id == author_id인 유저 객체가 하나라도 있다면 true
            author_exists = User.objects.filter(id=author_id).exists()
            # 유저 객체가 있다면 저장 후 응답
            if author_exists:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "존재하지 않는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)

class BoardDeleteAPIView(APIView):
    @swagger_auto_schema(operation_id="게시글 삭제")
    # 게시판 id를 입력 받아서 존재 하는 게시글이라면 삭제
    def delete(self, request, board_id):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            # 존재하는 게시글이라면 board 객체 추출
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return Response({"message": "존재하지 않는 게시글입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 게시글 삭제
        board.delete()
        return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    

class CommentAPIView(APIView):
    @swagger_auto_schema(operation_id="댓글 조회")
    # 게시글 id 입력 받음
    def get(self, request, board_id):
        # board_id에 속해 있는 모든 comment를 가져옴
        try:
            comments = Comment.objects.filter(board_id=board_id)
        except Comment.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글입니다."}, status=status.HTTP_404_NOT_FOUND)

        # 게시글에 존재하는 댓글들 직렬화
        serializer = CommentSerializer(comments, many=True)
        # 직렬화된 댓글들 전부 response
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentPostAPIView(APIView):
    @swagger_auto_schema(request_body=CommentSerializer, operation_id="댓글 작성")
    def post(self, request):
        board_id = request.data.get('board')
        # 입력받은 board_id가 존재하는지 확인
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # board_id가 존재한다면 입력받은 댓글 정보들을 직렬화
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # board 때문에 매개 변수를 넣고 save
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentUpdateAPIView(APIView):
    @swagger_auto_schema(request_body=CommentSerializer, operation_id="댓글 수정")
    def put(self, request, comment_id):
        serializer = CommentSerializer(data=request.data)
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "존재하지 않는 댓글입니다."}, status=status.HTTP_404_NOT_FOUND)

        board_id = request.data.get('board_id')
        # 게시글 번호로 해당 게시글이 존재하는지 확인
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return Response({"message": "존재하지 않는 게시글입니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteAPIView(APIView):
    def delete(self, request, comment_id, author_id):
        author = Comment.objects.get(id=author_id)
        try:
            # 주어진 댓글 ID로 댓글을 찾습니다.
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"message": "해당 댓글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 댓글 작성자와 요청을 보낸 사용자가 동일한지 확인합니다.
        if comment.author_id != author.author_id:
            return Response({"message": "댓글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 댓글 삭제
        comment.delete()

        return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_200_OK)

