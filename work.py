# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Work']
__metaclass__ = PoolMeta


class Work:
    __name__ = 'project.work'
    assigned_employee = fields.Function(fields.Many2One('company.employee',
            'Assigned'), 'get_assigned_employee',
        setter='set_assigned_employee', searcher='search_assigned_employee')

    def get_assigned_employee(self, name):
        if self.allocations:
            return self.allocations[0].employee.id

    @classmethod
    def set_assigned_employee(cls, works, name, value):
        Allocation = Pool().get('project.allocation')
        Allocation.delete([allocation for work in works
                for allocation in work.allocations])
        if value:
            to_create = []
            for work in works:
                to_create.append({
                        'employee': value,
                        'work': work.id,
                        })
            Allocation.create(to_create)

    @classmethod
    def search_assigned_employee(cls, name, clause):
        if clause[2] is None:
            return [('allocations',) + tuple(clause[1:])]
        return [('allocations.employee',) + tuple(clause[1:])]
