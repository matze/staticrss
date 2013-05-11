srss
====

srss is a static site generator similar to Jekyll but for RSS pages. Think of
GoogleReader gone static.


Usage
-----

srss comes with a `srss` binary to build your page. Run::

    $ srss build

to generate the current folder into `./_site`. To create an initial
configuration, you can import an OMPL subscription file like this::

    $ srss import <subscription-file.xml>


Dependencies
------------

* Jinja2
* dateutil
* pytz
* PyYAML
* feedcache
