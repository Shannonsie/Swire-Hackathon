#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import openai
openai.api_key = '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'
while True:
    prompT = str(input())
    response = openai.Completion.create(
        model="curie:ft-personal-2023-03-23-14-57-37",
        prompt=prompT,
        max_tokens = 150
    )
    print(response.choices[0].text.strip())


# In[ ]:




