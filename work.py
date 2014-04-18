# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Work']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'
    assigned_employees = fields.Function(fields.Char('Assigned'),
        'get_assigned_employees', searcher='search_assigned_employees')

    def get_assigned_employees(self, name):
        return ",".join([x.employee.rec_name for x in self.allocations])

    @classmethod
    def search_assigned_employees(cls, name, clause):
        pool = Pool()
        Allocation = pool.get('project.allocation')
        clause2 = ['employee'] + clause[1:]
        allocation = Allocation.search(clause2)
        tasks = [x.work.id for x in allocation]
        return [('id', 'in', tasks)]
