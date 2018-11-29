from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
vendor.add('lib')
#from requests_toolbelt.adapters import appengine as requests_toolbelt_appengine
#requests_toolbelt_appengine.monkeypatch()
#from google.appengine.tools.devappserver2.python.runtime import sandbox
#sandbox._WHITE_LIST_C_MODULES += ['_ssl', '_socket']