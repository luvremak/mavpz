## [PlantUML](https://github.com/luvremak/mavpz/tree/main/er-diagrams/diagrams/PlantUML)


## [ER-діаграма (нотація Чена)](https://github.com/luvremak/mavpz/blob/main/er-diagrams/diagrams/er-chen-notation/image.png)


## [ER-діаграма (Crow's Foot)](https://github.com/luvremak/mavpz/blob/main/er-diagrams/diagrams/er-crows-foot/image.png)


## [Декларативний опис](https://github.com/luvremak/mavpz/blob/main/er-diagrams/diagrams/%D0%9E%D0%BF%D0%B8%D1%81%20ER-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%96.pdf)


## [Відображення у коді](https://github.com/luvremak/mavpz/blob/main/er-diagrams/code/entities.py)


## Пояснення зв'язків між сутностями

### Зв'язки «один до багатьох»

- **Therapist → Session**: один терапевт проводить багато сесій.  
- **Client → Session**: один клієнт відвідує багато сесій.  
- **Client → ThoughtRecord**: один клієнт веде багато записів думок.  
- **Client → MoodEntry**: один клієнт робить багато записів настрою.  
- **Therapist → Assignment**: один терапевт призначає багато завдань.  
- **Client → Assignment**: один клієнт отримує багато завдань.
