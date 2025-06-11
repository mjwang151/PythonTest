import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime, timedelta
import time
import logging

# 设置最大行长度
imaplib._MAXLINE = 10_000_000

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OptimizedEmailDeleter:
    def __init__(self, imap_server, email_account, password):
        self.imap_server = imap_server
        self.email_account = email_account
        self.password = password
        self.mail = None
        self.deleted_total = 0

    def connect(self):
        """建立IMAP连接"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_account, self.password)
            self.mail.select('INBOX')
            logger.info("IMAP连接成功")
            return True
        except Exception as e:
            logger.error(f"IMAP连接失败: {e}")
            return False

    def disconnect(self):
        """断开IMAP连接"""
        if self.mail:
            try:
                self.mail.logout()
                logger.info("IMAP连接已关闭")
            except:
                pass

    def clean_subject(self, subject):
        """清理邮件主题"""
        if subject is None:
            return ""
        try:
            decoded_fragments = decode_header(subject)
            decoded_subject = ''
            for fragment, encoding in decoded_fragments:
                if isinstance(fragment, bytes):
                    decoded_subject += fragment.decode(encoding or 'utf-8', errors='ignore')
                else:
                    decoded_subject += fragment
            return decoded_subject
        except Exception as e:
            logger.warning(f"解析主题失败: {e}")
            return str(subject)

    def to_imap_date(self, date_obj):
        """转换日期格式"""
        return date_obj.strftime("%d-%b-%Y")

    def delete_emails_by_uid_batch(self, uid_list, batch_size=50):
        """
        批量删除邮件 - 优化版本
        关键优化：
        1. 直接按UID批量标记删除，无需逐个获取邮件内容
        2. 减少网络请求次数
        3. 使用更大的批次大小
        """
        deleted_count = 0

        for i in range(0, len(uid_list), batch_size):
            batch_uids = uid_list[i:i + batch_size]
            uid_str = ','.join(
                uid.decode('utf-8') if isinstance(uid, bytes) else str(uid)
                for uid in batch_uids
            )

            try:
                # 直接标记删除，无需获取邮件内容
                self.mail.uid('store', uid_str, '+FLAGS', '(\\Deleted)')
                deleted_count += len(batch_uids)
                logger.info(f"批量标记删除 {len(batch_uids)} 封邮件")

                # 添加小延迟避免服务器过载
                time.sleep(0.1)

            except imaplib.IMAP4.error as e:
                logger.error(f"标记删除失败 UIDs: {uid_str[:100]}..., 错误: {e}")
                # 如果批量失败，尝试逐个删除
                self._delete_individual_uids(batch_uids)
            except Exception as e:
                logger.error(f"未知错误: {e}")

        return deleted_count

    def _delete_individual_uids(self, uid_list):
        """逐个删除UID（备用方案）"""
        for uid in uid_list:
            try:
                uid_str = uid.decode('utf-8') if isinstance(uid, bytes) else str(uid)
                self.mail.uid('store', uid_str, '+FLAGS', '(\\Deleted)')
                time.sleep(0.05)  # 更短的延迟
            except Exception as e:
                logger.warning(f"单个删除失败 UID: {uid_str}, 错误: {e}")

    def search_emails_adaptive(self, sender, start_date, end_date, max_emails_per_chunk=5000):
        """
        自适应的邮件搜索
        关键优化：
        1. 动态调整日期块大小
        2. 根据邮件数量自动缩小搜索范围
        3. 添加重试机制和超时保护
        """
        all_uids = []
        current_date = start_date

        # 初始日期块大小（从7天开始，可根据结果动态调整）
        date_chunk_days = 7
        max_chunk_days = 30  # 最大不超过30天
        min_chunk_days = 1  # 最小1天

        while current_date < end_date:
            chunk_end = min(current_date + timedelta(days=date_chunk_days), end_date)
            since_date = self.to_imap_date(current_date)
            before_date = self.to_imap_date(chunk_end)

            search_criteria = f'(FROM "{sender}" SINCE "{since_date}" BEFORE "{before_date}")'
            logger.info(f"搜索: {search_criteria} (日期块: {date_chunk_days}天)")

            # 添加重试机制
            max_retries = 3
            uid_list = []
            search_success = False

            for attempt in range(max_retries):
                try:
                    # 设置搜索超时保护
                    typ, data = self.mail.uid('search', None, search_criteria)
                    if typ == 'OK':
                        if data[0]:
                            uid_list = data[0].split()
                        search_success = True
                        break
                except Exception as e:
                    logger.warning(f"搜索失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # 指数退避
                    else:
                        logger.error(f"搜索最终失败: {search_criteria}")

            if not search_success:
                # 如果搜索失败，缩小日期块重试
                if date_chunk_days > min_chunk_days:
                    date_chunk_days = max(date_chunk_days // 2, min_chunk_days)
                    logger.info(f"搜索失败，缩小日期块到 {date_chunk_days} 天")
                    continue
                else:
                    # 如果已经是最小块还是失败，跳过这个日期
                    logger.error(f"跳过日期范围: {since_date} - {before_date}")
                    current_date = chunk_end
                    continue

            email_count = len(uid_list)
            logger.info(f"找到 {email_count} 封邮件")

            # 动态调整下次的日期块大小
            if email_count > max_emails_per_chunk:
                # 邮件太多，缩小日期块
                date_chunk_days = max(date_chunk_days // 2, min_chunk_days)
                logger.info(f"邮件数量过多({email_count})，缩小日期块到 {date_chunk_days} 天")
            elif email_count < max_emails_per_chunk // 4 and date_chunk_days < max_chunk_days:
                # 邮件较少，可以适当增大日期块
                date_chunk_days = min(date_chunk_days * 2, max_chunk_days)
                logger.info(f"邮件数量较少({email_count})，增大日期块到 {date_chunk_days} 天")

            all_uids.extend(uid_list)
            current_date = chunk_end

            # 添加适当延迟，避免频繁请求
            time.sleep(0.5)

        return all_uids

    def batch_expunge(self, max_batch_size=1000):
        """
        批量执行expunge
        关键优化：控制expunge的频率，避免一次性删除过多邮件导致超时
        """
        try:
            self.mail.expunge()
            logger.info("成功执行expunge")
            return True
        except Exception as e:
            logger.error(f"Expunge失败: {e}")
            return False

    def delete_emails_for_senders(self, sender_list, start_date, end_date, batch_size=100):
        """
        为多个发件人删除邮件的主函数
        """
        if not self.connect():
            return False

        try:
            for sender in sender_list:
                sender = sender.strip()
                if not sender:
                    continue

                logger.info(f"\n开始处理发件人: {sender}")

                # 搜索邮件（使用自适应搜索）
                uid_list = self.search_emails_adaptive(sender, start_date, end_date)

                if not uid_list:
                    logger.info(f"发件人 {sender} 没有找到邮件")
                    continue

                logger.info(f"发件人 {sender} 共找到 {len(uid_list)} 封邮件")

                # 批量删除
                deleted_count = self.delete_emails_by_uid_batch(uid_list, batch_size)

                # 定期执行expunge（每处理完一个发件人执行一次）
                if deleted_count > 0:
                    if self.batch_expunge():
                        self.deleted_total += deleted_count
                        logger.info(f"发件人 {sender}: 成功删除 {deleted_count} 封邮件")
                    else:
                        logger.warning(f"发件人 {sender}: 标记删除但expunge失败")

                # 处理完每个发件人后短暂休息
                time.sleep(1)

        finally:
            self.disconnect()

        logger.info(f"\n全部完成，共删除邮件：{self.deleted_total}")
        return True


def main():
    """主函数"""
    # 配置信息
    IMAP_SERVER = 'imap.amarsoft.com'  # 你的IMAP服务器，比如imap.gmail.com
    EMAIL_ACCOUNT = 'mjwang@amarsoft.com'
    PASSWORD = 'Wangminjie151'


    # 发件人列表
    sender_list = [
        'amarMonitorFullLink',
        'amarMonitorFullLink@mail.amarsoft.com',
        'cdh_crdc@amarsoft.com',
        'cdh_dev@amarsoft.com',
        'llzhang2@amarsoft.com'
    ]

    # 日期范围
    start_date = datetime.strptime('2021-01-01', "%Y-%m-%d")
    end_date = datetime.strptime('2022-01-01', "%Y-%m-%d")

    # 批次大小（可根据服务器性能调整）
    BATCH_SIZE = 50  # 保守的批次大小，避免超时

    # 如果想要更激进的设置，可以尝试：
    # BATCH_SIZE = 100  # 中等批次大小
    # BATCH_SIZE = 200  # 较大批次大小（需要服务器性能支持）

    # 创建删除器实例
    deleter = OptimizedEmailDeleter(IMAP_SERVER, EMAIL_ACCOUNT, PASSWORD)

    # 执行删除
    success = deleter.delete_emails_for_senders(
        sender_list,
        start_date,
        end_date,
        BATCH_SIZE
    )

    if success:
        logger.info("邮件删除任务完成")
    else:
        logger.error("邮件删除任务失败")


if __name__ == '__main__':
    main()