class KartsDbRouter(object):
    """A router to control all database operations on models in
    the myapp2 application"""
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'live':
            return 'kartsdb'
        return None
