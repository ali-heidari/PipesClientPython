
from component.app import ClientApp

c = ClientApp('cApp')
c.establish_connection()
c.ask(unitId='cService', operation='sum', input={'a': 5, 'b': 6})
