from typing import Dict, List, Optional
import re

class KyrgyzDeclension:
    def __init__(self):
        # Падежи
        self.cases = ["Атооч", "Илик", "Барыш", "Табыш", "Жатыш", "Чыгыш"]
        
        # Гласные и их категории
        self.vowels = "аеёиоөуүыэюя"
        self.back_vowels = "аоуыя"
        self.front_vowels = "еёиöүэю"
        self.labial_vowels = "оöуү"
        
        # Согласные
        self.voiceless_consonants = "пфктсшчщхц"
        self.voiced_consonants = "бвгджзлмнңрй"
        
        # Паттерны для заимствованных слов (окончания, требующие соединительной гласной)
        self.foreign_patterns = ["ск$", "нк$", "нг$", "рк$", "рг$", "нт$", "ст$", "зд$", "др$", "тр$", "кт$"]
        
        # Аффиксы для каждого падежа в зависимости от гармонии и контекста
        self.affixes = {
            "Илик": {
                "back": {"labial": "дун", "non_labial": "дын", "vowel": "нун", "voiceless": "тун"},
                "front": {"labial": "дүн", "non_labial": "дин", "vowel": "нин", "voiceless": "тин"}
            },
            "Барыш": {
                "back": {"labial": "го", "non_labial": "га", "vowel": "га", "voiceless": "ка"},
                "front": {"labial": "гө", "non_labial": "ге", "vowel": "ге", "voiceless": "ке"}
            },
            "Табыш": {
                "back": {"labial": "ду", "non_labial": "ды", "vowel": "ну", "voiceless": "ту"},
                "front": {"labial": "дү", "non_labial": "ди", "vowel": "ни", "voiceless": "ти"}
            },
            "Жатыш": {
                "back": {"labial": "до", "non_labial": "да", "vowel": "да", "voiceless": "та"},
                "front": {"labial": "дө", "non_labial": "де", "vowel": "де", "voiceless": "те"}
            },
            "Чыгыш": {
                "back": {"labial": "дон", "non_labial": "дан", "vowel": "дан", "voiceless": "тан"},
                "front": {"labial": "дөн", "non_labial": "ден", "vowel": "ден", "voiceless": "тен"}
            }
        }
        
        # Словарь исключений
        self.exceptions = {
            "мен": ["мен", "менин", "мага", "мени", "менде", "менден"],
            "сен": ["сен", "сенин", "сага", "сени", "сенде", "сенден"],
            "ал": ["ал", "анын", "ага", "аны", "анда", "андан"],
            "биз": ["биз", "биздин", "бизге", "бизди", "бизде", "бизден"],
            "силер": ["силер", "силердин", "силерге", "силерди", "силерде", "силерден"],
            "алар": ["алар", "алардын", "аларга", "аларды", "аларда", "алардан"],
            "бу": ["бу", "бул", "буга", "буну", "бул", "булдан"],
            "ошол": ["ошол", "ошолдун", "ошолго", "ошолду", "ошолдо", "ошолдон"],
            "ким": ["ким", "кимдин", "кимге", "кимди", "кимде", "кимден"],
            "эмне": ["эмне", "эмненин", "эмнеге", "эмнени", "эмнеде", "эмнеден"],
            "эч ким": ["эч ким", "эч кимдин", "эч кимге", "эч кимди", "эч кимде", "эч кимден"],
            "эч нерсе": ["эч нерсе", "эч нерсенин", "эч нерсеге", "эч нерсени", "эч нерседе", "эч нерседен"],
            "бирөө": ["бирөө", "бирөөнүн", "бирөөгө", "бирөөнү", "бирөөдө", "бирөөдөн"],
            "баары": ["баары", "баарынын", "баарыга", "баарыны", "баарыда", "баарыдан"],
            "ар ким": ["ар ким", "ар кимдин", "ар кимге", "ар кимди", "ар кимде", "ар кимден"],
            "омск": ["Омск", "Омскинин", "Омскиге", "Омскини", "Омскиде", "Омскиден"],
            "телефон": ["телефон", "телефондун", "телефондогу", "телефонду", "телефондодо", "телефондон"],
            "имарат": ["имарат", "имараттын", "имаратка", "имаратты", "имаратта", "имараттан"],
            "китеп": ["китеп", "китептин", "китепке", "китепти", "китепте", "китептен"],
            "автобус": ["автобус", "автобустун", "автобусга", "автобусту", "автобуста", "автобустан"],
            "радио": ["радио", "радионун", "радиого", "радиону", "радиодо", "радиодон"],
            "стол": ["стол", "столдун", "столго", "столду", "столдо", "столдон"],
            "компьютер": ["компьютер", "компьютердин", "компьютерге", "компьютерди", "компьютерде", "компьютерден"],
            "телевизор": ["телевизор", "телевизордун", "телевизорго", "телевизорду", "телевизордо", "телевизордон"],
            "музыка": ["музыка", "музыканын", "музыкага", "музыканы", "музыкада", "музыкадан"],
            "интернет": ["интернет", "интернеттин", "интернетке", "интернетти", "интернетте", "интернеттен"],
            "суу": ["суу", "суунун", "сууга", "сууну", "сууда", "суудан"],
            "көз": ["көз", "көздүн", "көзгө", "көздү", "көздө", "көздөн"],
            "кол": ["кол", "колдун", "колго", "колду", "колдо", "колдон"],
            "жол": ["жол", "жолдун", "жолго", "жолду", "жолдо", "жолдон"]
        }

    def get_last_vowel(self, word: str) -> Optional[str]:
        """Находит последний гласный в слове."""
        for ch in reversed(word.lower()):
            if ch in self.vowels:
                return ch
        return None

    def get_harmony(self, vowel: Optional[str]) -> str:
        """Определяет тип гармонии (передняя/задняя)."""
        if not vowel:
            return "back"  # По умолчанию задняя гармония для слов без гласных
        return "back" if vowel in self.back_vowels else "front"

    def is_labial(self, vowel: Optional[str]) -> bool:
        """Проверяет, является ли гласный губным."""
        return vowel in self.labial_vowels if vowel else False

    def is_foreign(self, word: str) -> bool:
        """Проверяет, является ли слово заимствованным по паттернам окончаний."""
        for pattern in self.foreign_patterns:
            if re.search(pattern, word.lower()):
                return True
        return False

    def get_connective_vowel(self, word: str, harmony: str) -> str:
        """Определяет соединительный гласный для заимствованных слов."""
        if harmony == "back":
            return "ы" if not self.is_labial(self.get_last_vowel(word)) else "у"
        return "и"

    def decline(self, word: str) -> Dict[str, str]:
        """Склоняет слово по всем падежам."""
        word_lower = word.lower()

        # Проверяем исключения
        if word_lower in self.exceptions:
            return dict(zip(self.cases, self.exceptions[word_lower]))

        # Определяем характеристики слова
        last_vowel = self.get_last_vowel(word)
        harmony = self.get_harmony(last_vowel)
        labial = self.is_labial(last_vowel)
        ends_with_vowel = word[-1].lower() in self.vowels
        ends_with_voiceless = word[-1].lower() in self.voiceless_consonants
        ends_with_y = word[-1].lower() == "й"
        is_foreign = self.is_foreign(word)

        result = {self.cases[0]: word}
        connective = self.get_connective_vowel(word, harmony) if is_foreign else ""

        for case in self.cases[1:]:
            # Определяем контекст для выбора аффикса
            if ends_with_vowel:
                context = "vowel"
            elif ends_with_voiceless:
                context = "voiceless"
            elif ends_with_y:
                context = "labial" if labial else "non_labial"
            else:
                context = "labial" if labial else "non_labial"

            # Получаем аффикс
            affix = self.affixes[case][harmony][context]
            
            # Для заимствованных слов добавляем соединительный гласный
            if is_foreign and not ends_with_vowel:
                result[case] = word + connective + affix
            else:
                result[case] = word + affix

        return result

    def decline_to_list(self, word: str) -> List[str]:
        """Возвращает склонения в виде списка для совместимости с форматом исключений."""
        declension = self.decline(word)
        return [declension[case] for case in self.cases]


if __name__ == "__main__":
    declension = KyrgyzDeclension()
    # Тестовые примеры
    test_words = ["тоо"]
    for word in test_words:
        result = declension.decline(word)
        print(f"\nСклонение слова '{word}':")
        for case, form in result.items():
            print(f"{case}: {form}")