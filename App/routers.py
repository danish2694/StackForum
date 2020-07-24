import App.models
allmodels = dict([(name.lower(), cls) for name, cls in App.models.__dict__.items() if isinstance(cls, type)])
# print(allmodels)
class DbRouter(object):
    route_app_labels = {'default','second'}
    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name = None, **hints):
        """ migrate to appropriate database per model """
        # print(model_name)
        try:
            model = allmodels.get(model_name)
            return(model.params.db == db)
        except:
            pass
            
    