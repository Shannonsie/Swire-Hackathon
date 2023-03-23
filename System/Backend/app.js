
const express = require('express')
const app = express()
const port = 3000
const apiKey = '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';
const prompt = 'Hello, how are you?';

const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
  apiKey: "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",
});
const openai = new OpenAIApi(configuration);

app.get('/', async (req, res) => {
    const prompt = req.body.prompt
    console.log("prompt: ", prompt)
    const response = await openai.createCompletion({
        model: "text-davinci-003",
        prompt,
      });
    console.log(response.data.choices)
    res.send(response.data.choices[0].text)
})

app.listen(port, () => {
    console.log('App listening on Port 3000')
})




