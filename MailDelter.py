import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr

imaplib._MAXLINE = 10_000_000

# 邮箱账号信息





import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime, timedelta

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

def to_imap_date(date_obj):
    return date_obj.strftime("%d-%b-%Y")

def main():
    IMAP_SERVER = 'imap.amarsoft.com'  # 你的IMAP服务器，比如imap.gmail.com
    EMAIL_ACCOUNT = 'mjwang@amarsoft.com'
    PASSWORD = 'Wangminjie151'
    BATCH_SIZE = 10
    # 模糊匹配关键词
    KEYWORD = '测试'
    TARGET_SENDER = ''  # 要匹配的发件人邮箱地址
    sender_list = 'amarMonitorFullLink,amarMonitorFullLink@mail.amarsoft.com,cdh_crdc@amarsoft.com,cdh_dev@amarsoft.com,llzhang2@amarsoft.com'.split(",")
    start_date = datetime.strptime('2025-06-01', "%Y-%m-%d")
    end_date = datetime.strptime('2025-06-12', "%Y-%m-%d")

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select('INBOX')

    deleted_total = 0

    for sender in sender_list:
        sender = sender.strip()
        current_date = start_date
        while current_date < end_date:
            next_date = current_date + timedelta(days=1)
            since_date = to_imap_date(current_date)
            before_date = to_imap_date(next_date)
            search_criteria = f'(FROM "{sender}" SINCE "{since_date}" BEFORE "{before_date}")'
            print(f"\n查询: {search_criteria}")
            try:
                typ, data = mail.uid('search', None, search_criteria)
                if typ != 'OK':
                    print('搜索失败')
                    current_date = next_date
                    continue

                uid_list = data[0].split()
                deleted_count = 0

                for i in range(0, len(uid_list), BATCH_SIZE):
                    batch_uids = uid_list[i:i+BATCH_SIZE]
                    # uid_str = ','.join(uid.decode('utf-8') if isinstance(uid, bytes) else uid for uid in batch_uids)
                    uid_str = ','.join(
                        uid.decode('utf-8') if isinstance(uid, bytes)
                        else str(uid)
                        for uid in batch_uids
                    )
                    try:
                        typ, msg_data = mail.uid('fetch', uid_str, '(RFC822)')
                        if typ != 'OK':
                            print(f'获取失败: {uid_str}')
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
                        _, email_addr = parseaddr(from_raw)
                        subject = clean_subject(msg.get('Subject'))

                        if sender.lower() in email_addr.lower():
                            mail.uid('store', batch_uids[j // 2], '+FLAGS', '(\\Deleted)')
                            deleted_count += 1
                            print(f'标记删除：From: {email_addr} | Subject: {subject}')

                if deleted_count > 0:
                    try:
                        mail.expunge()
                        print(f"日期 {since_date}: 已删除 {deleted_count} 封邮件")
                    except Exception as e:
                        print(f'expunge 出错: {e}')

                deleted_total += deleted_count

            except Exception as e:
                print(f"处理日期 {since_date} 出错: {e}")

            current_date = next_date

    mail.logout()
    print(f"\n全部完成，共删除邮件：{deleted_total}")

if __name__ == '__main__':
    main()