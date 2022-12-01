from django import forms
from .brain import Statistic
#
object_main = Statistic()
l_country = [''] + object_main.l_country

# l_country = ['', 'Ukraine', 'Poland', 'Spain', 'Brazil', 'Austria', 'France']

# countries for data
class FiveCountryChoseForm(forms.Form):
    tuple_country_0 = ((num, i)  for num, i in enumerate(l_country))
    tuple_country_1 = ((num, i)  for num, i in enumerate(l_country))
    tuple_country_2 = ((num, i)  for num, i in enumerate(l_country))
    tuple_country_3 = ((num, i)  for num, i in enumerate(l_country))
    tuple_country_4 = ((num, i)  for num, i in enumerate(l_country))

    country_0 = forms.ChoiceField(choices=tuple_country_0)
    country_1 = forms.ChoiceField(choices=tuple_country_1)
    country_2 = forms.ChoiceField(choices=tuple_country_2)
    country_3 = forms.ChoiceField(choices=tuple_country_3)
    country_4 = forms.ChoiceField(choices=tuple_country_4)

class YearChoseForm(forms.Form):
    tuple_year = ((num, i)  for num, i in enumerate([i for i in range(1950, 2021)]))
    year = forms.ChoiceField(choices=tuple_year, initial=2020)


