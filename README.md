# ��� ��������
���-��������� ��� telegram �� python � SpeechKit
# ��� ������������
1) ���������� ���� �����������:
```
git clone https://github.com/karukador/_bot.git
```
2) ���������� ����������� �� `requirements.txt`
3) ���������� DB Browser  
4) �������� ����� ����� [BotFather](https://telegram.me/BotFather) � Telegram 
5) �������� �������� � ������������ � ����� ����������� ������:  
   ���������� [�����](https://code.s3.yandex.net/kids-ai/video/1710521524357368.mp4) �� ������ ����������  
   ������� �� ������, ��������� ������� (������� IP � ����� ������������ �����):  
```
ssh -i <����_��_�����_�_������> student@<ip_�����_�������>  
```
6) �������� IAM-�����, ������� ����� 12 �����  
   ���������� [�����](https://code.s3.yandex.net/kids-ai/video/1710080423616925.mp4) � ��������� IAM-������  
   ������� �� ������� ������� ����:  
```
curl -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token
```
7) �������� ���� `.env`
8) � ����� `.env` �������� ��� TOKEN, iam_token, folder_id:
```
TOKEN = "���_�����"
iam_token = "���_IAM-�����"
folder_id = "���_FOLDER_ID"
```
9) �������� ������ � ����� system_config.py (�� �������)  
10) ��������� ���� bot.py  