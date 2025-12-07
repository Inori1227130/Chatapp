from django.shortcuts import render,redirect
from .models import User,Room,ChatLog
import urllib.parse

#ログイン認証処理(ログイン画面&メイン画面)
def mainView(request):
    template_file = "mychat/main.html"
    back_file = "mychat/start.html"
    
    error_message = []
    
    # [1] クッキー情報(後述)からユーザ名(USER をキー名とする)を取得する。 
    cookie_user = request.COOKIES.get('USER')
    if cookie_user is not None:
        username = urllib.parse.unquote(cookie_user)
    else:
        username = None
        
    roomlist = Room.objects.all()
        
    options = {
        'error_message': error_message,
        'username':username,
        'roomlist' : roomlist
    }

    
    # [2] ユーザ名を取得できた場合
    if username:
        #[2](1)データベースからそのユーザ名と完全一致するユーザ情報を取得する。 
        user = User.objects.filter(name=username).first()
        if user:
            if user.islogin:
                # [2](2)ユーザ情報のログイン状態がログイン中(True)ならば認証処理は行わずにメイン画面に遷移する。（遷移パターン A） 
                return render(request, template_file, options)
            else:
                # [2](3)ユーザ情報のログイン状態がログイン中でない(False)場合、クッキーからユーザ名を削除(後述)してから、ログイン画面に遷移する（遷移パターン B） 
                response = render(request, back_file, options)
                response.delete_cookie('USER')
                return response
    
    # [3]フォームのデータとしてユーザ名、パスワード、ログインフラグを取得し、内部変数 user、password、login にそれぞれ代入する。ログインフラグが取得できなかった場合は None ではなく"off"を値として代入する。 
    if "name" in request.POST:
        name = request.POST.get("name")
        
    if "password" in request.POST:
        password = request.POST.get("password")
        
    if "login" in request.POST:
        login_flag = request.POST.get("login", "off")
        
        #[4] ログインフラグが "on"ではない 場合は、ログイン画面に遷移する。（遷移パターン C）
        if login_flag != "on":
            return render(request, back_file, options)
        
        #[5] ユーザ名が取得できない場合は「ユーザ名が入力されていません」というエラーメッセージを用意する。
        if not name:
            error_message.append("ユーザ名が入力されていません")
        #[6] パスワードが取得できない場合は「パスワードが入力されていません」というエラーメッセージを用意する。
        if not password:
            error_message.append("パスワードが入力されていません")
        
        #[7] [5][6]で入力エラーのメッセージが１つでも用意されたならば、それをテンプレートに渡すデータとして設定し、ログイン画面に遷移し、それをメッセージ表示エリアに赤字で表示する。（遷移パターンD)
        if error_message:
            return render(request, back_file, options)
        
        #[8] データベースから「ユーザ名」と「パスワード」の両方が完全一致するユーザ情報を取得する。
        dbuser = User.objects.filter(name=name, password=password).first()
        #[9] 一致するユーザ情報が取得できなかった場合は、「ユーザ名、パスワードが一致しません」というエラーメッセージを用意し、ログイン画面に遷移し、それをメッセージ表示エリアに赤字で表示する。（遷移パターンE)
        if not dbuser:
            error_message.append("ユーザ名、パスワードが一致しません")
            return render(request, back_file, options)
        #[10] 一致するユーザ情報が取得できた場合には、そのユーザ情報のログイン状態を Trueにして、データベースを更新する。
        else:
            dbuser.islogin = True
            dbuser.save()
        
        # [11] 更新後、ユーザ名(USER をキー名、入力されたユーザ名を value 値とする)をクッキー情報として設定しつつメイン画面に遷移する。（遷移パターン F）テンプレート側でクッキー情報を取得する処理を記述し、画面上にユーザ名を表示する。
        response = redirect('mychat:main')
        response.set_cookie('USER', urllib.parse.quote(name))
        return response

    return render(request, back_file, options)


# 新規ユーザ登録画面
def createUser(request):
    # 展開される出力画面のテンプレートファイル
    template_file = "mychat/createuser.html"

    # = テンプレートに受け渡されるデータ(今回はメッセージすべて)
   
    options = {
    
    }        

    # テンプレートを展開(処理)して結果画面としてブラウザに返す
    return render(request, template_file, options)
 
 
 # ユーザ登録結果画面
def addUser(request):
    # 展開される出力画面のテンプレートファイル
    template_file = "mychat/adduser.html"

    # エラーメッセージの出力
    error_message = []
    success_message =[]
     
    #[1] フォームの入力データを取得し、内部変数 name, password にそれぞれ代入する。 
    if "name" in request.POST:
        name = request.POST.get("name")
    if "password" in request.POST:
        password = request.POST.get("password")
        
        #[2] 受け取ったユーザ名が未記入か空文字の場合は、未記入であることを伝えるエラーメッセージを用意する。
        if name is None or name == '':
           error_message.append("名前が入力されていません")
        #[3] 受け取ったパスワードが未記入か空文字の場合は、[2]と同様に、未記入であることを伝えるエラーメッセージを用意する。
        if password is None or password == '':
           error_message.append("パスワードが入力されていません")
           
        #[4]エラーメッセージが無いとき
        if len(error_message) == 0:
           #データベースから「ユーザ名」が完全⼀致するユーザ情報を取得する
           exisinguser = User.objects.filter(name=name).first()
           #[4](1)ユーザ情報が取得できた時
           if exisinguser is not None: 
              #[4](2)「すでにそのユーザは存在します」というエラーメッセージを⽤意
              error_message.append("すでにそのユーザは存在します")
           #[4](3)ユーザ情報が取得できなかった時
           else:
              #[4](3)新たなユーザ情報を作成
              newuser = User.objects.create(name = name,password = password)
              #[4](3)作成したユーザ情報を保存
              newuser.save()
              #[4](3) 「ユーザ 〇〇 を登録しました」というメッセージを⽤意
              success_message.append(f"ユーザ{name}を登録しました")

    # = テンプレートに受け渡されるデータ
    options = {
         'error_message':error_message,
         'success_message':success_message,
    }        

    # テンプレートを展開(処理)して結果画面としてブラウザに返す
    return render(request, template_file, options)

 # 新規ルーム登録画面
def createRoom(request):
    # 展開される出力画面のテンプレートファイル
    template_file = "mychat/createroom.html"

    #-------------------------------
    # 連想配列の生成
    # = テンプレートに受け渡されるデータ(今回はメッセージすべて)
    #-------------------------------
    options = {
    }        

    # テンプレートを展開(処理)して結果画面としてブラウザに返す
    return render(request, template_file, options)
 
 # ルーム作成結果画面
def addRoom(request):
    # 展開される出力画面のテンプレートファイル
    template_file = "mychat/addroom.html"
    error_message = []
    success_message = []

    if "name" in request.POST:
      name = request.POST.get("name")
      
      if name is None or name == '':
        error_message.append("ルーム名が入力されていません")
      else:
        existinguser = Room.objects.filter(name=name).first()

        if existinguser is not None:
           error_message.append("すでにそのルームは存在します")
        else:
           newroom = Room.objects.create(name = name)
           newroom.save()
           success_message.append(f"ルーム{name}を登録しました")

    # = テンプレートに受け渡されるデータ(今回はメッセージすべて)
   
    options = {
        'error_message':error_message,
        'success_message':success_message,

    }        

    # テンプレートを展開(処理)して結果画面としてブラウザに返す
    return render(request, template_file, options)
 
 # ログアウト
def logout(request):
    
    cookie_user = request.COOKIES.get('USER')
    if cookie_user is not None:
      username = urllib.parse.unquote(cookie_user)
      user = User.objects.filter(name=username).first()

      if user:
         user.login = False
         user.save()
      response = redirect('mychat:main')
      response.delete_cookie('USER') 
      return response       

    # テンプレートを展開(処理)して結果画面としてブラウザに返す
    return redirect('mychat:main')
 
 # チャット画面
def chatView(request,id=None):
    # 展開される出力画面のテンプレートファイル
    template_file = "mychat/chat.html"
    
    cookie_user = request.COOKIES.get('USER')
    if cookie_user:
        username = urllib.parse.unquote(cookie_user)
    else:
        username = None
    

    if id is not None:
        room = Room.objects.filter(id=id).first()
    else:
        room = None
    # = テンプレートに受け渡されるデータ(今回はメッセージすべて)
    #-------------------------------
    
    if room is not None:
        options = {
            'username':username,
            'room':room,
        }   
        
    else:
        options = {
        }     

    # テンプレートを展開(処理)して結果画面としてブラウザに返す
    return render(request, template_file, options)

 


 
 

 
