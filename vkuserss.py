from bs4 import BeautifulSoup
import urllib.request
import jsonlines

count=0
id_links=[]


def search_links(url, param):
    global count, id_links    
    html = urllib.request.urlopen(url + param)
    soup = BeautifulSoup(html)
    links = soup.select('a[href*="{0}"]'.format(param))
    if links:
        for link in links:
            if count > 1000:
                break
            search_links(url, link['href'])
    else:
        for link in soup.select('a[href*="{0}"]'.format('id')):
            id_links.append(url+link['href'])
        count = len(id_links)


def process_links(links): #id_links
    users = []
    for link in links:
        req = urllib.request.Request(link, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})

        html = urllib.request.urlopen(req)
        soup = BeautifulSoup(html)
        labels = soup.select('div.label.fl_l')
        user = {'url':link, 'Имя':soup.title.get_text().split(" | ")[0]}

        for label in labels:
            key = label.string[0:-1]
            label_sibling = label.find_next_sibling('div', class_='labeled')

            if label_sibling.string:
                value = label_sibling.string
            else:
                value = ''.join(str(child.string) for child in label_sibling.children)

            user[key] = value            
        users.append(user)

    with jsonlines.open('vkusers.json', mode='w') as writer:
        writer.write_all(users)


def main():
    search_links('http://vk.com/','catalog.php')
    process_links(id_links)
    print("We have %d links" % count)

if __name__ == '__main__':
    main()
