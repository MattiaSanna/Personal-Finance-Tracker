choice="show_off"
choice_2="show_off_less"
fifty_thirty='false'

header=32
header_1=header-22

import json
# load your category keyl
with open("data_2.json", "r") as f:
    data = json.load(f)

categories = data.get("categories", {})

months_list = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

# prepare the master dictionary structure
dict_lists = {category: {} for category in categories}
dict_categ = {}

p = open("money.txt", "r")

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
            num/=2                     #split with my gf
        
        try:
            month=int(line[3:5])
            month_name=months_list[month-1]
        except (ValueError, IndexError):
            pass
        #it's necvessary to keep them divide cause of the txt file. at first it didn't have that much info
        try:
            day=int(line[0:2])
            hour=int(line[12:14])
            minute=str(line[15:16])
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
            
        if len(name)>19:
            name=name[0:19]
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
            dict_categ.setdefault(category, {}).setdefault(month_name, {}).setdefault(name, []).append(num) 



#here's the printing

last_up = f"\nLast update: {months_list[month-1]} {day} at {int(hour):02d}:{int(minute):02d}"
print (month)
n=int(month)
months_list_2=months_list[(0):n]
del months_list[0:n]
months_list=months_list+months_list_2            
           

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
                
                print(f"{category:<19} | {total_cat:>{header_1}.2f} €")         
        total_month+=total_cat
    
    if choice=="show_off":
        
        print("-" * header)
        
        if choice_2=='show_off_less':
            
            show_list=['Online shopping','Dining out','Miscellaneous']
            dict_categ = {k: v for k, v in dict_categ.items() if k in show_list}
            
        first_line='full'
        for category, months in dict_categ.items():
            
            if month in months:
                
                if first_line=='full':
                    first_line='empty'
                else:
                    print (f"{'':<19} | {'|':>{header_1+2}} ")
                print (f"{category:<19} | {'|':>{header_1+2}} ")
            
                for sub_month, entry in months.items():
                    if sub_month==month:
                        for name, values in entry.items():
                            for val in values:
                                #print (name, val)
                                print (f"{name:<19} | {val:>{header_1}.2f} €")   
                
    print("-" * header)
    
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
    wants=abs(salary)-abs(living_cat)-abs(savings)
    fluff=abs(salary)-abs(living_cat)-abs(savings)-abs(come_cat)
    
    sav_perc=round(abs(savings/salary*100),2)
    ess_perc=round(abs(living_cat/salary*100),2)
    wants_perc=round(100-ess_perc-sav_perc,2)
   
    if fifty_thirty=='true':
        
        print (f"{'Coming back':<19} | {come_cat:>{header_1}.2f} €")
        print("-" * header)
        print(f"{'Essentials   '+str(ess_perc)+' %':<19}| {living_cat:>{header_1}.2f} €")
        print(f"{'Wants        '+str(wants_perc)+' %':<19}| {wants:>{header_1}.2f} €")   
        print(f"{'Savings      '+str(sav_perc)+' %' :<19}| {savings:>{header_1}.2f} €")
        print("-" * header)
        print(f"{'Total   ' + month:<19} | {total_month:>{header_1}.2f} €")

        
        
    else:
        print (f"{'Coming back':<19} | {come_cat:>{header_1}.2f} €")
        print (f"{'Essentials':<19} | {living_cat:>{header_1}.2f} €")
        print (f"{'Fluff':<19} | {fluff:>{header_1}.2f} €")
    
        
        print("-" * header)
        print(f"{'Total   ' + month:<19} | {total_month:>{header_1}.2f} €")
        print(f"{'Savings      ' :<19} | {savings:>{header_1}.2f} €")
        
print (last_up)
    
