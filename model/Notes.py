from model.Item import Item


class QuickNote(Item):
    def __init__(self, load):
        super().__init__("QuickNotes", load)

    def makeNote(self):
        QNote = []
        flag = True
        mode = 'r'
        while True:
            line = input()
            if line.strip() == 'END':
                confirm = input("Rewrite(w) | Append(a) | Continue(c) | Quit without save(q)")
                if confirm.lower() in ['a', 'w']:
                    mode = confirm
                    break
                elif confirm.lower() == 'q':
                    flag = False
                    break
                elif confirm.lower() == 'c':
                    print("=====continue=======")
                else:
                    print("Wrong choice,try to enter 'END' again")

            else:
                QNote.append(line)

        if flag:
            note_text = '\n'.join(QNote)
            try:
                with open(self.filename, mode) as file:
                    file.write(note_text)
                print("Note saved successfully")
            except FileNotFoundError:
                print("File save fail")
