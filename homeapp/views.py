from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from homeapp.models import Contact
from blogapp.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    post=Post.objects.all()
    print(post)
    context={'post':post}
    return render(request, 'homeapp/index.html', context)

def contact(request):
    if request.method=="POST":
        name=request.POST['name']        
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name, email, phone, content)
        
        if len(name)<2 or len(email)<5 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly...!!")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Messages sent successfully...")

    return render(request, 'homeapp/contact.html')

def about(request):
    return render(request, 'homeapp/about.html')

def search(request):
    query=request.GET['query']
    if len(query)>50:
        allposts=Post.objects.none()
    else:
        allpoststitle=Post.objects.filter(title__icontains=query)
        allpostscontent=Post.objects.filter(content__icontains=query)
        allposts=allpoststitle.union(allpostscontent)

    if allposts.count()==0:
        messages.error(request, "No result found please refined your query")        
    params={'allposts':allposts,'query':query}

    return render(request, 'homeapp/search.html', params)


# authentication APIs
def handlesignup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        phone=request.POST['phone']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        print(username,fname,phone,email,pass1,pass2)

        if len(username)>10:
            messages.error(request,"username not greater than 10")
            return redirect('home')

        if not username.isalnum():
            messages.error(request,"username should contain letter and number only")
            return redirect('home')

        if pass1!=pass2:
            messages.error(request,"Password not matched")
            return redirect('home')     
        
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.phone=phone
        myuser.save()
        messages.success(request, "your account created successfully")
        return redirect('home')
    else:
        return HttpResponse ('404 - Not found')
    
def handlelogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'successfully logged in')
            return redirect('home')
        else:
            messages.error(request, "invalid credentials, try again")
            return redirect('home')
    else:
        return HttpResponse('404 - Not found')

def handlelogout(request):
    # if request.method=='POST':
    logout(request)
    messages.success(request, "Successfully logout")
    return redirect('home')

#Comment Views Here...



























