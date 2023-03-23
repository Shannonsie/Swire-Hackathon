#!/usr/bin/env python
# coding: utf-8

# In[55]:


import fitz
doc = fitz.open("/mnt/c/Users/user/Desktop/Swireview/Jane.pdf")
text = ""
for page in doc:
    text +=  page.get_text()
with open("/mnt/c/Users/user/Desktop/Swireview/Jane.txt", "w", encoding='utf-8') as f:
    f.write(text)
text = ""

for i in range(1):
    text_number = i
    text_file = '/mnt/c/Users/user/Desktop/Swireview/Jane.txt'
    # CV transcript
    with open(text_file) as f:
        text = f.readlines()
    text = [line for line in text if line != "\n"]
    # Number of lines
    n = len(text)
    text += " "

    # Credentials
    name, email, number = "", "", ""
    profile = ""
    unis = []
    jobs = []
    extras = []
    awards = []
    Skills = ""

    # Get the ranges of CV parts
    headers = ["PERSONAL PROFILE", "EDUCATION", "WORK EXPERIENCE", "EXTRACURRICULARS", "AWARDS", "SKILLS"]
    indices = []
    for i in range(n):
        if text[i].strip() in headers:
            indices.append(i)
    indices.append(n)

    # Get the name, the email address, and the phone number
    name = text[0].strip()
    for x in text[1]:
        if x == '|':
            email, number = number, email
        else:
            number += x
    name = name.strip()
    email = email.strip()
    number = number.strip()
    while len(name) > 0 and name[0] == '.':
        name = name[1:]
    while len(name) > 0 and name[-1] == '.':
        name = name[:-1]
        
    for i in range(len(indices) - 1):
        # Get the personal profile
        if text[indices[i]].strip() == "PERSONAL PROFILE":
            for j in range(indices[i] + 1, indices[i + 1]):
                profile += text[j]
            profile = profile.replace('\n', ' ').strip()
            if profile[-1] != '.':
                profile += '.'

        # Get the education credentials
        elif text[indices[i]].strip() == "EDUCATION":
            bullet_points, subheaders = [], []
            for j in range(indices[i] + 1, indices[i + 1]):
                if text[j].strip() == '●' and text[j].strip() == '●':
                    bullet_points.append(j)
                    subheaders.append(text[j + 1].strip())
            bullet_points.append(indices[i + 1] + 1)
            subheaders.append(text[indices[i + 1]].strip())
            last_pos = indices[i]

            for j in range(len(bullet_points) - 1):
                if subheaders[j] != "Additional points:":
                    uni, dates, start_date, end_date, major = "", "", "", "", ""
                    add_points = []

                    # Uni name and dates
                    tmp = ""
                    for k in range(last_pos + 1, bullet_points[j]):
                        tmp += text[k]
                    tmp = tmp.replace("\n", " ")
                    for ch in tmp:
                        if ch == ',':
                            uni, dates = dates, uni
                        else:
                            dates += ch
                    for ch in dates:
                        if ch == '-' or ch == '–':
                            start_date, end_date = end_date, start_date
                        else:
                            end_date += ch

                    # Uni major
                    tmp = ""
                    end_pos = bullet_points[j + 1]
                    if subheaders[j + 1] != "Additional points:":
                        end_pos -= 1
                    for k in range(bullet_points[j] + 1, end_pos):
                        tmp += text[k]
                        last_pos = k
                    tmp = tmp.replace("\n", " ")
                    major = tmp

                    # Uni additional points
                    if subheaders[j + 1] == "Additional points:":
                        tmp = "" 
                        for k in range(bullet_points[j + 1] + 1, bullet_points[j + 2] - 1):
                            if text[k].strip() != '○':
                                tmp += text[k]
                            if text[k].strip() == '○' or k + 1 == bullet_points[j + 2] - 1:
                                tmp = tmp.replace("\n", " ")
                                add_points.append(tmp)
                                tmp = " "
                            last_pos = k

                    while len(start_date) > 0 and start_date[0] == '.':
                        start_date = start_date[1:]
                    while len(start_date) > 0 and start_date[-1] == '.':
                        start_date = start_date[:-1]
                    while len(end_date) > 0 and end_date[0] == '.':
                        end_date = end_date[1:]
                    while len(end_date) > 0 and end_date[-1] == '.':
                        end_date = end_date[:-1]
                    uni = uni.strip()
                    start_date = start_date.strip()
                    end_date = end_date.strip()
                    major = major.strip()
                    add_points = [x.strip() for x in add_points[1:]]
                    unis.append([uni, start_date, end_date, major, add_points])

        # Get the work credentials
        elif text[indices[i]].strip() == "WORK EXPERIENCE":
            bullet_points, subheaders = [], []
            for j in range(indices[i] + 1, indices[i + 1]):
                if text[j].strip() == '●' and text[j].strip() == '●':
                    bullet_points.append(j)
                    subheaders.append(text[j + 1].strip())
            bullet_points.append(indices[i + 1])
            subheaders.append(text[indices[i + 1]].strip())
            last_pos = indices[i]

            for j in range(len(bullet_points) - 1):
                if subheaders[j] == "Description:":
                    position, company, dates, start_date, end_date = "", "", "", "", ""
                    description, skills = [], []

                    # Job position, company and dates
                    tmp = ""
                    for k in range(last_pos + 1, bullet_points[j]):
                        tmp += text[k]
                    tmp = tmp.replace("\n", " ")
                    values = [""]
                    for ch in tmp:
                        if ch == ',':
                            values.append("")
                        else:
                            values[-1] += ch
                    position, dates = values[0], values[-1]
                    for ch in values[1:-1]:
                        company += ch
                        if ch != values[-2]:
                            company += ','
                    for ch in dates:
                        if ch == '-' or ch == '–':
                            start_date, end_date = end_date, start_date
                        else:
                            end_date += ch

                    # Job description
                    tmp = ""
                    end_pos = bullet_points[j + 1]
                    if subheaders[j + 1] == "Description:":
                        end_pos -= 1
                    for k in range(bullet_points[j] + 1, end_pos):
                        if text[k].strip() != '○':
                            tmp += text[k]
                        if text[k].strip() == '○' or k + 1 == end_pos:
                            tmp = tmp.replace("\n", " ")
                            description.append(tmp)
                            tmp = ""
                        last_pos = k

                    # Job skills
                    if subheaders[j + 1] == "Skills:" or subheaders[j + 1] == "Skills learned:" or\
                        subheaders[j + 1] == "Skills Learned":
                        tmp = ""
                        end_pos = bullet_points[j + 2]
                        if subheaders[j + 2] == "Description:":
                            end_pos -= 1
                        for k in range(bullet_points[j + 1] + 1, end_pos):
                            if text[k].strip() != '○':
                                tmp += text[k]
                            if text[k].strip() == '○' or k + 1 == end_pos:
                                tmp = tmp.replace("\n", " ")
                                skills.append(tmp)
                                tmp = ""
                            last_pos = k

                    while len(start_date) > 0 and start_date[0] == '.':
                        start_date = start_date[1:]
                    while len(start_date) > 0 and start_date[-1] == '.':
                        start_date = start_date[:-1]
                    while len(end_date) > 0 and end_date[0] == '.':
                        end_date = end_date[1:]
                    while len(end_date) > 0 and end_date[-1] == '.':
                        end_date = end_date[:-1]
                    position = position.strip()
                    company = company.strip()
                    start_date = start_date.strip()
                    end_date = end_date.strip()
                    description = [x.strip() for x in description[1:]]
                    skills = [x.strip() for x in skills[1:]]
                    jobs.append([company, position, start_date, end_date, description, skills])

        # Get the extracurriculars credentials
        elif text[indices[i]].strip() == "EXTRACURRICULARS":
            bullet_points, subheaders = [], []
            for j in range(indices[i] + 1, indices[i + 1]):
                if text[j].strip() == '●' and text[j].strip() == '●':
                    bullet_points.append(j)
                    subheaders.append(text[j + 1].strip())
            bullet_points.append(indices[i + 1])
            subheaders.append(text[indices[i + 1]].strip())
            last_pos = indices[i]

            for j in range(len(bullet_points) - 1):
                if subheaders[j] == "Description:":
                    position, company, dates, start_date, end_date = "", "", "", "", ""
                    description, skills = [], []

                    # Extracurricular's position, company and dates
                    tmp = ""
                    for k in range(last_pos + 1, bullet_points[j]):
                        tmp += text[k]
                    tmp = tmp.replace("\n", " ")
                    values = [""]
                    for ch in tmp:
                        if ch == ',':
                            values.append("")
                        else:
                            values[-1] += ch
                    position, dates = values[0], values[-1]
                    for ch in values[1:-1]:
                        company += ch
                        if ch != values[-2]:
                            company += ','
                    for ch in dates:
                        if ch == '-' or ch == '–':
                            start_date, end_date = end_date, start_date
                        else:
                            end_date += ch

                    # Extracurricular's description
                    tmp = ""
                    end_pos = bullet_points[j + 1]
                    if subheaders[j + 1] == "Description:":
                        end_pos -= 1
                    for k in range(bullet_points[j] + 1, end_pos):
                        if text[k].strip() != '○':
                            tmp += text[k]
                        if text[k].strip() == '○' or k + 1 == end_pos:
                            tmp = tmp.replace("\n", " ")
                            description.append(tmp)
                            tmp = ""
                        last_pos = k

                    # Extracurricular's skills
                    if subheaders[j + 1] == "Skills:" or subheaders[j + 1] == "Skills learned:" or\
                        subheaders[j + 1] == "Skills Learned":
                        tmp = ""
                        end_pos = bullet_points[j + 2]
                        if subheaders[j + 2] == "Description:":
                            end_pos -= 1
                        for k in range(bullet_points[j + 1] + 1, end_pos):
                            if text[k].strip() != '○':
                                tmp += text[k]
                            if text[k].strip() == '○' or k + 1 == end_pos:
                                tmp = tmp.replace("\n", " ")
                                skills.append(tmp)
                                tmp = ""
                            last_pos = k

                    while len(start_date) > 0 and start_date[0] == '.':
                        start_date = start_date[1:]
                    while len(start_date) > 0 and start_date[-1] == '.':
                        start_date = start_date[:-1]
                    while len(end_date) > 0 and end_date[0] == '.':
                        end_date = end_date[1:]
                    while len(end_date) > 0 and end_date[-1] == '.':
                        end_date = end_date[:-1]
                    position = position.strip()
                    company = company.strip()
                    start_date = start_date.strip()
                    end_date = end_date.strip()
                    description = [x.strip() for x in description[1:]]
                    skills = [x.strip() for x in skills[1:]]
                    extras.append([company, position, start_date, end_date, description, skills])

        # Get the awards credentials
        elif text[indices[i]].strip() == "AWARDS":
            bullet_points, subheaders = [], []
            for j in range(indices[i] + 1, indices[i + 1]):
                if text[j].strip() == '●' and text[j].strip() == '●':
                    bullet_points.append(j)
                    subheaders.append(text[j + 1].strip())
            bullet_points.append(indices[i + 1])
            subheaders.append(text[indices[i + 1]].strip())

            for j in range(len(bullet_points) - 1):
                award, body, date = "", "", ""
                description = ""

                # All information
                tmp = ""
                for k in range(bullet_points[j] + 1, bullet_points[j + 1]):
                    if text[k].strip() != '○' and text[k].strip() != '●' and text[k].strip() != '●':
                        tmp += text[k]
                    if text[k].strip() == '○':
                        tmp = tmp.replace("\n", " ")
                        values = [""]
                        for ch in tmp:
                            if ch == ',':
                                values.append("")
                            else:
                                values[-1] += ch
                        award, date = values[0], values[-1]
                        for ch in values[1:-1]:
                            body += ch
                            if ch != values[-2]:
                                body += ','
                        tmp = ""
                    elif k + 1 == bullet_points[j + 1]:
                        tmp = tmp.replace("\n", " ")
                        description = tmp

                while len(date) > 0 and date[0] == '.':
                    date = date[1:]
                while len(date) > 0 and date[-1] == '.':
                    date = date[:-1]
                award = award.strip()
                body = body.strip()
                date = date.strip()
                description = description.strip()
                awards.append([award, body, date, description])

        # Get the skills credentials
        elif text[indices[i]].strip() == "SKILLS":
            bullet_points, subheaders = [], []
            for j in range(indices[i] + 1, indices[i + 1]):
                if text[j].strip() == '●' and text[j].strip() == '●':
                    bullet_points.append(j)
                    subheaders.append(text[j + 1].strip())
            bullet_points.append(indices[i + 1])
            subheaders.append(text[indices[i + 1]].strip())
            languages, hard_skills, soft_skills = [], [], []

            for j in range(len(bullet_points) - 1):
                # skills
                tmp = ""
                tmp_array = []
                for k in range(bullet_points[j] + 1, bullet_points[j + 1]):
                    if text[k].strip() != '○' and text[k].strip() != '●' and text[k].strip() != '●':
                        tmp += text[k]
                    if text[k].strip() == '○' or k + 1 == bullet_points[j + 1]:
                        tmp = tmp.replace("\n", " ")
                        tmp_array.append(tmp)
                        tmp = ""
                if subheaders[j] == "Languages:":
                    languages = [x.strip() for x in tmp_array[1:]]
                elif subheaders[j] == "Hard skills:" or subheaders[j] == "Hard Skills:":
                    hard_skills = [x.strip() for x in tmp_array[1:]]
                elif subheaders[j] == "Soft skills:" or subheaders[j] == "Soft Skills:":
                    soft_skills = [x.strip() for x in tmp_array[1:]]

            Skills = [languages, hard_skills, soft_skills]

    def convert_into_JSON(name, email, number, unis, jobs, extras, awards, skills):
        # Output into a JSON file format
        data = '{\n'
        data += '   "name": "' + str(name) + '",\n'
        data += '   "phone_number": "' + str(number) + '",\n'
        data += '   "email": "' + str(email) + '",\n'
        data += '   "personal_profile": "' + str(profile) + '",\n'
        data += '   "education": {\n'
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        i = 0
        # Add the education part into JSON
        for uni in unis:
            data += '      "school_' + str(i + 1) + '": ["' + str(uni[0]) + '", "' + str(uni[1]) + '", "' \
                 + str(uni[2]) + '", "' + str(uni[3]) + '", {"additional_points": ['
            j = 0
            for p in uni[4]:
                j += 1
                data += '"' + str(p) + '"'
                if j != len(uni[4]):
                    data += ', '
            data += ']}]'
            if i + 1 != len(unis):
                data += ',\n'
            else:
                data += '\n'
            i += 1
        data += '   },\n   "work_experience": {\n'
        i = 0
        # Add the work experience part into JSON
        for job in jobs:
            data += '      "company_' + str(i + 1) + '": ["' + str(job[0]) + '", "' + str(job[1]) + '", "' \
                 + str(job[2]) + '", "' + str(job[3]) + '", {"description": ['
            j = 0
            for p in job[4]:
                j += 1
                data += '"' + str(p) + '"'
                if j != len(job[4]):
                    data += ', '
            data += ']}, {"skills": ['
            j = 0
            for p in job[5]:
                j += 1
                data += '"' + str(p) + '"'
                if j != len(job[5]):
                    data += ', '
            data += ']}]'
            if i + 1 != len(jobs):
                data += ',\n'
            else:
                data += '\n'
            i += 1
        data += '   },\n   "extracurriculars": {\n'
        i = 0
        # Add the extracurriculars part into JSON
        for extra in extras:
            data += '      "organization_' + str(i + 1) + '": ["' + str(extra[0]) + '", "' + str(extra[1]) \
                  + '", "' + str(extra[2]) + '", "' + str(extra[3]) + '", {"description": ['
            j = 0
            for p in extra[4]:
                j += 1
                data += '"' + str(p) + '"'
                if j != len(extra[4]):
                    data += ', '
            data += ']}, {"skills": ['
            j = 0
            for p in extra[5]:
                j += 1
                data += '"' + str(p) + '"'
                if j != len(extra[5]):
                    data += ', '
            data += ']}]'
            if i + 1 != len(extras):
                data += ',\n'
            else:
                data += '\n'
            i += 1
        data += '   },\n   "awards": {\n'
        i = 0
        # Add the awards part into JSON
        for award in awards:
            data += '      "award_' + str(i + 1) + '": ["' + str(award[0]) + '", "' + str(award[1]) \
                  + '", "' + str(award[2]) + '", "' + str(award[3]) + '"]'
            if i + 1 != len(awards):
                data += ',\n'
            else:
                data += '\n'
            i += 1
        data += '   },\n   "skills": {\n'
        data += '      "languages": ['
        i = 0
        # Add the skills part into JSON
        if Skills != "":
            if len(Skills[0]) > 0:
                for language in Skills[0]:
                    data += '"' + str(language) + '"'
                    if i + 1 != len(Skills[0]):
                        data += ', '
                    i += 1
        data += '],\n      "hard_skills": ['
        i = 0
        if Skills != "":
            if len(Skills[1]) > 0:
                for Skill in Skills[1]:
                    data += '"' + str(Skill) + '"'
                    if i + 1 != len(Skills[1]):
                        data += ', '
                    i += 1
        data += '],\n      "soft_skills": ['
        i = 0
        if Skills != "":
            if len(Skills[2]) > 0:
                for Skill in Skills[2]:
                    data += '"' + str(Skill) + '"'
                    if i + 1 != len(Skills[2]):
                        data += ', '
                    i += 1
        data += ']\n'
        data += '   }\n'
        data += "}\n"
        return data

    data = convert_into_JSON(name, email, number, unis, jobs, extras, awards, Skills)
   
    # Generate the questions
    from datetime import date
    from random import randint
    import json

    applicant_data = json.loads(data)

    language_dictionary = {
        "Bahasa Indonesia":"Indonesia",
        "Indonesian":"Indonesia",
        "Kyrgyz" : "Kyrgyzstan",
        "Cantonese" :"Hong Kong",
        "Thai":"Thailand",
        "French":"France",
        "Spanish":"Spain",
        "Puthonghua":"China",
        "Mandarin":"China",
        "Russian":"Russia",
        "Korean":"South Korea",
        "Malay":"Malaysia",
        "Bahasa Melayu":"Malaysia", 
        "German":"Germany", 
        "Italian":"Italy",
        "Mandarin Chinese":"China",
        "Uzbek":"Uzbekistan",
        "Turkish":"Turkey",
        "Japanese":"Japan",
        "Swahili":"Kenya",
        "Portuguese":"Portugal",
        "Arabic":"Egypt",
        "Persian":"Iran",
        "Hungarian":"Hungary",
        "Bulgarian":"Bulgaria",
        "Nepali":"Nepal",
        "Swedish":"Sweden",
        "Norwegian":"Norway",
        "Danish":"Denmark",
        "Hindi":"India",
        "Kazakh":"Kazakhstan",
        "Turkmen":"Turkmenistan",
        "Filipino": "Philippines",
        "Tagalog":"Philippines"
    }
    def latest_job(applicant_data):
        if applicant_data["work_experience"]=={}:
            return None
        for i in applicant_data["work_experience"]:
            if str(applicant_data["work_experience"][i][2]).lower().strip()=="present":
                return i
        else:
            return max(applicant_data["work_experience"], key = lambda x: int(applicant_data["work_experience"][x][2] ))

    def question_3_generator(applicant_data):
        if latest_job(applicant_data) == None:
            return "You have no work experience as stated in your CV. Why do you think you are suitable for the front desk manager role?"
        else:
            return "What was the reason for leaving your previous job at [" + applicant_data["work_experience"][latest_job(applicant_data)][0] +"]? And how do you think your experience as a [" + applicant_data["work_experience"][latest_job(applicant_data)][1]+ "] there will help you in your role as a front desk manager at Swire Hotels?"

    def question_4_generator(applicant_data):
        random_extra = randint(1, len(applicant_data["extracurriculars"]))
        dictkey = "organization_" + str(random_extra)
        return "In your CV, you mentioned that one of your extracurriculars was being a ["+ applicant_data["extracurriculars"][dictkey][1] + "] at [" + applicant_data["extracurriculars"][dictkey][0] + "]. Can you tell us about one of the values you learned from this experience and how it aligns with Swire Hotels' values?"

    def question_5_generator(applicant_data):
        language_spoken = applicant_data["skills"]["languages"]
        if "English" in language_spoken:
            language_spoken.remove("English")
        language_chosen = language_spoken[randint(0,len(language_spoken)-1)]
        country = language_dictionary[language_chosen]
        return "This guest is now very satisfied with the service at Swire Hotels and is about to check out. You meet him again at the front desk and learn that he is from [" + str(country) +"]. As you speak ["+ str(language_chosen) +"], could you give a few short sentences expressing your gratitude for him choosing Swire Hotels before he departs?"


    question_1 = "Why did you apply to Swire Hotels?"
    question_2 = "Imagine a scenario where a guest is arguing with the front desk and you happen to arrive just as she says this to you: \"I'm sorry, but this is ridiculous. I've been waiting at the front desk for over 20 minutes now, and I have things to do. I don't understand why there aren't more staff members working to help guests like me. I demand a refund for my stay because of this poor service.\" What would your response be?"
    question_6 = "Good morning [" + applicant_data["name"].split(' ', 1)[0] + "]! How are you doing today?"
    

    def question_list_generator(applicant_data):
        return [question_6, question_3_generator(applicant_data), question_4_generator(applicant_data), question_5_generator(applicant_data)]
    
    questions = question_list_generator(applicant_data)
    
    
    
    
    
    
    # Read into the model
    
    Q = ""
    for question in questions:
        Q += question.replace("[","") + '\n\n'
    Q = Q.replace("[", "").replace("]", "")
    print(Q)
    file_path = "/mnt/c/Users/user/Desktop/Swireview/Jane_questions.txt"
    text_file = open(file_path, "w")
    n = text_file.write(Q)
    text_file.close()
    


# In[ ]:





# In[ ]:




