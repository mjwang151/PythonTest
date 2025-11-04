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

    def connect(self, debug_mode=False):
        """
        建立IMAP连接 - 增强诊断版本
        """
        try:
            if debug_mode:
                logger.info(f"尝试连接IMAP服务器: {self.imap_server}")
                logger.info(f"用户名: {self.email_account}")
                logger.info(f"密码长度: {len(self.password) if self.password else 0}")

            # 检查基本参数
            if not self.imap_server or not self.email_account or not self.password:
                logger.error("IMAP服务器、邮箱账号或密码为空")
                return False

            # 检查密码是否还是占位符
            if self.password in ['****', '***', 'your_password', 'password']:
                logger.error("请设置正确的邮箱密码，当前使用的是占位符")
                return False

            logger.info("正在建立SSL连接...")
            self.mail = imaplib.IMAP4_SSL(self.imap_server)

            if debug_mode:
                # 启用调试模式
                self.mail.debug = 4

            logger.info("正在进行身份验证...")

            # 尝试登录
            try:
                self.mail.login(self.email_account, self.password)
                logger.info("身份验证成功")
            except imaplib.IMAP4.error as e:
                error_msg = str(e)
                logger.error(f"身份验证失败: {error_msg}")

                # 提供详细的错误分析
                if "authentication failed" in error_msg.lower():
                    logger.error("可能的解决方案:")
                    logger.error("1. 检查用户名和密码是否正确")
                    logger.error("2. 如果是企业邮箱，可能需要应用专用密码")
                    logger.error("3. 检查是否需要启用IMAP服务")
                elif "parse error" in error_msg.lower():
                    logger.error("可能的解决方案:")
                    logger.error("1. 用户名或密码包含特殊字符，尝试URL编码")
                    logger.error("2. 检查密码是否包含空格或特殊符号")
                    logger.error("3. 尝试使用不同的认证方式")
                elif "connection" in error_msg.lower():
                    logger.error("可能的解决方案:")
                    logger.error("1. 检查网络连接")
                    logger.error("2. 确认IMAP服务器地址正确")
                    logger.error("3. 检查防火墙设置")

                return False

            logger.info("正在选择收件箱...")
            self.mail.select('INBOX')
            logger.info("IMAP连接成功")
            return True

        except Exception as e:
            logger.error(f"IMAP连接失败: {e}")

            # 提供通用的解决建议
            logger.error("\n=== 连接失败诊断 ===")
            logger.error("请检查以下项目:")
            logger.error("1. IMAP服务器地址是否正确")
            logger.error("2. 邮箱账号格式是否正确（需要完整邮箱地址）")
            logger.error("3. 密码是否正确（可能需要应用专用密码）")
            logger.error("4. 是否启用了IMAP服务")
            logger.error("5. 网络连接是否正常")
            logger.error("6. 防火墙是否阻止连接")

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

    def search_emails_by_subject_adaptive(self, subject_keyword, start_date, end_date, max_emails_per_chunk=5000):
        """
        基于主题关键词的自适应邮件搜索
        关键优化：
        1. 使用IMAP SUBJECT搜索
        2. 动态调整日期块大小
        3. 添加重试机制和超时保护
        """
        all_uids = []
        current_date = start_date

        # 初始日期块大小
        date_chunk_days = 7
        max_chunk_days = 30
        min_chunk_days = 1

        while current_date < end_date:
            chunk_end = min(current_date + timedelta(days=date_chunk_days), end_date)
            since_date = self.to_imap_date(current_date)
            before_date = self.to_imap_date(chunk_end)

            # 构建主题搜索条件
            search_criteria = f'(SUBJECT "{subject_keyword}" SINCE "{since_date}" BEFORE "{before_date}")'
            logger.info(f"搜索: {search_criteria} (日期块: {date_chunk_days}天)")

            # 添加重试机制
            max_retries = 3
            uid_list = []
            search_success = False

            for attempt in range(max_retries):
                try:
                    typ, data = self.mail.uid('search', None, search_criteria)
                    if typ == 'OK':
                        if data[0]:
                            uid_list = data[0].split()
                        search_success = True
                        break
                except Exception as e:
                    logger.warning(f"搜索失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                    else:
                        logger.error(f"搜索最终失败: {search_criteria}")

            if not search_success:
                if date_chunk_days > min_chunk_days:
                    date_chunk_days = max(date_chunk_days // 2, min_chunk_days)
                    logger.info(f"搜索失败，缩小日期块到 {date_chunk_days} 天")
                    continue
                else:
                    logger.error(f"跳过日期范围: {since_date} - {before_date}")
                    current_date = chunk_end
                    continue

            email_count = len(uid_list)
            logger.info(f"找到 {email_count} 封邮件")

            # 动态调整日期块大小
            if email_count > max_emails_per_chunk:
                date_chunk_days = max(date_chunk_days // 2, min_chunk_days)
                logger.info(f"邮件数量过多({email_count})，缩小日期块到 {date_chunk_days} 天")
            elif email_count < max_emails_per_chunk // 4 and date_chunk_days < max_chunk_days:
                date_chunk_days = min(date_chunk_days * 2, max_chunk_days)
                logger.info(f"邮件数量较少({email_count})，增大日期块到 {date_chunk_days} 天")

            all_uids.extend(uid_list)
            current_date = chunk_end
            time.sleep(0.5)

    def search_emails_by_subject_with_verification(self, subject_keywords, start_date, end_date,
                                                   max_emails_per_chunk=5000):
        """
        基于主题关键词搜索并验证匹配的邮件
        支持多个关键词的模糊匹配

        Args:
            subject_keywords: 字符串或列表，支持多个关键词
            start_date: 开始日期
            end_date: 结束日期
            max_emails_per_chunk: 每个日期块最大邮件数
        """
        # 处理关键词参数
        if isinstance(subject_keywords, str):
            keywords = [subject_keywords]
        else:
            keywords = subject_keywords

        all_matched_uids = []
        current_date = start_date

        date_chunk_days = 7
        max_chunk_days = 30
        min_chunk_days = 1

        while current_date < end_date:
            chunk_end = min(current_date + timedelta(days=date_chunk_days), end_date)
            since_date = self.to_imap_date(current_date)
            before_date = self.to_imap_date(chunk_end)

            # 先获取日期范围内的所有邮件
            search_criteria = f'(SINCE "{since_date}" BEFORE "{before_date}")'
            logger.info(f"搜索日期范围: {since_date} - {before_date} (日期块: {date_chunk_days}天)")

            max_retries = 3
            uid_list = []
            search_success = False

            for attempt in range(max_retries):
                try:
                    typ, data = self.mail.uid('search', None, search_criteria)
                    if typ == 'OK':
                        if data[0]:
                            uid_list = data[0].split()
                        search_success = True
                        break
                except Exception as e:
                    logger.warning(f"搜索失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                    else:
                        logger.error(f"搜索最终失败: {search_criteria}")

            if not search_success:
                if date_chunk_days > min_chunk_days:
                    date_chunk_days = max(date_chunk_days // 2, min_chunk_days)
                    logger.info(f"搜索失败，缩小日期块到 {date_chunk_days} 天")
                    continue
                else:
                    logger.error(f"跳过日期范围: {since_date} - {before_date}")
                    current_date = chunk_end
                    continue

            email_count = len(uid_list)
            logger.info(f"日期范围内共找到 {email_count} 封邮件")

            # 动态调整日期块大小
            if email_count > max_emails_per_chunk:
                date_chunk_days = max(date_chunk_days // 2, min_chunk_days)
                logger.info(f"邮件数量过多({email_count})，缩小日期块到 {date_chunk_days} 天")
                continue
            elif email_count < max_emails_per_chunk // 4 and date_chunk_days < max_chunk_days:
                date_chunk_days = min(date_chunk_days * 2, max_chunk_days)

            # 如果邮件数量合理，进行主题匹配验证
            if uid_list:
                matched_uids = self._verify_subject_match(uid_list, keywords)
                all_matched_uids.extend(matched_uids)
                logger.info(f"主题匹配的邮件: {len(matched_uids)} 封")

            current_date = chunk_end
            time.sleep(0.5)

        return all_matched_uids

    def _verify_subject_match(self, uid_list, keywords, batch_size=50):
        """
        验证邮件主题是否匹配关键词
        """
        matched_uids = []

        for i in range(0, len(uid_list), batch_size):
            batch_uids = uid_list[i:i + batch_size]
            uid_str = ','.join(
                uid.decode('utf-8') if isinstance(uid, bytes) else str(uid)
                for uid in batch_uids
            )

            try:
                # 只获取邮件头部信息，不获取邮件体
                typ, msg_data = self.mail.uid('fetch', uid_str, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
                if typ != 'OK':
                    logger.warning(f'获取邮件头失败: {uid_str}')
                    continue

                # 解析每封邮件的主题
                for j in range(0, len(msg_data), 2):
                    if j + 1 >= len(msg_data) or not msg_data[j] or not msg_data[j][1]:
                        continue

                    try:
                        # 解析邮件头
                        header_data = msg_data[j][1]
                        if isinstance(header_data, bytes):
                            header_text = header_data.decode('utf-8', errors='ignore')
                        else:
                            header_text = str(header_data)

                        # 提取主题
                        subject_line = ''
                        for line in header_text.split('\n'):
                            if line.lower().startswith('subject:'):
                                subject_line = line[8:].strip()  # 去掉 'Subject:' 前缀
                                break

                        if subject_line:
                            subject = self.clean_subject(subject_line)

                            # 检查是否匹配任何关键词（不区分大小写）
                            for keyword in keywords:
                                if keyword.lower() in subject.lower():
                                    matched_uids.append(batch_uids[j // 2])
                                    logger.debug(f'匹配: 关键词="{keyword}" | 主题="{subject}"')
                                    break
                    except Exception as e:
                        logger.warning(f'解析邮件主题失败: {e}')
                        continue

            except Exception as e:
                logger.error(f'批量获取邮件头失败: {e}')
                continue

        return matched_uids
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

    def delete_emails_by_subject(self, subject_keywords, start_date, end_date, batch_size=100, use_imap_search=True):
        """
        根据邮件主题删除邮件的主函数

        Args:
            subject_keywords: 主题关键词，可以是字符串或列表
            start_date: 开始日期
            end_date: 结束日期
            batch_size: 批次大小
            use_imap_search: 是否使用IMAP原生搜索（更快但可能不支持模糊匹配）
        """
        if not self.connect():
            return False

        try:
            logger.info(f"\n开始处理主题关键词: {subject_keywords}")

            if use_imap_search and isinstance(subject_keywords, str):
                # 使用IMAP原生搜索（更快，但可能不支持复杂的模糊匹配）
                uid_list = self.search_emails_by_subject_adaptive(subject_keywords, start_date, end_date)
            else:
                # 使用验证式搜索（支持复杂的模糊匹配，但较慢）
                uid_list = self.search_emails_by_subject_with_verification(subject_keywords, start_date, end_date)

            if not uid_list:
                logger.info(f"没有找到匹配主题的邮件")
                return True

            logger.info(f"共找到 {len(uid_list)} 封匹配的邮件")

            # 批量删除
            deleted_count = self.delete_emails_by_uid_batch(uid_list, batch_size)

            # 执行expunge
            if deleted_count > 0:
                if self.batch_expunge():
                    self.deleted_total += deleted_count
                    logger.info(f"成功删除 {deleted_count} 封邮件")
                else:
                    logger.warning(f"标记删除但expunge失败")

        finally:
            self.disconnect()

        logger.info(f"\n全部完成，共删除邮件：{self.deleted_total}")
        return True
    def list_all_folders(self):
        if not self.mail:
            logger.warning("尚未建立连接，无法列出文件夹")
            return

        logger.info("开始列出邮箱文件夹：")
        try:
            typ, folders = self.mail.list()
            if typ == 'OK':
                for folder in folders:
                    print(folder.decode())  # 或 logger.info(folder.decode())
            else:
                logger.error("无法获取文件夹列表")
        except Exception as e:
            logger.error(f"列出文件夹时出错: {e}")

def main():
    """主函数 - 支持按发件人和按主题两种删除方式"""

    # 配置信息
    IMAP_SERVER = 'imap.amarsoft.com'  # 你的IMAP服务器，比如imap.gmail.com
    EMAIL_ACCOUNT = 'mjwang@amarsoft.com'
    PASSWORD = 'Wangminjie151'

    # 日期范围
    start_date = datetime.strptime('2017-05-15', "%Y-%m-%d")
    end_date = datetime.strptime('2025-01-01', "%Y-%m-%d")

    # 批次大小（可根据服务器性能调整）
    BATCH_SIZE = 50  # 保守的批次大小，避免超时

    # 创建删除器实例
    deleter = OptimizedEmailDeleter(IMAP_SERVER, EMAIL_ACCOUNT, PASSWORD)
    # 选择删除方式
    delete_mode = "subject"  # 可选: "sender" 或 "subject"

    if delete_mode == "sender":
        # 方式1: 按发件人删除
        sender_list = [
            'amarMonitorFullLink',
            'amarMonitorFullLink@mail.amarsoft.com',
            'cdh_crdc@amarsoft.com',
            'cdh_dev@amarsoft.com',
            'llzhang2@amarsoft.com'
        ]

        success = deleter.delete_emails_for_senders(
            sender_list,
            start_date,
            end_date,
            BATCH_SIZE
        )

    elif delete_mode == "subject":
        # 方式2: 按主题关键词删除

        # 单个关键词
        # subject_keyword = "测试"

        # 或者多个关键词（匹配任意一个即可）
        subject_keywords = ["amarMonitor"]

        success = deleter.delete_emails_by_subject(
            subject_keywords,  # 或 subject_keywords
            start_date,
            end_date,
            BATCH_SIZE,
            use_imap_search=False  # True=使用IMAP搜索(快), False=使用验证搜索(准确)
        )

    if success:
        logger.info("邮件删除任务完成")
    else:
        logger.error("邮件删除任务失败")

if __name__ == '__main__':
    main()