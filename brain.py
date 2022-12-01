import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas
import os
import io
import base64
import csv

matplotlib.use('Agg')

class Statistic():
    l_country = []
    def __init__(self):
        self.d_gradient, self.d_median, self.d_10_better, self.d_res, self.d_10_better = Statistic.f_parser()
        self.d_population_under_5 = Statistic.f_parser_population_under_5()
        self.xpoints = np.array([i for i in range(1950, 2021)])


    # for Median
    def f_median(self, l_countries):
        l_countries = [i for i in set(l_countries)]
        l_countries.append('Median')

        for country in l_countries:
            tmp = [i for i in self.d_res[country].values()]
            data = [values for values in tmp[0].values()]
            ypoints = np.array(data)
            my_label = country if country != 'Median' else 'LEADERS'
            plt.plot(self.xpoints, ypoints, marker='.', label=my_label)

        plt.title("Child Mortality Estimates\nCountry-specific Under-five mortality rate")
        plt.xlabel("Years")
        plt.ylabel("Child mortality")
        plt.grid()
        plt.legend()

        s = io.BytesIO()
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,{}".format(s)


    # for Gradient
    def f_gradient(self, l_countries):
        l_countries = [i for i in set(l_countries)]
        l_countries.append('Median')

        for country in l_countries:
            tmp = self.d_gradient[country]
            data = [values for values in tmp.values()]
            ypoints = np.array(data)
            plt.plot(self.xpoints, ypoints, marker='.', label=country if country != 'Median' else 'LEADERS')

        plt.title("The Speed of Improving the situation\nCountry-specific Under-five mortality rate")
        plt.xlabel("Years")
        plt.ylabel("Gradient of changing child mortality")
        plt.grid()
        plt.legend()
        s = io.BytesIO()
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,{}".format(s)

    def f_distance(self, l_countries):
        l_countries = [i for i in set(l_countries)]
        d_for_median = self.d_median['Median']['MEDIAN']

        for country in l_countries:
            tmp = [i for i in self.d_res[country].values()]
            data = tmp[0]

            points = [Statistic.f_find_year(d_for_median, values, keys) for keys, values in data.items()]
            extra_note = ' (too far to more than 70 years ago level)' if all([i == None for i in points]) else ''
            ypoints = np.array(points)
            plt.plot(self.xpoints, ypoints, marker='.', label=country + extra_note if country != 'Median' else 'LEADERS')

        plt.title("The Gaps between countries and LEADERS countries\nCountry-specific Under-five mortality rate")
        plt.xlabel("Years")
        plt.ylabel("Gaps in the years")
        plt.grid()
        plt.legend()
        s = io.BytesIO()
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,{}".format(s)

   # for chart population under five
    def f_population_under_five(self, l_countries):
        l_countries = [i for i in set(l_countries)]
        for country in l_countries:
            data = [i for i in self.d_population_under_5[country].values()]
            ypoints = np.array(data)
            my_label = country
            plt.plot(self.xpoints, ypoints, marker='.', label=my_label)

        plt.title("Child Population Under-five years")
        plt.xlabel("Years")
        plt.ylabel("Population, millions")
        plt.grid()
        plt.legend()

        s = io.BytesIO()
        plt.savefig(s, format='png', bbox_inches="tight")
        plt.close()
        s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,{}".format(s)

    def f_10_better(self, year):
        data = self.d_10_better.get(year, None)
        return [(i, data[i], self.d_population_under_5[i][year]) for i in sorted(data, key=lambda x: data[x]) if i != 'Median']

    @staticmethod
    def f_parser():
        path_old = os.getcwd()
        path_new = path_old + '\datasandbox'
        os.chdir(path_old)
        excel_data_df = pandas.read_excel('Mortality-rate-under-five_2021.xlsx', sheet_name='U5MR Country estimates',
                                          usecols='A:BV', header=14)
        os.chdir(path_old)
        # l_years =  [1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
        l_years = [i for i in range(1950, 2021)]

        # l_columns_name =  ['ISO.Code' 'Country.Name' 'Uncertainty.Bounds*' '1950.5' '1951.5'  '1952.5' '1953.5' '1954.5' '1955.5' '1956.5' '1957.5' '1958.5' '1959.5'  '1960.5' '1961.5' '1962.5' '1963.5' '1964.5' '1965.5' '1966.5' '1967.5'
        l_columns_name = excel_data_df.columns.ravel()

        # d_res = {'Afghanistan': {'AFG': {1950: nan, 1951: nan, 1952: nan, 1953: nan, 1954: nan, 1955: nan, 1956: nan, 1957: 377.8412, 1958: 370.9016, 1959: 364.408, 1960: 358.2051, 1961: 352.212,
        d_res = {}
        df = pandas.DataFrame(excel_data_df)
        for index, row in df.iterrows():
            if row['Uncertainty.Bounds*'] == 'Median':
                country = row['Country.Name']
                code = row['ISO.Code']
                tmp = {country: {code: {int(float(i)): round(row[i], 4) for i in l_columns_name[3:]}}}
                d_res.update(tmp)

        """
        d_10_better = {1950: {}, 1951: {}, 1952: {}, 1953: {}, 1954: {}, 1955: {}, 1956: {}, 1957: {}, 1958: {}, 1959: {}, 1960: {}, 1961: {}, 1962: {}, 1963: {}, 1964: {},
        """
        d_10_better = {i: {} for i in l_years}

        for key, value in d_res.items():
            country = key
            for i in value.values():
                for key_d, value_d in i.items():
                    if value_d == value_d:  # checking for 'nan'
                        tmp = d_10_better.get(key_d, None)
                        tmp.update({country: value_d})
                        l_candidates = [i for i in tmp]
                        l_candidates.sort(key=lambda x: tmp[x])
                        if len(l_candidates) > 10:  # we need only 10 countries
                            l_candidates.pop(10)
                        tmp = {key_tmp: values_tmp for key_tmp, values_tmp in tmp.items() if key_tmp in l_candidates}
                        d_10_better[key_d] = tmp

        # d_10_better =  {1950: {'Australia': 31.5901, 'Denmark': 33.944, 'Iceland': 29.6153, 'Netherlands': 31.8878, 'New Zealand': 35.5187, 'Norway': 32.8052, 'Sweden': 27.1305, 'Switzerland': 38.5582, 'United

        # Adding 'Median' in the d_10_better
        for key, values in d_10_better.items():
            median = round(sum([values for keys, values in values.items()]) / 10, 4)
            values.update({'Median': median})
            d_10_better[key] = values
        print()
        # d_10_better = {1950 : {'Australia': 31.5901, 'Denmark': 33.944, 'Iceland': 29.6153, 'Netherlands': 31.8878,
        # 'New Zealand': 35.5187, 'Norway': 32.8052, 'Sweden': 27.1305, 'Switzerland': 38.5582, 'United Kingdom': 36.6001,
        # 'United States of America': 37.6149, 'Median': 33.5265}}

        # d_median = {'Median': {'MEDIAN': {1950: 33.5265, 1951: 32.3325, 1952: 31.161, 1953: 30.0184, 1954: 28.9462,
        d_median = {'Median': {'MEDIAN': {key: d_10_better[key]['Median'] for key, value in d_10_better.items()}}}

        d_gradient = {}
        d_res.update(d_median)
        for d_res_key, data in d_res.items():
            for data_key, data_value in data.items():
                code_country = data_key
                tmp = {}
                for d_key, d_val in data_value.items():
                    # print(d_key, d_val)
                    if d_key == 1950:
                        gradient = None
                    else:
                        current_level = data_value[d_key]
                        previous_level = data_value[d_key - 1]
                        if current_level != current_level or previous_level != previous_level:  # 'nan' exception
                            gradient = None
                        else:
                            gradient = round((previous_level - current_level) / previous_level, 4)
                    tmp[d_key] = gradient

            d_gradient[d_res_key] = tmp
        # d_res = {'Afghanistan': {'AFG': {1950: nan, 1951: nan, 1952: nan, 1953: nan, 1954: nan, 1955: nan, 1956: nan, 1957: 377.8412, 1958: 370.9016, 1959: 364.408, 1960: 358.2051, 1961: 352.212,
        # d_10_better = {1950: {}, 1951: {}, 1952: {}, 1953: {}, 1954: {}, 1955: {}, 1956: {}, 1957: {}, 1958: {}, 1959: {}, 1960: {}, 1961: {}, 1962: {}, 1963: {}, 1964: {},
        # d_median = {'Median': {'MEDIAN': {1950: 33.5265, 1951: 32.3325, 1952: 31.161, 1953: 30.0184, 1954: 28.9462,
        # d_gradient = {'Afghanistan': {1950: 0, 1951: 0, 1952: 0, 1953: 0, 1954: 0, 1955: 0.005, 1956: 0.0031, 1957: 0.0031, 1958: 0.0029, 1959: 0.003,
        Statistic.l_country = sorted(d_res)
        return d_gradient, d_median, d_10_better, d_res, d_10_better

    @staticmethod
    def f_parser_population_under_5():
        # Afghanistan, AFG, 1950, 1291622,
        d_population_under_5 = {i : {y: None for y in range(1950, 2021)} for i in Statistic.l_country}
        with open('under-5-population.csv', 'r') as f:
            data = f.readlines()
            for line in data[1:]:
                country, code, year, data = line.split(',')[:4]
                # normalization for different datasets
                if country == 'Russia':
                    country = 'Russian Federation'
                tmp = d_population_under_5.get(country, None)
                if tmp and data and int(year) <= 2020:
                    year = int(year)
                    tmp[year] = round(float(data)/1000000, 4)  # quantity in millions
                    d_population_under_5[country] = tmp
        # {'Afghanistan': {1950: 1291622.0, 1951: 1314492.0, 1952: 1320099.0, 1953: 1323502.0, 1954: 1333989.0, 1955: 1357410.0, 1956: 1387305.0, 1957:
        return d_population_under_5

    @staticmethod
    def f_find_year(d_for_median, data, year):
        if data == data:
            for year_median, data_median in d_for_median.items():
                if data > data_median:
                    return 1 + year - year_median if year_median != 1950 else None
            if data <= data_median:
                return 1 + year - year_median

        return None
