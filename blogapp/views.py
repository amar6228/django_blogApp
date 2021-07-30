from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from blogapp.models import Post, Blogcomment
from django.contrib import messages
from blogapp.templatetags import extras

# Create your views here.
def bloghome(request):
    allposts=Post.objects.all().order_by('-timestamp')
    context={'allposts':allposts}
    return render(request, 'blogapp/bloghome.html', context)

def blogpost(request, slug):
    post=Post.objects.filter(post_slug=slug).first()
    post.views=post.views+1
    post.save()
    comments=Blogcomment.objects.filter(post=post, parent=None)
    replies=Blogcomment.objects.filter(post=post).exclude(parent=None)
    
    rep_dict={}
    for reply in replies:
        if reply.parent.sno not in rep_dict.keys():
            rep_dict[reply.parent.sno]=[reply]
        else:
            rep_dict[reply.parent.sno].append(reply)
    
    print(rep_dict)
    context={'post':post, 'comments':comments, 'user':request.user, 'rep_dict':rep_dict}
    return render(request, 'blogapp/blogpost.html', context)

def postcomment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postsno')
        post=Post.objects.get(sno=postsno)
        parentsno=request.POST.get('parentsno')

        if parentsno=="":
            comment=Blogcomment(comment=comment, user=user, post=post)  
            comment.save()
            messages.success(request, "Comment success")
        else:
            parent=Blogcomment.objects.get(sno=parentsno)
            comment=Blogcomment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "reply success")

    return redirect(f'/blog/{post.post_slug}')








    