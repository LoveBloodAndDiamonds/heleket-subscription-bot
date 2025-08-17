START_COMMAND_RESPONSE = """
<b>Здравствуйте, {user}!</b>

Вы зашли в бота для получения доступа в приватный канал/чат.

❔ Введите в поле для ввода "/" для получения списка доступных команд.
"""


HELP_COMMAND_RESPONSE = """
ℹ️ Список команд:
/subscribe - Оформить подписку
/profile - Ваш профиль
/contacts - Контакты для связи
/help - Список доступных команд
"""


PROFILE_COMMAND_RESPONSE = """
🧍Ваш профиль:
id: <code>{user_id}</code>
{subscribtion_status}
"""

CONTACTS_COMMAND_RESPONSE = """
📞 Контакты для связи:
Telegram: {admin_username}
"""

SUBSCRIBE_COMMAND_RESPONSE = """
🏷️ Для оплаты подписки нажмите на кнопку ниже.
Подпска стоит {subscription_price}$ и выдается сроком на 1 мес.
Платеж проверяется автоматически. После перевода - вы получите сообщение об успешной оплате.
"""
