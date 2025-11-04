import imaplib
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 账户配置
IMAP_SERVER = 'imap.amarsoft.com'
EMAIL_ACCOUNT = 'mjwang@amarsoft.com'
PASSWORD = 'Wangminjie151'

# 要清空的文件夹列表
FOLDERS_TO_CLEAR = [

    # '&Tgp+v3Uzi,c-',
    # '&WRaQ6GcNUqFec1PwY6VT418CXjhj0JGS-',
    # '&WRaQ6GcNUqFec1PwY6VT418CXjhj0JGS-/&UXZO1piEi2Y-',
    # '&WRaQ6GcNUqFec1PwY6VT418CXjhj0JGS-/&XwJeOG1Bkc920WOn-',
    # '&WRaQ6GcNUqFec1PwY6VT418CXjhj0JGS-/&ZXBjbk4tX8OYhItm-',
    # '&WRaQ6GcNUqFec1PwY6VT418CXjhj0JGS-/&bWZT0XbRY6eQrk72-',
    # '&WRaQ6GcNUqFec1PwY6VT418CXjhj0JGS-/&dtFjp1QNU1V7oXQG-',
    # '&WRaQ6GcNUqFec1PwY6VT418CXjhj0JGS-/&dtFjp2KliGg-',
    # '&jSZiN15zU,A-',
    'JIRA',
    # 'Trash',

]


def clear_folder(mail, folder_name):
    """选择指定文件夹并清空所有邮件"""
    try:
        typ, _ = mail.select(f'"{folder_name}"', readonly=False)
        if typ != 'OK':
            logger.warning(f"无法选择文件夹：{folder_name}")
            return

        logger.info(f"✅ 正在清空文件夹：{folder_name}")

        typ, data = mail.search(None, 'ALL')
        if typ != 'OK':
            logger.warning(f"搜索邮件失败：{folder_name}")
            return

        msg_nums = data[0].split()
        if not msg_nums:
            logger.info(f"📭 文件夹 {folder_name} 中没有邮件。")
            return

        for num in msg_nums:
            mail.store(num, '+FLAGS', '\\Deleted')

        mail.expunge()
        logger.info(f"🗑️ 文件夹 {folder_name} 已清空（共 {len(msg_nums)} 封邮件）\n")

    except Exception as e:
        logger.error(f"清理文件夹 {folder_name} 时出错: {e}")


def main():
    try:
        logger.info("🔐 正在连接邮箱服务器...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        logger.info("✅ 登录成功")

        for folder in FOLDERS_TO_CLEAR:
            clear_folder(mail, folder)

        mail.logout()
        logger.info("📴 已退出邮箱连接")

    except Exception as e:
        logger.error(f"执行失败: {e}")


if __name__ == '__main__':
    main()