from kyrgyz_declension import KyrgyzDeclension

def main():
    decliner = KyrgyzDeclension()
    print("Кыргызча сөздөрдү жөндөп берүүчү программа!")
    print("Чыгуу үчүн 'exit' жазыңыз.")

    while True:
        word = input("\nСөз: ").strip()
        if word.lower() == "exit":
            print("Программа жабылды.")
            break
        if not word:
            print("Сөз киргизилген жок.")
            continue
        
        forms = decliner.decline(word)
        for case, form in forms.items():
            print(f"{case}: {form}")

if __name__ == "__main__":
    main()
