
from component.app import App

c = App('cApp')
c.establish_connection()
c.ask(unitId='cService', operation='sum', input={'a': 5, 'b': 6})
