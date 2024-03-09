from django.shortcuts import render,redirect
from django.urls import reverse_lazy
# Create your views here.
from store.models import Category,Product,Cart,Order
from store.forms import Register,Login,orderform
from django.contrib.auth.models import User
from django.views.generic import View,ListView,CreateView
from django.contrib.auth import authenticate,login,logout

# DECORATOR
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            return redirect("log")
    return wrapper
    

# HOME PAGE
class Home(ListView):
    # def get(self,request,*args,**kwargs):
    #     return render(request,"store/index.html")
    model = Category
    template_name="store/index.html"
    context_object_name="categories"

# CATEGORY 
class Category_detail(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product.objects.filter(category_id=id)
        name=Category.objects.get(id=id)
        return render(request,"store/category_detail.html",{"data":data,"name":name})


# PRODUCT
class Product_detail(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        p_data=Product.objects.filter(id=id)
        return render(request,"store/p_details.html",{"p_data":p_data})


# REGISTRATION
class Registerview(CreateView):
    template_name="store/register.html"
    form_class =  Register
    model = User 
    success_url=reverse_lazy("log")


# LOGIN
class Loginview(View):
    def get(self,request,*args,**kwargs):
        form=Login()   
        return render(request,"store/login.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=Login(request.POST)
        print(request.user)
        if form.is_valid():
            print(form.cleaned_data)
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                print("valid crendential")
                login(request,user_obj)
                print(request.user)
                return redirect("home")
            else:
                print("invalid credentials")
        else:
            print("get out")
        return render(request,"Store/login.html",{"form":form})


#LOGOUT
class logoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('home')


# ADDCART'
@method_decorator(signin_required,name="dispatch")   
class Cartview(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product.objects.get(id=id)
        Cart.objects.create(item=data,user=request.user)        
        return redirect("cartdetails")
    

# CART
@method_decorator(signin_required,name="dispatch")    
class Cartdetails(View):
    def get(self,request,*args,**kwargs):
        data=Cart.objects.filter(user=request.user)
        return render(request,"store/cart.html",{"data":data})      
    
# DELETE    
class Cartdelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cart.objects.get(id=id).delete()
        return redirect ("cartdetails")
    

# ORDER
@method_decorator(signin_required,name="dispatch")   
class Orderview(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk") 
        data=Product.objects.get(id=id)  
        form=Order()
        return render(request,'Store/orderpage.html',{'form':form,"data":data})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Product.objects.get(id=id)
        form=orderform(request.POST)
        if form.is_valid():
            adrs=form.cleaned_data.get("address")
            Order.objects.create(order_item=data,customer=request.user,address=adrs)
            return redirect("home")
        return redirect("cart")
    
class order_list(View):
    def get(self,request,*args,**kwargs):
        data=Order.objects.filter(customer=request.user)
        return render(request,"store/view_order.html",{"data":data})


# Remove_order
class remove_order(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Order.objects.get(id=id).delete()
        return redirect("cart")
    

