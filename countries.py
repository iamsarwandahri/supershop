import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supershop.settings')

import django
django.setup()

from superapp.models import Countries
import pycountry


if __name__ == '__main__':
    countries = list(pycountry.countries)
    # print(countries)

    # for country in countries:
    #     coun = Countries.objects.create(code=country.alpha_2,name=country.name)
    #     coun.save()



    countrycode = 'PK'
    subdivisions = list(pycountry.subdivisions.get(country_code=countrycode))

    for sub in subdivisions:
        print(sub.name)
