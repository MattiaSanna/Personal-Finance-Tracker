import json

# --- YOUR MONEY SCRIPT LOGIC (MERGED HERE) ---
# This version uses print() inside the logic (like your original script).
def run_tracker(choice):
    # Example prints — replace/add whatever print() calls your real script uses
        
    choice_2="show_off_more"
    #choice="50 30 20"
    fifty_thirty='false'


    total_header=8
    first_header=15


    # load your category keyl
    with open("data/categories.json", "r") as f:
        data = json.load(f)

    categories = data.get("categories", {})

    car_list = list(categories.get("Gas", []))
    car_list += ["*PRIMA", "*PAG", "OLLU", "*AGCOMPANYSR", "*MOONEY.","BOLLO"]
    salary_list = categories.get("Salary", [])
    car = 0
    salary_tot = 0

    months_list = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]

    # prepare the master dictionary structure
    dict_lists = {category: {} for category in categories}
    dict_categ = {}

    p = open("data/transactions.txt", "r")

    #for each line in the file check what it says
    for line in p:
        
        names_values = {}
        dict_month = {}    
        
        miscellanous_idx='true'
        num=0
        l = line.split()
        
        if l[3] == "Mattia" and len(l) >5 and l[5] != "Negato":   #so we only select the lines with my name, this comes from whatsapp export
                
            
            try:
                num = float(l[9].replace(",", "."))
                if num == 103.29:
                    num=0                     #cause the gas station charges 103.29 at first
            except (ValueError, IndexError):
                pass
            
            if 'SPOTIFY' in line:         #family subscrption, 6 people
                num/=6
                line=line[0:-17]+'SPOTIFY'
            if 'RYANAIR' in line:
                if l[-1]!='NOSPLIT':
                    num/=2                     #split with my gf
            if 'AEROITALI' in line:
                if l[-1]!='NOSPLIT':
                    num/=2                     
            
            if any(w in car_list for w in l[-15:]):
                car+=num
                
            if any(w in salary_list for w in l[-15:]):
                salary_tot+=num
                
            
            
            try:
                month=int(line[3:5])
                month_name=months_list[month-1]
            except (ValueError, IndexError):
                pass
            #it's necvessary to keep them divide cause of the txt file. at first it didn't have that much info
            try:
                day=int(line[0:2])
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
            
            #this is to store the data of each if you want to better inspect each esxpense
            lenght=len(l)
            
            if lenght>13 and 'PAYPAL' not in line:
                name=l[12]+' '+l[13] 
            elif lenght>14 and 'PAYPAL' in line:
                name=l[13]+' '+l[14] 
            elif lenght>15 and 'PAYPAL' in line:
                name=l[14]+' '+l[15] 
            elif lenght>12 and 'PAYPAL' in line:
                name=l[13]
            elif lenght>12:
                name=l[12] 
                
            if len(name)>first_header:
                name=name[0:first_header]
            #now for each category in my dict check if it matches the line
            for category, keywords in categories.items():
                
                if any(keyword in line.split() for keyword in keywords):
                             
                    #if it mathces then add the value into the dict
                    dict_lists[category].setdefault(month_name, []).append(num) 
                    
                    #also, it's not miscellanous
                    miscellanous_idx='false'
                    
                    dict_categ.setdefault(category, {}).setdefault(month_name, {}).setdefault(name, []).append(num) 
                    
            #if the algorithm didn't find the right category it goes to misc
            if miscellanous_idx=='true' and num!=0:
                
                add=line[-4:-1]
                
                if l[-1]=='ADD':
                    
                    for category in categories:
                        if category in line:
                            data["categories"].setdefault(category, []).append(l[12])

                    with open("data_2.json", "w") as f:
                        json.dump(data, f, indent=2)

                dict_lists['Miscellaneous'].setdefault(month_name, []).append(num)
                dict_categ.setdefault('Miscellaneous', {}).setdefault(month_name, {}).setdefault(name, []).append(num)


    #here's the printing
    last_up = f"\nLast update:\n{months_list[month-1]} {day} at {int(hour):02d}:{int(minute):02d}"
    print (last_up,"\n\n")



    months_list = [
        'December', 'November', 'October', 'September', 
        'August', 'July', 'June', 'May', 
        'April', 'March', 'February', 'January'
    ]


    n=-int(month)
    months_list_2=months_list[(0):n]

    del months_list[0:n]
    months_list=months_list+months_list_2            
    saving_tot=0  
    x=0                 

    for month in months_list:
        salary=0
        
        print ('\n\n')
        print("Money spent in:", month,'\n')
        total_month=0
        for category in dict_lists:
            total_cat = 0
            
            if month in dict_lists[category]:
                
                if category=='Salary':   
                    salary += round(-sum(dict_lists[category][month]),2)
                    
                else:
                    total_cat += round(sum(dict_lists[category][month]),2)
                    
                    print(f"{category:<{first_header}}|{total_cat:>{total_header}.2f}€")         
            total_month+=total_cat
        
        if choice=="Show more":
            
            print("-" * (total_header+first_header+2))
            
            if choice_2=='show_off_less':
                
                show_list=['Online shopping','Dining out','Groceries Turin','Flights','Miscellaneous']
                dict_categ = {k: v for k, v in dict_categ.items() if k in show_list}
                
            first_line='full'
            for category, months in dict_categ.items():
                
                if month in months:
                    
                    if first_line=='full':
                        first_line='empty'
                    else:
                        print (f"{'':<{first_header}}|{'|':>{total_header+1}} ")
                    print (f"{category:<{first_header}}|{'|':>{total_header+1}} ")
                
                    for sub_month, entry in months.items():
                        if sub_month==month:
                            for name, values in entry.items():
                                for val in values:
                                    #print (name, val)
                                    print (f"{name:<{first_header}}|{val:>{total_header}.2f}€")   
                    
        print("-" * (total_header+first_header+2))
        
        living_list=['Rent','Bills','Groceries Turin','Groceries Sardinia','GTT','GYM','Subscriptions','Chinese market', 'Pharmacy']
        come_back=['Flights','Transports','Gas','Booking']
        

        living_cat=0
        come_cat=0
        
        dict_living = {k: v for k, v in dict_lists.items() if k in living_list}
        dict_come = {k: v for k, v in dict_lists.items() if k in come_back}
        
        #print (dict_fluff)
        for cat in dict_living:
            if month in dict_living[cat]:
                living_cat+=round(sum(dict_living[cat][month]),2)
        for cat in dict_come:
           if month in dict_come[cat]:        
                come_cat+=round(sum(dict_come[cat][month]),2)
                
        if salary==0:
            salary=1750
        
        savings=abs(salary)-abs(total_month)
        if salary!=1750:
         saving_tot+=savings
         x+=1
        wants=abs(salary)-abs(living_cat)-abs(savings)
        fluff=abs(salary)-abs(living_cat)-abs(savings)-abs(come_cat)
        
        sav_perc=int(abs(savings/salary*100))
        ess_perc=int(abs(living_cat/salary*100))
        wants_perc=int(100-ess_perc-sav_perc)
       
        if choice=='50 30 20':
            
            print(f"{'Essential':<{first_header-4}}{ess_perc:>3.0f}%|{living_cat:>{total_header}.2f}€")
            print(f"{'Wants':<{first_header-4}}{wants_perc:>3.0f}%|{wants:>{total_header}.2f}€")
            print(f"{'Savings':<{first_header-4}}{sav_perc:>3.0f}%|{savings:>{total_header}.2f}€")
            print("-" * (total_header+first_header+2))
            print(f"{'Total':<{first_header}}|{total_month:>{total_header}.2f}€")

            
        else:
            print (f"{'Coming back':<{first_header}}|{come_cat:>{total_header}.2f}€")
            print (f"{'Essentials':<{first_header}}|{living_cat:>{total_header}.2f}€")
            print (f"{'Fluff':<{first_header}}|{fluff:>{total_header}.2f}€")
        
            
            print("-" * (total_header+first_header+2))
            print(f"{'Total':<{first_header}}|{total_month:>{total_header}.2f}€")
            print(f"{'Savings' :<{first_header}}|{savings:>{total_header}.2f}€")

    if choice=="50 30 20":
        print(
        f"\n\nMoney saved in total\n"
        f"{'-'*25}\n"
        f"Total    {saving_tot / salary_tot * 100:>4.1f}%|{saving_tot:>9.2f}€\n"
        f"Per month     |{saving_tot / x:>9.2f}€\n"
        f"{'-'*25}\n"
        f"\nMoney spent on the car\n"
        f"{'-'*25}\n"
        f"Total    {car / salary_tot * 100:>4.1f}%|{car:>9.2f}€"
    )
