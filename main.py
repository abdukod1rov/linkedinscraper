from bs4 import BeautifulSoup
import requests
import json

base_url = "https://www.linkedin.com/jobs/search?keywords=Python&location=United%20States&geoId=103644278&trk" \
           "=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0 "
hrefs = []
try:
    response = requests.get(base_url)
    soup2 = BeautifulSoup(response.text, 'html.parser')
    job_listings = soup2.find_all('li')

    jobs = []
    job_links = []
    for job in job_listings:
        a = job.find('a')
        if a:
            hrefs.append(a['href'])
        job_links = [link for link in hrefs if 'view' in link]

    for url in job_links:
        job_response = requests.get(url)
        if job_response:
            print("Parsing", url)
            job_soup = BeautifulSoup(job_response.text, 'html.parser')
            # Extracting header main section
            if job_soup:
                position = job_soup.find('h1', {'class': 'top-card-layout__title'}).text.strip()
                company = job_soup.find('a', {'class': 'topcard__org-name-link'}).text.strip()
                location = job_soup.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'}).text.strip()

                # Extracting job level and employment type information
                description = job_soup.find('ul', {'class': 'description__job-criteria-list'})
                desc_list = description.get_text().split('\n')

                if len(desc_list) > 14:
                    job_level = desc_list[6].strip()
                    employment_type = desc_list[14].strip()
                    industry = desc_list[30].strip()

                else:
                    job_level = 'Not Applicable'
                    employment_type = desc_list[6].strip()
                    industry = 'Not Applicable'

                print(
                    f'Company : {company} ||Industry: {industry}||\n Job level: {job_level}||'
                    f' Employment type: {employment_type}\n Location: {location}')
                print()
                print()

                main_desc = job_soup.find('div', {'class': 'description__text description__text--rich'}).text.strip()
                sentences = main_desc.split('.') if main_desc else None

                final_desc = ''
                if len(sentences) > 2:
                    final_desc = '.'.join(sentences[:2])

                else:
                    final_desc = sentences[0].replace('\n', '').replace('\n\n', '').replace('\n\n\n', '').replace(
                        'Show more', '').replace(
                        'Show less',
                        '')

                final_desc += '.'

                if position and location and company and job_level and employment_type:
                    job_data = {
                        'title': position,
                        'company': company,
                        'level': job_level,
                        'location': location,
                        'employment_type': employment_type,
                        'description': final_desc

                    }
                    jobs.append(job_data)
                    job_data = {}
    json_data = json.dumps(jobs)
    with open('job_listings.json', 'w') as file:
        file.write(json_data)
except requests.exceptions.RequestException as e:
    print("Error fetching page", e)

"""

I tried many times to get the key skills and requirement section. While I was able to get the key skills for some jobs,
I could not implement a general program that works for any html template. But, I am still trying to accomplish this task


# u_sections = job_soup.find_all('strong')
# # print(u_sections)
# # pattern = r'\b(Job Requirements:?' \
# #           r'|Requirements:?\s|Must-Haves:?\s|Qualifications:\s|Key ' \
# #           r'Skills:?\s|Skills:?\s|Required:?\s)\b'
#
# words2 = [word.text for word in u_sections]
# # Find the matching word in the list of words
#
# # Example list of words
# words = ['The role:', 'Location:', 'Qualifications:', 'Offer:', 'Python Developer', 'Texas, United States',
#          'English (English)', 'Python Developer', 'Texas, United States']
#
# # Regular expression pattern to match the required keyword

#
# # Find the matching word in the list of words
# matched_word = None
# for word in words:
#     if word in keywords:
#         matched_word = word
#         break
#
# # Print the matched word
# print(matched_word)
# job_requirements = job_soup.find_next('strong', string=matched_word)
# if job_requirements:
#     print(job_requirements)
#     # job_list = job_requirements.parent.find_next('ul')
#
# print(job_requirements)
# if job_requirements:
#     must_haves = job_requirements.find_next('ul')
#
#     for requirement in must_haves.find_all('li'):
#         print(requirement.text.strip()) """

"""I didn't add the try and except block because the code didn't have any critical sections that could raise exceptions. However, if you expect that some parts of the code may raise exceptions, it's always good practice to handle them gracefully using a try and except block.

Regarding the session object, using a session object can improve performance by reusing the same TCP connection for multiple requests, thus reducing the overhead of establishing a new connection for each request. However, since this code only makes a small number of requests, the impact on performance is likely to be minimal. Nonetheless, using a session object is a good practice and can be added to the code for future scalability.

"""
