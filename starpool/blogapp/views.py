from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Post

from userapp.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, CommentBox, Review
from django.http import HttpResponse
from django.http import JsonResponse

def home(request):
    posts = Post.objects.all().order_by('-id') # admin에서 생성한 공모전 post 개체 생성 
    return render(request, 'mainpage.html', {'posts':posts})

def detail(request, id):
    # pk값이 id인 Post 객체 하나를 가져와 post라는 변수에 담아줌
    post = get_object_or_404(Post, pk=id)
    comments = CommentBox.objects.filter(post=id).order_by('-id')
    context = {
        'post' : post,
        'comments': comments
    }
    return render(request, 'listpage.html', context)

# 평가해달라는 입력창
# 여기서 id가 필요힐까???
@login_required
def commentBox(request, id):
    error_message = None

    if request.method == "POST":
        post = get_object_or_404(Post, pk=id)
        comment_pw = request.POST.get('pw')
        content = request.POST.get('message')
        
        # 해당 내용들이 하나라도 없는 경우
        if not comment_pw or not content:
            error_message = '평가 코드와 내용을 입력해주세요.'
        else:
            comment = CommentBox.objects.create(
                post=post, # post필드에 해당게시물 할당
                comment_pw = comment_pw,
                content = content,
                writer = request.user #현재 로그인한 사용자
            )
            # 앱이름 안써서 한참..해맸다..
            return redirect('blog:detail', post.id)

# 평가보기 클릭시 보이는 평가디테일
# post:id, comment:id 둘다 가져옴
def comment_detail(request, id, comment_id):
    post = get_object_or_404(Post, pk=id)
    comment = get_object_or_404(CommentBox, id=comment_id)
    reviews = Review.objects.order_by('id')

    context = {
        'post':post,
        'comment': comment,
        'review' :reviews
    }
    return render(request, 'commentpage.html', context)

def comment_review(request, id, comment_id):

    if request.method == "POST":
        # url에 post:id 필요하니깐 
        post = get_object_or_404(Post, pk=id)
        comment = get_object_or_404(CommentBox, id=comment_id)
        
        rating = request.POST.get('rating')
        if rating is None:
            rating = 0  # 또는 다른 기본값 설정
        review_pw = request.POST.get('review_pw')
        review = request.POST.get('review')
        # 비밀번호 일치하는지 확인하기 위해서  comment_id 가져옴
        
        # 비번이 같을때
        review = Review.objects.create(
            comment=comment,
            writer=request.user,
            rating=rating,
            review_pw=review_pw,
            review=review
        )  
        # 저장
        return redirect('blog:comment_detail', id=post.id, comment_id=comment.id)
