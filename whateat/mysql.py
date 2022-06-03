#채은 : 깃 연동 이후 본인 컴퓨터 설정에 맞게 주석을 바꿔서 사용하세욧
class oursql():

    # =============AWS환경 사용 시================
    # serverhost = ['43.200.16.33',"*"]
    # s_host = 'ec2-43-200-16-33.ap-northeast-2.compute.amazonaws.com'
    # s_port = 3306
    # s_user = 'user1'
    # s_passwd='1111'

    # =============local환경 사용 시==============
    serverhost = ['*', 'localhost']
    s_host = '192.168.0.29'
    s_port = 3306
    s_user = 'user1'
    s_passwd='1111'

    # =============채은 재택근무==================
    # serverhost = ['*', 'localhost']
    # s_host = '127.0.0.1'
    # s_port = 3306
    # s_user = 'root'
    # s_passwd='00000'


