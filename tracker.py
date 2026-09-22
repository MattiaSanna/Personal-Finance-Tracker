import json


def run_tracker(choice):
        
    path="data/transactions.txt"

    total_header=8
    first_header=15

    import json
    import re

    # load the categories data
    with open("data/categories.json", "r") as f:
        data = json.load(f)

    categories = data.get("categories", {})
    months_list = data.get("months_list", [])
    months_days = data.get("months_days", [])

    # prepare the master dictionary structure
    dict_lists = {category: {} for category in categories}
    dict_categ = {}
    car = 0



    def add_name(categories, data):
        if l[-1]=='ADD':

            for category in categories:
                if category in line:
                    data["categories"].setdefault(category, []).append(l[12])
                    

            with open("data/categories.json", "w") as f:
                json.dump(data, f, indent=2)
        return data

    def fill_miscellanous (miscellanous_idx, num):
        
        if miscellanous_idx== True and num!=0:

            dict_lists['Miscellaneous'].setdefault(month_name, []).append(num)
            dict_categ.setdefault('Miscellaneous', {}).setdefault(month_name, {}).setdefault(name, []).append(num)
        return dict_lists, dict_categ


    def addto_dictionary(categories, dict_lists, dict_categ):
        miscellanous_idx = True
        #global miscellanous_idx
        for category, keywords in categories.items():
            
            if any(keyword in line.split() for keyword in keywords):
                         
                #if it mathces then add the value into the dict
                dict_lists[category].setdefault(month_name, []).append(num) 
                
                #also, it's not miscellanous
                miscellanous_idx = False
                
                dict_categ.setdefault(category, {}).setdefault(month_name, {}).setdefault(name, []).append(num) 
        return (miscellanous_idx)


    def save_name(line):
        
        name=''
        
        try:
            match = re.search(r"presso\s+(.+)", line)
            if match:
                name = match.group(1)
                name = name.replace("PAYPAL ", "", 1)      
                
            if len(name)>first_header:
                name=name[0:first_header]
        except (NameError):
            pass
        return name


    def get_transaction(l, line):
        num = 0
        try:
            num = float(l[9].replace(",", "."))
            if num == 103.29:
                num = 0
        except (ValueError, IndexError):
            pass
        
        if 'SPOTIFY' in line:         #family subscrption, 6 people
            num/=6
            line=line[0:-17]+'SPOTIFY'
            
            
        elif 'SPLIT' in line:
            num/=2                     #split flight tickets with my gf
       
        
        return num, line


    def last_update(line):
        try:
            year=int(line[6:10])
            month=int(line[3:5])
            last_month=int(line[3:5])
            month_name=months_list[last_month-1]
            day=int(line[0:2])
            last_date=year*12+last_month
            
            if line[14]==':':
                hour=int(line[12:14])
                minute=str(line[15:17])
            else:
                hour=int(line[12:13])
                minute=str(line[14:16])
            if len(minute)==1:
                minute='0'+minute            
        except (ValueError, IndexError):
            pass
        return (year, last_month, month_name,day, last_date, hour, minute, month)
     
        
     
    def get_date(line, current_year, current_month, current_date):
        try:
            current_year=int(line[6:10])
            current_month=int(line[3:5])
            current_date=current_year*12+current_month
            return current_year, current_month, current_date
        except (ValueError, IndexError):
            pass
        return current_year, current_month, current_date
            



    #open the money.txt file 
    with open(path) as p:

        #in order not to start from the first line
         
        line = p.readline()
        
        p.seek(0)
        
        
        
        #get the date of the last update, first line
        year, last_month, month_name, day, last_date, hour, minute, month = last_update(line)

        #for each line in the file check what it says
        for line in p:
            
            names_values = {}
            dict_month = {}    
            l = line.split()
            
            current_year = None
            current_month = None
            current_date = None
                    
            current_year, current_month, current_date = get_date(line, current_year, current_month, current_date)
            
            if current_date is None or len(l) <= 5:
                continue
            if l[3] == "Mattia" and len(l) >5 and l[5] != "Negato" and current_date+11>=last_date:   #so we only select the lines with my name, this comes from whatsapp export          
            
                month_name = months_list[int(current_month) - 1]
                
                num, line = get_transaction(l, line)

                name = save_name(line)
                miscellanous_idx = addto_dictionary(categories, dict_lists, dict_categ)
                
                #addto_dictionary(categories, dict_lists, dict_categ)
                fill_miscellanous (miscellanous_idx, num)
                add_name(categories, data)




    def print_normal(salary, total_cat, saved_month, salary_tot):  
        
        if month in dict_lists[category]:
            if category == 'Salary':
                salary_tot = round(sum(sum(vals) for vals in dict_lists['Salary'].values()), 2)
                return salary, total_cat, saved_month, salary_tot
                
        
            total_cat += round(sum(dict_lists[category][month]),2)
            
            globals()[f"{category}"]+=total_cat
            
            dict_totals[f"{category}"]=globals()[f"{category}"]
            #dict_totals+=[f"{category}"]
            
            if salary==0:
        
                salary=months_days[index]*80
        
            if choice=="Stats": 
                
                print(f"{category :<{first_header-5}.{first_header-6}}{abs(total_cat / salary) * 100:>4.1f}%|{total_cat:>{total_header}.2f}€")
            else:
                print(f"{category:<{first_header}}|{total_cat:>{total_header}.2f}€")  
            if category=='Saves':   
                saved_month += round(sum(dict_lists[category][month]),2)
        return salary, total_cat, saved_month, salary_tot

                 
                                
    def print_show_more(come_cat, living_cat, fluff, total_month, savings, saved_month):
        print("-" * (total_header+first_header+2))

        separator_needed=True
        for category, months in dict_categ.items():
            
            if month in months:
                
                if separator_needed==True:
                    separator_needed=False
                else:
                    print (f"{'':<{first_header}}|{'|':>{total_header+1}} ")
                print (f"{category:<{first_header}}|{'|':>{total_header+1}} ")
            
                for sub_month, entry in months.items():
                    if sub_month==month:
                        for name, values in entry.items():
                            for val in values:
                                
                                print (f"{name:<{first_header}}|{val:>{total_header}.2f}€") 

        print("-" * (total_header+first_header+2))

        print (f"{'Coming back':<{first_header}}|{come_cat:>{total_header}.2f}€")
        print (f"{'Essentials':<{first_header}}|{living_cat:>{total_header}.2f}€")
        print (f"{'Fluff':<{first_header}}|{fluff:>{total_header}.2f}€")

        print("-" * (total_header+first_header+2))

        print(f"{'Total':<{first_header}}|{total_month:>{total_header}.2f}€")
        print(f"{'Saved' :<{first_header}}|{savings+saved_month:>{total_header}.2f}€")
        
    def print_stats(ess_perc, wants_perc, sav_perc, living_cat, wants, savings, total_month):
        print("-" * (total_header+first_header+2))

        print(f"{'Essential':<{first_header-4}}{ess_perc:>3.0f}%|{living_cat:>{total_header}.2f}€")
        print(f"{'Wants':<{first_header-4}}{wants_perc:>3.0f}%|{wants:>{total_header}.2f}€")
        print(f"{'Money left':<{first_header-4}}{sav_perc:>3.0f}%|{savings:>{total_header}.2f}€")
        print("-" * (total_header+first_header+2))
        print(f"{'Total spent':<{first_header}}|{total_month:>{total_header}.2f}€")
        
    def print_normal2(total_month, savings):
        print("-" * (total_header+first_header+2))

        print(f"{'Total':<{first_header}}|{total_month:>{total_header}.2f}€")
        print(f"{'Money left' :<{first_header}}|{savings:>{total_header}.2f}€")
        
        
    def print_stats2(day, living_cat, car):
        if int(day)==day:
            pass
        else:
            day=int(day)+1

        print (

        f"\n\n\nMoney spent on average in\n{int(n_months)} months and {day} days:\n"
        )

        for cat in dict_living:

            living_cat += round(dict_totals.get(cat, 0), 2)
        car += round(dict_totals.get("Gas", 0), 2)
        car += round(dict_totals.get("Car", 0), 2)

        ess_perc=int(abs(living_cat/salary_tot*100))

        print (f"{'Rent':<{first_header-5}.{first_header-6}}{round(dict_totals['Rent'], 2) /  salary_tot* 100:>4.1f}%|{round(dict_totals['Rent'], 2) / len(dict_categ['Rent']):>{total_header}.2f}€")

        for each_category, each_value in dict_totals.items():
            if each_category=='Rent':
                continue

            print(

            f"{each_category:<{first_header-5}.{first_header-6}}{each_value / salary_tot * 100:>4.1f}%|{each_value / n_months:>{total_header}.2f}€")
        print("-" * (total_header+first_header+2))
        print (
        f"{'Essential':<{first_header-4}}{ess_perc:>3.0f}%|{living_cat/n_months:>{total_header}.2f}€\n"
        f"{'Wants':<{first_header-4}}{saving_tot / salary_tot * 100:>3.0f}%|{salary_tot / len(dict_categ['Salary']) - saving_tot / n_months - living_cat/n_months:>8.2f}€\n"
        f"{'Saves':<{first_header-4}}{saving_tot / salary_tot * 100:>3.0f}%|{saving_tot / n_months:>8.2f}€\n"

    )
        print(

        f"\n\n\nAverage salary\n"
        f"{'-'*25}\n"
        f"Per month     |{salary_tot / len(dict_categ['Salary']):>9.2f}€\n"
        f"{'-'*25}\n"
        f"\nMoney spent on average\n"
        f"{'-'*25}\n"
        f"Per month     |{salary_tot / n_months-saving_tot / n_months:>9.2f}€\n"
        f"\nMoney saved in total\n"
        f"{'-'*25}\n"
        f"Total    {saving_tot / salary_tot * 100:>4.1f}%|{saving_tot:>9.2f}€\n"
        f"Per month     |{saving_tot / n_months:>9.2f}€\n"
        f"\nMoney spent on car and gas\n"
        f"{'-'*25}\n"
        f"Total    {car / salary_tot * 100:>4.1f}%|{car:>9.2f}€\n"
        f"Per month     |{car / n_months:>9.2f}€\n"

    )
        
        
    def living_come_cat(dict_lists):
        
        living_cat=0
        come_cat=0
        salary=0
        
        

        living_list=['Rent','Bills','Groceries Turin','Groceries Sardinia','GTT','GYM','Subscriptions','Chinese market', 'Pharmacy']
        come_back=['Flights','Transports','Gas','Booking']
        dict_living = {k: v for k, v in dict_lists.items() if k in living_list}
        dict_come = {k: v for k, v in dict_lists.items() if k in come_back}

        for cat in dict_living:
            if month in dict_living[cat]:
                living_cat+=round(sum(dict_living[cat][month]),2)
        for cat in dict_come:
           if month in dict_come[cat]:
                come_cat+=round(sum(dict_come[cat][month]),2)
        return salary, living_cat, come_cat, dict_living, dict_come

    def percentages(salary, saving_tot, months_days, total_month, living_cat, come_cat):
        if salary==0:
            salary=months_days[index]*80
            skip='true'
        else:
            skip='false'

        savings=abs(salary)-abs(total_month)

        if skip=='false':
            saving_tot+=savings
            print ()

        wants=abs(salary)-abs(living_cat)-abs(savings)
        fluff=abs(salary)-abs(living_cat)-abs(savings)-abs(come_cat)

        sav_perc=int(abs(savings/salary*100))
        ess_perc=int(abs(living_cat/salary*100))
        wants_perc=int(100-ess_perc-sav_perc)
        
        return savings, salary, wants, fluff, sav_perc, ess_perc, wants_perc, saving_tot


    def months(dict_categ, months_list, months_days):
        
        from datetime import date

        today = date.today()

        month_datetime = today.month

        day = today.day

        n_months=len(dict_categ['Salary'])

        if n_months==month_datetime:
            n_months-=1


        if n_months>11:
            n_months=11

        if n_months==months_list[last_month-1]:
            n_months=n_months-1
        n_months=n_months+int(day)/31


        months_list = list(reversed(months_list))
        months_days = list(reversed(months_days))


        n=-int(month)
        months_list_2=months_list[(0):n]

        del months_list[0:n]
        months_list=months_list+months_list_2             
        months_days_2 = months_days[(0):n]

        del months_days[0:n]
        months_days = months_days + months_days_2
        
        return n_months, months_days, months_days_2, months_list

    #here's the printing
    last_up = f"\nLast update:\n{months_list[last_month-1]} {day} at {int(hour):02d}:{int(minute):02d}"
    print (last_up,"\n\n")

    n_months, months_days, months_days_2, months_list = months(dict_categ, months_list, months_days)

    saving_tot=0 
    salary_tot=0


    dict_totals={}

    for category in dict_lists:
        globals()[f"{category}"]=0




    for index, month in enumerate(months_list):
        
        saved_month=0
        total_month=0
        
        salary, living_cat, come_cat, dict_living, dict_come = living_come_cat(dict_lists)
        

        print ('\n\n')

        print("Money spent in:", month,'\n')

        if month in dict_lists.get('Salary', {}):
            salary = round(-sum(dict_lists['Salary'][month]), 2)

        # category lines are the same for every choice, so they stay in one place
        for category in dict_lists:
            total_cat = 0

            salary, total_cat, saved_month, salary_tot = print_normal(salary, total_cat, saved_month, salary_tot)
            total_month+=total_cat

        dict_totals = dict(sorted(dict_totals.items(), key=lambda item: item[1], reverse=True))

        # everything below needs salary and total_month, so it comes after the category loop
        savings, salary, wants, fluff, sav_perc, ess_perc, wants_perc, saving_tot = percentages(salary, saving_tot, months_days, total_month, living_cat, come_cat)

        if choice=="Show more":

            print_show_more(come_cat, living_cat, fluff, total_month, savings, saved_month)

        elif choice=="Stats":

            print_stats(ess_perc, wants_perc, sav_perc, living_cat, wants, savings, total_month)

        else:
            
            print_normal2(total_month, savings)

    # the averages are printed once, after all the months, so this stays outside the loop
    if choice=="Stats":

        print_stats2(day, living_cat, car)
