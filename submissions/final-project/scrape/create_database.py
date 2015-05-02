'''
Create a new database based on the given datasets from BrunchBase

Credit to: https://github.com/mode/blog/tree/master/2014-01-30-founder-experience/API_scripts

Crunchbase Schema:

mode.crunchbase_dimension_companies
    company_name                str
    company_permalink           str
    category_code               str
    market                      str
    created_at                  timestamp
    number_of_employees         int
    founded_year                int
    founded_month               int
    founded_day                 int
    founded_date                timestamp
    exit                        str
    country_code                str
    state_code                  str
    city                        str
    latitude                    float
    longitude                   float
    funding_rounds              int
    total_money_raised          int
    total_money_raised_s        str
    exit                        str
    extracted_at                timestamp

mode.crunchbase_dimension_financial_orgs
    financial_org_name          str
    financial_org_permalink     str
    created_at                  timestamp
    number_of_employees         int
    founded_year                int
    founded_month               int
    founded_day                 int
    founded_date                timestamp
    country_code                str
    state_code                  str
    city                        str
    latitude                    float
    longitude                   float
    investments                 int
    total_funds                 int
    extracted_at                timestamp
                                
mode.crunchbase_dimension_competitors           
    company_permalink           str
    company_name                str
    competitor_name             str
    competitor_permalink        str
    extracted_at                timestamp
                                
mode.crunchbase_dimension_funding_rounds        
    company_permalink           str
    company_name                str
    round_id                    int
    round_code                  str
    raised_amount               int
    raised_currency_code        str
    funded_year                 int
    funded_month                int
    funded_day                  int
    funded_date                 timestamp
    investor_count              int
    extracted_at                timestamp
                                
mode.crunchbase_dimension_investments           
    company_permalink           str
    company_name                str
    round_id                    int
    round_code                  str
    round_amount                int
    round_currency_code         str
    round_date                  timestamp
    investor_entity             str
    investor_name               str
    investor_permalink          str
    extracted_at                timestamp
                                
mode.crunchbase_dimension_acquisitions          
    company_permalink           str
    company_name                str
    acquiring_company           str
    acquiring_permalink         str
    acquired_year               int
    acquired_month              int
    acquired_day                int
    acquired_date               timestamp
    price                       int
    price_currency_code         str
    term_code                   str
    extracted_at                timestamp

mode.crunchbase_dimension_funds
    fund_name                   str
    financial_org_permalink     str
    financial_org_name          str
    funded_year                 int
    funded_month                int
    funded_day                  int
    funded_date                 timestamp
    raised_amount               int
    raised_currency_code        str
    extracted_at                timestamp

'''

import sqlite3

def create_db():
    conn = sqlite3.connect('crunchbase.db')
    cursor = conn.cursor()
    
    create_dimension_companies(cursor)
    create_dimension_financial_orgs(cursor)
    create_dimension_competitors(cursor)
    create_dimension_funding_rounds(cursor)
    create_dimension_investments(cursor)
    create_dimension_acquisitions(cursor)
    create_dimension_funds(cursor)
    create_tests(cursor)
    
    conn.commit()
    conn.close()

def create_dimension_acquisitions(cursor):
    cursor.execute('''CREATE TABLE dimension_acquisitions
        (   company_name text,
            company_permalink text,
            acquiring_company text,
            acquiring_permalink text,
            acquired_year real,
            acquired_month real,
            acquired_day real,
            acquired_date text,
            price real,
            price_currency_code text,
            term_code text,
            extracted_at text
            )''')

def create_dimension_companies(cursor):
    cursor.execute('''CREATE TABLE dimension_companies
        (   company_name text,
            company_permalink text,
            category_code text,
            market text,
            created_at text,
            number_of_employees real,
            founded_year real,
            founded_month real,
            founded_day real,
            founded_date text,
            country_code text,
            state_code text,
            city text,
            latitude real,
            longitude real,
            funding_rounds real,
            total_money_raised real,
            total_money_raised_s text,
            exit text,
            extracted_at text
            )''')

def create_dimension_competitors(cursor):
    cursor.execute('''CREATE TABLE dimension_competitors
        (   company_name text,
            company_permalink text,
            competitor_name text,
            competitor_permalink text,
            extracted_at text
            )''')

def create_dimension_financial_orgs(cursor):
    cursor.execute('''CREATE TABLE dimension_financial_orgs
        (   financial_org_name text,
            financial_org_permalink text,
            created_at text,
            number_of_employees real,
            founded_year real,
            founded_month real,
            founded_day real,
            founded_date text,
            country_code text,
            state_code text,
            city text,
            latitude real,
            longitude real,
            investments real,
            total_fund real,
            extracted_at text
            )''')

def create_dimension_funding_rounds(cursor):
    cursor.execute('''CREATE TABLE dimension_funding_rounds
        (   company_name text,
            company_permalink text,
            round_id real,
            round_code text,
            raised_amount real,
            raised_currency_code text,
            funded_year real,
            funded_month real,
            funded_day real,
            funded_date text,
            investor_count real,
            extracted_at text
            )''')

def create_dimension_funds(cursor):
    cursor.execute('''CREATE TABLE dimension_funds
        (   fund_name text,
            financial_org_permalink text,
            financial_org_name text,
            funded_year real,
            funded_month real,
            funded_day real,
            funded_date text,
            raised_amount real,
            raised_currency_code text,
            extracted_at text
            )''')

def create_dimension_investments(cursor):
    cursor.execute('''CREATE TABLE dimension_investments
        (   company_name text,
            company_permalink text,
            round_id real,
            round_code text,
            round_amount real,
            round_currency_code text,
            round_date text,
            investor_entity text,
            investor_name text,
            investor_permalink text,
            extracted_at text
            )''')

def create_tests(cursor):
    cursor.execute('''CREATE TABLE tests
        (   text_column text,
            real_column real
            )''')

'''
Helper functions
'''

def ifnull(var, val):
  if var is None:
    return val
  return var

def drop_table(tables):
    conn = sqlite3.connect('crunchbase.db')
    cursor = conn.cursor()
    
    for t in tables:
        cursor.execute("DROP TABLE" + " " + t)
    
    conn.commit()
    conn.close()

def unc(string):
    n = string.encode('utf-8').strip()
    return n

def strip_special_2(array,columns_with_string):
    new_table = []
    for i in array:
        print(i)
        new_row =[]
        for j in range(len(i)):
            print(j)
            if j in columns_with_string:
                print(i[j])
                x = i[j].encode('utf-8').strip()
            else:
                x = i[j]
            new_row.append(x)
            
        new_table.append(new_row)
    
    return new_table
