from bs4 import BeautifulSoup
import urllib.request
import jsonlines

n_users=0
idlinks=[]

def search_links(url,param):
    global n_users,idlinks    
    html_doc = urllib.request.urlopen(url+param)
    soup = BeautifulSoup(html_doc)
    links = soup.select('a[href*="{0}"]'.format(param))
    if links:
        for link in links:
            if n_users>1000:
                break
            search_links(url,link['href'])
    else:
        for link in soup.select('a[href*="{0}"]'.format('id')):
            idlinks.append(url+link['href'])
        n_users=len(idlinks)
def process_links(links):#id_links
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    user_info = []
    for link in links:
        req = urllib.request.Request(link, headers=headers)
        print(link)
        html_doc = urllib.request.urlopen(req)
        soup = BeautifulSoup(html_doc)
        labels = soup.select('div.label.fl_l')
        user = {'url':link,'Имя':soup.title.get_text().split(" | ")[0]}
        for label in labels:
            key = label.string[0:-1]
            label_sibling = label.find_next_sibling('div',class_='labeled')
            if label_sibling.string:
                value = label_sibling.string
            else:
                value = ''.join(str(child.string) for child in label_sibling.children)
            user[key] = value            
        user_info.append(user)
    with jsonlines.open('vkusers.jsonl', mode='w') as writer:
        writer.write_all(user_info)

search_links('http://vk.com/','catalog.php')
process_links(idlinks)
print(n_users)
