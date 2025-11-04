import imaplib
import logging

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置邮箱账户
IMAP_SERVER = 'imap.amarsoft.com'   # 更换成你的 IMAP 服务器
EMAIL_ACCOUNT = 'mjwang@amarsoft.com'
PASSWORD = 'Wangminjie151'  # ⚠️ 不要在生产代码中明文写密码，建议用环境变量或配置文件管理

def list_mail_folders():
    try:
        logger.info("连接邮箱中...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        logger.info("登录成功")

        logger.info("正在列出文件夹...")
        typ, folders = mail.list()
        if typ == 'OK':
            print("\n📂 可用的邮箱文件夹如下：\n")
            for folder in folders:
                print(folder.decode())  # 打印文件夹原始信息
        else:
            logger.error("无法获取文件夹列表")

        mail.logout()
        logger.info("连接已关闭")

    except Exception as e:
        logger.error(f"操作失败: {e}")


if __name__ == '__main__':
    list_mail_folders()