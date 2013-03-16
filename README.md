opps_poll
=========

Application Poll for Opps

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

``pip install opps_poll``

Configuration
-------------

**App**

Include opps_poll on your django settings

```python
INSTALLED_APPS += (
    'opps_poll'
)
```

**URL**

Include in your project urls.py before the opps entry

```python
urlpatterns = patterns('',
    ...
    ...
    url(r'^poll/', include('opps_poll.urls', namespace='opps_poll', app_name='opps_poll')),
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
Creating table opps_poll_poll
Creating table opps_poll_pollpost
Creating table opps_poll_choice
...
```

Now **opps_poll** is available on your Django admin and you can access the url *http://..../poll/*

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

* opps_poll/pool_list.html (List all polls)
* opps_poll/pool_detail.html (Show details and voting form)
* opps_poll/pool_voted.html (Showed after the user has voted)
* opps_poll/pool_result.html (Results percentage)
* opps_poll/pool_closed.html (Showed when poll is not opened for voting or results)


**Custom template files**

opps_poll will try to find the most specific template to render.  
You can choose some ways to force a custom template  
In order of precedence:  

1. Set **template_path** in each poll object
2. Create a **opps_poll/< channel-slug >/< poll-slug >_<sufix>.html**
3. Create a **opps_poll/< channel-slug >_< sufix >.html**
4. Create a **opps_poll/< poll-slug >_< sufix >.html**
5. Create a **opps_poll/poll_< sufix >.html**

Available sufix are: list, detail, voted, result, closed




