from .models import User, Board, Comment
from .serializers import BoardSerializer, BoardDetailSerializer, UserSerializer, CommentSerializer, CommentDetailSerializer
from rest_framework import generics

class UserAPIView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = UserSerializer

# ListCreateAPIView : 조회, 생성
class BoardAPIView(generics.ListCreateAPIView):
    queryset = Board.objects.all() # Board 모델의 모든 레코드 가져오는 django ORM

    # serializer_class : 클래스 기반 뷰에서 사용
    # serializer : 함수 기반 뷰에서 사용
    serializer_class = BoardSerializer
    
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    
    # 사용자의 인증 방식을 설정
    #authentication_classes = [TokenAuthentication]
    
    # 사용자의 권한을 설정하는 데 사용
    # IsAuthenticatedOrReadOnly : 로그인을 안했다면 ReadOnly
    #permission_classes = [IsAuthenticatedOrReadOnly]
        
# DestroyAPIView : 삭제
class BoardDetailAPIView(generics.DestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    #authentication_classes = [TokenAuthentication]
    # IsOwnerOrReadOnly : 계정 주인이 아니면 ReadOnly
    #permission_classes = [IsOwnerOrReadOnly]
    
    # create : 요청을 처리하는 메서드로 오버라이딩
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        request.data['author'] = user.id
        return super().create(request, *args, **kwargs)
    
# ListCreateAPIView : 조회, 생성
class CommentAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# RetrieveUpdateDestroyAPIView : 수정, 삭제
class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    
    