# -*- coding: utf-8 -*-
from decorated.base.context import Context

class SessionContext(Context):
    def __init__(self, dao, **kw):
        super(SessionContext, self).__init__(**kw)
        self._dao = dao
        
    def __enter__(self):
        super(SessionContext, self).__enter__()
        self.session = self._dao.create_session()
        return self

    def __exit__(self, error_type, error_value, traceback):
        try:
            if error_value:
                self.session.rollback()
            else:
                self.session.commit()
            self.session.close()
        finally:
            super(SessionContext, self).__exit__(error_type, error_value, traceback)
            