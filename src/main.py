
from component.app import ClientApp
from component.service import ClientService

ca = ClientApp('cApp')
ca.establish_connection()



cs = ClientService('cService');
cs.establish_connection()
cs.add('sum', lambda args: args.a + args.b);
theList = []
cs.add('add', lambda args: theList.push(args.a));
cs.add('list', lambda : theList);



ca.ask(unitId='cService', operation='sum', input={'a': 5, 'b': 6})
ca.request('cService', 'add', {
    "a": 555
});
ca.request('cService', 'add', {
    "a": "test"
});

ca.ask('cService', 'list', None);
