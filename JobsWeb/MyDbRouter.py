# -*- coding:utf-8 -*-
class MyAppRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'user':
            return 'user'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'user':
            return 'user'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'user' or obj2._meta.app_label == 'user':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'user':
            return model._meta.app_label == 'user'
        elif model._meta.app_label == 'user':
            return False
        return None
