from django.urls import path
from . import views
from .views import rating_line_chart, rating_line_chart_json,avg_line_chart,avg_line_chart_json,sumscore_line_chart_json,sumscore_line_chart

urlpatterns = [
    path('', views.index, name='index'),
    path('', rating_line_chart, name='rating_line_chart'),
    path('', avg_line_chart, name='avg_line_chart'),
    path('', sumscore_line_chart, name='sumscore_line_chart'),
	path('chartJSON', rating_line_chart_json, name='rating_line_chart_json'),
	path('avgchartJSON', avg_line_chart_json, name='avg_line_chart_json'),
	path('sumscorechartJSON', sumscore_line_chart_json, name='sumscore_line_chart_json'),
	path('newgame',views.newGame,name='newgame'),
	path('profile/<user_id>',views.profile,name='profile')
]