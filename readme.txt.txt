1. app.yaml�� application �̸� ���
2. apps/settings.py�� SECRET_KEY, ADMIN, SQLALCHEMY_DATABASE_URI ����
3. models.py�� class ����
4. cmd���� ���� ��ġ�� �̵� �� python manger.py db init / python manager.py db migrate / python manager.py db upgrade
* such no revision �߸� drop alembic_version 