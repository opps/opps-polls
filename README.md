opps.polls
=========

Application Poll for Opps


Opps
----

Version: 0.1.x


Features
---------
* Custom urls
* Custom templates
* Single or Multiple choice pool
* Results page
* Hide/Show results page
* Block multiple votes by cookie
* End date and Start date
* Allow images for each choice
* Set min and max allowed choices for voting

Requirements
-----------
Django>1.5
Opps

Instalation
----------
``python setup.py install``

or

``pip install opps-polls``

Configuration
-------------

**App**

Include opps.polls on your django settings

```python
INSTALLED_APPS += (
    'opps.polls'
)
```

**URL**

Include in your project urls.py before the opps entry

```python
urlpatterns = patterns('',
    ...
    ...
    url(r'^poll/', include('opps.polls.urls', namespace='polls', app_name='polls')),
    ...
    url(r'^', include('opps.urls')),
    ...
    ...
)
```

Create the tables

```python
python manage.py syncdb
```
You should see:

```
...
Creating table polls_poll
Creating table polls_pollpost
Creating table polls_choice
...
```

Now **opps.polls** is available on your Django admin and you can access the url *http://..../poll/*

Application URLs
----------------

*    List all polls
     /poll/
*    List all polls by channel
     /poll/channel/< channel-slug >
*    Poll voting page
     /poll/< poll-slug >
*    Poll results page
     /poll/< poll-slug >/results (you can use any word here i.e: /poll/< poll-slug >/resultados)

Application Templates
---------------

For any template the context has the following objects:

* poll (The poll)
* voted (The choices when the user has voted)
* error (A string message when there is some error)

**Default template files**

* polls/pool_list.html (List all polls)
* polls/pool_detail.html (Show details and voting form)
* polls/pool_voted.html (Showed after the user has voted)
* polls/pool_result.html (Results percentage)
* polls/pool_closed.html (Showed when poll is not opened for voting or results)


**Custom template files**

polls will try to find the most specific template to render.
You can choose some ways to force a custom template
In order of precedence:

1. Set **template_path** in each poll object
2. Create a **polls/< channel-slug >/< poll-slug >_<sufix>.html**
3. Create a **polls/< channel-slug >_< sufix >.html**
4. Create a **polls/< poll-slug >_< sufix >.html**
5. Create a **polls/poll_< sufix >.html**

Available sufix are: list, detail, voted, result, closed


Contacts
========
The place to create issues is `polls github issues <https://github.com/opps/opps.poll/issues>`_. The more information you send about an issue, the greater the chance it will get fixed fast.

If you are not sure about something, have a doubt or feedback, or just want to ask for a feature, feel free to join `our mailing list <http://groups.google.com/group/opps-developers>`_, or, if you're on FreeNode (IRC), you can join the chat #opps .


License
=======

Copyright 2013 `YACOWS <http://yacows.com.br/>`_. and other contributors

Licensed under the `MIT License <http://www.oppsproject.org/en/latest/#license>`_


