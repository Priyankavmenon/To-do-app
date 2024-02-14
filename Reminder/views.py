from django.shortcuts import render, redirect
from django.views.generic import View
from Reminder.forms import Register, Login, Todo
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Reminder.models import Task
from django.utils.decorators import method_decorator


def signin_reqd(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return fn(request, *args, **kwargs)
        else:
            return redirect("login")
    return wrapper


def Owner(fn):
    def wrapper(request, *args, **kwargs):
        checkid = kwargs.get("pdk")
        obj = Task.objects.get(id=checkid)
        if obj.user != request.user:
            return redirect("login")
        else:
            return fn(request, *args, **kwargs)
    return wrapper

decorators=[signin_reqd,Owner]
class Registerview(View):
    def get(self, request, *args, **kwargs):
        rform = Register()

        return render(request, "reg.html", {"rf": rform})

    def post(self, request, *args, **kwargs):
        rform = Register(request.POST, files=request.FILES)
        print(rform)

        if rform.is_valid():
            User.objects.create_user(**rform.cleaned_data)

            messages.success(request, "Successfully registered")
        else:
            messages.error(request, "registration unsuccessful")
        rform = Register()
        return render(request, "reg.html", {"rf": rform})

class Loginview(View):
    def get(self, request, *args, **kwargs):
        lform = Login()
        
        return render(request, "log.html", {"lf": lform})

    def post(self, request, *args, **kwargs):
        lform = Login(request.POST)

        if lform.is_valid():
            username = lform.cleaned_data.get("username")
            # print(username)
            password = lform.cleaned_data.get("password")
            obj = authenticate(request, username=username, password=password)
            # print(obj)
            if obj:
                
                print(request.user)
                login(request, obj)
                messages.success(request, "You have successfully logged in")

            else:
                messages.error(request, "Invalid credentials")
                return redirect("login")
            lform = Login()
            return render(request,"welcome.html",{"lf":lform})
class Profileview(View):
    def get(self, request, *args, **kwargs):
        # pid=kwargs.get("pk")
        # print(pid)
        user=request.user
        details=User.objects.filter(username=user) 
        print(details)      
        return render(request,"userprofile.html",{"d":details})
@method_decorator(signin_reqd,name="dispatch")
class Updateprofile(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        print(id)
        details=User.objects.get(id=id)
        print(details)
        form=Register(instance=details)
        return render(request,"redit.html",{"f":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        details=User.objects.get(id=id)
        form=Register(request.POST,instance=details)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            messages.error(request,"Invalid credentials,Please try again")
        return redirect("login")

class Profiledelete(View):
    def get(self, request, *args, **kwargs):
        delid=kwargs.get("pk")
        details=User.objects.get(id=delid).delete()
        return redirect("login")
@method_decorator(signin_reqd, name="dispatch")
class Taskview(View):
    def get(self, request, *args, **kwargs):
        tform = Todo()
        taskname = Task.objects.filter(user=request.user).order_by('completed')
        print(taskname)

        if "completed" in request.GET:
            filterkey = request.GET.get("completed")
            taskname = Task.objects.filter(completed=filterkey)
        return render(request, "index.html", {"tf": tform, "tn": taskname})

    def post(self, request, *args, **kwargs):
        tform = Todo(request.POST)
        if tform.is_valid():
            tform.instance.user = request.user
            print(request.user)
            tform.save()
            messages.success(request, "Task entered succesfully")
        else:
            messages.error(request, "Unsuccessful")
        taskname = Task.objects.filter(user=request.user)
        return render(request, "index.html", {"tf": tform, "tn": taskname})
# @method_decorator(signin_reqd, name="dispatch")


@method_decorator(Owner, name="dispatch")
class Taskedit(View):
    def get(self, request, *args, **kwargs):
        editid = kwargs.get("pk")
        # obj= Task.objects.get(id=editid)
        # print(obj.user)
        status = Task.objects.get(id=editid)
        print(status)
        print(status.completed)
        if status.completed == True:
            status.completed = False
            status.save()
            messages.success(request, "Task edited successfully")

        else:
            status.completed = True
            status.save()
            messages.error(request, "unsuccessful")
        return redirect("task")


# @method_decorator(signin_reqd, name="dispatch")
@method_decorator(Owner, name="dispatch")
class Taskdelete(View):
    def get(self, request, *args, **kwargs):
        delid = kwargs.get("pdk")
        Task.objects.get(id=delid).delete()
        messages.success(request, "Task edited successfuly")
        return redirect("task")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(
            request, "You have logged out,Please login to continue")
        return redirect("login")
