
import sqlite3 as sql
import pyperclip

def show_sites(c):
    c.execute('select site, username from pwm order by site asc')
    sites = [s[0] + ' - ' + s[1] for s in c.fetchall()]
    for i, site in enumerate(sites):
        print(f'{i + 1}. {site}')

    return sites

def retrieve(c):
    site = input('Enter the site to retrieve or nothing to show all sites: ')
    if site == '':
        sites = show_sites(c)
        site = input('Enter the number of the site to retrieve: ')
        try:
            site = sites[int(site) - 1]
        except:
            return
    
    c.execute("select * from pwm where site == ?", (site,))
    cred = c.fetchall()
    if cred == []:
        print('\tSite does not exist')
    else:
        site, usr, pw = cred[0]
        print(f'\tSite = {site}\n\tUsername = {usr}')
        pyperclip.copy(pw)
        action = input('Show password? [y/n] ').lower()
        if action == 'y':
            print(f'\tPassword = {pw}')

def add(c):
    site = input('Enter the new site: ') 
    usr = input('Enter the new username: ')
    pw = input('Enter new password: ')
    c.execute("insert into pwm values (?,?,?)",(site,usr,pw))
   

def edit(c):
    pass

def delete(c):
    pass


if __name__ == '__main__':
    conn = sql.connect('pwm.db')
    c = conn.cursor()
    c.execute("""
        create table if not exists pwm (
            site char(100), 
            username char(100),
            password char(20)
            )
    """)

    action = ''
    while True:
        action = input('='* 45 + '\n[A]dd, [R]etrieve, [E]dit, [D]elete, [Q]uit: ').lower()
        if action == 'a':
            add(c)
        elif action == 'r':
            retrieve(c)
        # elif action == 'e':
        #     edit(c)
        # elif action == 'd':
        #     delete(c)
        elif action == 'q':
            break
        else:
            print('Invalid Input!')
        if action in ('a', 'e', 'd'):
            conn.commit()
    
    conn.close()




"""

shelved
    - editting and deleting
    - editting when trying to add the same site 2 times
    - generate passwords
    - encrypt database


"""