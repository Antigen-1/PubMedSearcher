import npyscreen
import mesh
import typing
import traceback

class TermBuildForm(npyscreen.Form):
    def create(self):
        def output(ss: typing.List[str]):
            self.output.values.append("")
            for s in ss:
                self.output.values.append(s)
            self.output.values.append("")
            self.output.display()
        class Confirm(npyscreen.ButtonPress):
            def whenPressed(this):
                ind1 = self.connective.value
                if len(ind1) == 0:
                    output([f"Please select a connective first."])
                    return
                conn = ["And", "Or"][ind1[0]]
                ind2 = self.field.value
                if len(ind2) == 0:
                    output(["Please select a field first."])
                    return
                prefix = ["Plain ", ""][ind2[0]]
                self.current.value = f"({conn} ({prefix}{self.input.value}) {self.current.value})"
                self.input.value = ""
                self.input.display()
                self.current.display()
        class Search(npyscreen.ButtonPress):
            def whenPressed(this):
                try:
                    terms = mesh.search_mesh_terms(self.input.value, "startswith", 20)
                    output(terms)
                except Exception as e:
                    output(traceback.format_exception_only(e))

        self.connective = self.add(npyscreen.TitleSelectOne, name="Connective", values=["And", "Or"], scroll_exit = True, max_height=2)
        self.field = self.add(npyscreen.TitleSelectOne, name="Field", values=["All Fields", "User-defined Field"], scroll_exit = True, max_height=2)
        
        self.input = self.add(npyscreen.TitleText, name="Input")
        self.submit = self.add(Confirm, name="submit")
        self.search = self.add(Search, name="search")

        self.current = self.add(npyscreen.TitleText, name="Current Query String")
        self.output = self.add(npyscreen.TitlePager, name="Output")
    
    def afterEditing(self):
        self.parentApp.setNextForm(None)
class TermBuildApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', TermBuildForm, name='PubmedSearcher')

if __name__ == '__main__':
    App = TermBuildApplication().run()
