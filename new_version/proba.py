import eval
ud = eval.load_conllu_file("my_corpus/proba.conllu")
print(ud.characters)
for word in ud.words:
    print(word.columns)
