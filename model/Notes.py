from model.pim_model import Item


class QuickNote(Item):
    def __init__(self, load):
        super().__init__("QuickNotes", load)

    def makeNote(self):
        QNote = []
        flag = True
        while True:
            line = input()
            if line.strip() == 'END':
                confirm = input("Save(s) | Continue(c) | Quit without save(q)")
                if confirm.lower() == 's':
                    break
                elif confirm.lower() == 'q':
                    flag = False
                    break
                else:
                    print("=====continue=======")

            else:
                QNote.append(line)

        if flag:
            note_text = '\n'.join(QNote)
            try:
                with open(self.filename, 'w') as file:
                    file.write(note_text)
                print("Note saved successfully")
            except FileNotFoundError:
                print("File save fail")
