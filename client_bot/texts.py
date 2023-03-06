# /start
start_cmd_reply = \
"""
Привіт! На зв‘язку mila’s bot. Я з радістю допоможу тобі у будь-якому б‘юті питанні, навіть, якщо він не зв’язаний з магазином.
Що обереш?
"""

# Б‘юті Консьєрж
beauty_concierge_cmd_start_reply = \
"""
Ооо, я можу підказати який крем тобі не підійде, які рум’яна купити (не у нас😁), де класно роблять зачіску у Києві або як твоє замовлення. Ділись, що турбує?
Залишайся на зв’язку, я скоро відповім <3
"""

beauty_concierge_cmd_end_reply = \
"""
Сподіваюсь, ти від мене в захваті, як я від тебе. Тільки не виходь, бо я тобі не зможу розказати про нові офігенні інфоприводи!🫂
"""

beauty_concierge_message_to_expert = """
[Нове повідомлення] [@{from_user_tg_username}]
{from_user_tg_id}
{client_text}
"""

# Залишити відгук
feedback_cmd_start_reply = \
"""
Ооо, розкажи чесно свою думку, вона дуже потрібна нам для розвитку. Про баночку, новий бренд який десь побачила, класне місце та думку про нашу роботу. Зізнавайся 😁

(відправ будь ласка одним повідомленням, щоб ми не загубили важливі зауваження або ідеї)
"""

feedback_next_step_reply = """
Можливо, ще щось хочеш додати?
"""

feedback_cmd_end_reply = \
"""
Дякую!
Тільки не виходь, бо я тобі не зможу розказати про нові офігенні інфоприводи!🫂
"""

feedback_message_to_expert = """
[Новий відгук] [@{from_user_tg_username}]
{from_user_tg_id}
{client_text}
"""

# Q&A
q_and_a_cmd_reply = """
Що тебе цікавить? Ми відповімо!
"""

q_and_a_shop_reply = """
МАГАЗИН (адреса, номер, паркування, графік)

Магазин працює з 10 до 19, за адресою вул. Велика Васильківська, 49 (між Чорноморкою та Master Zoo). У нас є парковка, тож подзвоніть на 073 000 38 34, щоб ми підняли шлагбаум.
"""

q_and_a_delivery_reply = """
ДОСТАВКА

<b>1. Експрес-доставка по Києву</b>
Ми здійснюємо експрес доставку протягом двох годин Києвом за допомогою служби таксі або 
нашого кур'єра.

Вартість послуги – 100 грн (обрати та оплатити можна у кошику).
Ми обробляємо та відправляємо замовлення щоденно 
з 10:00 до 19:00.

<b>2.Самовивіз</b>
Замовлення, оформлені у нас на сайті, ви можете забрати у той самий день за адресою 
вул. Велика Васильківська, 49 

<b>3. Нова пошта</b>
Ми здійснюємо доставку товару в будь-який населений пункт України, з яким налагоджено кур’єрське сполучення компанією Нова Пошта.

Замовлення понад 3000 грн доставляються безкоштовно. 
Замовлення до 3000 грн оплачуються вами згідно з тарифами транспортної компанії Нова Пошта.
"""

q_and_a_payment_reply = """
ОПЛАТА

<b>Оплата замовлення на сайті:</b>
Кредитна картка Visa/Mastercard, Apple Pay, Google Pay, оплата через термінал та Privat24. Після оплати вам на пошту прийде фіскальний чек.

<b>Оплата самовивозу:</b>
Можна одразу на сайті, або фізично в магазині карткою чи готівкою. Фіскальний чек відправляємо на пошту по запиту клієнта.
"""

q_and_a_certificate_reply = """
СЕРТИФІКАТ

У нас для тебе є класне рішення у вигляді онлайн та офлайн сертифікатів на такі суми: 500, 1000, 1500, 2000, 5 000, 10 000 та 20 000 грн. Їх можна замовити на сайті - http://bit.ly/3xYAIsz

Сертифікат на будь-яку зручну для тебе суму можна замовити, написавши нам в дірект
"""
