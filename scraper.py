from bs4 import BeautifulSoup as bs
import urllib
import os

def run():
    working_dir = os.getcwd()
    if not os.path.exists(working_dir + '/summaries'):
        os.mkdir('summaries')

    main_page_url = 'https://simpsonsarchive.com/episodes.html'
    page = urllib.request.urlopen(main_page_url)
    soup = bs(page, 'html.parser')
    links = []
    all_as = soup.find_all('a', href=True)

    for a in all_as:
        text = a.text
        if not text or 'MG' in text:
            continue

        href = a['href']
        if not href or 'episodes' not in href or 'mini' in href or '7F76' in href:
            continue

        links.append(href)

    base_url = 'https://simpsonsarchive.com/'

    for link in links:
        if link:
            try:
                page = urllib.request.urlopen(base_url + link)
            except Exception as e:
                print(e)
                print('an exception occurred')
                print(base_url + link)
                pass

            if not page:
                print('no page')
                print(base_url + link)
                continue

            soup = bs(page, 'html.parser')

            if not soup:
                print('no soup')
                print(base_url + link)
                continue


            h1s = soup.find_all('h1')
            target = 'quotes and scene summary'

            anchor = None
            wrote_something = False
            for h1 in h1s:
                if not anchor and target in h1.text.lower():
                    anchor = h1

            if not anchor:
                h2s = soup.find_all('h2')
                for h2 in h2s:
                    if not anchor and target in h2.text.lower():
                        anchor = h2
            if not anchor:
                pres = soup.find_all('pre')
                print('Using text strategy for ' + link)

                if not len(pres):
                    try:
                        page = urllib.request.urlopen(base_url + link.replace('html', 'txt'))
                    except Exception:
                        pass
                    start_found = False
                    lines = str(page).split("\n")

                    summary_rows = []
                    for line in lines:
                        if 'episode summaries' in line.lower() or 'episode capsule' in line.lower():
                            start_found = False
                            if start_found:
                                summary_rows.append(line)
                            if target in line.lower() or 'scene summaries' in line.lower():
                                start_found = True

                    raw_str = ''
                    for row in summary_rows:
                        raw_str += '\n' + row

                    with open(working_dir + '/summaries/' + link.replace('/',''), 'w+') as new_html:
                        print('composing from raw string')
                        wrote_something = True
                        new_html.write(raw_str)
                        new_html.close()

                for pre in pres:
                    if target in pre.text.lower() or 'scene summaries' in pre.text.lower():
                        summary_rows = []
                        target_pre = pre.prettify()
                        lines = [s.strip() for s in target_pre.splitlines()]
                        found = False
                        for line in lines:
                            if 'episode summaries' in line.lower() or 'episode capsule' in line.lower():
                                found = False
                            if found:
                                summary_rows.append(line)
                            if target in line.lower() or 'scene summaries' in line.lower():
                                found = True

                        raw_str = ''
                        for row in summary_rows:
                            raw_str += '\n' + row

                        with open(working_dir + '/summaries/' + link.replace('/',''), 'w+') as new_html:
                            print('composing from string')
                            wrote_something = True
                            new_html.write(raw_str)
                            new_html.close()
                    
            if anchor:
                summary = anchor.find_next_sibling('pre')
                with open(working_dir + '/summaries/' + link.replace('/',''), 'w+') as new_file:
                    wrote_something = True
                    new_file.write(summary.prettify())
                    new_file.close()

            if not wrote_something:
                print('summary not found for: ' + link)

if __name__ == '__main__':
    run()




