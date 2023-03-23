#!/usr/bin/env python
# coding: utf-8

# In[43]:


import os
fine_tune_jsonl = ""
l = []
for file_number in range(1, 150):
    text_file = '/mnt/c/Users/user/Desktop/Swireview/fdata/data' + str(file_number) + '.txt'
    if os.path.exists(text_file):
        with open(text_file, encoding = "latin-1") as f:
            text = f.readlines()
        text = [t.replace('"', '“') for t in text]
        text = [t.replace("Interviewer:", "") for t in text]
        text = [t.replace("Applicant:", "") for t in text]
        messages = [""]
        questions_index = -1
        for i in range(len(text)):
            if text[i][0].isdigit() == 0:
                questions_index = i
                break
        tmp = ""
        
        for i in range(questions_index):
            tmp += text[i][:-1]
        text[questions_index - 1] = tmp
        text = text[questions_index - 1 : ]
        for t in text:
            if t != "\n":
                messages[-1] += t
            else:
                messages.append("")
        messages = [m.rstrip('\n') for m in messages if m != ' ' and m != '' and m != '\n']
        words = []
        flag = 0
        for ch in messages[0]:
            if ch == '[':
                words.append("[")
                flag = 1
            elif ch == ']':
                flag = 0
                words[-1] += ch
            elif flag == 1:
                words[-1] += ch
        messages.append("")
        mm = messages
        
        mm[0] = words[0] + " start"
        mm[4] = words[1] + words[2] + mm[4]
        mm[6] = words[3] + words[4] + mm[6]
        mm[10] = words[5] + words[6] + mm[10]
        mm[12] = words[0] + mm[12]
        for i in range(0, 14, 2):
            prompt = mm[i]
            completion = mm[i + 1]
            l.append('{"prompt": "'+prompt.strip()+'#", "completion" : " '+completion.strip()+'###"}\n')
            
            

for i in range(7):
    for j in range(i, len(l), 7):
        fine_tune_jsonl += l[j]
print(fine_tune_jsonl)
file_path = "/mnt/c/Users/user/Desktop/Swireview/Training_data/training_data3.jsonl"
text_file = open(file_path, "w")
n = text_file.write(fine_tune_jsonl)
text_file.close() 


# In[ ]:


"""I want you to act as an interviewer from this point and for your next response to this question, you will start speaking from the first line of the question. Here are the questions:

    1. Good morning, Jessica! How are you today?
    2. I'm great, thank you. So, let's start with the first question. Why did you apply to Swire Hotels?
    3. Thank you for that, Jessica. Moving on to the second question, what was your reason for leaving your latest job in The Peninsula? And how do you think your experience as a Guest Services Manager there will help you as a front desk manager in Swire Hotels?
    4. Impressive. Thank you for sharing that with us. Now, the third question is regarding your extracurricular activity. In your CV, you mentioned that one of your extracurriculars was volunteering in a local animal shelter. Can you tell us more about one of the values that you learned from the position and how does it align with Swire Hotel's value?
    5. Thank you for sharing that, Jessica. The fourth question is a challenging one. Imagine a scenario where a guest is arguing at the front desk, and you happen to just come when she says this to you: " I'm sorry, but this is ridiculous. I've been waiting at the front desk for over 20 minutes now, and I have things to do. I don't understand why there aren't more staff members working to help guests like me. I demand a refund for my stay because of this poor service." What would be your response?
    6. Thank you, Jessica. Last but not least, in the scenario earlier, the guest is now very satisfied with the service that Swire hotels are giving, and now he is about to check out of the hotel when you meet him at the front desk. When you talk to him, he happens to be from Brazil. As you mentioned that one of the languages that you speak is Portuguese, can you give a short sentence or two thanking him for choosing Swire Hotels?
    7. Thank you so much for your time and answers today, Jessica. We will be in touch soon regarding the next steps. Have a great day!
"""

