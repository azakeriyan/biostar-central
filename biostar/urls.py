from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


import biostar.accounts.urls as accounts_urls
import biostar.engine.urls as engine_urls
import biostar.forum.urls as forum_urls
import biostar.message.urls as message_urls


ACCOUNTS = url(r'^accounts/', include(accounts_urls))
ADMIN = url(r'^django/admin/', admin.site.urls, name='django_admin')


# Default url patters for the engine.
urlpatterns = [

    # The engine handler.
    url(settings.ENGINE_ROOT_URLPATTERN, include(engine_urls)),

    # The django generated admin site.
    ADMIN,

    ACCOUNTS,

    # Forum urls
    url(settings.FORUM_ROOT_URLPATTERN, include(forum_urls)),

    # Message urls
    url(settings.MESSAGE_ROOT_URL_PATTERN, include(message_urls)),

]


# Urls mounted when forum is enabled by itself
if settings.ONLY_FORUM_URLS:

    # Replace the engine handler with the forums
    urlpatterns = [
                    url(settings.FORUM_ROOT_URLPATTERN, include(forum_urls)),
                    ADMIN, ACCOUNTS,
                    url(settings.MESSAGE_ROOT_URL_PATTERN, include(message_urls))
                    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)

if settings.DEBUG and settings.INTERNAL_IPS:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

