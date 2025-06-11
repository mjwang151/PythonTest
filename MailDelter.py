import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr

imaplib._MAXLINE = 10_000_000

# 邮箱账号信息
IMAP_SERVER = 'imap.amarsoft.com'  # 你的IMAP服务器，比如imap.gmail.com
EMAIL_ACCOUNT = 'mjwang@amarsoft.com'
PASSWORD = 'Wangminjie151'


# 模糊匹配关键词
KEYWORD = '测试'
TARGET_SENDER = 'cdh_crdc@amarsoft.com'  # 要匹配的发件人邮箱地址


def clean_subject(subject):
    if subject is None:
        return ""
    decoded_fragments = decode_header(subject)
    decoded_subject = ''
    for fragment, encoding in decoded_fragments:
        if isinstance(fragment, bytes):
            decoded_subject += fragment.decode(encoding or 'utf-8', errors='ignore')
        else:
            decoded_subject += fragment
    return decoded_subject

def main():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select('INBOX')

    # typ, data = mail.uid('search', None, 'ALL')
    typ, data = mail.uid('search', None, '(FROM "cdh_crdc@amarsoft.com" SINCE "01-May-2025" BEFORE "01-Jun-2025")')
    if typ != 'OK':
        print('搜索邮件失败')
        return

    uid_list = data[0].split()
    batch_size = 10  # 每批只处理10封，防止请求太长
    deleted_count = 0

    for i in range(0, len(uid_list), batch_size):
        batch_uids = uid_list[i:i+batch_size]
        uid_str = ','.join(uid.decode('utf-8') if isinstance(uid, bytes) else uid for uid in batch_uids)

        try:
            typ, msg_data = mail.uid('fetch', uid_str, '(RFC822)')
            if typ != 'OK':
                print(f'获取邮件失败，UIDs: {uid_str}')
                continue
        except imaplib.IMAP4.error as e:
            print(f'Fetch 出错，UIDs: {uid_str}，错误: {e}')
            continue

        for j in range(0, len(msg_data), 2):
            if j+1 >= len(msg_data):
                break
            if not msg_data[j] or not msg_data[j][1]:
                continue
            msg = email.message_from_bytes(msg_data[j][1])
            from_raw = msg.get('From', '')
            name, email_addr = parseaddr(from_raw)  # 解析邮箱地址
            subject = clean_subject(msg['Subject'])

            # if KEYWORD in subject:
            #     print('邮件名称：' + subject)
            #     mail.uid('store', batch_uids[j//2], '+FLAGS', '(\\Deleted)')
            #     deleted_count += 1
            #     print(f'标记删除邮件: {subject}')

            # 匹配发件人邮箱（可改成模糊匹配）
            if TARGET_SENDER.lower() in email_addr.lower():
                mail.uid('store', batch_uids[j // 2], '+FLAGS', '(\\Deleted)')
                deleted_count += 1
                print(f'标记删除：From: {email_addr} | Subject: {subject}')
    mail.expunge()
    mail.logout()
    print(f'已删除邮件数量: {deleted_count}')

if __name__ == '__main__':
    main()