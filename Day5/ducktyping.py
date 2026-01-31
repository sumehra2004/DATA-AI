class pycharm:
    def execute(self):
        print("Compiling+Running")
class VSCode:
    def execute(self):
        print("Running+linting")
def code(editor):
    editor.execute()
code(pycharm())
code(VSCode())