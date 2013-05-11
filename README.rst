staticrss
=========

srss is a static site generator similar to Jekyll but for RSS pages. Think of
GoogleReader gone static.

Quickly install srss with::

    $ pip install staticrss


Configuration
-------------

The site configuration is stored in a YAML file called ``_config.yml``. The most
important key is the ``feeds`` list that contains all your feed urls::

    feeds:
    - http://xkcd.com/rss.xml
    - https://github.com/blog.atom
    - http://bloerg.net/atom.xml

To create an initial configuration from an existing OMPL subscription file, run
the ``import`` command of the ``srss`` tool::

    $ srss import <subscription-file.xml>


Generating a page
-----------------

Each file that does not start with an underscore ``_`` or a dot ``.`` is either copied
or processed by the template engine when it has an ``html`` file extension.

Templates are written in the Jinja2_ template language. Each template receives
an ``entries`` variable that contains the different feed items sorted by age. To
list *all* entries you would write something like this::

    <ul>
    {% for entry in entries %}
        <li><a href="{{ entry.link }}">{{ entry.title }}</a></li>
    {% endfor %}
    </ul>

Now run the ``build`` command of the ``srss`` tool::

    $ srss build

The final HTML pages are stored in the ``./_site``.

.. _Jinja2: http://jinja.pocoo.org/docs/


Dependencies
------------

* Jinja2
* dateutil
* pytz
* PyYAML
* feedcache
