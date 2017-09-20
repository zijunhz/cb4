from os import path

import jinja2
import jinja2.ext
import jinja2.runtime

import vj4
import vj4.constant
import vj4.job
from vj4.service import staticmanifest
from vj4.util import json
from vj4.util import options
from vj4.util import template_func


class Undefined(jinja2.runtime.Undefined):
  def __getitem__(self, _):
    return self

  if options.debug:
    __str__ = jinja2.runtime.Undefined.__call__


class Environment(jinja2.Environment):
  def __init__(self):
    super(Environment, self).__init__(
        loader=jinja2.FileSystemLoader(path.join(path.dirname(__file__), 'ui/templates')),
        extensions=[jinja2.ext.with_],
        auto_reload=options.debug,
        autoescape=True,
        trim_blocks=True,
        undefined=Undefined)
    globals()[self.__class__.__name__] = lambda: self  # singleton

    self.globals['vj4'] = vj4
    self.globals['static_url'] = lambda s: options.cdn_prefix + staticmanifest.get(s)
    self.globals['paginate'] = template_func.paginate

    self.filters['nl2br'] = template_func.nl2br
    self.filters['markdown'] = template_func.markdown
    self.filters['json'] = json.encode
    self.filters['gravatar_url'] = template_func.gravatar_url
    self.filters['format_size'] = template_func.format_size
    self.filters['format_seconds'] = template_func.format_seconds
    self.filters['base64_encode'] = template_func.base64_encode
