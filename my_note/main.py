import os
import shutil
import getpass

# 需要加密的文件夹列表
note_list = [
    'Wisdomhub'
]
note_dir = os.path.abspath(os.curdir)


def get_md5(p_str):
    """
    计算md5值, 用于本地保存密码, 免得输错后无法解密
    """
    import hashlib
    m = hashlib.md5()
    m.update(p_str.encode(encoding='utf-8'))
    return m.hexdigest()


def check_pw(my_pw):
    """
    通过.pw文件检查输入密码是否正确
    """
    if os.path.exists(os.path.join(note_dir, '.pw')):
        with open(os.path.join(note_dir, '.pw'), 'r', encoding='utf-8') as f:
            pw_md5 = f.read()
        if get_md5(my_pw) == str(pw_md5):
            return True
        else:
            return False
    else:
        return None


def create_pw():
    """
    创建新密码, 保存新密码md5值到.pw文件
    """
    pwd = str(getpass.getpass('new password:'))
    pwd_md5 = get_md5(pwd)
    with open(os.path.join(note_dir, '.pw'), 'w', encoding='utf-8') as f:
        f.write(pwd_md5)
    pwd_check = str(getpass.getpass('repeat password:'))
    with open(os.path.join(note_dir, '.pw'), 'r', encoding='utf-8') as f:
        pw_md5_stored = f.read()
    if pwd_check == pw_md5_stored:
        print('Done!')
    else:
        print('Wrong!')


def main():
    """
    检查密码
    1. 如果没有密码就提示创建
    2. 如果密码错误就提示退出
    3. 密码正确时继续

    遍历笔记列表
    1. 如果存在笔记名.zip文件, 认为此时为编辑模式
    1.1 根据密码执行2次解压
    1.2 确认解压没有出问题确时删除压缩文件
    1.3 正常使用文件

    2. 如果笔记名.zip文件不存在, 认为此时编辑完成需要加密退出
    2.1 根据密码执行2次加密 (避免看到文件名)
    2.2 确认压缩过程没有出问题时删除源文件
    2.3 完成加密, 可以同步到云服务中
    """
    pwd = str(getpass.getpass('password:'))
    cp = check_pw(pwd)
    if cp is None:
        if str(input('create new password?')) == 'y':
            create_pw()
        return None
    elif cp is False:
        if len(input('press to exit')) != '':
            return None
    else:
        pass
    for file_name in note_list:
        file_name_zip = file_name + '.zip'
        file_name_tmp_zip = file_name + '_7ming.zip'
        file_path = os.path.join(note_dir, file_name_zip)
        file_path_tmp = os.path.join(note_dir, file_name_tmp_zip)
        file_dir = os.path.join(note_dir, file_name)
        if os.path.exists(file_path):
            cmd = '"C:/Program Files/7-Zip/7z.exe" x %s -p%s' % (
                file_path, pwd)
            os.system(cmd)
            cmd = '"C:/Program Files/7-Zip/7z.exe" x %s -p%s' % (
                file_path_tmp, pwd)
            os.system(cmd)
            if str(input('OK?')) == 'y':
                os.remove(file_path)
                os.remove(file_path_tmp)
        else:
            cmd = '"C:/Program Files/7-Zip/7z.exe" a %s %s -p%s' % (
                file_name_tmp_zip, file_dir, pwd)
            os.system(cmd)
            cmd = '"C:/Program Files/7-Zip/7z.exe" a %s %s -p%s' % (
                file_name_zip, file_path_tmp, pwd)
            os.system(cmd)
            if str(input('OK?')) == 'y':
                shutil.rmtree(file_dir)
                os.remove(file_path_tmp)


if __name__ == '__main__':
    main()
