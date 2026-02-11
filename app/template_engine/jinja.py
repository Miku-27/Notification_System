from jinja2 import Environment,StrictUndefined,TemplateSyntaxError,UndefinedError,TemplateError
from app.utils.response import ResultCodes
from app.utils.exceptions import ServiceException

class JinjaEngine():

    def __init__(self,autoescape:bool = True):
        self.env = Environment(
            autoescape=autoescape,
            undefined = StrictUndefined
        )

    def validate(self,template:str,payload:dict|None = None):
        payload = payload or {}
        try:
            templ=self.env.from_string(template)
            templ.render(**payload)
        except TemplateSyntaxError as tse:
            raise ServiceException(ResultCodes.TEMPLATE_SYNTAX_ERROR)
        except UndefinedError as ue:
            raise ServiceException(ResultCodes.TEMPLATE_MISSING_VARAIABLE)
        except TemplateError as te:
            raise ServiceException(ResultCodes.TEMPLATE_RENDER_ERROR)

    def render():
        pass

_template_engine : JinjaEngine = None
def get_template_engine():
    global _template_engine
    if _template_engine == None:
        _template_engine = JinjaEngine()
        return _template_engine
    else:
        return _template_engine
