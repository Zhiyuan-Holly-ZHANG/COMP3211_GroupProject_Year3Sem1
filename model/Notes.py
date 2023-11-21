from model.Item import Item


class QuickNote(Item):
    # Only call superclass' init function, no information added
    def __init__(self, load):
        super().__init__("QuickNotes", load)

    # create the note
    def makeNote(self):
        QNote = []
        flag = True
        mode = 'r'
        while True:
            line = input()
            if line.strip() == 'END':
                # enter w to rewrite the previous file,
                # enter a to append information
                # enter c to continue writing taking END as an input
                # enter q to quit without save
                confirm = input("Rewrite(w) | Append(a) | Continue(c) | Quit without save(q)")
                if confirm.lower() in ['a', 'w']:
                    mode = confirm
                    break
                elif confirm.lower() == 'q':
                    flag = False
                    print("Quit successfully")
                    break
                elif confirm.lower() == 'c':
                    print("=====continue=======")
                else:
                    print("Wrong choice,try to enter 'END' again")

            else:
                QNote.append(line)

        # indicate user want to end taking note and want to save
        if flag:
            note_text = '\n'.join(QNote)
            try:
                with open(self.filename, mode) as file:
                    file.write(note_text)
                print("Note saved successfully")
            except FileNotFoundError:
                print("File save fail")
