from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Literal
from enum import Enum


class SessionType(str, Enum):
    """Типи терапевтичних сесій"""
    INITIAL = "initial"     
    REGULAR = "regular"      
    FINAL = "final"          
    CRISIS = "crisis"        


class AssignmentStatus(str, Enum):
    """Статуси виконання завдань"""
    PENDING = "pending"      
    COMPLETED = "completed"  
    OVERDUE = "overdue"      

@dataclass
class Therapist:
    """
    Сутність: THERAPIST (Терапевт/Психолог)
    Один терапевт може мати багато клієнтів та проводити багато сесій.
    """
    therapist_id: int  
    full_name: str
    email: str
    specialization: str  
    registration_date: date
    
    def __str__(self) -> str:
        return f"Терапевт #{self.therapist_id}: {self.full_name} ({self.specialization})"


@dataclass
class Client:
    """
    Сутність: CLIENT (Клієнт)
    зв'язок 1:N з SESSION
    зв'язок 1:N з THOUGHT_RECORD
    зв'язок 1:N з MOOD_ENTRY
    зв'язок 1:N з ASSIGNMENT
    """
    client_id: int 
    full_name: str
    email: str
    birth_date: date
    registration_date: date
    
    def __str__(self) -> str:
        return f"Клієнт #{self.client_id}: {self.full_name}"
    
    def calculateAge(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )


@dataclass
class Session:
    """
    Сутність: SESSION 

    therapist_id → FK до THERAPIST (багато сесій належать одному терапевту)
    client_id → FK до CLIENT (багато сесій належать одному клієнту)
    """
    session_id: int  
    therapist_id: int  
    client_id: int  
    session_date: datetime
    duration_minutes: int  
    notes: str 
    session_type: SessionType
    
    def __str__(self) -> str:
        return (f"Сесія #{self.session_id}: {self.session_type.value} "
                f"({self.session_date.strftime('%d.%m.%Y %H:%M')})")


@dataclass
class ThoughtRecord:
    """
    Сутність: THOUGHT_RECORD 
    
    - client_id → FK до CLIENT (багато записів належать одному клієнту)
    """
    record_id: int  
    client_id: int  
    record_date: datetime
    situation: str  
    automatic_thought: str  
    emotion: str  
    emotion_intensity: int  
    alternative_thought: Optional[str] = None  
    
    def __str__(self) -> str:
        return (f"Запис думки #{self.record_id}: {self.emotion} "
                f"({self.emotion_intensity}/10)")
    
    def isProcessed(self) -> bool:
        """Перевіряє, чи клієнт опрацював думку (чи є альтернативна думка)"""
        return self.alternative_thought is not None and len(self.alternative_thought) > 0


@dataclass
class MoodEntry:
    """
    Сутність: MOOD_ENTRY 

    - client_id → FK до CLIENT (багато записів належать одному клієнту)
    """
    mood_id: int  
    client_id: int  
    entry_date: datetime
    mood_score: int  
    notes: Optional[str] = None
    
    def __str__(self) -> str:
        date_str = self.entry_date.strftime('%d.%m.%Y %H:%M')
        return f"Настрій {self.mood_score}/10 ({date_str})"
    
    def getMoodLabel(self) -> str:
        """Повертає текстовий опис настрою на основі оцінки"""
        if self.mood_score <= 3:
            return "Дуже погано"
        elif self.mood_score <= 5:
            return "Погано"
        elif self.mood_score <= 7:
            return "Середньо"
        elif self.mood_score <= 9:
            return "Добре"
        else:
            return "Відмінно"


@dataclass
class Assignment:
    """
    Сутність: ASSIGNMENT 

    - therapist_id → FK до THERAPIST (терапевт, який призначив завдання)
    - client_id → FK до CLIENT (клієнт, якому призначено завдання)
    """
    assignment_id: int  
    therapist_id: int  
    client_id: int  
    title: str
    description: str
    assigned_date: date
    due_date: date
    status: AssignmentStatus
    
    def __str__(self) -> str:
        return f"Завдання #{self.assignment_id}: {self.title} [{self.status.value}]"
    
    def isOverdue(self) -> bool:
        """Перевіряє, чи прострочене завдання"""
        return date.today() > self.due_date and self.status != AssignmentStatus.COMPLETED
    
    def daysUntilDue(self) -> int:
        """Скільки днів залишилось до дедлайну"""
        return (self.due_date - date.today()).days


if __name__ == "__main__":
    print("ПОЧАТОК")
    
    therapist = Therapist(
        therapist_id=1,
        full_name="Олена Голуб",
        email="olena.holub@gmail.com",
        specialization="ПТСР, депресія та тривожні розлади",
        registration_date=date(2024, 6, 1)
    )
    print(f"\n✓ {therapist}")

    client = Client(
        client_id=5,
        full_name="Іван Петренко",
        email="ivan.petrenko@gmail.com",
        birth_date=date(1990, 3, 15),
        registration_date=date(2025, 9, 10)
    )
    print(f"✓ {client}, вік: {client.calculateAge()} років")

    session = Session(
        session_id=101,
        therapist_id=therapist.therapist_id,  
        client_id=client.client_id,  
        session_date=datetime(2025, 10, 23, 10, 0),
        duration_minutes=50,
        notes="Клієнт почав відкриватися. Працювали над панічними атаками.",
        session_type=SessionType.REGULAR
    )
    print(f"✓ {session}")
    
    thought = ThoughtRecord(
        record_id=50,
        client_id=client.client_id,  # FK до клієнта
        record_date=datetime(2025, 10, 23, 14, 30),
        situation="Почув сирену повітряної тривоги",
        automatic_thought="Зараз щось страшне станеться, я не в безпеці",
        emotion="Паніка, тривога",
        emotion_intensity=9,
        alternative_thought="Я в укритті. Сирена — це попередження, а не гарантія небезпеки."
    )
    print(f"✓ {thought}")
    print(f"  Опрацьовано: {'Так' if thought.isProcessed() else 'Ні'}")
    
    mood = MoodEntry(
        mood_id=1,
        client_id=client.client_id,  
        entry_date=datetime(2025, 10, 23, 8, 0),
        mood_score=4,
        notes="Прокинувся з тривогою, важко зосередитися"
    )
    print(f"✓ {mood} - {mood.getMoodLabel()}")
    
    assignment = Assignment(
        assignment_id=10,
        therapist_id=therapist.therapist_id,  
        client_id=client.client_id,  
        title="Щоденник думок",
        description="Записувати 3 автоматичні думки щодня протягом тижня",
        assigned_date=date(2025, 10, 20),
        due_date=date(2025, 10, 27),
        status=AssignmentStatus.PENDING
    )
    print(f"✓ {assignment}")
    print(f"  Днів до дедлайну: {assignment.daysUntilDue()}")
    print(f"  Прострочене: {'Так' if assignment.isOverdue() else 'Ні'}")
    
    print("\n ЗАРВЕРШЕНО")