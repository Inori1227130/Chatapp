from django.contrib import admin
from django.urls import include, path
from . import views, chat
app_name = 'mychat'
urlpatterns = [

#ログイン認証処理(ログイン画面&メイン画面)
path( '', views.mainView, name='main' ) ,    
#新規ユーザ登録画面
path( 'createuser', views.createUser, name='createuser' ) ,
#ユーザ登録結果画面
path( 'adduser', views.addUser, name='adduser' ) ,
#新規ルーム作成画面
path( 'createroom', views.createRoom, name='createroom' ) ,
#ルーム作成結果画面
path( 'addroom', views.addRoom, name='addroom' ) ,
#ログイン画面にリダイレクト
path( 'logout', views.logout, name='logout' ) ,
#チャット画面
path( 'chat/<int:id>', views.chatView, name='chat' ) ,
# チャット処理１：全メッセージの取得
path('getChatMessage/<int:id>', chat.getChatMessage, name='getChatMessage'),
# チャット処理２：新規メッセージの投稿
path('submitChatMessage/<int:id>', chat.submitChatMessage, name='submitChatMessage'),
# チャット処理３：指定メッセージの削除
path('deleteChatMessage/<int:id>', chat.deleteChatMessage, name='deleteChatMessage'),
]