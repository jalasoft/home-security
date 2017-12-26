from django.conf.urls import url

from dashboard.endpoints import main_view, login_endpoints, camera_endpoints

#DASHBOARD

urlpatterns = [
    url(r'dashboard/', main_view.dashboard, name='dashboard'),
    url(r"login/$", login_endpoints.login),
    url(r"logout/$", login_endpoints.logout),
    url(r"validateToken/$", login_endpoints.validateToken),
    url(r"camera/(?P<area>[a-z]+)$", camera_endpoints.captureArea)
]
