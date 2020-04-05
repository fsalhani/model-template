# coding: utf-8
import django
from django.conf.urls import include, url as addurl


DJANGO_GTE_17 = django.VERSION >= (1, 7)
DJANGO_GTE_110 = django.VERSION >= (1, 10)


def routing(root=""):
    """
        Return a url patterns list that Django can use for routing, and
        a url decorator that adds any view as a route to this list.
        url, urlpatterns = routing()
        @url(r'/home/')
        def view(request):
            ...
        @url(r'/thing/(?P<pk>\d+)/$', name="thingy")
        def other_view(request, pk):
            ...
    """

    urlpatterns = UrlList()

    def url(regex, kwargs=None, name=None, prefix=''):
        if prefix and DJANGO_GTE_110:
            raise RuntimeError("Support for 'prefix' option on url() was dropped in Django 1.10. Please update your code")

        def decorator(func):
            kwargs = {'prefix': prefix} if prefix else {}
            final_func = func.as_view() if hasattr(func, 'as_view') else func
            urlpatterns.append(
                addurl(regex, final_func, kwargs, name or func.__name__, **kwargs),
            )
            return func

        return decorator

    def http403(func):
        django.conf.urls.handler403 = func
        return func
    url.http403 = http403

    def http404(func):
        django.conf.urls.handler404 = func
        return func
    url.http404 = http404

    def http405(func):
        django.conf.urls.handler405 = func
        return func
    url.http405 = http405

    return url, urlpatterns


class UrlList(list):
    """
        Sublass list to allow shortcuts to add urls to this pattern.
    """

    admin_added = False


    def add_url(self, regex, func, kwargs=None, name="", prefix=""):
        self.append(addurl(regex, func, kwargs, name, prefix))


    def include(self, regex, module, name="", prefix=""):
        self.add_url(regex, include(module), name=name, prefix=prefix)


    def add_admin(self, url):

        from django.contrib import admin

        if not UrlList.admin_added:
            admin.autodiscover()

        self.include(url, admin.site.urls, 'admin')

UrlList.admin_added = True
