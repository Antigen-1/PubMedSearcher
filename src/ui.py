import npyscreen
import mesh
import typing
import traceback
import term
import curses.ascii

class TermBuildForm(npyscreen.Form):
    def send_output(self, ss: typing.List[str]):
        for s in ss:
            self.output.values().append(s.rstrip())
        self.output.values().append("")
        self.output.display()
    def do_search(self, *args):
        try:
            terms = mesh.search_mesh_terms(self.input.value, "startswith", 20)
            self.send_output([f"{repr(self.input.value)} search results:"]+terms)
        except Exception as e:
            self.send_output(["MESH search:"]+traceback.format_exception_only(e))
    
    def create(self):
        class Confirm(npyscreen.ButtonPress):
            def whenPressed(this):
                ind1 = self.connective.value
                if len(ind1) == 0:
                    self.send_output([f"submit: Please select a connective first."])
                    return
                conn = ["And", "Or"][ind1[0]]
                # Strip the string to test for empty input
                prefix = self.field.value.strip()
                if len(prefix) == 0:
                    prefix = "Plain"
                # The field value is left as-is.
                self.current.value = f"({conn} ({prefix} {self.input.value}) {self.current.value})"
                self.input.value = ""
                self.input.display()
                self.current.display()
        class Compile(npyscreen.ButtonPress):
            def whenPressed(this):
                try:
                    query = term.compile_term(self.current.value)
                    self.send_output([f"compiled term: {query}"])
                except Exception as e:
                    self.send_output(["compile:"]+traceback.format_exception_only(e))
        class Output(npyscreen.BoxTitle):
            _contained_widget_class = npyscreen.TitlePager
            def values(self):
                return self.entry_widget.values
            def display(self):
                self.entry_widget.display()

        self.connective = self.add(npyscreen.TitleSelectOne, name="Connective", values=["And", "Or"], scroll_exit = True, max_height=2)

        self.field = self.add(npyscreen.TitleText, name="Field")
        self.input = self.add(npyscreen.TitleText, name="Input")
        self.current = self.add(npyscreen.TitleText, name="Current Query String")

        self.input.add_handlers({
            curses.ascii.NL: self.do_search,
            curses.ascii.CR: self.do_search,
        })

        self.submit = self.add(Confirm, name="submit")
        self.compile = self.add(Compile, name="compile")

        self.output = self.add(Output, name="Output", scroll_exit=True)
    
    def afterEditing(self):
        self.parentApp.setNextForm(None)
class TermBuildApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', TermBuildForm, name='PubmedSearcher')

if __name__ == '__main__':
    App = TermBuildApplication().run()
