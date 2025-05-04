#!/usr/bin/env python
# -*- coding: utf-8 -*-

class KyrgyzDeclension:
    """Кыргыз тилиндеги сөздөрдү жөндөмөлөргө бөлүү системасы."""
    
    def __init__(self):
        # Жөндөмөлөрдүн аттары
        self.cases = [
            "Атооч", "Илик", "Барыш", "Табыш", "Жатыш", "Чыгыш"
        ]
        
        # Үндүү тыбыштар
        self.vowels = "аеёиоөуүыэюя"
        self.back_vowels = "аоуыя"   # Жоон үндүүлөр
        self.front_vowels = "еёиөүэю"  # Ичке үндүүлөр
        
        # Жумшак жана катуу тыбыштар
        self.voiceless_consonants = "пфктсшчщх"  # Каткалаң үнсүздөр
        self.sonorants = "йлмнңрв"  # Үндүү үнсүздөр
        self.voiced_consonants = "бвгдж"  # Жумшак үнсүздөр
        
        # Тамгалардын туркүмдөрү
        self.labial_vowels = "оөуү"  # Эриндешкен үндүүлөр
        self.non_labial_vowels = "аеёиыэюя"  # Эриндешпеген үндүүлөр
        
        # Өзгөчө сөздөр үчүн сөздүк
        self.exceptions = {
            # Өзгөчө жөндөлүүчү сөздөр
            "су": {
                "Атооч": "су",
                "Илик": "суунун",
                "Барыш": "сууга",
                "Табыш": "сууну",
                "Жатыш": "сууда", 
                "Чыгыш": "суудан"
            }
        }
    
    def get_last_vowel(self, word):
        """Сөздүн акыркы үндүүсүн кайтарат."""
        for char in reversed(word):
            if char.lower() in self.vowels:
                return char.lower()
        return None
    
    def get_harmony_type(self, word):
        """
        Сөздүн үндөшүү тибин аныктайт.
        Returns: 
            - "back": жоон үндүүлөр үчүн
            - "front": ичке үндүүлөр үчүн
        """
        last_vowel = self.get_last_vowel(word)
        if last_vowel in self.back_vowels:
            return "back"
        elif last_vowel in self.front_vowels:
            return "front"
        # Эгер үндүү табылбаса, жоон үндүү катары эсептейбиз
        return "back"
    
    def is_labial(self, word):
        """Сөздүн акыркы үндүүсү эриндешкенби же жокпу."""
        last_vowel = self.get_last_vowel(word)
        return last_vowel in self.labial_vowels
    
    def decline_noun(self, word):
        """Сөздү жөндөмөлөргө бөлөт."""
        # Өзгөчө сөз эмеспи деп текшерүү
        if word.lower() in self.exceptions:
            return self.exceptions[word.lower()]
        
        # Жыйынтык сөздүгү
        result = {self.cases[0]: word}  # Атооч жөндөмөсү өзгөрүүсүз калат
        
        # Сөздүн аягы
        last_char = word[-1].lower()
        second_last_char = word[-2].lower() if len(word) > 1 else ""
        
        # Сөздүн түзүлүшү боюнча анализ
        harmony = self.get_harmony_type(word)
        ends_with_vowel = last_char in self.vowels
        ends_with_consonant = not ends_with_vowel
        is_labial = self.is_labial(word)
        
        # Өзгөчө тамгалар менен бүткөн сөздөрдү текшерүү
        ends_with_y = last_char == "й"
        ends_with_voiceless = last_char in self.voiceless_consonants
        ends_with_sonorant = last_char in self.sonorants
        ends_with_voiced = last_char in self.voiced_consonants
        
        # ==== ИЛИК ЖӨНДӨМӨСҮ (Кимдин? Эмненин?) ====
        if word.lower() == "мен":
            result[self.cases[1]] = "менин"
        elif word.lower() == "сен":
            result[self.cases[1]] = "сенин"
        elif word.lower() == "ал":
            result[self.cases[1]] = "анын"
        elif word.lower() == "биз":
            result[self.cases[1]] = "бизин"
        elif word.lower() == "силер":
            result[self.cases[1]] = "силердин"
        elif word.lower() == "алар":
            result[self.cases[1]] = "алардын"
        elif ends_with_y:
            if harmony == "back":
                result[self.cases[1]] = word + "дын" if not is_labial else word + "дун"
            else:
                result[self.cases[1]] = word + "дин" if not is_labial else word + "дүн"
        elif ends_with_vowel:
            if harmony == "back":
                result[self.cases[1]] = word + "нын" if not is_labial else word + "нун"
            else:
                result[self.cases[1]] = word + "нин" if not is_labial else word + "нүн"
        elif ends_with_voiceless:
            if harmony == "back":
                result[self.cases[1]] = word + "тын" if not is_labial else word + "тун"
            else:
                result[self.cases[1]] = word + "тин" if not is_labial else word + "түн"
        else:  # Жумшак үнсүз же үндүү үнсүздөр менен бүткөн сөздөр
            if harmony == "back":
                result[self.cases[1]] = word + "дын" if not is_labial else word + "дун"
            else:
                result[self.cases[1]] = word + "дин" if not is_labial else word + "дүн"
        
        # ==== БАРЫШ ЖӨНДӨМӨСҮ (Кимге? Эмнеге?) ====
        if word.lower() == "мен":
            result[self.cases[2]] = "мага"
        elif word.lower() == "сен":
            result[self.cases[2]] = "сага"
        elif word.lower() == "ал":
            result[self.cases[2]] = "ага"
        elif word.lower() == "биз":
            result[self.cases[2]] = "бизге"
        elif word.lower() == "силер":
            result[self.cases[2]] = "силерге"
        elif word.lower() == "алар":
            result[self.cases[2]] = "аларга"
        elif ends_with_y:
            if harmony == "back":
                result[self.cases[2]] = word + "го" if is_labial else word + "га"
            else:
                result[self.cases[2]] = word + "гө" if is_labial else word + "ге"
        elif ends_with_voiceless:
            if harmony == "back":
                result[self.cases[2]] = word + "ко" if is_labial else word + "ка"
            else:
                result[self.cases[2]] = word + "кө" if is_labial else word + "ке"
        else:  # Үндүү, жумшак үнсүз же үндүү үнсүз менен бүткөн сөздөр
            if harmony == "back":
                result[self.cases[2]] = word + "го" if is_labial else word + "га"
            else:
                result[self.cases[2]] = word + "гө" if is_labial else word + "ге"
        
        # ==== ТАБЫШ ЖӨНДӨМӨСҮ (Кимди? Эмнени?) ====
        if word.lower() == "мен":
            result[self.cases[3]] = "мени"
        elif word.lower() == "сен":
            result[self.cases[3]] = "сени"
        elif word.lower() == "ал":
            result[self.cases[3]] = "аны"
        elif word.lower() == "биз":
            result[self.cases[3]] = "бизди"
        elif word.lower() == "силер":
            result[self.cases[3]] = "силерди"
        elif word.lower() == "алар":
            result[self.cases[3]] = "аларды"
        elif ends_with_vowel:
            if harmony == "back":
                result[self.cases[3]] = word + "ны"
            else:
                result[self.cases[3]] = word + "ни"
        elif ends_with_voiceless:
            if harmony == "back":
                result[self.cases[3]] = word + "ты"
            else:
                result[self.cases[3]] = word + "ти"
        else:  # Жумшак үнсүз же үндүү үнсүздөр менен бүткөн сөздөр
            if harmony == "back":
                result[self.cases[3]] = word + "ды"
            else:
                result[self.cases[3]] = word + "ди"
        
        # ==== ЖАТЫШ ЖӨНДӨМӨСҮ (Кимде? Эмнеде?) ====
        if word.lower() == "мен":
            result[self.cases[4]] = "менде"
        elif word.lower() == "сен":
            result[self.cases[4]] = "сенде"
        elif word.lower() == "ал":
            result[self.cases[4]] = "анда"
        elif word.lower() == "биз":
            result[self.cases[4]] = "бизде"
        elif word.lower() == "силер":
            result[self.cases[4]] = "силерде"
        elif word.lower() == "алар":
            result[self.cases[4]] = "аларда"
        elif ends_with_vowel:
            if harmony == "back":
                result[self.cases[4]] = word + "да"
            else:
                result[self.cases[4]] = word + "де"
        elif ends_with_voiceless:
            if harmony == "back":
                result[self.cases[4]] = word + "та"
            else:
                result[self.cases[4]] = word + "те"
        else:  # Жумшак үнсүз же үндүү үнсүздөр менен бүткөн сөздөр
            if harmony == "back":
                result[self.cases[4]] = word + "да"
            else:
                result[self.cases[4]] = word + "де"
        
        # ==== ЧЫГЫШ ЖӨНДӨМӨСҮ (Кимден? Эмнеден?) ====
        if word.lower() == "мен":
            result[self.cases[5]] = "менден"
        elif word.lower() == "сен":
            result[self.cases[5]] = "сенден"
        elif word.lower() == "ал":
            result[self.cases[5]] = "андан"
        elif word.lower() == "биз":
            result[self.cases[5]] = "бизден"
        elif word.lower() == "силер":
            result[self.cases[5]] = "силерден"
        elif word.lower() == "алар":
            result[self.cases[5]] = "алардан"
        elif ends_with_vowel:
            if harmony == "back":
                result[self.cases[5]] = word + "дан"
            else:
                result[self.cases[5]] = word + "ден"
        elif ends_with_voiceless:
            if harmony == "back":
                result[self.cases[5]] = word + "тан"
            else:
                result[self.cases[5]] = word + "тен"
        else:  # Жумшак үнсүз же үндүү үнсүздөр менен бүткөн сөздөр
            if harmony == "back":
                result[self.cases[5]] = word + "дан"
            else:
                result[self.cases[5]] = word + "ден"
        
        # "й" менен бүткөн сөздөр үчүн өзгөчө оңдоолор
        if ends_with_y:
            if harmony == "back":
                result[self.cases[3]] = word + "ду"
                result[self.cases[4]] = word + "до"
                result[self.cases[5]] = word + "дон"
            else:
                result[self.cases[3]] = word + "дү"
                result[self.cases[4]] = word + "дө"
                result[self.cases[5]] = word + "дөн"
        
        return result


def main():
    """Негизги программа."""
    print("Кыргыз тилиндеги сөздөрдү жөндөмөлөргө бөлүү программасы")
    print("--------------------------------------------------------")
    
    decliner = KyrgyzDeclension()
    
    # Бир нече мисалдар
    examples = ["токой", "китеп", "бала", "мектеп", "сөз", "үй", "доктор", "суу", "ай", "жол"]
    

    
    # Колдонуучудан киргизүү
    while True:
        word = input("\nСөздү киргизиңиз (чыгуу үчүн 'exit' жазыңыз): ")
        
        if word.lower() == 'exit':
            print("Программа аяктады. Көрүшкөнчө!")
            break
        
        if not word:
            print("Сөз киргизилген жок. Кайрадан аракет кылыңыз.")
            continue
        
        results = decliner.decline_noun(word)
        
        print(f"\n{word} сөзүнүн жөндөмөлөрү:")
        print("--------------------------------")
        for case, declined in results.items():
            print(f"{case}: {declined}")


if __name__ == "__main__":
    main()