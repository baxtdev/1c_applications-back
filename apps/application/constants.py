LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'


IMPORTANCE_CHOICE = (
    (LOW, 'низкий'),
    (MEDIUM, 'средний'),
    (HIGH, 'высокий'),
)


PRIMARY = 'primary'
CORRECTED ='corrected'

STATUS_CHOICE = (
    (PRIMARY, 'первичная'),
    (CORRECTED, 'исправленное'),
)

CONFIRMED = 'СONFIRMED'
CANCELED = 'CANCELED'
NOT_CONFIRMED = 'NOT_CONFIRMED'


RECONCILIATORS_STATUS_CHOICE = (
    (CONFIRMED, 'Подтвержден'),
    (NOT_CONFIRMED, 'Не подтвержден'),
    (CANCELED, 'Отменен'),
)
