from peewee import *

db = SqliteDatabase('student_movement.db')


class BaseModel(Model):
    class Meta:
        database = db


class MovementType(BaseModel):
    class Meta:
        db_table = "movement_types"
    
    name = CharField(max_length=50, unique=True)
    code = CharField(max_length=30, unique=True)


class MovementRecord(BaseModel):
    class Meta:
        db_table = "movement_records"
        indexes = (
            (('student_id', 'movement_date', 'movement_type'), True),
        )
    
    student_id = IntegerField()
    movement_type = ForeignKeyField(MovementType, backref='records', on_delete='RESTRICT')
    movement_date = DateField()
    order_number = CharField(max_length=50)
    is_active = BooleanField(default=True)


def init_db():
    db.connect()
    db.create_tables([MovementType, MovementRecord], safe=True)
    
    if not MovementType.select().exists():
        MovementType.create(name='Перевод', code='transfer')
        MovementType.create(name='Отчисление', code='expelled')
        MovementType.create(name='Восстановление', code='reinstated')
        MovementType.create(name='Академический отпуск', code='academic_leave')
        MovementType.create(name='Выход из академа', code='academic_leave_end')
    
    print("База данных инициализирована")


if __name__ == '__main__':
    init_db()