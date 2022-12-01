from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from . forms import FiveCountryChoseForm, l_country, YearChoseForm
from . brain import Statistic
import os

# https://www.codechit.com/django-github-auto-deployment-to-heroku/
# -------------------------------------------------------------------------------
# https://medium.com/nuances-of-programming/%D0%BE%D0%B2%D0%BB%D0%B0%D0%B4%D0%B5%D0%B9-python-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%B2%D0%B0%D1%8F-%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D1%87%D0%B0%D1%81%D1%82%D1%8C-4-60e016f18422

# heroku create YourName

# requirements.txt   pip gunicorn / pip list /          pip list > requirements.txt
                                                         # pip freeze

# Procfile           web: gunicorn mainscript:app
# runtime.txt        python-3.7.1

#         !!!!!!     app.debug =     !!!!!!

# !!!!  pip install  gunicorn #for NEW !!!!

#!!!  Убедитесь, что находитесь в той же директории, !!!!!!!!!  где лежит ваш файл Python !!!!!!!!!!!

#Убедитесь, что находитесь в той же директории, !!!!!!!!!  где лежит ваш файл Python !!!!!!!!!!!
#Убедитесь, что вы залогинены в heroku                    // heroku login
#Вызовите свое приложение                                 // heroku git:remote --app YourName
#Инициализируйте git, чтобы загрузить все файлы           // git init
#Добавьте все файлы (это точка в конце, что означает все) // git add .
#Теперь, зафиксируйте все добавленные файлы на сервер     // git commit -m    / example - "First upload"
#Запушьте все в master branch                             // git push heroku master
# -------------------------------------------------------------------------------

def hello(request):
    return HttpResponse("Hello world!")

def f(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())

a = Statistic()

def download_file(request):
    with open('Mortality-rate-under-five_2021.xlsx', 'rb') as file:
        result = file.read()
    response = HttpResponse(result)
    response['Content-Disposition'] = 'attachment; filename=Mortality-rate-under-five_2021.xlsx'
    return response

def leaders(request):
    context = {}
    context['years_leaders'] = YearChoseForm()
    data = a.f_10_better(2020)
    context['years_leaders']['year'].initial = '70'

    if request.method == 'POST' and 'year' in request.POST:
        year_from_request = request.POST['year']
        context['years_leaders']['year'].initial = year_from_request
        year = int(year_from_request) + 1950
        data = a.f_10_better(year)


    data = ['{} ..... {} ....... {} ..  millions children under five'.format(i[0], i[1], i[2] if i[2] else "'We do not have information'") for i in data]
    context['leaders'] = data
    return render(request, "leaders.html", context)

def mortality_page_view(request):
    context = {}
    context['form_1'] = FiveCountryChoseForm()
    if request.method == 'POST':
        if 'Create_charts' in request.POST:
            data = [request.POST['country_0'], request.POST['country_1'], request.POST['country_2'],
                    request.POST['country_3'], request.POST['country_4']]
            data = [i for i in set(data) if i != '0']
            data = data + ['0'] * (5 - len(data))  # '0' to the end of the list 'data'

            # data = ['3', '0', '0', '3', '0']
            for num, i in enumerate(data):
                context['form_1']['country_{}'.format(num)].initial = i
            l_countries_for_check = [a.l_country[int(i) - 1] for i in data if i != '0']
            res_median = a.f_median((l_countries_for_check))
            res_gradient = a.f_gradient((l_countries_for_check))
            res_distance = a.f_distance((l_countries_for_check))
            res_population_under_five = a.f_population_under_five((l_countries_for_check))

        elif 'Clear_countries' in request.POST:
            for i in range(5):
                context['form_1']['country_{}'.format(i)].initial = '0'
            res_median = a.f_median(([]))
            res_gradient = a.f_gradient(([]))
            res_distance = a.f_distance(([]))
            res_population_under_five = a.f_population_under_five(([]))

        context['data_chart_median'] = res_median
        context['data_chart_gradient'] = res_gradient
        context['data_chart_distance'] = res_distance
        context['data_chart_population_under_five'] = res_population_under_five

        return render(request, "mortality_page.html", context)

    else:
        l_countries_for_check = ['Ukraine', 'Poland']
        context['form_1']['country_0'].initial = '184' # 'Ukraine'
        context['form_1']['country_1'].initial = '139' # 'Poland'

        res_median = a.f_median((l_countries_for_check))
        res_gradient = a.f_gradient((l_countries_for_check))
        res_distance = a.f_distance((l_countries_for_check))
        res_population_under_five = a.f_population_under_five((l_countries_for_check))

        context['data_chart_median'] = res_median
        context['data_chart_gradient'] = res_gradient
        context['data_chart_distance'] = res_distance
        context['data_chart_population_under_five'] = res_population_under_five

        return render(request, "mortality_page.html", context)