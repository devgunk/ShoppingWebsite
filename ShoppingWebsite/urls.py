"""ShoppingWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from ShoppingWebsite.ShoppingWebsite import *

urlpatterns = [
    #-----------------------------------------------------TEMPLATE------------------------------------------------------
    path('',index),
    path('showreviewsaction',showreviewsaction),
    path('showaction',showaction),
    path('showcat',showcat),
    path('index',index),
    path('contact',contact),
    path('contentaction',contentaction),
    path('about',about),
    path('service',service),
    path('reviews',reviews),
    path('shop',shop),
    path('product',product),
    path('single',single),
    path('showallproductaction',showallproductaction),
    path('addtocartquickviewaction',addtocartquickviewaction),
    #---------------------------------------------------END-TEMPLATE----------------------------------------------------
    #------------------------------------------------------ADMIN-------------------------------------------------------------
    path('AdminHomePage',AdminHomePage),
    path('InsertRecord',InsertRecord),
    path('OnInsertClick',OnInsertClick),
    path('ViewRecord',ViewRecord),
    path('EditRecord',EditRecord),
    path('DeleteRecord',DeleteRecord),
    path('OnClickEditRecord',OnClickEditRecord),
    path('loginadmin',loginadmin),
    path('adminloginaction',adminloginaction),
    path('adminlogout',adminlogout),
    path('pendingorderpage',pendingorderpage),
    path('pendingordersaction',pendingordersaction),
    path('approve_reject_action',approve_reject_action),
    path('myorders',myorders),
    path('viewcontacts',viewcontacts),
    path('viewreviews',viewreviews),
    path('DeleteReviews',DeleteReviews),
    path('DeleteContent',DeleteContent),
    path('PostReview',PostReview),
    path('postedreviews',postedreviews),
    path('Deletepostedreview',Deletepostedreview),
    path('myordersaction',myordersaction),
    path('editadminprofile',editadminprofile),
#----------------------------------------------------END-ADMIN-----------------------------------------------------------
#----------------------------------------------------CATEGORY------------------------------------------------------------
    path('InsertCT',InsertCT),
    path('ViewCT',ViewCT),
    path('EditCT',EditCT),
    path('DeleteCT',DeleteCT),
    path('OnClickEditCT',OnClickEditCT),
    path('OnClickInsertCT',OnClickInsertCT),
    path('changepassword',changepassword),
    path('OnClickChangePassword',OnClickChangePassword),
    path('OnClickChangeName',OnClickChangeName),
#--------------------------------------------------END-CATEGORY----------------------------------------------------------
#-----------------------------------------------------PRODUCT------------------------------------------------------------
    path('addproductpage',addproductpage),
    path('addproductaction',addproductaction),
    path('viewproductpage',viewproductpage),
    path('viewproductaction',viewproductaction),
    path('deleteproductaction',deleteproductaction),
    path('editproductpage',editproductpage),
    path('editproductaction',editproductaction),
#---------------------------------------------------END-PRODUCT----------------------------------------------------------
#------------------------------------------------------USER--------------------------------------------------------------
    path('usersignupaction',usersignupaction),
    path('userloginaction',userloginaction),
    path('userlogin',userlogin),
    path('userlogout',userlogout),
    path('changeuserpassword',changeuserpassword),
    path('edituserprofile',edituserprofile),
    path('OnClickChangeUserName',OnClickChangeUserName),
    path('OnClickChangeUserPassword',OnClickChangeUserPassword),
#----------------------------------------------------END-USER------------------------------------------------------------
#------------------------------------------------------CART--------------------------------------------------------------
    path('addtocartaction',addtocartaction),
    path('mycart',mycart),
    path('mycartaction',mycartaction),
#----------------------------------------------------END-CART------------------------------------------------------------
#----------------------------------------------------PAYMENT-------------------------------------------------------------
    path('proceedtopay',proceedtopay),
    path('billinginfo',billinginfo),
    path('checkoutaction',checkoutaction),
#--------------------------------------------------END-PAYMENT-----------------------------------------------------------
]