'''
Get the individual database entry/row based on the given datasets from BrunchBase

Credit to: https://github.com/mode/blog/tree/master/2014-01-30-founder-experience/API_scripts
'''


def get_acquisition(company_json):
    j = company_json
    
    company_name = j['name']
    company_permalink = j['permalink']
    a = j['acquisition']
    
    if a is None:
        acquisition = None
    else:
        acquiring_company =  a['acquiring_company']['name']
        acquiring_permalink = a['acquiring_company']['permalink']
        acquired_year = ifnull(a['acquired_year'],1900)
        acquired_month = ifnull(a['acquired_month'],1)
        acquired_day = ifnull(a['acquired_day'],1)
        acquired_date = (str(acquired_year) + "-" + str(acquired_month) + "-" + 
                        str(acquired_day) + "T00:00:00Z")
        price = a['price_amount']
        price_currency_code = a['price_currency_code']
        term_code = a['term_code']
        
        extracted_at = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        acquisition = (company_name,company_permalink,acquiring_company,
                        acquiring_permalink,acquired_year,acquired_month,
                        acquired_day,acquired_date,price,price_currency_code,
                        term_code,extracted_at)
        
        return acquisition

def get_company_info(company_json):
    j = company_json['data']['properties']
    
    name = j['name']
    permalink = j['permalink']
    category_code = j['category_code']
    created_at = j['created_at']

    market = j['market']
    number_of_employees = j['number_of_employees']
    founded_year = ifnull(j['founded_year'],1900)
    founded_month = ifnull(j['founded_month'],01)
    founded_day = ifnull(j['founded_day'],01)
    founded_date = (str(founded_year) + "-" + str(founded_month) + "-" +
        str(founded_day) + "T00:00:00Z")
    funding_rounds = len(j['funding_rounds'])
    total_money_raised_s = j['total_money_raised']
    
    # info on location
    if len(j['offices']) > 0:
        country_code = j['offices'][0]['country_code']
        state_code = j['offices'][0]['state_code']
        city = j['offices'][0]['city']
        latitude = j['offices'][0]['latitude']
        longitude = j['offices'][0]['longitude']
    else:
        country_code = None
        state_code = None
        city = None
        latitude = None
        longitude = None
    
    # find total funding
    total_money_raised = 0
    currencies = []
    for r in j['funding_rounds']:
        total_money_raised += ifnull(r['raised_amount'],0)
        currencies.append(r['raised_currency_code'])
    
    currency_count = len(list(set(currencies)))
    
    if currency_count != 1:
        total_money_raised = 0
        
    # find exit
    if j['ipo'] is None:
        if j['acquisition'] is None:
            exit = 'no_exit'
        else:
            exit = 'acquired'
    else:
        exit = 'ipo'
    
    extracted_at = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    row = (name,permalink,category_code,created_at,number_of_employees,
    founded_year,founded_month,founded_day,founded_date,country_code,
    state_code,city,latitude,longitude,funding_rounds,total_money_raised,
    total_money_raised_s,exit,extracted_at)
    
    return row

def get_competitors(company_json):
    j = company_json
    
    company_name = j['name']
    company_permalink = j['permalink']
    competitors = j['competitions']
    
    coms = []
    
    for c in competitors:
        competitor_name = c['competitor']['name']
        competitor_permalink = c['competitor']['permalink']
        
        extracted_at = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        com = (company_name,company_permalink,competitor_name,competitor_permalink,
                extracted_at)
        
        coms.append(com)
        
    return coms

def get_financial_org_info(company_json):
    j = company_json
    
    name = j['name']
    permalink = j['permalink']
    created_at = j['created_at']
    number_of_employees = j['number_of_employees']
    founded_year = ifnull(j['founded_year'],1900)
    founded_month = ifnull(j['founded_month'],1)
    founded_day = ifnull(j['founded_day'],1)
    founded_date = (str(founded_year) + "-" + str(founded_month) + "-" +
        str(founded_day) + "T00:00:00Z")
    investments = len(j['investments'])
    
    # info on location
    if len(j['offices']) > 0:
        country_code = j['offices'][0]['country_code']
        state_code = j['offices'][0]['state_code']
        city = j['offices'][0]['city']
        latitude = j['offices'][0]['latitude']
        longitude = j['offices'][0]['longitude']
    else:
        country_code = None
        state_code = None
        city = None
        latitude = None
        longitude = None
    
    # total_fund_size
    total_fund = 0
    currencies = []
    for r in j['funds']:
        total_fund += ifnull(r['raised_amount'],0)
        currencies.append(r['raised_currency_code'])
    
    currency_count = len(list(set(currencies)))
    
    if currency_count != 1:
        total_money_raised = 0
    
    extracted_at = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    row = (name,permalink,created_at,number_of_employees,founded_year,
        founded_month,founded_day,founded_date,country_code,
        state_code,city,latitude,longitude,investments,total_fund,
        extracted_at)
    
    return row

def get_funding_rounds(company_json):
    j = company_json
    
    company_name = j['name']
    company_permalink = j['permalink']
    rounds = j['funding_rounds']
    
    rnds = []
    
    for r in rounds:
        round_id = r['id']
        round_code = r['round_code']
        raised_amount = r['raised_amount']
        raised_currency_code = r['raised_currency_code']
        funded_year = ifnull(r['funded_year'],1900)
        funded_month = ifnull(r['funded_month'],01)
        funded_day = ifnull(r['funded_day'],01)
        funded_date = (str(funded_year) + "-" + str(funded_month) + "-" +
            str(funded_day) + "T00:00:00Z")
        investor_count = len(r['investments'])
        
        extracted_at = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        rnd = (company_name,company_permalink,round_id,round_code,raised_amount,
                raised_currency_code,funded_year,funded_month,funded_day,
                funded_date,investor_count,extracted_at)
        
        rnds.append(rnd)
        
    return rnds

def get_funds(json):
    j = json
    
    financial_org_name = j['name']
    financial_org_permalink = j['permalink']
    funds = j['funds']
    
    fds = []
    
    for f in funds:
        fund_name = f['name']
        funded_year = ifnull(f['funded_year'],1900)
        funded_month = ifnull(f['funded_month'],1)
        funded_day = ifnull(f['funded_day'],1)
        funded_date = (str(funded_year) + "-" + str(funded_month) + "-" +
            str(funded_day) + "T00:00:00Z")
        raised_amount = f['raised_amount']
        raised_currency_code = f['raised_currency_code']
        
        extracted_at = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        fd = (fund_name,financial_org_permalink,financial_org_name,
                funded_year,funded_month,funded_day,funded_date,raised_amount,
                raised_currency_code,extracted_at)
        
        fds.append(fd)
        
    return fds

def get_investments(company_json):
    j = company_json
    
    company_name = j['name']
    company_permalink = j['permalink']
    rounds = j['funding_rounds']
    
    invsmts = []
    
    for r in rounds:
        round_id = r['id']
        round_code = r['round_code']
        round_amount = r['raised_amount']
        round_currency_code = r['raised_currency_code']
        year = ifnull(r['funded_year'],1900)
        month = ifnull(r['funded_month'],01)
        day = ifnull(r['funded_day'],01)
        round_date = (str(year) + "-" + str(month) + "-" + str(day) + "T00:00:00Z")
        
        investments = r['investments']
        
        for i in investments:
            if i['company'] is None:
                if i['financial_org'] is None:
                    if i['person'] is None:
                        investor_entity = None
                        investor_name = None
                        investor_permalink = None
                    else:
                        investor_entity = "person"
                        first_name = i['person']['first_name']
                        last_name = i['person']['last_name']
                        investor_name = first_name + " " + last_name
                        investor_permalink = i['person']['permalink']
                else:
                    investor_entity = "financial_org"
                    investor_name = i['financial_org']['name']
                    investor_permalink = i['financial_org']['permalink']
            else:
                investor_entity = "company"
                investor_name = i['company']['name']
                investor_permalink = i['company']['permalink']
            
            extracted_at = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            invsmt = (company_name,company_permalink,round_id,round_code,round_amount,
                round_currency_code,round_date,investor_entity,investor_name,
                investor_permalink,extracted_at)
                
            invsmts.append(invsmt)
    
    return invsmts