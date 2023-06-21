"""Ewondo Transcription Tansform API (ETTA)

Authors
 * St Germes Bengono Obiang 2023
"""

import re
import unicodedata
import unidecode

import Utils


class SyllabificationEwonodo:
    def __init__(self, word):
        self.word = word
        self.state = ["A", "B", "C", "D", "E"] #State list of finite automate
        self.initState = "A" #Initial state
        self.finalState= ["C", "D", "E"] #final state
        self.currentState = "A"  # Initial state
        self.consonant = ["m", "b", "k", "s", "g", "n", "d", "y", "z", "p", "s", "l", "ŋ", "t", "w", "f", "h", "r", "v", "j"]
        self.consonantEwo = ["p", "t", "ts", "k", "kp",
                             "b", "d", "dz", "g",
                             "mb", "mv", "nd", "ndz", "ng", "mgb",
                             "m", "n", "ny", "ŋ",
                             "f", "s",
                             "v", "l", "z", "y", "w", "h",
                             "r"]
        self.voyell = ["a", "e","ə", "ɛ", "i", "o", "u", "ɔ"]
        self.nasal = ["ǹ", "m̀", "ŋ̀", "ŋ́", "ń", "ḿ"]
        self.syllabes = []
        self.tones = Utils.loadTone()
        self.voyell = Utils.builVoyell(self.voyell, self.tones)
        # print("ǹ" in self.nasal)
        # print(self.voyell)
        # print(self.nasal)
        # print(self.f_remove_accents(self.word))
        self.verif()

    def verif(self):
            if not isinstance(self.word, str):
                raise Exception("the word nee to be a string")

            for char in self.strip_accents(self.word):
                # print(char)
                if not (self.f_remove_accents(char) in self.consonant or self.f_remove_accents(char) in self.voyell or self.f_remove_accents(char) in self.nasal):
                    raise Exception(f'Bar caracter, {char}')

    def strip_accents(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    def isDiacritic(self, char):
        for name, tone in self.tones.items():
            if tone == char:
                return True
        return False

    def findTone(self, search_tone):
        tone_resp = 'M'
        for name, tone in self.tones.items():
            if tone == search_tone:
                tone_resp = name
        return tone_resp

    def generate(self):
            alpha = self.separe_alphabet()
            # print("CURENT ALPHABET" , alpha)
            # print('alphabet', alpha)
            syllabe = []
            cursor = 1
            tone = "M"
            trans_current = ""
            trans_current_old = ""
            trans_final = "" #trans for catch last consonant symbol

            for char in alpha:
                syllabe.append(char)
                trans_current = trans_current + " " + self.removeDiacritic(char)
                # print("caractere: ", char , " etat: ", self.currentState, " syllabe: ", syllabe)

                if self.currentState == "A":
                    if char in self.consonantEwo:
                        self.currentState = "B"
                        # Si c'est le dernier caractere alors la consonne apartient a la syllabe precedente
                        if cursor == len(alpha):
                            self.syllabes[-1]['item'] = ''.join((self.syllabes[-1]['item'], char))
                            trans_final = trans_current_old + " " + self.removeDiacritic(char) + " -" + tone

                    elif char in self.voyell:
                        self.currentState = "C"
                        tone = self.getTone(char)
                    elif char in self.nasal:
                        self.currentState = "D"
                        tone = self.getTone(char)
                    else:
                        raise Exception(f'Bad caracter, {char}for state {self.currentState} and {char in self.consonantEwo}, word {alpha} and {self.word}')
                elif self.currentState == "B":
                    if char in self.consonantEwo:
                        self.currentState = "B"  # Do noting
                    elif char in self.voyell:
                        self.currentState = "E"
                        tone = self.getTone(char)
                    else:
                        print()
                        raise Exception(f'Bad caracter, {char} for state {self.currentState}, word {alpha}')

                if self.currentState in self.finalState:
                    # print("ENTER IN FINAL STATE WITH: ", char)
                    # self.syllabes.append({"item": ''.join(syllabe), "tone": tone, 'automate_state': self.currentState})
                    self.syllabes.append({"item": ''.join(syllabe), "tone": tone})
                    trans_final = trans_current + " -" + tone
                    trans_current_old = trans_current
                    trans_current = trans_final
                    syllabe = []
                    self.currentState = self.initState
                cursor = cursor + 1
            #create transcription
            trans = ""
            for syll in self.syllabes:
                trans = trans + self.removeDiacritic(syll['item']) + "-" + syll['tone'] + " "
            return {"word": self.word, "syllabes": self.syllabes, "alphabet": [self.removeDiacritic(char) for char in alpha], "AllFeats": trans_final.strip()}
    def getDiacritic(self, cursor):
        if cursor < len(self.word):
            if self.word[cursor] not in self.consonant and self.word[cursor] not in self.voyell and self.word[cursor] not in self.nasal:
                return self.word[cursor], self.findTone(self.word[cursor])
        return '', 'M'

    def getTone(self, voyell):
        if len(voyell) > 1:
            return self.findTone(voyell[-1])
        return 'M'

    def removeDiacritic(self, sequence):
        final_syll = ''
        for char in sequence:
            # print("syll char", char)
            if char in self.voyell or char in self.consonant:
                if char in self.voyell:
                    # print("vowel char", char)
                    final_syll = final_syll + char
                else:
                    final_syll = final_syll + char

        return final_syll


    def f_remove_accents(self, old):
        # print("OLD", old)
        """
        Removes common accent characters, lower form.
        Uses: regex.
        """
        new = old.lower()
        new = re.sub(r'[àáâǎ]', 'a', new)
        new = re.sub(r'[èéêě]', 'e', new)
        new = re.sub(r'[ə́ə̀]', 'ə', new)
        new = re.sub(r'[ɛ́ɛ̌]', 'ɛ', new)
        new = re.sub(r'[ìíîǐ]', 'i', new)
        new = re.sub(r'[òóôǒ]', 'o', new)
        new = re.sub(r'[ɔ́ɔ̀ɔ̌]', 'o', new)
        new = re.sub(r'[ɔ́ɔ̀ɔ̌]', 'ɔ', new)
        new = re.sub(r'[ùúûǔ]', 'u', new)
        new = re.sub(r'[ùúûǔ]', 'u', new)
        # print("new", new)
        return new


    def word_to_alphabet(self):
        """
        Transform et sequence o
        :return:
        """
        return "good"

    def separe_alphabet(self):
        words = self.word + "#"
        stack = []
        final_word = []
        i = 0


        while i < len(words):
            word = words[i]
            # print("traiter " ,word, final_word, stack)

            #gestion des son nasaux
            #il sagit generalement d'une consone qui est suivi d'une diacritique
            if word in self.consonant and self.isDiacritic(words[i+1]):
                final_word.append(''.join((word, words[i+1])))
                i = i+2
                continue

            # Gestion des voyelles
            if word in self.voyell:
                # print("voyell", word)
                # print(self.isDiacritic(words[i+1]))
                if len(stack) > 0: # si on rencontre une voyelle c la fin de la syllabe
                    final_word.append(''.join(stack))
                    stack = []
                # print(word, i, len(words))
                if i < len(words)-1 and self.isDiacritic(words[i+1]):
                    final_word.append(''.join((word, words[i+1])))
                    i = i+2
                    continue
                else:
                    final_word.append(word)
                    i=i+1
                    continue
            # Gestion des consones
            if len(stack) == 0:
                stack.append(word)
                i = i + 1
                continue
            ############################ m #############################
            if word == 'g' and ''.join(stack) == 'm':
                stack.append(word)
                i = i + 1
                continue
            if (word == 'b' or word == 'v') and ''.join(stack) == 'm':
                stack.append(word)
                i = i + 1
                continue
            if word == 'b' and ''.join(stack) == 'mg':
                stack.append(word)
                i = i + 1
                continue
            ############################ n ############################
            if word == 'y' and ''.join(stack) == 'n':
                stack.append(word)
                i = i + 1
                continue
            if (word == 'd' or word == 'g') and ''.join(stack) == 'n':
                stack.append(word)
                # print("stack vaut n ", stack)
                i = i + 1
                continue
            if word == 'z' and ''.join(stack) == 'nd':
                stack.append(word)
                i = i + 1
                continue
            if word == 'b' and ''.join(stack) == 'ng':
                stack.append(word)
                i = i + 1
                continue

            ############################ d ############################
            if word == 'z' and ''.join(stack) == 'd':
                stack.append(word)
                i = i + 1
                continue
            ############################ t ############################
            if word == 's' and ''.join(stack) == 't':
                stack.append(word)
                i = i + 1
                continue
            ############################ k ############################
            if word == 'p' and ''.join(stack) == 'k':
                stack.append(word)
                i = i + 1
                continue
            # gestion des different cas d'arret
            # print("controle de fin")
            join_stack = ''.join(stack)
            # print("non gerer", word, i, join_stack)
            final_word.append(join_stack)
            stack = []
            if i == len(words) - 1:
                final_word.append(word)
        # print("final word", final_word)
        if len(self.word) > 0 and '#' in final_word[-1]:
            # print("Le dernier c'est #")
            final_word[-1] = final_word[-1].replace('#', '')
            if final_word[-1] == '':
                final_word.pop()
        return final_word